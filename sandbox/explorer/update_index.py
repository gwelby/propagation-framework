import re

with open('D:/Fundamentals/sandbox/explorer/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_overlay = """<!-- Visual Hook — Confrontation Overlay -->
  <div id="visualHookOverlay" class="visual-hook-overlay" role="dialog" aria-modal="true" aria-labelledby="hook-title" style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; position: fixed; inset: 0; background: var(--void); z-index: 9999; transition: opacity 0.5s ease; opacity: 0;">
    <div class="vh-inner" style="max-width: 800px; padding: 40px; border: 1px solid rgba(200, 168, 255, 0.2); border-radius: 12px; background: var(--deep); box-shadow: 0 20px 80px rgba(0, 0, 0, 0.5);">
      <div class="vh-content vh-confrontation">
        <h1 class="vh-headline" style="color:var(--axiom); font-size: 3rem; margin-bottom: 24px; font-family: var(--headline);">YOUR MODEL OF REALITY IS WRONG.</h1>
        <div class="vh-claims" style="font-size:1.4rem; margin:32px 0; color:var(--text); line-height: 1.8; font-family: var(--body);">
          <p>Gravity isn't a pull. Matter isn't particles.</p>
          <p>Three generations makes no sense.</p>
          <p>The universe has no dark matter.</p>
        </div>
        <div class="vh-actions" style="margin-top: 40px;">
          <button class="vh-cta" id="vhStartBtn" type="button" style="background:var(--axiom); color:var(--void); border: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; font-size: 1.1rem; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; font-family: var(--ui);">
            [But the math works. Explore why.]
          </button>
        </div>
      </div>
    </div>
  </div>"""

# Replace the HTML overlay
html = re.sub(
    r'<!-- Visual Hook — Confrontation Overlay -->.*?</div>\s*</div>',
    new_overlay,
    html,
    flags=re.DOTALL
)

new_script = """<script>
    /* ═══════════════════════════════════════════════════════════
       CONFRONTATION OVERLAY — Static Hook
       ═══════════════════════════════════════════════════════════ */
    (function () {
      const SESSION_KEY = 'pf_explorer_visited';
      let overlayEl, startBtnEl;

      function getOverlayElements() {
        overlayEl = document.getElementById('visualHookOverlay');
        startBtnEl = document.getElementById('vhStartBtn');
      }

      function closeOverlay() {
        if (!overlayEl) return;
        overlayEl.style.opacity = '0';
        try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (e) {}
        setTimeout(() => {
          overlayEl.style.display = 'none';
        }, 500);
      }

      function init() {
        getOverlayElements();
        if (startBtnEl) {
            startBtnEl.addEventListener('click', closeOverlay);
            startBtnEl.addEventListener('mouseover', () => {
                startBtnEl.style.transform = 'scale(1.05)';
                startBtnEl.style.boxShadow = '0 0 20px rgba(200, 168, 255, 0.4)';
            });
            startBtnEl.addEventListener('mouseout', () => {
                startBtnEl.style.transform = 'scale(1)';
                startBtnEl.style.boxShadow = 'none';
            });
        }
        
        try {
          if (!sessionStorage.getItem(SESSION_KEY)) {
            if (overlayEl) {
                overlayEl.style.display = 'flex';
                setTimeout(() => {
                    overlayEl.style.opacity = '1';
                }, 100);
            }
          } else {
            if (overlayEl) overlayEl.style.display = 'none';
          }
        } catch (e) {
          if (overlayEl) {
            overlayEl.style.display = 'flex';
            setTimeout(() => {
                overlayEl.style.opacity = '1';
            }, 100);
          }
        }
      }

      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
      } else {
        init();
      }
    })();"""

# Replace the script that controls it
html = re.sub(
    r'<script>\s*/\* ═══════════════════════════════════════════════════════════\s*CONFRONTATION OVERLAY.*?\n    // Loading screen management',
    new_script + '\n\n    // Loading screen management',
    html,
    flags=re.DOTALL
)

with open('D:/Fundamentals/sandbox/explorer/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
