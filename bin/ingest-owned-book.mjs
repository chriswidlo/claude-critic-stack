#!/usr/bin/env node
// bin/ingest-owned-book.mjs
//
// Populates a paywalled-book stub at canon/corpus/<slug>/ from a LOCAL plaintext
// file that the user has legitimately obtained (OCR of an owned ebook, plain-text
// export from an O'Reilly / Manning / Pragmatic subscription, etc.).
//
// Usage:
//   node ./bin/ingest-owned-book.mjs <slug> <path-to-text>
//
// The stub entry (citation.yaml with body_completeness: stub, README.md)
// must already exist at canon/corpus/<slug>/. This script:
//   1. Refuses if source.txt already exists (use --force to overwrite).
//   2. Refuses if <path> is empty or smaller than 10 KB.
//   3. Soft-warns if <path> looks like libgen/sci-hub/z-library to
//      encourage the user to pause; does NOT block.
//   4. Copies the text to canon/corpus/<slug>/source.txt and updates
//      citation.yaml (body_completeness: full, sha256, ingested_at).

import { readFile, writeFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, join, dirname, basename } from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const MIN_BYTES = 10 * 1024;

function die(msg, code = 1) {
  console.error(`error: ${msg}`);
  process.exit(code);
}

function softWarn(msg) {
  console.warn(`warning: ${msg}`);
}

async function main() {
  const argv = process.argv.slice(2);
  const force = argv.includes('--force');
  const positional = argv.filter(a => !a.startsWith('--'));
  const [slug, inputPath] = positional;

  if (!slug || !inputPath) {
    die('usage: node ./bin/ingest-owned-book.mjs <slug> <path-to-text> [--force]');
  }

  const slugDir = join(ROOT, 'canon', 'corpus', slug);
  const sourcePath = join(slugDir, 'source.txt');
  const citationPath = join(slugDir, 'citation.yaml');

  if (!existsSync(slugDir)) {
    die(`stub not found: ${slugDir}\nCreate a stub first (citation.yaml + README.md) or check the slug.`);
  }
  if (!existsSync(citationPath)) {
    die(`stub missing citation.yaml: ${citationPath}`);
  }
  if (existsSync(sourcePath) && !force) {
    die(`${sourcePath} already exists; pass --force to overwrite.`);
  }

  const absInput = resolve(inputPath);
  if (!existsSync(absInput)) {
    die(`input file not found: ${absInput}`);
  }

  const s = await stat(absInput);
  if (s.size < MIN_BYTES) {
    die(`input file is suspiciously small (${s.size} bytes < ${MIN_BYTES}). Refusing to ingest.`);
  }

  const lowerPath = absInput.toLowerCase();
  const red = ['libgen', 'z-library', 'zlibrary', 'sci-hub', 'scihub'].filter(k => lowerPath.includes(k));
  if (red.length) {
    softWarn(`input path contains keyword(s) ${red.join(', ')}. canon/README.md requires text you are licensed to have on your machine. Proceeding — please verify your source is legitimate.`);
  }

  const bytes = await readFile(absInput);
  const text = bytes.toString('utf8');
  const sha = crypto.createHash('sha256').update(text, 'utf8').digest('hex');
  const now = new Date().toISOString();

  // Build a provenance header consistent with bin/ingest-canon.mjs
  const header = [
    `---`,
    `slug:         ${slug}`,
    `source_url:   null`,
    `ingested_at:  ${now}`,
    `sha256_short: ${sha.slice(0, 16)}`,
    `fetch_mode:   owned-local`,
    `license:      owned-book`,
    `---`,
    ``,
  ].join('\n');

  await writeFile(sourcePath, header + text + (text.endsWith('\n') ? '' : '\n'));

  // Patch citation.yaml: flip body_completeness to full, record sha256 + ingested_at.
  let citation = await readFile(citationPath, 'utf8');
  citation = citation.replace(/body_completeness:\s*\w+/, 'body_completeness: full');
  if (/^sha256:/m.test(citation)) {
    citation = citation.replace(/^sha256:.*$/m, `sha256: "${sha}"`);
  } else {
    citation += `\nsha256: "${sha}"\n`;
  }
  if (/^ingested_at:/m.test(citation)) {
    citation = citation.replace(/^ingested_at:.*$/m, `ingested_at: "${now}"`);
  } else {
    citation += `ingested_at: "${now}"\n`;
  }
  await writeFile(citationPath, citation);

  console.log(`ok  ${slug}  (${s.size.toLocaleString()} bytes, sha ${sha.slice(0, 12)}…)`);
}

main().catch(err => {
  console.error(err);
  process.exit(2);
});
