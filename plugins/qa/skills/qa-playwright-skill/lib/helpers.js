// playwright-helpers.js
// Reusable utility functions for Playwright automation

const fs = require('fs');
const path = require('path');

function getPlaywright() {
  return require('playwright');
}

const SENSITIVE_HEADER_NAMES = new Set([
  'authorization',
  'cookie',
  'proxy-authorization',
  'set-cookie',
]);

function validateHeaders(headers, allowSensitiveHeaders = false) {
  const validated = {};
  for (const [name, value] of Object.entries(headers || {})) {
    if (!/^[!#$%&'*+.^_`|~0-9A-Za-z-]+$/.test(name)) {
      throw new Error(`Invalid HTTP header name: ${name}`);
    }
    if (typeof value !== 'string' || /[\r\n]/.test(value)) {
      throw new Error(`Invalid HTTP header value for ${name}`);
    }
    if (!allowSensitiveHeaders && SENSITIVE_HEADER_NAMES.has(name.toLowerCase())) {
      throw new Error(`Sensitive HTTP header requires explicit approval: ${name}`);
    }
    validated[name] = value;
  }
  return validated;
}

/**
 * Parse extra HTTP headers from environment variables.
 * Supports two formats:
 * - PW_HEADER_NAME + PW_HEADER_VALUE: Single header (simple, common case)
 * - PW_EXTRA_HEADERS: JSON object for multiple headers (advanced)
 * Single header format takes precedence if both are set.
 * @returns {Object|null} Headers object or null if none configured
 */
function getExtraHeadersFromEnv(options = {}) {
  const headerName = process.env.PW_HEADER_NAME;
  const headerValue = process.env.PW_HEADER_VALUE;

  if (Boolean(headerName) !== Boolean(headerValue)) {
    throw new Error('PW_HEADER_NAME and PW_HEADER_VALUE must be provided together');
  }

  if (headerName && headerValue) {
    return validateHeaders(
      { [headerName]: headerValue },
      options.allowSensitiveHeaders === true,
    );
  }

  const headersJson = process.env.PW_EXTRA_HEADERS;
  if (headersJson) {
    try {
      const parsed = JSON.parse(headersJson);
      if (typeof parsed === 'object' && parsed !== null && !Array.isArray(parsed)) {
        return validateHeaders(parsed, options.allowSensitiveHeaders === true);
      }
      throw new Error('PW_EXTRA_HEADERS must be a JSON object');
    } catch (e) {
      throw new Error(`Invalid PW_EXTRA_HEADERS: ${e.message}`);
    }
  }

  return null;
}

/**
 * Launch browser with standard configuration
 * @param {string} browserType - 'chromium', 'firefox', or 'webkit'
 * @param {Object} options - Additional launch options
 */
async function launchBrowser(browserType = 'chromium', options = {}) {
  const { chromium, firefox, webkit } = getPlaywright();
  const configuredSlowMo = Number.parseInt(process.env.SLOW_MO || '0', 10);
  const defaultOptions = {
    headless: process.env.HEADLESS !== 'false',
    slowMo: Number.isFinite(configuredSlowMo) && configuredSlowMo >= 0
      ? configuredSlowMo
      : 0,
  };
  
  const browsers = { chromium, firefox, webkit };
  const browser = browsers[browserType];
  
  if (!browser) {
    throw new Error(`Invalid browser type: ${browserType}`);
  }
  
  return browser.launch({ ...defaultOptions, ...options });
}

/**
 * Create a new page with viewport and user agent
 * @param {Object} context - Browser context
 * @param {Object} options - Page options
 */
async function createPage(context, options = {}) {
  const page = await context.newPage();
  
  if (options.viewport) {
    await page.setViewportSize(options.viewport);
  }
  
  if (options.userAgent) {
    await page.setExtraHTTPHeaders({
      'User-Agent': options.userAgent
    });
  }
  
  // Set default timeout
  page.setDefaultTimeout(options.timeout || 30000);
  
  return page;
}

/**
 * Smart wait for page to be ready
 * @param {Object} page - Playwright page
 * @param {Object} options - Wait options
 */
async function waitForPageReady(page, options = {}) {
  const waitOptions = {
    waitUntil: options.waitUntil || 'domcontentloaded',
    timeout: options.timeout || 30000
  };
  
  await page.waitForLoadState(waitOptions.waitUntil, {
    timeout: waitOptions.timeout
  });
  
  // Additional wait for dynamic content if selector provided
  if (options.waitForSelector) {
    await page.waitForSelector(options.waitForSelector, { 
      timeout: options.timeout 
    });
  }
}

/**
 * Safe click with retry logic
 * @param {Object} page - Playwright page
 * @param {string} selector - Element selector
 * @param {Object} options - Click options
 */
async function safeClick(page, selector, options = {}) {
  const maxRetries = options.retries || 1;
  const retryDelay = options.retryDelay || 1000;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      await page.waitForSelector(selector, { 
        state: 'visible',
        timeout: options.timeout || 5000 
      });
      await page.click(selector, {
        force: options.force || false,
        timeout: options.timeout || 5000
      });
      return true;
    } catch (e) {
      if (i === maxRetries - 1) {
        console.error(`Failed to click ${selector} after ${maxRetries} attempts`);
        throw e;
      }
      console.log(`Retry ${i + 1}/${maxRetries} for clicking ${selector}`);
      await page.waitForTimeout(retryDelay);
    }
  }
}

/**
 * Safe text input with clear before type
 * @param {Object} page - Playwright page
 * @param {string} selector - Input selector
 * @param {string} text - Text to type
 * @param {Object} options - Type options
 */
async function safeType(page, selector, text, options = {}) {
  await page.waitForSelector(selector, { 
    state: 'visible',
    timeout: options.timeout || 10000 
  });
  
  if (options.clear !== false) {
    await page.fill(selector, '');
  }
  
  if (options.slow) {
    await page.locator(selector).pressSequentially(text, {
      delay: options.delay || 100
    });
  } else {
    await page.fill(selector, text);
  }
}

/**
 * Extract text from multiple elements
 * @param {Object} page - Playwright page
 * @param {string} selector - Elements selector
 */
async function extractTexts(page, selector) {
  await page.waitForSelector(selector, { timeout: 10000 });
  return await page.$$eval(selector, elements => 
    elements.map(el => el.textContent?.trim()).filter(Boolean)
  );
}

/**
 * Take screenshot with timestamp
 * @param {Object} page - Playwright page
 * @param {string} name - Screenshot name
 * @param {Object} options - Screenshot options
 */
async function takeScreenshot(page, name, options = {}) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  if (!/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name)) {
    throw new Error('Screenshot name must be a safe base name');
  }
  const outputDirectory = path.resolve(options.outputDirectory || '.');
  const metadata = fs.lstatSync(outputDirectory);
  if (!metadata.isDirectory() || metadata.isSymbolicLink()) {
    throw new Error('Screenshot output directory must be a non-symlink directory');
  }
  if (fs.realpathSync(outputDirectory) !== outputDirectory) {
    throw new Error('Screenshot output path must not traverse symlinks');
  }
  const filename = path.join(outputDirectory, `${name}-${timestamp}.png`);
  const screenshotOptions = { ...options };
  delete screenshotOptions.outputDirectory;
  delete screenshotOptions.path;
  
  await page.screenshot({
    path: filename,
    fullPage: options.fullPage !== false,
    ...screenshotOptions
  });
  
  console.log(`Screenshot saved: ${filename}`);
  return filename;
}

/**
 * Handle authentication
 * @param {Object} page - Playwright page
 * @param {Object} credentials - Username and password
 * @param {Object} selectors - Login form selectors
 */
async function authenticate(page, credentials, selectors = {}) {
  if (!credentials || !credentials.username || !credentials.password) {
    throw new Error('Credentials must come from an approved runtime channel');
  }
  if (!selectors.successIndicator && !selectors.successURL) {
    throw new Error('Authentication requires a successIndicator or successURL');
  }
  const defaultSelectors = {
    username: 'input[name="username"], input[name="email"], #username, #email',
    password: 'input[name="password"], #password',
    submit: 'button[type="submit"], input[type="submit"], button:has-text("Login"), button:has-text("Sign in")'
  };
  
  const finalSelectors = { ...defaultSelectors, ...selectors };
  
  await safeType(page, finalSelectors.username, credentials.username);
  await safeType(page, finalSelectors.password, credentials.password);
  await safeClick(page, finalSelectors.submit);
  
  if (selectors.successURL) {
    await page.waitForURL(selectors.successURL, { timeout: 10000 });
  }
  if (selectors.successIndicator) {
    await page.locator(selectors.successIndicator).waitFor({
      state: 'visible',
      timeout: 10000,
    });
  }
}

/**
 * Scroll page
 * @param {Object} page - Playwright page
 * @param {string} direction - 'down', 'up', 'top', 'bottom'
 * @param {number} distance - Pixels to scroll (for up/down)
 */
async function scrollPage(page, direction = 'down', distance = 500) {
  switch (direction) {
    case 'down':
      await page.evaluate(d => window.scrollBy(0, d), distance);
      break;
    case 'up':
      await page.evaluate(d => window.scrollBy(0, -d), distance);
      break;
    case 'top':
      await page.evaluate(() => window.scrollTo(0, 0));
      break;
    case 'bottom':
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      break;
  }
  await page.waitForTimeout(500); // Wait for scroll animation
}

/**
 * Extract table data
 * @param {Object} page - Playwright page
 * @param {string} tableSelector - Table selector
 */
async function extractTableData(page, tableSelector) {
  await page.waitForSelector(tableSelector);
  
  return await page.evaluate((selector) => {
    const table = document.querySelector(selector);
    if (!table) return null;
    
    const headers = Array.from(table.querySelectorAll('thead th')).map(th => 
      th.textContent?.trim()
    );
    
    const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr => {
      const cells = Array.from(tr.querySelectorAll('td'));
      if (headers.length > 0) {
        return cells.reduce((obj, cell, index) => {
          obj[headers[index] || `column_${index}`] = cell.textContent?.trim();
          return obj;
        }, {});
      } else {
        return cells.map(cell => cell.textContent?.trim());
      }
    });
    
    return { headers, rows };
  }, tableSelector);
}

/**
 * Wait for and apply an explicit cookie-banner decision
 * @param {Object} page - Playwright page
 * @param {'accept'|'reject'} decision - User-authorized consent decision
 * @param {number} timeout - Max time to wait
 */
async function handleCookieBanner(page, decision, timeout = 3000) {
  const selectorsByDecision = {
    accept: [
      'button:has-text("Accept")',
      'button:has-text("Accept all")',
      '.cookie-accept',
      '[data-testid="cookie-accept"]'
    ],
    reject: [
      'button:has-text("Reject")',
      'button:has-text("Reject all")',
      '.cookie-reject',
      '[data-testid="cookie-reject"]'
    ],
  };
  const commonSelectors = selectorsByDecision[decision];
  if (!commonSelectors) {
    throw new Error('Cookie decision must be explicitly "accept" or "reject"');
  }
  
  for (const selector of commonSelectors) {
    try {
      const element = await page.waitForSelector(selector, { 
        timeout: timeout / commonSelectors.length,
        state: 'visible'
      });
      if (element) {
        await element.click();
        console.log('Cookie banner dismissed');
        return true;
      }
    } catch (e) {
      // Continue to next selector
    }
  }
  
  return false;
}

/**
 * Retry a function with exponential backoff
 * @param {Function} fn - Function to retry
 * @param {number} maxRetries - Maximum retry attempts
 * @param {number} initialDelay - Initial delay in ms
 */
async function retryWithBackoff(fn, maxRetries = 3, initialDelay = 1000) {
  let lastError;
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      const delay = initialDelay * Math.pow(2, i);
      console.log(`Attempt ${i + 1} failed, retrying in ${delay}ms...`);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
  
  throw lastError;
}

/**
 * Create browser context with common settings
 * @param {Object} browser - Browser instance
 * @param {Object} options - Context options
 */
async function createContext(browser, options = {}) {
  const allowSensitiveHeaders = options.allowSensitiveHeaders === true;
  const envHeaders = getExtraHeadersFromEnv({
    allowSensitiveHeaders,
  });
  const optionHeaders = validateHeaders(
    options.extraHTTPHeaders || {},
    allowSensitiveHeaders,
  );

  // Merge environment headers with any passed in options
  const mergedHeaders = {
    ...(envHeaders || {}),
    ...optionHeaders,
  };

  const {
    allowSensitiveHeaders: _allowSensitiveHeaders,
    extraHTTPHeaders: _extraHTTPHeaders,
    mobile: _mobile,
    ...playwrightOptions
  } = options;
  const defaultOptions = {
    viewport: { width: 1280, height: 720 },
    userAgent: options.mobile
      ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1'
      : undefined,
    permissions: options.permissions || [],
    geolocation: options.geolocation,
    locale: options.locale || 'en-US',
    timezoneId: options.timezoneId || 'America/New_York',
    // Only include extraHTTPHeaders if we have any
    ...(Object.keys(mergedHeaders).length > 0 && { extraHTTPHeaders: mergedHeaders })
  };

  return browser.newContext({
    ...defaultOptions,
    ...playwrightOptions,
    ...(Object.keys(mergedHeaders).length > 0 && {
      extraHTTPHeaders: mergedHeaders,
    }),
  });
}

/**
 * Detect running dev servers only on reviewed candidate ports
 * @param {Array<number>} candidatePorts - Explicit ports to check
 * @returns {Promise<Array>} Array of detected server URLs
 */
async function detectDevServers(candidatePorts = []) {
  const http = require('http');

  if (!Array.isArray(candidatePorts) || candidatePorts.length === 0) {
    throw new Error('Provide reviewed candidate ports from the target project');
  }
  const allPorts = [...new Set(candidatePorts.map(port => Number(port)))];
  if (allPorts.some(port => !Number.isInteger(port) || port < 1 || port > 65535)) {
    throw new Error('Candidate ports must be integers between 1 and 65535');
  }

  const detectedServers = [];

  console.log('🔍 Checking for running dev servers...');

  for (const port of allPorts) {
    try {
      await new Promise((resolve, reject) => {
        const req = http.request({
          hostname: 'localhost',
          port: port,
          path: '/',
          method: 'HEAD',
          timeout: 500
        }, (res) => {
          if (res.statusCode < 500) {
            detectedServers.push(`http://localhost:${port}`);
            console.log(`  ✅ Found server on port ${port}`);
          }
          resolve();
        });

        req.on('error', () => resolve());
        req.on('timeout', () => {
          req.destroy();
          resolve();
        });

        req.end();
      });
    } catch (e) {
      // Port not available, continue
    }
  }

  if (detectedServers.length === 0) {
    console.log('  ❌ No dev servers detected');
  }

  return detectedServers;
}

module.exports = {
  launchBrowser,
  createPage,
  waitForPageReady,
  safeClick,
  safeType,
  extractTexts,
  takeScreenshot,
  authenticate,
  scrollPage,
  extractTableData,
  handleCookieBanner,
  retryWithBackoff,
  createContext,
  detectDevServers,
  getExtraHeadersFromEnv,
  validateHeaders,
};
