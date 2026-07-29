'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');

const skillDirectory = path.resolve(__dirname, '..');
const runnerPath = path.join(skillDirectory, 'run.js');
const {
  buildEnvironment,
  parseArgs,
  readCode,
  resolveExecutionDirectory,
  wrapCodeIfNeeded,
} = require(runnerPath);

function temporaryDirectory(t) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'qa-playwright-run-'));
  t.after(() => fs.rmSync(directory, { recursive: true, force: true }));
  return directory;
}

function fakePlaywright(directory) {
  const packageDirectory = path.join(directory, 'node_modules', 'playwright');
  fs.mkdirSync(packageDirectory, { recursive: true });
  const entry = path.join(packageDirectory, 'index.js');
  fs.writeFileSync(entry, 'module.exports = {};\n');
  return entry;
}

function runWithFakePlaywright(t, args, input) {
  const directory = temporaryDirectory(t);
  fakePlaywright(directory);
  return spawnSync(process.execPath, [runnerPath, ...args], {
    cwd: directory,
    encoding: 'utf8',
    env: { ...process.env, NODE_PATH: path.join(directory, 'node_modules') },
    input,
  });
}

test('explicit modes require exactly one source', () => {
  assert.equal(parseArgs(['--file', 'scenario.js']).source.kind, 'file');
  assert.equal(parseArgs(['--inline', 'console.log(1)']).source.kind, 'inline');
  assert.equal(parseArgs(['--stdin']).source.kind, 'stdin');
  assert.throws(
    () => parseArgs(['--stdin', '--inline', 'console.log(1)']),
    /exactly one code source/,
  );
  assert.throws(() => parseArgs(['--unknown']), /unknown option/);
});

test('original positional file, inline, and stdin modes remain compatible', (t) => {
  const directory = temporaryDirectory(t);
  const script = path.join(directory, 'scenario.js');
  fs.writeFileSync(script, 'console.log("file");\n');

  assert.deepEqual(parseArgs([script]).source, { kind: 'file', value: script });
  assert.deepEqual(parseArgs(['console.log("inline")']).source, {
    kind: 'inline',
    value: 'console.log("inline")',
  });
  assert.equal(parseArgs([]).source.kind, 'stdin');
  assert.equal(parseArgs([script]).cwd, skillDirectory);
  assert.equal(parseArgs([]).cwd, skillDirectory);
});

test('file and working-directory paths reject direct and ancestor symlinks', (t) => {
  const directory = temporaryDirectory(t);
  const realDirectory = path.join(directory, 'real');
  const linkedDirectory = path.join(directory, 'linked');
  fs.mkdirSync(realDirectory);
  fs.symlinkSync(realDirectory, linkedDirectory, 'dir');
  const realScript = path.join(realDirectory, 'scenario.js');
  fs.writeFileSync(realScript, 'console.log("safe");\n');
  const directLink = path.join(directory, 'scenario-link.js');
  fs.symlinkSync(realScript, directLink);

  assert.throws(() => readCode({ kind: 'file', value: directLink }), /non-symlink/);
  assert.throws(
    () => readCode({ kind: 'file', value: path.join(linkedDirectory, 'scenario.js') }),
    /traverse symlinks/,
  );
  assert.throws(
    () => resolveExecutionDirectory(linkedDirectory),
    /non-symlink|traverse symlinks/,
  );
});

test('environment is reduced and extra variables require explicit availability', (t) => {
  const directory = temporaryDirectory(t);
  const entry = fakePlaywright(directory);
  const variable = 'QA_PLAYWRIGHT_TEST_VALUE';
  const prior = process.env[variable];
  process.env[variable] = 'synthetic';
  t.after(() => {
    if (prior === undefined) delete process.env[variable];
    else process.env[variable] = prior;
  });

  const environment = buildEnvironment([variable], entry);
  assert.equal(environment[variable], 'synthetic');
  assert.equal(environment.QA_PLAYWRIGHT_HELPERS, path.join(skillDirectory, 'lib/helpers.js'));
  assert.equal(environment.NODE_PATH, path.join(directory, 'node_modules'));
  assert.equal(environment.NODE_OPTIONS, undefined);
  assert.throws(
    () => buildEnvironment(['QA_PLAYWRIGHT_MISSING_VALUE'], entry),
    /unavailable/,
  );
});

test('wrapper preserves injected Playwright and header helper capabilities', () => {
  const wrapped = wrapCodeIfNeeded('console.log(typeof chromium);');
  assert.match(wrapped, /require\('playwright'\)/);
  assert.match(wrapped, /QA_PLAYWRIGHT_HELPERS/);
  assert.match(wrapped, /function getContextOptionsWithHeaders/);
});

test('explicit file, inline, and stdin modes execute in a separate process', (t) => {
  const inline = runWithFakePlaywright(
    t,
    ['--inline', 'console.log("inline-ok")'],
  );
  assert.equal(inline.status, 0, inline.stderr);
  assert.match(inline.stdout, /inline-ok/);

  const fileDirectory = temporaryDirectory(t);
  const fileEntry = fakePlaywright(fileDirectory);
  const script = path.join(fileDirectory, 'scenario.js');
  fs.writeFileSync(script, 'console.log("file-ok");\n');
  const file = spawnSync(
    process.execPath,
    [runnerPath, '--file', script, '--cwd', fileDirectory],
    {
      encoding: 'utf8',
      env: {
        ...process.env,
        NODE_PATH: path.dirname(path.dirname(fileEntry)),
      },
    },
  );
  assert.equal(file.status, 0, file.stderr);
  assert.match(file.stdout, /file-ok/);

  const stdin = runWithFakePlaywright(t, ['--stdin'], 'console.log("stdin-ok");\n');
  assert.equal(stdin.status, 0, stdin.stderr);
  assert.match(stdin.stdout, /stdin-ok/);
});

test('legacy execution preserves skill cwd, helpers, and ambient environment', (t) => {
  const priorHeaderName = process.env.PW_HEADER_NAME;
  process.env.PW_HEADER_NAME = 'X-Synthetic';
  t.after(() => {
    if (priorHeaderName === undefined) delete process.env.PW_HEADER_NAME;
    else process.env.PW_HEADER_NAME = priorHeaderName;
  });
  const source = [
    "const helpers = require('./lib/helpers');",
    "console.log(process.cwd(), typeof helpers.safeClick, process.env.PW_HEADER_NAME);",
  ].join('\n');

  const inline = runWithFakePlaywright(t, [source]);
  assert.equal(inline.status, 0, inline.stderr);
  assert.match(inline.stdout, new RegExp(`${skillDirectory} function X-Synthetic`));

  const stdin = runWithFakePlaywright(t, [], source);
  assert.equal(stdin.status, 0, stdin.stderr);
  assert.match(stdin.stdout, new RegExp(`${skillDirectory} function X-Synthetic`));

  const directory = temporaryDirectory(t);
  const entry = fakePlaywright(directory);
  const script = path.join(directory, 'legacy.js');
  fs.writeFileSync(script, source);
  const file = spawnSync(process.execPath, [runnerPath, script], {
    cwd: directory,
    encoding: 'utf8',
    env: {
      ...process.env,
      NODE_PATH: path.dirname(path.dirname(entry)),
    },
  });
  assert.equal(file.status, 0, file.stderr);
  assert.match(file.stdout, new RegExp(`${skillDirectory} function X-Synthetic`));
});

test('stdin size is rejected before unbounded buffering', (t) => {
  const result = runWithFakePlaywright(t, ['--stdin'], 'x'.repeat(256 * 1024 + 1));
  assert.equal(result.status, 2);
  assert.match(result.stderr, /stdin code exceeds/);
});

test('runner never performs dependency installation', () => {
  const source = fs.readFileSync(runnerPath, 'utf8');
  assert.doesNotMatch(source, /execSync|npm\s+install|npx\s+playwright/);
  assert.doesNotMatch(source, /\.temp-execution-/);
});
