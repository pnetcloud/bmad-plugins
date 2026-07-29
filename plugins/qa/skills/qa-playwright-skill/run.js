#!/usr/bin/env node
'use strict';

/**
 * Explicit Playwright code runner.
 *
 * This is an execution tool, not a sandbox. It runs reviewed code with the
 * current user's filesystem and network authority in a separate Node process.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const maxFileBytes = 256 * 1024;
const maxInlineBytes = 64 * 1024;
const DEFAULT_ENV_NAMES = [
  'CI',
  'DBUS_SESSION_BUS_ADDRESS',
  'DISPLAY',
  'HOME',
  'PATH',
  'PLAYWRIGHT_BROWSERS_PATH',
  'TMP',
  'TEMP',
  'TMPDIR',
  'WAYLAND_DISPLAY',
  'XAUTHORITY',
];

function usage() {
  return `Usage:
  node run.js --file SCRIPT [--cwd DIR] [--pass-env NAME ...]
  node run.js --inline CODE [--cwd DIR] [--pass-env NAME ...]
  node run.js --stdin [--cwd DIR] [--pass-env NAME ...]

Exactly one code source is required. Code is arbitrary local execution and must
be reviewed before use. Dependencies and browser binaries are never installed
automatically.`;
}

function fail(message) {
  const error = new Error(message);
  error.code = 'USAGE';
  throw error;
}

function takeValue(args, index, option) {
  if (index + 1 >= args.length || !args[index + 1]) {
    fail(`missing value for ${option}`);
  }
  return args[index + 1];
}

function parseArgs(args) {
  if (args.length === 0) {
    return {
      cwd: __dirname,
      passEnv: [],
      source: { kind: 'stdin' },
      legacy: true,
    };
  }

  if (!args.some(argument => argument.startsWith('--'))) {
    const candidate = args.length === 1 ? path.resolve(args[0]) : null;
    const isFile = candidate !== null && fs.existsSync(candidate);
    return {
      cwd: __dirname,
      passEnv: [],
      source: isFile
        ? { kind: 'file', value: candidate }
        : { kind: 'inline', value: args.join(' ') },
      legacy: true,
    };
  }

  const options = {
    cwd: process.cwd(),
    passEnv: [],
    source: null,
  };

  for (let index = 0; index < args.length; index += 1) {
    const option = args[index];
    if (option === '--help') {
      options.help = true;
    } else if (option === '--file' || option === '--inline') {
      if (options.source) fail('choose exactly one code source');
      options.source = {
        kind: option.slice(2),
        value: takeValue(args, index, option),
      };
      index += 1;
    } else if (option === '--stdin') {
      if (options.source) fail('choose exactly one code source');
      options.source = { kind: 'stdin' };
    } else if (option === '--cwd') {
      options.cwd = takeValue(args, index, option);
      index += 1;
    } else if (option === '--pass-env') {
      options.passEnv.push(takeValue(args, index, option));
      index += 1;
    } else {
      fail(`unknown option: ${option}`);
    }
  }

  if (!options.help && !options.source) fail('a code source is required');
  return options;
}

function readRegularFile(fileName, byteLimit) {
  const resolved = path.resolve(fileName);
  const metadata = fs.lstatSync(resolved);
  if (!metadata.isFile() || metadata.isSymbolicLink()) {
    fail('script must be a regular non-symlink file');
  }
  if (metadata.size > byteLimit) {
    fail(`script exceeds ${byteLimit} bytes`);
  }
  if (fs.realpathSync(resolved) !== resolved) {
    fail('script path must not traverse symlinks');
  }
  return fs.readFileSync(resolved, 'utf8');
}

function readStdin(byteLimit) {
  const chunks = [];
  let totalBytes = 0;
  while (true) {
    const buffer = Buffer.allocUnsafe(Math.min(64 * 1024, byteLimit + 1));
    let bytesRead;
    try {
      bytesRead = fs.readSync(0, buffer, 0, buffer.length, null);
    } catch (error) {
      if (error.code !== 'EAGAIN') throw error;
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 1);
      continue;
    }
    if (bytesRead === 0) break;
    totalBytes += bytesRead;
    if (totalBytes > byteLimit) {
      fail(`stdin code exceeds ${byteLimit} bytes`);
    }
    chunks.push(buffer.subarray(0, bytesRead));
  }
  return Buffer.concat(chunks, totalBytes).toString('utf8');
}

function readCode(source) {
  if (source.kind === 'file') {
    return readRegularFile(source.value, maxFileBytes);
  }
  if (source.kind === 'inline') {
    if (Buffer.byteLength(source.value, 'utf8') > maxInlineBytes) {
      fail(`inline code exceeds ${maxInlineBytes} bytes`);
    }
    return source.value;
  }
  if (process.stdin.isTTY) fail('--stdin requires piped input');
  return readStdin(maxFileBytes);
}

function wrapCodeIfNeeded(code) {
  const hasRequire = code.includes('require(');
  const hasAsyncWrapper =
    code.includes('(async () => {') || code.includes('(async()=>{');
  if (hasRequire && hasAsyncWrapper) return code;

const imports = hasRequire
    ? ''
    : `
const { chromium, firefox, webkit, devices } = require('playwright');
const helpers = require(process.env.QA_PLAYWRIGHT_HELPERS);
function getContextOptionsWithHeaders(options = {}) {
  const environmentHeaders = helpers.getExtraHeadersFromEnv({
    allowSensitiveHeaders: options.allowSensitiveHeaders === true,
  });
  const optionHeaders = helpers.validateHeaders(
    options.extraHTTPHeaders || {},
    options.allowSensitiveHeaders === true,
  );
  const {
    allowSensitiveHeaders: _allowSensitiveHeaders,
    extraHTTPHeaders: _extraHTTPHeaders,
    ...contextOptions
  } = options;
  const extraHTTPHeaders = {
    ...(environmentHeaders || {}),
    ...optionHeaders,
  };
  return {
    ...contextOptions,
    ...(Object.keys(extraHTTPHeaders).length > 0 && { extraHTTPHeaders }),
  };
}
`;
  return `'use strict';
${imports}
(async () => {
  try {
${code}
  } catch (error) {
    console.error('Automation error:', error.message);
    process.exitCode = 1;
  }
})();
`;
}

function resolveExecutionDirectory(directory) {
  const resolved = path.resolve(directory);
  const metadata = fs.lstatSync(resolved);
  if (!metadata.isDirectory() || metadata.isSymbolicLink()) {
    fail('--cwd must be an existing non-symlink directory');
  }
  if (fs.realpathSync(resolved) !== resolved) {
    fail('--cwd path must not traverse symlinks');
  }
  return resolved;
}

function buildEnvironment(extraNames, playwrightEntry, inheritEnvironment = false) {
  const environment = inheritEnvironment ? { ...process.env } : {};
  for (const name of [...DEFAULT_ENV_NAMES, ...extraNames]) {
    if (!/^[A-Za-z_][A-Za-z0-9_]*$/.test(name)) {
      fail(`invalid environment variable name: ${name}`);
    }
    if (Object.prototype.hasOwnProperty.call(process.env, name)) {
      environment[name] = process.env[name];
    } else if (extraNames.includes(name)) {
      fail(`requested environment variable is unavailable: ${name}`);
    }
  }
  environment.NODE_PATH = path.dirname(path.dirname(playwrightEntry));
  environment.QA_PLAYWRIGHT_HELPERS = path.join(__dirname, 'lib/helpers.js');
  return environment;
}

function resolvePlaywright() {
  try {
    return require.resolve('playwright');
  } catch {
    fail('Playwright is not installed; run the reviewed package setup explicitly');
  }
}

function execute(options, code) {
  const playwrightEntry = resolvePlaywright();
  const child = spawnSync(process.execPath, ['-'], {
    cwd: resolveExecutionDirectory(options.cwd),
    env: buildEnvironment(options.passEnv, playwrightEntry, options.legacy === true),
    input: wrapCodeIfNeeded(code),
    stdio: ['pipe', 'inherit', 'inherit'],
  });
  if (child.error) throw child.error;
  return child.status === null ? 1 : child.status;
}

function main(args = process.argv.slice(2)) {
  try {
    const options = parseArgs(args);
    if (options.help) {
      console.log(usage());
      return 0;
    }
    return execute(options, readCode(options.source));
  } catch (error) {
    console.error(error.message);
    if (error.code === 'USAGE') console.error(usage());
    return 2;
  }
}

if (require.main === module) {
  process.exitCode = main();
}

module.exports = {
  buildEnvironment,
  main,
  parseArgs,
  readCode,
  readStdin,
  resolveExecutionDirectory,
  usage,
  wrapCodeIfNeeded,
};
