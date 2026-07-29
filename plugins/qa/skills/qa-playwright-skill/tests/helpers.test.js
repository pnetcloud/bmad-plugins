'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const test = require('node:test');

const helpers = require('../lib/helpers');

function temporaryDirectory(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'qa-playwright-help-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  return directory;
}

test('header validation rejects injection and requires sensitive-header opt-in', () => {
  assert.deepEqual(helpers.validateHeaders({ 'X-Test': 'synthetic' }), {
    'X-Test': 'synthetic',
  });
  assert.throws(
    () => helpers.validateHeaders({ 'Bad Header': 'value' }),
    /Invalid HTTP header name/,
  );
  assert.throws(
    () => helpers.validateHeaders({ 'X-Test': 'value\r\nInjected: yes' }),
    /Invalid HTTP header value/,
  );
  assert.throws(
    () => helpers.validateHeaders({ Authorization: 'synthetic' }),
    /explicit approval/,
  );
  assert.deepEqual(
    helpers.validateHeaders({ Authorization: 'synthetic' }, true),
    { Authorization: 'synthetic' },
  );
});

test('environment header configuration fails closed when malformed', (t) => {
  const originalName = process.env.PW_HEADER_NAME;
  const originalValue = process.env.PW_HEADER_VALUE;
  const originalExtra = process.env.PW_EXTRA_HEADERS;
  t.after(() => {
    for (const [name, value] of [
      ['PW_HEADER_NAME', originalName],
      ['PW_HEADER_VALUE', originalValue],
      ['PW_EXTRA_HEADERS', originalExtra],
    ]) {
      if (value === undefined) delete process.env[name];
      else process.env[name] = value;
    }
  });

  process.env.PW_HEADER_NAME = 'X-Test';
  delete process.env.PW_HEADER_VALUE;
  delete process.env.PW_EXTRA_HEADERS;
  assert.throws(() => helpers.getExtraHeadersFromEnv(), /provided together/);

  delete process.env.PW_HEADER_NAME;
  process.env.PW_EXTRA_HEADERS = '{invalid';
  assert.throws(() => helpers.getExtraHeadersFromEnv(), /Invalid PW_EXTRA_HEADERS/);
});

test('createContext validates and merges headers without leaking helper options', async () => {
  let received;
  const browser = {
    async newContext(options) {
      received = options;
      return { options };
    },
  };

  await helpers.createContext(browser, {
    allowSensitiveHeaders: true,
    extraHTTPHeaders: { Authorization: 'synthetic' },
    locale: 'en-GB',
    mobile: true,
  });

  assert.equal(received.allowSensitiveHeaders, undefined);
  assert.equal(received.mobile, undefined);
  assert.deepEqual(received.extraHTTPHeaders, { Authorization: 'synthetic' });
  assert.equal(received.locale, 'en-GB');
  assert.match(received.userAgent, /Mobile/);
});

test('page readiness defaults to DOM content loaded and propagates failures', async () => {
  let state;
  const page = {
    async waitForLoadState(value) {
      state = value;
    },
  };
  await helpers.waitForPageReady(page);
  assert.equal(state, 'domcontentloaded');

  await assert.rejects(
    helpers.waitForPageReady({
      async waitForLoadState() {
        throw new Error('timeout');
      },
    }),
    /timeout/,
  );
});

test('screenshot output requires a safe task-owned non-symlink path', async (t) => {
  const directory = temporaryDirectory(t);
  let received;
  const page = {
    async screenshot(options) {
      received = options;
    },
  };

  const result = await helpers.takeScreenshot(page, 'result', {
    outputDirectory: directory,
    path: path.join(path.dirname(directory), 'escape.png'),
  });
  assert.equal(received.path, result);
  assert.ok(result.startsWith(`${directory}${path.sep}`));
  await assert.rejects(
    helpers.takeScreenshot(page, '../escape', { outputDirectory: directory }),
    /safe base name/,
  );

  const linked = path.join(path.dirname(directory), `${path.basename(directory)}-link`);
  fs.symlinkSync(directory, linked, 'dir');
  t.after(() => fs.rmSync(linked, { force: true }));
  await assert.rejects(
    helpers.takeScreenshot(page, 'result', { outputDirectory: linked }),
    /non-symlink|traverse symlinks/,
  );
});

test('authentication and cookie helpers require explicit success and consent', async () => {
  const credentials = new Proxy({}, { get: () => true });
  await assert.rejects(
    helpers.authenticate({}, credentials),
    /successIndicator or successURL/,
  );
  await assert.rejects(
    helpers.handleCookieBanner({}, undefined),
    /explicitly "accept" or "reject"/,
  );
});

test('server detection probes only reviewed ports', async (t) => {
  await assert.rejects(helpers.detectDevServers(), /reviewed candidate ports/);
  await assert.rejects(helpers.detectDevServers([0]), /between 1 and 65535/);

  const server = http.createServer((request, response) => {
    response.writeHead(204);
    response.end();
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, 'localhost', resolve);
  });
  t.after(() => server.close());
  const address = server.address();
  const detected = await helpers.detectDevServers([address.port]);
  assert.deepEqual(detected, [`http://localhost:${address.port}`]);
});
