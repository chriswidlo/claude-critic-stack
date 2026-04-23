#!/usr/bin/env node
// bin/ingest-canon.mjs
//
// Populates canon/corpus/<slug>/ from canon/sources.ingest.yaml.
// Zero dependencies: uses Node 18+ built-ins only (fetch, crypto, fs).
//
// Usage:
//   node ./bin/ingest-canon.mjs                 # ingest all sources not yet present
//   node ./bin/ingest-canon.mjs --force         # refetch everything
//   node ./bin/ingest-canon.mjs --only=<slug>   # restrict to one slug
//
// Idempotent: skips slugs whose source.txt already exists unless --force.

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve, join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import crypto from 'node:crypto';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

// ---------------------------------------------------------------------------
// Argv
// ---------------------------------------------------------------------------
function parseArgs(argv) {
  const out = { force: false, only: null };
  for (const a of argv) {
    if (a === '--force') out.force = true;
    else if (a.startsWith('--only=')) out.only = a.slice(7);
  }
  return out;
}

// ---------------------------------------------------------------------------
// Minimal YAML parser for canon/sources.ingest.yaml's restricted schema.
// Handles: `key: value`, list items under `sources:` beginning with `- `,
// flow maps `{a: b, c: d}`, flow sequences `[a, b]`, quoted/unquoted scalars,
// numbers, booleans, comments. Does NOT handle anchors, block scalars,
// deep nesting beyond `sources: -` items.
// ---------------------------------------------------------------------------
function parseSourcesYaml(text) {
  const lines = text.split('\n');
  const entries = [];
  let current = null;
  let inSources = false;

  for (let raw of lines) {
    // strip trailing comment but not inside quotes; easier: drop whole-line comments
    if (/^\s*#/.test(raw)) continue;
    // strip trailing comment: `  key: value  # note` -> `  key: value`
    raw = raw.replace(/(^|\s)#.*$/, '$1').replace(/\s+$/, '');
    if (!raw.trim()) continue;

    if (/^sources:\s*$/.test(raw)) { inSources = true; continue; }
    if (!inSources) continue;

    // Block-sequence item: starts with `  - key: value`
    const itemMatch = raw.match(/^(\s*)-\s+(.+)$/);
    if (itemMatch) {
      if (current) entries.push(current);
      current = {};
      const kv = parseKv(itemMatch[2]);
      if (kv) Object.assign(current, kv);
      continue;
    }
    // Continuation field of current entry: `    key: value`
    const kvMatch = raw.match(/^(\s+)(\w+):\s*(.*)$/);
    if (kvMatch && current) {
      const key = kvMatch[2];
      const val = parseValue(kvMatch[3]);
      current[key] = val;
    }
  }
  if (current) entries.push(current);
  return { sources: entries };
}

function parseKv(fragment) {
  const m = fragment.match(/^(\w+):\s*(.*)$/);
  if (!m) return null;
  return { [m[1]]: parseValue(m[2]) };
}

function parseValue(rawIn) {
  const raw = String(rawIn ?? '').trim();
  if (!raw) return null;
  if ((raw.startsWith('"') && raw.endsWith('"')) || (raw.startsWith("'") && raw.endsWith("'"))) {
    return raw.slice(1, -1);
  }
  if (raw.startsWith('{') && raw.endsWith('}')) {
    const inner = raw.slice(1, -1);
    const obj = {};
    for (const p of splitTopLevel(inner, ',')) {
      const idx = p.indexOf(':');
      if (idx === -1) continue;
      const k = p.slice(0, idx).trim().replace(/^["']|["']$/g, '');
      obj[k] = parseValue(p.slice(idx + 1));
    }
    return obj;
  }
  if (raw.startsWith('[') && raw.endsWith(']')) {
    return splitTopLevel(raw.slice(1, -1), ',').map(parseValue).filter(v => v !== null);
  }
  if (/^-?\d+(\.\d+)?$/.test(raw)) return parseFloat(raw);
  if (raw === 'true') return true;
  if (raw === 'false') return false;
  if (raw === 'null' || raw === '~') return null;
  return raw;
}

function splitTopLevel(s, delim) {
  const out = [];
  let depth = 0, inStr = null, buf = '';
  for (const ch of s) {
    if (inStr) {
      if (ch === inStr) inStr = null;
      buf += ch;
    } else if (ch === '"' || ch === "'") {
      inStr = ch; buf += ch;
    } else if (ch === '[' || ch === '{') {
      depth++; buf += ch;
    } else if (ch === ']' || ch === '}') {
      depth--; buf += ch;
    } else if (ch === delim && depth === 0) {
      if (buf.trim()) out.push(buf);
      buf = '';
    } else {
      buf += ch;
    }
  }
  if (buf.trim()) out.push(buf);
  return out;
}

// ---------------------------------------------------------------------------
// HTML → plain text. Regex-based; handles the common subset we need.
// ---------------------------------------------------------------------------
function stripHtml(html) {
  if (!html) return '';
  // Remove full blocks we don't want (script/style/nav/footer/aside/header/head/noscript).
  // NOTE: `<form>` is intentionally NOT in this list — ASP.NET WebForms and other
  // legacy CMSes wrap the entire page body in a single <form>, so dropping form
  // blocks deletes all content. We instead strip form open/close tags below and
  // keep their children, which is the right behavior for content extraction.
  html = html.replace(/<(script|style|nav|footer|aside|header|head|noscript)\b[^>]*>[\s\S]*?<\/\1>/gi, '');
  // Remove HTML comments
  html = html.replace(/<!--[\s\S]*?-->/g, '');
  // Headings
  html = html.replace(/<h([1-6])[^>]*>([\s\S]*?)<\/h\1>/gi,
    (_, lvl, txt) => `\n\n${'#'.repeat(parseInt(lvl, 10))} ${stripInline(txt).trim()}\n\n`);
  // Block elements → newlines
  html = html.replace(/<\/(p|div|li|tr|blockquote|pre|section|article)>/gi, '\n');
  html = html.replace(/<(p|div|li|tr|blockquote|pre|section|article)[^>]*>/gi, '\n');
  html = html.replace(/<br\s*\/?>/gi, '\n');
  // Strip remaining tags
  html = html.replace(/<[^>]+>/g, '');
  // Decode entities
  html = decodeEntities(html);
  // Collapse whitespace
  html = html.replace(/[ \t]+/g, ' ');
  html = html.split('\n').map(l => l.trim()).join('\n');
  html = html.replace(/\n{3,}/g, '\n\n');
  return html.trim();
}

function stripInline(html) {
  return decodeEntities(String(html).replace(/<[^>]+>/g, ''));
}

function decodeEntities(s) {
  const named = {
    amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ',
    ldquo: '"', rdquo: '"', lsquo: '‘', rsquo: '’',
    mdash: '—', ndash: '–', hellip: '…', copy: '©', trade: '™',
  };
  return String(s)
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n, 10)))
    .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCharCode(parseInt(n, 16)))
    .replace(/&([a-z]+);/gi, (m, name) => named[name.toLowerCase()] ?? m)
    .replace(/&[a-z0-9]+;/gi, ''); // drop any remaining unknown named entities
}

// ---------------------------------------------------------------------------
// HTTP
// ---------------------------------------------------------------------------
const UA = 'Mozilla/5.0 (compatible; canon-ingest/1.0; +claude-critic-stack)';

async function httpGet(url, { retries = 2 } = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, {
        headers: {
          'User-Agent': UA,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-US,en;q=0.9',
        },
        redirect: 'follow',
      });
      if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText} from ${url}`);
      return await res.text();
    } catch (e) {
      lastErr = e;
      if (attempt < retries) {
        await new Promise(r => setTimeout(r, 500 * (attempt + 1)));
      }
    }
  }
  throw lastErr;
}

// ---------------------------------------------------------------------------
// Fetch modes
// ---------------------------------------------------------------------------
async function fetchAndExtract(src) {
  switch (src.fetch) {
    case 'html':       return stripHtml(await httpGet(src.url));
    case 'html-multi': return await fetchHtmlMulti(src);
    case 'arxiv-abs':  return await fetchArxivAbs(src);
    case 'aws-docs':   return await fetchAwsDocs(src);
    case 'pdf-manual':
      // Explicit signal: source is a PDF and must be ingested via
      // bin/ingest-owned-book.mjs after local pdftotext conversion.
      // Skip during automated runs — the entry stays as a stub.
      throw new Error('pdf-manual: this source is a PDF; convert with pdftotext and run bin/ingest-owned-book.mjs. Not fetched automatically.');
    default:           throw new Error(`unknown fetch mode: ${src.fetch}`);
  }
}

// AWS docs: TOC is a JSON file (toc-contents.json) listing href to each chapter.
// URL should point directly at the JSON endpoint; we walk recursively through `contents`.
async function fetchAwsDocs(src) {
  const tocRaw = await httpGet(src.url);
  const toc = JSON.parse(tocRaw);
  const tocUrl = new URL(src.url);
  const base = tocUrl.origin + tocUrl.pathname.replace(/[^/]+\/?$/, '');

  const flat = [];
  (function walk(items) {
    if (!Array.isArray(items)) return;
    for (const it of items) {
      if (it && it.href) flat.push({ title: it.title || '', href: it.href });
      if (it && Array.isArray(it.contents)) walk(it.contents);
    }
  })(toc.contents || []);

  if (flat.length === 0) throw new Error(`aws-docs: no entries found in ${src.url}`);

  const limited = flat.slice(0, HTML_MULTI_MAX_CHAPTERS);
  const parts = [`AWS documentation — ${flat.length} sections (ingesting first ${limited.length})`];
  for (const ch of limited) {
    const chUrl = new URL(ch.href, base).href;
    try {
      const body = await httpGet(chUrl);
      parts.push(`\n\n=== ${ch.title} ===\n${chUrl}\n\n${stripHtml(body)}`);
    } catch (e) {
      parts.push(`\n\n=== ${ch.title} ===\n${chUrl}\n\n[FETCH ERROR: ${e.message}]`);
    }
  }
  return parts.join('');
}

// Cap on how many child chapters html-multi / aws-docs will follow from a TOC.
// Prevents runaway ingestion if a TOC links to every page on a large doc site.
// 100 covers AWS SaaS Lens (~50 sections) fully; SRE Book will be capped at 100.
// Raise per-source in sources.ingest.yaml (future: add per-entry `max_chapters`).
const HTML_MULTI_MAX_CHAPTERS = 100;
const NAV_NOISE = /^(home|back|next|previous|search|menu|contents|index|about|contact|help|subscribe|login|sign\s*up)$/i;

async function fetchHtmlMulti(src) {
  const tocHtml = await httpGet(src.url);
  const tocUrl = new URL(src.url);
  // Strip the last path segment (with or without trailing slash):
  //   /a/b/c/      → /a/b/
  //   /a/b/c.html  → /a/b/
  const basePath = tocUrl.pathname.replace(/[^/]+\/?$/, '');
  const base = tocUrl.origin + basePath;

  const links = [...tocHtml.matchAll(/<a[^>]+href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi)];
  const seen = new Set();
  const chapters = [];
  for (const [, href, inner] of links) {
    if (href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('javascript:')) continue;
    let abs;
    try { abs = new URL(href, src.url).href; } catch { continue; }
    // strip query/fragment for dedup
    abs = abs.replace(/[#?].*$/, '');
    if (!abs.startsWith(base)) continue;
    if (abs === src.url || abs === src.url + '/') continue;
    if (seen.has(abs)) continue;
    const title = stripInline(inner).trim().replace(/\s+/g, ' ');
    if (!title || NAV_NOISE.test(title) || title.length < 3) continue;
    seen.add(abs);
    chapters.push({ url: abs, title });
    if (chapters.length >= HTML_MULTI_MAX_CHAPTERS) break;
  }

  if (chapters.length === 0) {
    // Fall back to just the TOC page
    return stripHtml(tocHtml);
  }

  const parts = [];
  parts.push(stripHtml(tocHtml));
  parts.push('\n\n=== TABLE OF CONTENTS END ===\n');

  for (const ch of chapters) {
    try {
      const body = await httpGet(ch.url);
      parts.push(`\n\n=== ${ch.title} ===\n${ch.url}\n\n${stripHtml(body)}`);
    } catch (e) {
      parts.push(`\n\n=== ${ch.title} ===\n${ch.url}\n\n[FETCH ERROR: ${e.message}]`);
    }
  }
  return parts.join('');
}

async function fetchArxivAbs(src) {
  // Normalize URL to /abs/ form
  let absUrl = src.url.replace(/\/html\//, '/abs/').replace(/\/pdf\//, '/abs/');
  absUrl = absUrl.replace(/v\d+(\/|$)/, '$1').replace(/\.pdf$/, '');
  const html = await httpGet(absUrl);

  const pickMeta = (name) => {
    const re = new RegExp(`<meta[^>]+name=["']${name}["'][^>]+content=["']([^"']+)["']`, 'i');
    const m = html.match(re);
    return m ? m[1] : null;
  };

  const title = pickMeta('citation_title') || pickMeta('og:title') || '';
  const date = pickMeta('citation_date') || pickMeta('citation_online_date') || '';
  const authors = [...html.matchAll(/<meta[^>]+name=["']citation_author["'][^>]+content=["']([^"']+)["']/gi)]
    .map(m => m[1]);

  const absBlock = html.match(/<blockquote[^>]*class=["'][^"']*abstract[^"']*["'][^>]*>([\s\S]*?)<\/blockquote>/i);
  let abstract = absBlock ? stripHtml(absBlock[1]) : stripHtml(html).slice(0, 3000);
  abstract = abstract.replace(/^Abstract:?\s*/i, '').trim();

  const subjBlock = html.match(/<td[^>]*class=["'][^"']*tablesubjects[^"']*["'][^>]*>([\s\S]*?)<\/td>/i);
  const subject = subjBlock ? stripHtml(subjBlock[1]).trim() : '';

  return [
    `Title: ${title}`,
    ``,
    `Authors: ${authors.join(', ')}`,
    ``,
    `Submitted: ${date}`,
    ``,
    subject ? `Subject: ${subject}` : '',
    ``,
    `Source: ${absUrl}`,
    ``,
    `Abstract`,
    `--------`,
    ``,
    abstract,
  ].filter(l => l !== null && l !== undefined).join('\n');
}

// ---------------------------------------------------------------------------
// Emitters — source.txt provenance header, citation.yaml, README.md
// ---------------------------------------------------------------------------
function sha256Short(s) {
  return crypto.createHash('sha256').update(s, 'utf8').digest('hex').slice(0, 16);
}

function provenanceHeader(src, body) {
  return [
    `---`,
    `slug:         ${src.slug}`,
    `source_url:   ${src.url}`,
    `fetched_at:   ${new Date().toISOString()}`,
    `sha256_short: ${sha256Short(body)}`,
    `fetch_mode:   ${src.fetch}`,
    `license:      ${src.license}`,
    `---`,
    ``,
  ].join('\n');
}

function kindFor(src) {
  if (src.url.includes('arxiv.org') || src.url.includes('aclanthology.org') || src.url.includes('queue.acm.org')) return 'paper';
  if (src.url.includes('sre.google') || src.url.includes('docs.aws.amazon.com')) return 'book';
  return 'essay';
}

function completenessFor(fetch) {
  if (fetch === 'arxiv-abs')  return 'abstract_only';
  if (fetch === 'html-multi') return 'toc_plus_chapters';
  return 'full';
}

function buildCitationYaml(src, sourceText) {
  const topicsList = (src.topics || []).map(String).join(', ');
  const mr = src.manifest_ref || {};
  return [
    `slug: ${src.slug}`,
    `author: "${(mr.author || '').replace(/"/g, '\\"')}"`,
    `title: "${(mr.title || '').replace(/"/g, '\\"')}"`,
    `year: ${mr.year ?? ''}`,
    `kind: ${kindFor(src)}`,
    `topics: [${topicsList}]`,
    `source_url: "${src.url}"`,
    `fetched_at: "${new Date().toISOString()}"`,
    `sha256: "${crypto.createHash('sha256').update(sourceText, 'utf8').digest('hex')}"`,
    `license: "${src.license}"`,
    `body_completeness: ${completenessFor(src.fetch)}`,
    `chapter_offsets: []`,
    `stale: false`,
    `notes: |`,
    `  Fetched by bin/ingest-canon.mjs (${src.fetch} mode).`,
    src.notes ? `  ${src.notes.replace(/\n/g, '\n  ')}` : '',
    ``,
  ].filter(l => l !== '').join('\n') + '\n';
}

function buildReadme(src) {
  const mr = src.manifest_ref || {};
  return [
    `# ${src.slug}`,
    ``,
    `**Author:** ${mr.author || ''}`,
    `**Title:** ${mr.title || ''}`,
    `**Year:** ${mr.year ?? ''}`,
    `**Source:** ${src.url}`,
    `**License:** ${src.license}`,
    `**Fetched:** ${new Date().toISOString().slice(0, 10)}`,
    `**Fetch mode:** ${src.fetch}`,
    ``,
    `## Provenance`,
    ``,
    `Fetched by \`bin/ingest-canon.mjs\` from the URL above. HTML stripped,`,
    `headings preserved as Markdown-style \`#\` lines. No editorial changes.`,
    ``,
    `## How to refresh`,
    ``,
    `\`\`\``,
    `node ./bin/ingest-canon.mjs --only=${src.slug} --force`,
    `\`\`\``,
    ``,
  ].join('\n');
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
async function main() {
  const args = parseArgs(process.argv.slice(2));
  const ingestPath = join(ROOT, 'canon', 'sources.ingest.yaml');
  const text = await readFile(ingestPath, 'utf8');
  const { sources } = parseSourcesYaml(text);

  let ok = 0, skipped = 0, failed = 0;
  const failures = [];

  for (const src of sources) {
    if (args.only && src.slug !== args.only) continue;
    if (!src.slug) {
      console.error(`skip entry without slug: ${JSON.stringify(src).slice(0, 120)}`);
      continue;
    }

    const slugDir = join(ROOT, 'canon', 'corpus', src.slug);
    const sourcePath = join(slugDir, 'source.txt');

    if (!args.force && existsSync(sourcePath)) {
      console.log(`skip    ${src.slug}  (already ingested)`);
      skipped++;
      continue;
    }

    try {
      await mkdir(slugDir, { recursive: true });
      process.stdout.write(`fetch   ${src.slug}  (${src.fetch}) ... `);
      const body = await fetchAndExtract(src);
      const full = provenanceHeader(src, body) + body + '\n';
      await writeFile(sourcePath, full);
      await writeFile(join(slugDir, 'citation.yaml'), buildCitationYaml(src, full));
      await writeFile(join(slugDir, 'README.md'), buildReadme(src));
      console.log(`ok (${full.length.toLocaleString()} chars)`);
      ok++;
    } catch (e) {
      console.log(`FAILED`);
      console.error(`  ↳ ${e.message}`);
      failures.push({ slug: src.slug, error: e.message });
      failed++;
    }
  }

  console.log('');
  console.log(`--- ${ok} ok, ${skipped} skipped, ${failed} failed ---`);
  if (failures.length) {
    console.log('');
    for (const f of failures) console.log(`  FAIL ${f.slug}: ${f.error}`);
  }
  process.exit(failed > 0 ? 1 : 0);
}

main().catch(err => {
  console.error(err);
  process.exit(2);
});
