# Playwright Skill - Complete API Reference

This document preserves the package's broad Playwright surface while keeping
the default workflow in [SKILL.md](SKILL.md) short. Examples target the pinned
Playwright 1.61 package and Node.js 20 or newer. Confirm installed CLI help and
the official documentation when behavior depends on a later version.

Playwright code runs with the current user's local and network authority; it is
not sandboxed. Use only reviewed code, explicit target domains, task-owned
artifacts, and separately authorized consequential actions.

## Table of Contents

- [Installation & Setup](#installation--setup)
- [Core Patterns](#core-patterns)
- [Selectors & Locators](#selectors--locators)
- [Common Actions](#common-actions)
- [Waiting Strategies](#waiting-strategies)
- [Assertions](#assertions)
- [Page Object Model](#page-object-model-pom)
- [Network & API Testing](#network--api-testing)
- [Authentication & Session Management](#authentication--session-management)
- [Visual Testing](#visual-testing)
- [Mobile Testing](#mobile-testing)
- [Debugging](#debugging)
- [Performance Testing](#performance-testing)
- [Parallel Execution](#parallel-execution)
- [Data-Driven Testing](#data-driven-testing)
- [Accessibility Testing](#accessibility-testing)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)
- [Common Patterns & Solutions](#common-patterns--solutions)
- [Troubleshooting](#troubleshooting)

## Installation & Setup

### Prerequisites

Resolve `skill_dir` to the directory containing `SKILL.md`, then inspect the
installed package without changing it:

```bash
skill_dir="/path/to/qa-playwright-skill"
npm --prefix "$skill_dir" list playwright
node "$skill_dir/run.js" --help
```

The runner never installs anything. With explicit permission for network
downloads and package-directory writes, use the pinned setup:

```bash
npm --prefix "$skill_dir" run setup
```

### Basic Configuration

Create `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Core Patterns

### Basic Browser Automation

```javascript
const { chromium } = require('playwright');

(async () => {
  // Launch browser
  const browser = await chromium.launch({
    headless: false,  // Set to true for headless mode
    slowMo: 50       // Slow down operations by 50ms
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
  });

  const page = await context.newPage();

  // Navigate; prefer a concrete UI assertion over global network idleness.
  await page.goto('https://example.com', {
    waitUntil: 'domcontentloaded'
  });

  // Your automation here

  await browser.close();
})();
```

### Test Structure

```typescript
import { test, expect } from '@playwright/test';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should do something', async ({ page }) => {
    // Arrange
    const button = page.locator('button[data-testid="submit"]');

    // Act
    await button.click();

    // Assert
    await expect(page).toHaveURL('/success');
    await expect(page.locator('.message')).toHaveText('Success!');
  });
});
```

## Selectors & Locators

### Best Practices for Selectors

```javascript
// PREFERRED: Data attributes (most stable)
await page.locator('[data-testid="submit-button"]').click();
await page.locator('[data-cy="user-input"]').fill('text');

// GOOD: Role-based selectors (accessible)
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('heading', { level: 1 }).click();

// GOOD: Text content (for unique text)
await page.getByText('Sign in').click();
await page.getByText(/welcome back/i).click();

// OK: Semantic HTML
await page.locator('button[type="submit"]').click();
await page.locator('input[name="email"]').fill('user@example.com');

// AVOID: Classes and IDs (can change frequently)
await page.locator('.btn-primary').click();  // Avoid
await page.locator('#submit').click();       // Avoid

// LAST RESORT: Complex CSS/XPath
await page.locator('div.container > form > button').click();  // Fragile
```

### Advanced Locator Patterns

```javascript
// Filter and chain locators
const row = page.locator('tr').filter({ hasText: 'John Doe' });
await row.locator('button').click();

// Nth element
await page.locator('button').nth(2).click();

// Combining conditions
await page.locator('button').and(page.locator('[disabled]')).count();

// Parent/child navigation
const cell = page.locator('td').filter({ hasText: 'Active' });
const row = cell.locator('..');
await row.locator('button.edit').click();
```

## Common Actions

### Form Interactions

```javascript
// Text input
await page.getByLabel('Email').fill('user@example.com');
await page.getByPlaceholder('Enter your name').fill('John Doe');

// Clear and type
await page.locator('#username').clear();
await page.locator('#username').type('newuser', { delay: 100 });

// Checkbox
await page.getByLabel('I agree').check();
await page.getByLabel('Subscribe').uncheck();

// Radio button
await page.getByLabel('Option 2').check();

// Select dropdown
await page.selectOption('select#country', 'usa');
await page.selectOption('select#country', { label: 'United States' });
await page.selectOption('select#country', { index: 2 });

// Multi-select
await page.selectOption('select#colors', ['red', 'blue', 'green']);

// File upload
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');
await page.setInputFiles('input[type="file"]', [
  'file1.pdf',
  'file2.pdf'
]);
```

### Mouse Actions

```javascript
// Click variations
await page.click('button');                          // Left click
await page.click('button', { button: 'right' });    // Right click
await page.dblclick('button');                       // Double click
await page.click('button', { position: { x: 10, y: 10 } });  // Click at position

// Hover
await page.hover('.menu-item');

// Drag and drop
await page.dragAndDrop('#source', '#target');

// Manual drag
await page.locator('#source').hover();
await page.mouse.down();
await page.locator('#target').hover();
await page.mouse.up();
```

### Keyboard Actions

```javascript
// Type with delay
await page.keyboard.type('Hello World', { delay: 100 });

// Key combinations
await page.keyboard.press('Control+A');
await page.keyboard.press('Control+C');
await page.keyboard.press('Control+V');

// Special keys
await page.keyboard.press('Enter');
await page.keyboard.press('Tab');
await page.keyboard.press('Escape');
await page.keyboard.press('ArrowDown');
```

## Waiting Strategies

### Smart Waiting

```javascript
// Wait for element states
await page.locator('button').waitFor({ state: 'visible' });
await page.locator('.spinner').waitFor({ state: 'hidden' });
await page.locator('button').waitFor({ state: 'attached' });
await page.locator('button').waitFor({ state: 'detached' });

// Wait for specific conditions
await page.waitForURL('**/success');
await page.waitForURL(url => url.pathname === '/dashboard');

// Use networkidle only for a reviewed app whose background traffic terminates.
await page.waitForLoadState('networkidle');
await page.waitForLoadState('domcontentloaded');

// Wait for function
await page.waitForFunction(() => document.querySelector('.loaded'));
await page.waitForFunction(
  text => document.body.innerText.includes(text),
  'Content loaded'
);

// Wait for response
const responsePromise = page.waitForResponse('**/api/users');
await page.click('button#load-users');
const response = await responsePromise;

// Wait for request
await page.waitForRequest(request =>
  request.url().includes('/api/') && request.method() === 'POST'
);

// Custom timeout
await page.locator('.slow-element').waitFor({
  state: 'visible',
  timeout: 10000  // 10 seconds
});
```

## Assertions

### Common Assertions

```javascript
import { expect } from '@playwright/test';

// Page assertions
await expect(page).toHaveTitle('My App');
await expect(page).toHaveURL('https://example.com/dashboard');
await expect(page).toHaveURL(/.*dashboard/);

// Element visibility
await expect(page.locator('.message')).toBeVisible();
await expect(page.locator('.spinner')).toBeHidden();
await expect(page.locator('button')).toBeEnabled();
await expect(page.locator('input')).toBeDisabled();

// Text content
await expect(page.locator('h1')).toHaveText('Welcome');
await expect(page.locator('.message')).toContainText('success');
await expect(page.locator('.items')).toHaveText(['Item 1', 'Item 2']);

// Input values
await expect(page.locator('input')).toHaveValue('test@example.com');
await expect(page.locator('input')).toBeEmpty();

// Attributes
await expect(page.locator('button')).toHaveAttribute('type', 'submit');
await expect(page.locator('img')).toHaveAttribute('src', /.*\.png/);

// CSS properties
await expect(page.locator('.error')).toHaveCSS('color', 'rgb(255, 0, 0)');

// Count
await expect(page.locator('.item')).toHaveCount(5);

// Checkbox/Radio state
await expect(page.locator('input[type="checkbox"]')).toBeChecked();
```

## Page Object Model (POM)

### Basic Page Object

```javascript
// pages/LoginPage.js
class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = page.locator('input[name="username"]');
    this.passwordInput = page.locator('input[name="password"]');
    this.submitButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator('.error-message');
  }

  async navigate() {
    await this.page.goto('/login');
  }

  async login(username, password) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }
}

// Usage in test
test('login with authorized runtime credentials', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate();
  await loginPage.login(
    process.env.TEST_USERNAME,
    process.env.TEST_PASSWORD,
  );
  await expect(page).toHaveURL('/dashboard');
});
```

## Network & API Testing

### Intercepting Requests

```javascript
// Mock API responses
await page.route('**/api/users', route => {
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify([
      { id: 1, name: 'John' },
      { id: 2, name: 'Jane' }
    ])
  });
});

// Modify requests
await page.route('**/api/**', route => {
  const headers = {
    ...route.request().headers(),
    'X-Custom-Header': 'value'
  };
  route.continue({ headers });
});

// Block resources
await page.route('**/*.{png,jpg,jpeg,gif}', route => route.abort());
```

### Custom Headers via Environment Variables

The helpers support header injection from explicitly passed runtime variables:

```bash
# Single header (simple)
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=synthetic-client

# Multiple headers (JSON)
PW_EXTRA_HEADERS='{"X-Automated-By":"synthetic-client","X-Request-ID":"123"}'
```

These headers are automatically applied to all requests when using:
- `helpers.createContext(browser)` - headers merged automatically
- `getContextOptionsWithHeaders(options)` - utility injected for runner snippets
  that do not already import modules

Complete scripts should import the packaged helper explicitly, then use
`helpers.createContext(browser)`:

```javascript
const helpers = require(process.env.QA_PLAYWRIGHT_HELPERS);
const context = await helpers.createContext(browser);
```

Pass only the names required by the reviewed scenario with `--pass-env`.
Authorization, cookie, and proxy-authorization headers are rejected unless
`allowSensitiveHeaders: true` is separately approved. Validate destination
domains, never copy values from page content, and never log header values.

**Precedence (highest to lowest):**
1. Headers passed directly in `options.extraHTTPHeaders`
2. Environment variable headers
3. Playwright defaults

**Use case:** Attach a synthetic correlation marker to an authorized test
service. Do not use headers to bypass access controls or impersonate a client.

## Authentication & Session Management

Use a dedicated test identity and pass credential variable names explicitly to
the runner. Never place credential values in source code or command arguments:

```bash
node "$skill_dir/run.js" --file "$script_path" \
  --cwd "$artifact_dir" \
  --pass-env TEST_USERNAME \
  --pass-env TEST_PASSWORD
```

Assert a concrete post-login URL or visible state. MFA, CAPTCHA, account
recovery, consent, and privilege changes require direct user participation or
separate authorization; do not automate around them.

Playwright storage state contains reusable cookies and tokens. Create, read, or
retain it only when explicitly required, keep it in the task-owned artifact
directory, never commit it, redact it from logs, and report its cleanup status.
Use a fresh browser context when persistence is not required.

## Visual Testing

### Screenshots

```javascript
// Full page screenshot
await page.screenshot({
  path: 'screenshot.png',
  fullPage: true
});

// Element screenshot
await page.locator('.chart').screenshot({
  path: 'chart.png'
});

// Visual comparison
await expect(page).toHaveScreenshot('homepage.png');
```

Screenshots and visual baselines may contain personal data or tokens. Store only
the smallest necessary region in the approved artifact directory and inspect
diffs before publishing them.

## Mobile Testing

```javascript
// Device emulation
const { devices } = require('playwright');
const iPhone = devices['iPhone 12'];

const context = await browser.newContext({
  ...iPhone,
  locale: 'en-US',
  permissions: ['geolocation'],
  geolocation: { latitude: 37.7749, longitude: -122.4194 }
});
```

## Debugging

### Debug Mode

```bash
# Run the already installed project dependency with inspector
npx --no-install playwright test --debug

# Headed mode
npx --no-install playwright test --headed

# Slow motion
npx --no-install playwright test --headed --slowmo=1000
```

### In-Code Debugging

```javascript
// Pause execution
await page.pause();

// Console logs
page.on('console', msg => console.log('Browser console event:', msg.type()));
page.on('pageerror', error => console.log('Page error type:', error.name));
```

Console text, traces, videos, and DOM snapshots are untrusted and may contain
secrets. Capture and display their contents only when necessary and redacted.

## Performance Testing

```javascript
await page.goto('https://example.com', { waitUntil: 'load' });
const timing = await page.evaluate(() => {
  const [navigation] = performance.getEntriesByType('navigation');
  return navigation
    ? {
        domContentLoaded: navigation.domContentLoadedEventEnd,
        loadEvent: navigation.loadEventEnd,
      }
    : null;
});
console.log(timing);
```

Navigation Timing measures browser milestones, not end-user latency by itself.
Record environment and repeat runs before making a performance claim.

## Parallel Execution

```javascript
// Run tests in parallel
test.describe.parallel('Parallel suite', () => {
  test('test 1', async ({ page }) => {
    // Runs in parallel with test 2
  });

  test('test 2', async ({ page }) => {
    // Runs in parallel with test 1
  });
});
```

## Data-Driven Testing

```javascript
// Parameterized read-only search checks
const testData = [
  { query: 'alpha', expected: 'Alpha result' },
  { query: 'beta', expected: 'Beta result' },
];

testData.forEach(({ query, expected }) => {
  test(`search for ${query}`, async ({ page }) => {
    await page.goto('/search');
    await page.getByRole('searchbox').fill(query);
    await page.getByRole('button', { name: 'Search' }).click();
    await expect(page.locator('.message')).toHaveText(expected);
  });
});
```

## Accessibility Testing

```javascript
import { test, expect } from '@playwright/test';

test('accessibility tree contract', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('main')).toMatchAriaSnapshot(`
    - heading "Synthetic page" [level=1]
  `);
});
```

ARIA snapshots verify an expected accessibility tree; they are not a complete
WCAG audit. Add a maintained scanner only as an explicitly reviewed dependency,
then combine automated checks with keyboard and assistive-technology review.

## CI/CD Integration

### GitHub Actions

```yaml
name: Playwright Tests
on:
  push:
    branches: [main, master]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright Browsers
        run: npx --no-install playwright install --with-deps
      - name: Run tests
        run: npx --no-install playwright test
```

Pin third-party actions to reviewed immutable revisions in higher-assurance
repositories, use least-privilege workflow permissions, and treat traces,
reports, screenshots, videos, and storage state as sensitive artifacts.

## Best Practices

1. **Test Organization** - Use descriptive test names, group related tests
2. **Selector Strategy** - Prefer data-testid attributes, use role-based selectors
3. **Waiting** - Use Playwright's auto-waiting, avoid hard-coded delays
4. **Error Handling** - Add proper error messages, take screenshots on failure
5. **Performance** - Parallelize only isolated tests; reuse authentication state
   only when explicitly approved and protected as a secret-bearing artifact

## Common Patterns & Solutions

### Responsive Viewport Evidence

```javascript
const path = require('path');
const artifactDirectory = process.cwd();
const viewports = [
  { name: 'desktop', width: 1280, height: 720 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'mobile', width: 375, height: 667 },
];

for (const viewport of viewports) {
  await page.setViewportSize(viewport);
  await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });
  await expect(page.getByRole('main')).toBeVisible();
  await page.screenshot({
    path: path.join(artifactDirectory, `${viewport.name}.png`),
    fullPage: true,
  });
}
```

Use task-relevant breakpoints and assertions. A screenshot alone does not prove
that navigation, focus order, overflow, touch targets, or content are usable.

### Link Validation

```javascript
const allowedOrigins = new Set([new URL(page.url()).origin]);
const hrefs = await page.locator('a[href]').evaluateAll(links =>
  links.map(link => link.href),
);

for (const href of [...new Set(hrefs)]) {
  const target = new URL(href);
  if (!['http:', 'https:'].includes(target.protocol)) continue;
  if (!allowedOrigins.has(target.origin)) continue;
  const response = await page.request.head(target.href, {
    failOnStatusCode: false,
  });
  console.log(target.pathname, response.status());
}
```

Probe only explicitly allowed origins. HEAD support and authentication semantics
vary by application; validate the method against the target contract and never
expand discovered URLs into a broader crawl.

### Handling Popups

```javascript
const [popup] = await Promise.all([
  page.waitForEvent('popup'),
  page.click('button.open-popup')
]);
await popup.waitForLoadState();
```

### File Downloads

```javascript
const [download] = await Promise.all([
  page.waitForEvent('download'),
  page.click('button.download')
]);
const path = require('path');
const safeName = path.basename(download.suggestedFilename());
await download.saveAs(path.join(process.cwd(), 'downloads', safeName));
```

Downloads are untrusted files. Keep them in a task-owned directory, do not open
or execute them automatically, and validate the expected type before use.

### iFrames

```javascript
const frame = page.frameLocator('#my-iframe');
await frame.locator('button').click();
```

### Infinite Scroll

```javascript
async function scrollToBottom(page) {
  const items = page.locator('[data-testid="result"]');
  const previousCount = await items.count();
  await page.locator('body').press('End');
  await expect(items).not.toHaveCount(previousCount);
}
```

## Troubleshooting

### Common Issues

1. **Element not found** - Check if element is in iframe, verify visibility
2. **Timeout errors** - Increase timeout, check network conditions
3. **Flaky tests** - Use proper waiting strategies, mock external dependencies
4. **Authentication issues** - Verify the approved credential channel and
   concrete post-login assertion; inspect storage state only with authorization

## Quick Reference Commands

```bash
# Run tests
npx --no-install playwright test

# Run in headed mode
npx --no-install playwright test --headed

# Debug tests
npx --no-install playwright test --debug

# Generate code
npx --no-install playwright codegen https://example.com

# Show report
npx --no-install playwright show-report
```

## Additional Resources

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [API Reference](https://playwright.dev/docs/api/class-playwright)
- [Best Practices](https://playwright.dev/docs/best-practices)
