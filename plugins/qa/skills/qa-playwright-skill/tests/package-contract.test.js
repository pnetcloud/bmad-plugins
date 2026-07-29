'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const skillDirectory = path.resolve(__dirname, '..');

function read(relativePath) {
  return fs.readFileSync(path.join(skillDirectory, relativePath), 'utf8');
}

test('all original package resources remain present', () => {
  for (const relativePath of [
    'SKILL.md',
    'API_REFERENCE.md',
    'run.js',
    'lib/helpers.js',
    'package.json',
  ]) {
    assert.ok(fs.statSync(path.join(skillDirectory, relativePath)).isFile());
  }
});

test('API reference retains every original capability section', () => {
  const reference = read('API_REFERENCE.md');
  for (const heading of [
    'Installation & Setup',
    'Core Patterns',
    'Selectors & Locators',
    'Common Actions',
    'Waiting Strategies',
    'Assertions',
    'Page Object Model (POM)',
    'Network & API Testing',
    'Authentication & Session Management',
    'Visual Testing',
    'Mobile Testing',
    'Debugging',
    'Performance Testing',
    'Parallel Execution',
    'Data-Driven Testing',
    'Accessibility Testing',
    'CI/CD Integration',
    'Best Practices',
    'Common Patterns & Solutions',
    'Troubleshooting',
  ]) {
    assert.ok(reference.includes(`## ${heading}\n`), heading);
  }
  for (const pattern of [
    '### Responsive Viewport Evidence',
    '### Link Validation',
    '### Handling Popups',
    '### File Downloads',
    '### iFrames',
    '### Infinite Scroll',
  ]) {
    assert.ok(reference.includes(pattern), pattern);
  }
});

test('helper module retains all original exports', () => {
  const exported = require('../lib/helpers');
  for (const name of [
    'launchBrowser',
    'createPage',
    'waitForPageReady',
    'safeClick',
    'safeType',
    'extractTexts',
    'takeScreenshot',
    'authenticate',
    'scrollPage',
    'extractTableData',
    'handleCookieBanner',
    'retryWithBackoff',
    'createContext',
    'detectDevServers',
    'getExtraHeadersFromEnv',
  ]) {
    assert.equal(typeof exported[name], 'function', name);
  }
});

test('entrypoint is compact while all advanced capabilities stay reachable', () => {
  const entrypoint = read('SKILL.md');
  const lineCount = entrypoint.split('\n').length;
  const wordCount = (entrypoint.match(/\S+/g) || []).length;
  assert.ok(lineCount >= 80 && lineCount <= 180, `SKILL.md lines: ${lineCount}`);
  assert.ok(wordCount >= 600 && wordCount <= 1500, `SKILL.md words: ${wordCount}`);
  assert.match(entrypoint, /\[API_REFERENCE\.md\]\(API_REFERENCE\.md\)/);
  assert.match(entrypoint, /\[lib\/helpers\.js\]\(lib\/helpers\.js\)/);
});
