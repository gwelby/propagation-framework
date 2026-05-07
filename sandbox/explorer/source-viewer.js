/**
 * source-viewer.js — Markdown source file viewer
 * Fetches .md files from the Fundamentals directory tree and renders them
 * inline in the evidence drawer. No external library required.
 *
 * Usage:
 *   SourceViewer.open('derivations/gr_fermat_equivalence.md')
 *   SourceViewer.open('definitions/coherence.md')
 *
 * Path resolution: tries paths relative to SOURCES_BASE first.
 * Set window.PF_SOURCES_BASE before this script loads to override.
 */

window.SourceViewer = (function () {
  'use strict';

  // Base path for .md source files.
  // serve.py maps /derivations/ → Fundamentals/derivations/ directly, so BASE = ''.
  // Override by setting window.PF_SOURCES_BASE before this script loads.
  var BASE = (window.PF_SOURCES_BASE !== undefined)
    ? window.PF_SOURCES_BASE
    : '';

  // ── Markdown → HTML renderer ───────────────────────────────────────────────
  // Handles the subset used in Fundamentals derivation files:
  // frontmatter, headers, bold/italic, code blocks, inline code,
  // bullet lists, tables, horizontal rules, math blocks, paragraphs.

  function mdToHtml(text) {
    // Strip frontmatter (--- ... ---)
    text = text.replace(/^---[\s\S]*?---\n?/, '');

    // Pre-pass: protect \[...\] display math blocks (multi-line LaTeX)
    // Replace with placeholder so line-based parser doesn't eat them
    var mathBlocks = [];
    text = text.replace(/\\\[[\s\S]*?\\\]/g, function (m) {
      var idx = mathBlocks.length;
      mathBlocks.push('<div class="sv-math-display">' + m + '</div>');
      return '\x01MATHBLOCK' + idx + '\x01';
    });

    var lines = text.split('\n');
    var out = [];
    var i = 0;

    while (i < lines.length) {
      var line = lines[i];

      // Restore pre-protected math blocks
      if (/\x01MATHBLOCK\d+\x01/.test(line)) {
        var restored = line.replace(/\x01MATHBLOCK(\d+)\x01/g, function (_, n) {
          return mathBlocks[parseInt(n, 10)];
        });
        out.push(restored);
        i++;
        continue;
      }

      // Fenced code block
      if (/^```/.test(line)) {
        var lang = line.replace(/^```/, '').trim();
        var code = [];
        i++;
        while (i < lines.length && !/^```/.test(lines[i])) {
          code.push(escHtml(lines[i]));
          i++;
        }
        out.push('<pre class="sv-code"><code' + (lang ? ' class="lang-' + escHtml(lang) + '"' : '') + '>' +
          code.join('\n') + '</code></pre>');
        i++; // skip closing ```
        continue;
      }

      // Table row
      if (/^\|/.test(line)) {
        var tableLines = [];
        while (i < lines.length && /^\|/.test(lines[i])) {
          tableLines.push(lines[i]);
          i++;
        }
        out.push(renderTable(tableLines));
        continue;
      }

      // Horizontal rule
      if (/^-{3,}$/.test(line.trim()) || /^\*{3,}$/.test(line.trim())) {
        out.push('<hr class="sv-rule">');
        i++;
        continue;
      }

      // Headings
      var hm = line.match(/^(#{1,4})\s+(.*)/);
      if (hm) {
        var lvl = hm[1].length + 1; // h2-h5 (h1 is reserved for the drawer title)
        if (lvl > 5) lvl = 5;
        out.push('<h' + lvl + ' class="sv-h' + lvl + '">' + inline(hm[2]) + '</h' + lvl + '>');
        i++;
        continue;
      }

      // Unordered list
      if (/^[-*+]\s/.test(line)) {
        var listItems = [];
        while (i < lines.length && /^[-*+]\s/.test(lines[i])) {
          listItems.push('<li>' + inline(lines[i].replace(/^[-*+]\s/, '')) + '</li>');
          i++;
        }
        out.push('<ul class="sv-list">' + listItems.join('') + '</ul>');
        continue;
      }

      // Numbered list
      if (/^\d+\.\s/.test(line)) {
        var olItems = [];
        while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
          olItems.push('<li>' + inline(lines[i].replace(/^\d+\.\s/, '')) + '</li>');
          i++;
        }
        out.push('<ol class="sv-list">' + olItems.join('') + '</ol>');
        continue;
      }

      // Blockquote
      if (/^>\s?/.test(line)) {
        var bqLines = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) {
          bqLines.push(lines[i].replace(/^>\s?/, ''));
          i++;
        }
        out.push('<blockquote class="sv-bq">' + inline(bqLines.join(' ')) + '</blockquote>');
        continue;
      }

      // Blank line — paragraph break
      if (line.trim() === '') {
        i++;
        continue;
      }

      // Paragraph — collect consecutive non-special lines
      var paraLines = [];
      while (i < lines.length &&
             lines[i].trim() !== '' &&
             !/^[#\-*+>|`\d\\]/.test(lines[i]) &&
             !/^\x01MATHBLOCK/.test(lines[i]) &&
             !/^-{3,}$/.test(lines[i].trim())) {
        paraLines.push(lines[i]);
        i++;
      }
      if (paraLines.length) {
        out.push('<p class="sv-p">' + inline(paraLines.join(' ')) + '</p>');
      } else {
        i++; // safety — skip unmatched line
      }
    }

    return out.join('\n');
  }

  function renderTable(rows) {
    var html = ['<div class="sv-table-wrap"><table class="sv-table">'];
    rows.forEach(function (row, idx) {
      // Skip separator rows (|---|---|)
      if (/^\|[-|: ]+\|$/.test(row.trim())) return;
      var cells = row.split('|').filter(function (c, ci, a) {
        return ci > 0 && ci < a.length - 1;
      });
      var tag = idx === 0 ? 'th' : 'td';
      html.push('<tr>' + cells.map(function (c) {
        return '<' + tag + '>' + inline(c.trim()) + '</' + tag + '>';
      }).join('') + '</tr>');
    });
    html.push('</table></div>');
    return html.join('');
  }

  function inline(text) {
    // Math — protect ALL forms before any other replacement
    var mathBlocks = [];
    function stash(s) {
      mathBlocks.push(s);
      return '\x00MATH' + (mathBlocks.length - 1) + '\x00';
    }
    // \(...\)  inline LaTeX
    text = text.replace(/\\\([\s\S]*?\\\)/g, function (m) { return stash(m); });
    // $$...$$ display
    text = text.replace(/\$\$([^$]+)\$\$/g, function (_, m) { return stash('$$' + m + '$$'); });
    // $...$ inline (single line only to avoid false positives)
    text = text.replace(/\$([^$\n]{1,120})\$/g, function (_, m) { return stash('$' + m + '$'); });

    // Bold + italic
    text = text.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
    text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
    text = text.replace(/__(.+?)__/g, '<strong>$1</strong>');
    text = text.replace(/_(.+?)_/g, '<em>$1</em>');

    // Inline code
    text = text.replace(/`([^`]+)`/g, '<code class="sv-ic">$1</code>');

    // Links — [text](url)
    text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, function (_, label, href) {
      if (/\.md$/.test(href)) {
        return '<button class="sv-md-link" onclick="SourceViewer.open(\'' +
          escAttr(href) + '\')">' + escHtml(label) + '</button>';
      }
      return '<a href="' + escAttr(href) + '" target="_blank" rel="noopener">' +
        escHtml(label) + '</a>';
    });

    // Restore math
    text = text.replace(/\x00MATH(\d+)\x00/g, function (_, n) {
      return mathBlocks[parseInt(n, 10)];
    });

    return text;
  }

  function escHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function escAttr(s) {
    return String(s).replace(/'/g, '&#39;').replace(/"/g, '&quot;');
  }

  // ── MathJax loader + typesetter ──────────────────────────────────────────
  var _mjLoading = false;
  var _mjReady   = false;

  function _loadMathJax(cb) {
    if (_mjReady) { cb(); return; }
    if (_mjLoading) { document.addEventListener('sv:mjready', cb, { once: true }); return; }
    _mjLoading = true;

    // Configure before loading
    window.MathJax = {
      tex: {
        inlineMath:  [['$','$'], ['\\(','\\)']],
        displayMath: [['$$','$$'], ['\\[','\\]']],
        processEscapes: true,
      },
      options: { skipHtmlTags: ['script','noscript','style','textarea','pre'] },
      startup: {
        ready: function () {
          MathJax.startup.defaultReady();
          _mjReady = true;
          document.dispatchEvent(new Event('sv:mjready'));
          cb();
        }
      }
    };

    var s  = document.createElement('script');
    s.src  = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.min.js';
    s.async = true;
    document.head.appendChild(s);
  }

  function _typeset() {
    _loadMathJax(function () {
      var el = document.getElementById('drawerBody');
      if (!el) return;
      if (window.MathJax && MathJax.typesetPromise) {
        MathJax.typesetPromise([el]).catch(function (e) {
          console.warn('MathJax typeset error:', e);
        });
      }
    });
  }

  // ── Breadcrumb stack for back-navigation ──────────────────────────────────
  var _stack = [];

  // ── Main open function ────────────────────────────────────────────────────
  function open(src, opts) {
    opts = opts || {};

    // Resolve path: try BASE + src, fall back to src as-is
    var url = BASE + src;

    // Show loading state in drawer
    _showInDrawer(
      src.split('/').pop(),
      src,
      '<p class="sv-loading">Loading…</p>',
      true
    );

    fetch(url)
      .then(function (res) {
        if (!res.ok) {
          // Try the path as-is (maybe served from Fundamentals root)
          return fetch(src).then(function (r2) {
            if (!r2.ok) throw new Error('Not found: ' + src);
            return r2;
          });
        }
        return res;
      })
      .then(function (res) { return res.text(); })
      .then(function (text) {
        // Extract title from first # heading or frontmatter
        var titleMatch = text.match(/^#\s+(.+)/m) ||
                         text.match(/^title:\s*(.+)/m);
        var title = titleMatch ? titleMatch[1].trim() : src.split('/').pop();

        var html = mdToHtml(text);
        _stack.push(src);
        _showInDrawer(title, src, html, false);
        _typeset();
      })
      .catch(function (err) {
        _showInDrawer(
          src.split('/').pop(),
          src,
          '<p class="sv-error"><strong>Could not load source file.</strong><br>' +
          '<code>' + escHtml(src) + '</code><br>' +
          '<small>Check that the file server is running from the Fundamentals root directory.</small></p>',
          false
        );
        console.warn('SourceViewer: fetch failed for', src, err);
      });
  }

  function _showInDrawer(title, src, bodyHtml, isLoading) {
    var drawer = document.getElementById('appDrawer');
    var drawerBody = document.getElementById('drawerBody');
    var drawerTitle = document.getElementById('drawerTitle');
    var drawerEyebrow = document.getElementById('drawerEyebrow');

    if (!drawer || !drawerBody) return;

    if (drawerTitle) drawerTitle.textContent = title;
    if (drawerEyebrow) {
      drawerEyebrow.textContent = 'Source File';
    }

    var backBtn = (_stack.length > 0 && !isLoading)
      ? '<button class="sv-back-btn" onclick="SourceViewer.back()">&#8592; Back</button>'
      : '';

    drawerBody.innerHTML =
      '<div class="sv-viewer">' +
        '<div class="sv-meta">' +
          backBtn +
          '<span class="obs-source-pill sv-path-pill">' + escHtml(src) + '</span>' +
        '</div>' +
        '<div class="sv-content">' + bodyHtml + '</div>' +
      '</div>';

    // Open the drawer
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
  }

  function back() {
    _stack.pop();
    if (_stack.length) {
      var prev = _stack.pop();
      open(prev);
    }
  }

  // ── Styles (injected once) ────────────────────────────────────────────────
  function _injectStyles() {
    if (document.getElementById('sv-styles')) return;
    var s = document.createElement('style');
    s.id = 'sv-styles';
    s.textContent = [
      '.sv-viewer { font-size: 14px; line-height: 1.6; color: var(--col-text, #d0d8e8); }',
      '.sv-meta { display:flex; align-items:center; gap:8px; padding:0 0 12px; border-bottom:1px solid rgba(255,255,255,.08); margin-bottom:16px; flex-wrap:wrap; }',
      '.sv-back-btn { background:none; border:1px solid rgba(0,207,255,.4); color:var(--col-cyan,#00cfff); padding:4px 10px; border-radius:4px; cursor:pointer; font-size:12px; }',
      '.sv-back-btn:hover { background:rgba(0,207,255,.1); }',
      '.sv-path-pill { font-size:11px; opacity:.6; word-break:break-all; }',
      '.sv-content { max-width:100%; overflow-x:auto; }',
      '.sv-h2 { font-size:1.15em; font-weight:600; color:var(--col-cyan,#00cfff); margin:1.4em 0 .5em; border-bottom:1px solid rgba(0,207,255,.2); padding-bottom:.3em; }',
      '.sv-h3 { font-size:1em; font-weight:600; color:rgba(255,255,255,.85); margin:1.2em 0 .4em; }',
      '.sv-h4, .sv-h5 { font-size:.95em; font-weight:600; color:rgba(255,255,255,.7); margin:1em 0 .4em; }',
      '.sv-p { margin:.6em 0; }',
      '.sv-code { background:rgba(0,0,0,.4); border:1px solid rgba(255,255,255,.1); border-radius:6px; padding:12px 14px; overflow-x:auto; font-family:monospace; font-size:12.5px; line-height:1.5; color:#c8e0ff; margin:.8em 0; }',
      '.sv-ic { background:rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.12); padding:1px 5px; border-radius:3px; font-family:monospace; font-size:.88em; color:#a8d0ff; }',
      '.sv-list { margin:.5em 0 .5em 1.2em; padding:0; }',
      '.sv-list li { margin:.25em 0; }',
      '.sv-bq { border-left:3px solid var(--col-amber,#ffaa33); margin:.8em 0; padding:.4em .8em; background:rgba(255,170,51,.06); color:rgba(255,255,255,.75); font-style:italic; }',
      '.sv-rule { border:none; border-top:1px solid rgba(255,255,255,.1); margin:1.2em 0; }',
      '.sv-table-wrap { overflow-x:auto; margin:.8em 0; }',
      '.sv-table { border-collapse:collapse; width:100%; font-size:13px; }',
      '.sv-table th, .sv-table td { padding:6px 10px; border:1px solid rgba(255,255,255,.1); text-align:left; }',
      '.sv-table th { background:rgba(0,207,255,.08); color:var(--col-cyan,#00cfff); font-weight:600; }',
      '.sv-table tr:hover td { background:rgba(255,255,255,.03); }',
      '.sv-md-link { background:none; border:none; color:var(--col-cyan,#00cfff); cursor:pointer; padding:0; text-decoration:underline; text-underline-offset:3px; font-size:inherit; }',
      '.sv-md-link:hover { color:#fff; }',
      '.sv-loading { color:rgba(255,255,255,.4); font-style:italic; }',
      '.sv-error { color:var(--col-red,#ff4455); background:rgba(255,68,85,.08); border:1px solid rgba(255,68,85,.2); padding:12px; border-radius:6px; }',
      // Math display blocks
      '.sv-math-display { background:rgba(0,10,30,.5); border:1px solid rgba(0,207,255,.15); border-left:3px solid rgba(0,207,255,.4); border-radius:6px; padding:14px 18px; margin:1em 0; overflow-x:auto; text-align:center; font-size:1.05em; }',
      '.sv-math-display mjx-container { color:#c8e8ff !important; }',
      // MathJax overrides for dark background
      'mjx-container[jax="CHTML"] { color:#c8e8ff; }',
      '.MathJax { color:#c8e8ff !important; }',
    ].join('\n');
    document.head.appendChild(s);
  }

  // Init
  _injectStyles();

  return { open: open, back: back };

}());
