const fs = require('fs');
const path = require('path');

/**
 * generate-data-graph.js
 * 
 * Generates the data.graph.js manifest for the PF Explorer.
 */

const BASE_DIR = path.resolve(__dirname, '../../');
const EXPLORER_DIR = path.join(BASE_DIR, 'sandbox/explorer');
const CLAIMS_PATH = path.join(BASE_DIR, 'CLAIMS.md');
const DEFS_DIR = path.join(BASE_DIR, 'definitions');
const NOGOS_PATH = path.join(EXPLORER_DIR, 'nogos.js');
const DATA_JS_PATH = path.join(EXPLORER_DIR, 'data.js');
const OUTPUT_PATH = path.join(EXPLORER_DIR, 'data.graph.js');

function slugify(text) {
  if (!text) return 'unnamed';
  
  // Strip bold markers
  let s = text.replace(/\*\*/g, '').trim();
  
  // Manual Mapping for core framework results to maintain stable IDs
  const mapping = {
    "Gravity as Optical Geometry": "gravity-optical",
    "Gravity as Optical Geometry / Refraction": "gravity-optical",
    "Koide Law for Charged Leptons": "koide-leptons",
    "Weinberg Angle": "weinberg-angle",
    "The God Equation": "god-equation",
    "λ_c from l_P": "god-equation",
    "Three Generations": "three-generations",
    "Koide Phase": "koide-phase",
    "Top Quark Limit": "top-quark-limit",
    "Top/Tau coupling": "top-tau-coupling",
    "Coherence Ceiling": "coherence-ceiling",
    "Propagation Lagrangian": "propagation-lagrangian",
    "Variable c Prediction": "variable-c",
    "QCD Confinement": "qcd-confinement",
    "Neutrino Koide non-universality": "neutrino-koide",
    "Topological Weights": "weights-21",
    "Electron/Up": "phi3-ratio",
    "2/3 Efficiency Ratio": "efficiency-ratio",
    "Aria Self-Reference": "aria-self-reference"
  };

  for (const [key, val] of Object.entries(mapping)) {
    if (s.includes(key)) return val;
  }

  return s.toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');
}

function parseMarkdownTable(text) {
  const lines = text.trim().split('\n').filter(l => l.trim().startsWith('|'));
  if (lines.length < 3) return [];
  
  const headers = lines[0].split('|').map(s => s.trim()).filter(Boolean);
  const data = [];
  
  for (let i = 2; i < lines.length; i++) {
    let cells = lines[i].split('|').map(s => s.trim());
    if (lines[i].trim().startsWith('|')) cells.shift();
    if (lines[i].trim().endsWith('|')) cells.pop();
    
    // Join extra cells back if we have more than headers (common in PF tables with pipes in evidence)
    if (cells.length > headers.length) {
      // Logic: if we have 5 headers but 7 cells, we assume cells[2] swallowed 2 pipes.
      // We merge cells[2...cells.length - (headers.length - 2)]
      const extraCount = cells.length - headers.length;
      const mergedCell = cells.slice(2, 2 + extraCount + 1).join(' | ');
      cells.splice(2, extraCount + 1, mergedCell);
    }
    
    if (cells.length < headers.length) continue;
    
    const obj = {};
    headers.forEach((h, idx) => {
      const key = h.toLowerCase().replace(/[^\w]/g, '_').replace(/_+/g, '_').replace(/^_|_$/g, '');
      obj[key] = (cells[idx] || '').trim();
    });
    data.push(obj);
  }
  return data;
}

function extractSections(text) {
  const sections = {};
  const lines = text.split('\n');
  let currentTitle = '';
  let currentContent = [];
  
  lines.forEach(line => {
    const headerMatch = line.match(/^#+\s+(.*)/);
    if (headerMatch) {
      if (currentTitle) {
        sections[currentTitle] = currentContent.join('\n');
      }
      let title = headerMatch[1].trim();
      // Cleanup common prefixes
      title = title.replace(/^[⦿\d\.\s]*/, '').trim();
      currentTitle = title;
      currentContent = [];
    } else {
      currentContent.push(line);
    }
  });
  if (currentTitle) {
    sections[currentTitle] = currentContent.join('\n');
  }
  return sections;
}

function extractTable(sectionText) {
  const lines = sectionText.split('\n');
  const tableLines = [];
  let inTable = false;
  
  for (const line of lines) {
    if (line.trim().startsWith('|')) {
      inTable = true;
      tableLines.push(line);
    } else if (inTable) {
      if (line.trim() === '' || line.trim().startsWith('---')) continue;
      if (!line.trim().startsWith('|')) break;
      tableLines.push(line);
    }
  }
  return tableLines.join('\n');
}

function findJSArray(content, key) {
  const startIdx = content.indexOf(key + ': [');
  if (startIdx === -1) return null;
  
  let depth = 0;
  let endIdx = -1;
  const sub = content.substring(startIdx + (key + ': ').length);
  for (let i = 0; i < sub.length; i++) {
    if (sub[i] === '[') depth++;
    if (sub[i] === ']') {
      depth--;
      if (depth === 0) {
        endIdx = i + 1;
        break;
      }
    }
  }
  
  if (endIdx !== -1) {
    const arrayStr = sub.substring(0, endIdx);
    try {
      return eval(arrayStr);
    } catch (e) {
      console.error(`Failed to eval ${key}`);
      return null;
    }
  }
  return null;
}

async function run() {
  console.log('--- Generating data.graph.js ---');
  
  // 1. Read Baseline data.js
  let baseline = { scales: [], panelMeta: [] };
  if (fs.existsSync(DATA_JS_PATH)) {
    const dataJsRaw = fs.readFileSync(DATA_JS_PATH, 'utf8');
    baseline.scales = findJSArray(dataJsRaw, 'scales') || [];
    baseline.panelMeta = findJSArray(dataJsRaw, 'panelMeta') || [];
  }

  // 2. Read and Parse CLAIMS.md
  const claimsRaw = fs.readFileSync(CLAIMS_PATH, 'utf8');
  const sections = extractSections(claimsRaw);
  
  const foundDefs = parseMarkdownTable(extractTable(sections['Foundational Definitions'] || ''));
  const physClaims = parseMarkdownTable(extractTable(sections['Fundamental Physics'] || ''));
  const bioClaims = parseMarkdownTable(extractTable(sections['Biological & Cognitive Systems'] || ''));

  // 3. Parse Duck's Honest Log
  const honestyLogs = [];
  const duckSection = sections["The Duck's Honest Log"] || sections["Honest Log"] || '';
  const duckLines = duckSection.split('\n');
  duckLines.forEach(line => {
    const match = line.match(/^\d+\.\s+\*\*(.*?)\*\*:\s*(.*)/);
    if (match) {
      honestyLogs.push({ title: match[1], content: match[2] });
    }
  });

  // 4. Map Claims
  const allRawClaims = [...physClaims, ...bioClaims];
  const claims = allRawClaims.map(c => {
    const title = c.claim || c.definition || 'Unnamed Claim';
    const id = slugify(title);
    
    let scaleId = 'matter';
    if (title.toLowerCase().includes('planck')) scaleId = 'planck';
    if (title.toLowerCase().includes('gravity')) scaleId = 'atomic';
    if (title.toLowerCase().includes('sleep') || title.toLowerCase().includes('beauty')) scaleId = 'human';
    if (title.toLowerCase().includes('consciousness')) scaleId = 'neural';

    return {
      id,
      title,
      status: (c.status || 'OPEN').replace(/\(.*\)/g, '').replace(/\*/g, '').replace(/—.*/, '').trim(),
      confidence: parseFloat(c.confidence) || 0,
      kind: physClaims.includes(c) ? "Fundamental Physics" : "Biological & Cognitive",
      summary: c.evidence || '',
      falsifier: c.what_falsifies_it || c.what_would_make_it_inadequate || '',
      scaleId
    };
  });

  // 5. Read definitions/*.md
  const defFiles = fs.readdirSync(DEFS_DIR).filter(f => f.endsWith('.md') && f !== 'README.md');
  const definitions = defFiles.map(file => {
    const content = fs.readFileSync(path.join(DEFS_DIR, file), 'utf8');
    const titleMatch = content.match(/^# (.*)/);
    const title = titleMatch ? titleMatch[1].trim() : file.replace('.md', '');
    const id = file.replace('.md', '').replace(/_/g, '-');
    
    // Better oneLiner: find the first bold block after ## The Definition or Axiom Statement
    let oneLiner = '';
    const defMatch = content.match(/## (?:The )?Definition[\s\S]*?\*\*([\s\S]*?)\*\*/i) || 
                      content.match(/## Axiom[\s\S]*?\*\*([\s\S]*?)\*\*/i) ||
                      content.match(/\*\*([\s\S]*?)\*\*/);
    if (defMatch) oneLiner = defMatch[1].replace(/\n/g, ' ').trim();

    // Extract Story Line (General Reader section)
    const readerMatch = content.match(/## For the General Reader\s*([\s\S]*?)(?=\n---|\n## |$)/i);
    let storyLine = readerMatch ? readerMatch[1].trim() : '';

    // Status
    const statusMatch = content.match(/\*Status: (.*?)\*/);
    const statusLine = statusMatch ? statusMatch[1] : 'CANONICAL v1.0';

    return {
      id,
      title,
      file,
      oneLiner,
      storyLine,
      status: statusLine,
      sources: [{ label: `definitions/${file}`, href: `../../definitions/${file}` }]
    };
  });

  // 6. Merge No-Gos
  let noGoEntries = [];
  if (fs.existsSync(NOGOS_PATH)) {
    const nogosRaw = fs.readFileSync(NOGOS_PATH, 'utf8');
    noGoEntries = findJSArray(nogosRaw, 'var NO_GO_ENTRIES = ') || findJSArray(nogosRaw, 'NO_GO_ENTRIES') || [];
  }

  // 7. Final Assembly
  const dataGraph = {
    generatedAt: new Date().toISOString().split('T')[0],
    sourceHash: "auto-generated",
    definitions,
    claims,
    noGos: noGoEntries,
    honestyLogs,
    scales: baseline.scales,
    panelMeta: baseline.panelMeta
  };

  const outputContent = `/**
 * data.graph.js - GENERATED FILE
 */

(function () {
  'use strict';
  window.PFDataGraph = ${JSON.stringify(dataGraph, null, 2)};
})();
`;

  fs.writeFileSync(OUTPUT_PATH, outputContent);
  console.log(`Successfully generated ${OUTPUT_PATH} with ${claims.length} claims and ${definitions.length} definitions.`);
}

run().catch(err => {
  console.error('Generation failed:', err);
  process.exit(1);
});
