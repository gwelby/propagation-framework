/**
 * panels/observatory.js — Observatory: Visual Launch Pad
 *
 * This is the entry point. It shows LIVE ANIMATED PREVIEWS of every demo,
 * not walls of text. Click any card to launch the full interactive experience.
 *
 * V2: Status badges are pulled from generated data (data.claims.js), not
 * hardcoded. Demo IDs map to authority claim IDs. No hand-written badge
 * may outrank its authority record.
 */
(function () {
  'use strict';

  // Map demo IDs to authority claim IDs for status lookup
  var DEMO_TO_CLAIM_ID = {
    'refraction': 'gravity-optical',
    'koide': 'koide-leptons',
    'weinberg': 'weinberg-angle',
    'bohr': 'bohr-spectrum',
    'generations': 'three-generations',
    'god-equation': 'god-equation-operator',
    'consciousness': 'consciousness-claim',
  };

  // Lookup status from generated data; fallback to UI-only label
  function lookupStatus(demoId, fallbackStatus, fallbackColor) {
    var claimId = DEMO_TO_CLAIM_ID[demoId];
    if (claimId && window.PFTruth && typeof window.PFTruth.getClaim === 'function') {
      var claim = window.PFTruth.getClaim(claimId);
      if (claim) {
        var status = claim.status || claim.badge || fallbackStatus;
        var statusClass = claim.statusClass || '';
        // Map status to color
        var colorMap = {
          'DERIVED': '#44ff88', 'EXACT IDENTITY': '#44ff88',
          'CONDITIONAL': '#ffaa33', 'ARGUED': '#ff9955',
          'EMPIRICAL': '#ffdd55', 'INTUITION': '#888888',
          'OPEN': '#666666', 'STANDARD MATH': '#6699ff'
        };
        return {
          status: status,
          statusColor: colorMap[claim.status] || fallbackColor,
          isSplit: claim.isSplit || false,
          badge: claim.badge || status
        };
      }
    }
    return { status: fallbackStatus, statusColor: fallbackColor, isSplit: false, badge: fallbackStatus };
  }

  // ── Demo catalogue ──────────────────────────────────────────────────────
  // Each entry drives a card. preview: function that draws onto a canvas.
  // Status fields are resolved at render time from generated data.
  var DEMOS = [
    {
      id: 'refraction',
      label: 'Gravity = Refraction',
      _fallbackStatus: 'UNAVAILABLE',
      _fallbackColor: '#44ff88',
      tagline: 'Light bends because space has a refractive index. Not a metaphor — a theorem.',
      preview: previewRefraction,
    },
    {
      id: 'koide',
      label: 'Koide Resonance',
      _fallbackStatus: 'UNAVAILABLE',
      _fallbackColor: '#44ff88',
      tagline: 'Three charged leptons locked at 120°. Q = 2/3 exactly. Zero free parameters.',
      preview: previewKoide,
    },
    {
      id: 'weinberg',
      label: 'Weinberg Angle',
      _fallbackStatus: 'UNAVAILABLE',
      _fallbackColor: '#ff9955',
      tagline: 'sin²θ_W from a Casimir polynomial. Matches experiment to 0.13σ.',
      preview: previewWeinberg,
    },
    {
      id: 'bohr',
      label: 'Bohr Spectrum',
      _fallbackStatus: 'UNAVAILABLE',
      _fallbackColor: '#44ff88',
      tagline: 'Phase closure in the Coulomb field selects the hydrogen energy levels.',
      preview: previewBohr,
    },
    {
      id: 'generations',
      label: 'Three Generations',
      _fallbackStatus: 'UNAVAILABLE',
      _fallbackColor: '#ffaa33',
      tagline: 'Why exactly three families of matter? Q(N)=2/3 has one solution: N=3.',
      preview: previewGenerations,
    },
    {
      id: 'god-equation',
      label: 'God Equation',
      _fallbackStatus: 'UNAVAILABLE',
      _fallbackColor: '#ffaa33',
      tagline: 'λ_c from the Planck length. 1.48% error. The open bridge: H_prod.',
      preview: previewGodEquation,
    },
    {
      id: 'foundations',
      label: 'Three Axioms',
      status: 'AXIOMS',
      statusColor: '#00cfff',
      tagline: 'Propagation · Causal bound · Coherence selection. The only assumptions.',
      preview: previewFoundations,
    },
    {
      id: 'consciousness',
      label: 'Consciousness',
      _fallbackStatus: 'UNAVAILABLE',
      _fallbackColor: 'rgba(255,255,255,.3)',
      tagline: 'Self-referential coherence as a hypothesis. Metric under development.',
      preview: previewConsciousness,
    },
    {
      href: 'belt-trick.html',
      label: 'Belt Trick',
      status: 'DEMO',
      statusColor: '#ffaa33',
      tagline: 'Why fermions need 720° — a visual proof of spin topology.',
      preview: previewBeltTrick,
    },
    {
      href: 'playground.html',
      label: 'Playground',
      status: 'INTERACTIVE',
      statusColor: '#ffdd55',
      tagline: 'Build your own propagation field. Adjust sources, watch interference.',
      preview: previewPlayground,
    },
    {
      href: 'scale-ladder.html',
      label: 'Scale Ladder',
      status: 'JOURNEY',
      statusColor: '#00cfff',
      tagline: '61 orders of magnitude from Planck to cosmic. Full Three.js immersion.',
      preview: previewScaleLadder,
    },
    {
      href: 'journey.html',
      label: 'Story Journey',
      status: 'NARRATIVE',
      statusColor: '#ffdd55',
      tagline: 'A guided path through the framework for a curious non-specialist.',
      preview: previewJourney,
    },
  ];

  // ── Mini canvas preview painters ───────────────────────────────────────
  // Each returns an animation handle { stop() }

  function animLoop(fn) {
    var running = true;
    var frame = 0;
    function tick() {
      if (!running) return;
      fn(frame++);
      requestAnimationFrame(tick);
    }
    tick();
    return { stop: function () { running = false; } };
  }

  function setupCanvas(canvas) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = canvas.offsetWidth || 280;
    var h = canvas.offsetHeight || 140;
    canvas.width  = w * dpr;
    canvas.height = h * dpr;
    var ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return { ctx, w, h };
  }

  function previewRefraction(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#060610';
      ctx.fillRect(0, 0, W, H);
      // Mass glow at right
      var cx = W * 0.75, cy = H * 0.5;
      var grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, H * 0.7);
      grd.addColorStop(0,   'rgba(255,200,60,.45)');
      grd.addColorStop(0.4, 'rgba(255,160,20,.15)');
      grd.addColorStop(1,   'rgba(255,160,20,0)');
      ctx.fillStyle = grd;
      ctx.beginPath(); ctx.arc(cx, cy, H * 0.7, 0, Math.PI * 2); ctx.fill();
      // Mass dot
      ctx.fillStyle = '#ffdd55';
      ctx.shadowColor = '#ffdd55'; ctx.shadowBlur = 12;
      ctx.beginPath(); ctx.arc(cx, cy, 7, 0, Math.PI * 2); ctx.fill();
      ctx.shadowBlur = 0;
      // Light rays — 7 rays, clearly spaced
      var rayCount = 7;
      for (var ray = 0; ray < rayCount; ray++) {
        var yOff = (ray - (rayCount - 1) / 2) * (H * 0.12);
        var bend = H * 0.28 * Math.exp(-Math.abs(yOff) / (H * 0.25));
        var isCentre = ray === Math.floor(rayCount / 2);
        ctx.beginPath();
        ctx.moveTo(0, H / 2 + yOff);
        ctx.bezierCurveTo(W * 0.35, H / 2 + yOff, W * 0.6, H / 2 + yOff + bend * 0.7, W, H / 2 + yOff + bend * 1.3);
        ctx.strokeStyle = isCentre ? 'rgba(0,230,255,.95)' : 'rgba(0,180,255,' + (0.35 + (1 - Math.abs(yOff) / (H * 0.5)) * 0.45) + ')';
        ctx.lineWidth = isCentre ? 2.5 : 1.5;
        ctx.stroke();
      }
      // Animated photon travelling along centre ray
      var t = (f % 90) / 90;
      var px = t * W;
      var bend0 = H * 0.28;
      var py = H / 2 + bend0 * t * (1 - Math.exp(-px / (W * 0.4)));
      ctx.fillStyle = '#ffffff';
      ctx.shadowColor = '#00cfff'; ctx.shadowBlur = 8;
      ctx.beginPath(); ctx.arc(px, py, 3.5, 0, Math.PI * 2); ctx.fill();
      ctx.shadowBlur = 0;
    });
  }

  function previewKoide(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    var masses = [0.511, 105.66, 1776.86];
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var cx = W/2, cy = H/2, r = Math.min(W,H)*0.32;
      var angle = f * 0.012;
      var colors = ['#00cfff','#44ff88','#ffdd55'];
      var labels = ['e','μ','τ'];
      // Triangle lines
      var pts = masses.map(function(m, i) {
        var a = angle + i*Math.PI*2/3 - Math.PI/2;
        var scale = Math.sqrt(m/masses[2]);
        return { x: cx + r*scale*Math.cos(a), y: cy + r*scale*Math.sin(a), color: colors[i] };
      });
      ctx.save();
      ctx.strokeStyle = 'rgba(255,255,255,.15)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      pts.forEach(function(p,i){ i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y); });
      ctx.closePath(); ctx.stroke();
      // Dots
      pts.forEach(function(p,i) {
        var grd = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,16);
        grd.addColorStop(0, p.color.replace(')',',0.4)').replace('rgb','rgba'));
        grd.addColorStop(1, 'transparent');
        ctx.fillStyle = grd;
        ctx.beginPath(); ctx.arc(p.x,p.y,16,0,Math.PI*2); ctx.fill();
        ctx.fillStyle = p.color;
        ctx.beginPath(); ctx.arc(p.x,p.y,5,0,Math.PI*2); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,.6)';
        ctx.font = '10px monospace';
        ctx.fillText(labels[i], p.x+8, p.y-8);
      });
      // Q label
      ctx.fillStyle = '#44ff88';
      ctx.font = 'bold 12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('Q = 2/3', cx, cy+4);
      ctx.textAlign = 'left';
      ctx.restore();
    });
  }

  function previewWeinberg(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var cx = W/2, cy = H/2;
      var t = f * 0.02;
      // Two rotating spin representations
      var r1 = 28, r2 = 42;
      [[r1,'#00cfff','j=½'],[r2,'#ffaa33','j=1']].forEach(function(item, idx) {
        var r=item[0], col=item[1], lbl=item[2];
        var speed = idx === 0 ? 1 : 0.5;
        var ax = cx + r*Math.cos(t*speed);
        var ay = cy + r*Math.sin(t*speed);
        ctx.strokeStyle = col+'66';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.stroke();
        ctx.fillStyle = col;
        ctx.beginPath(); ctx.arc(ax,ay,5,0,Math.PI*2); ctx.fill();
        ctx.font = '9px monospace';
        ctx.fillStyle = col;
        ctx.fillText(lbl, cx+r+4, cy-r+4);
      });
      // sin²θ_W label
      ctx.fillStyle = '#44ff88';
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('sin²θ_W = 0.2231', cx, H-16);
      ctx.fillStyle = 'rgba(255,255,255,.3)';
      ctx.font = '10px monospace';
      ctx.fillText('0.13σ from PDG', cx, H-4);
      ctx.textAlign = 'left';
    });
  }

  function previewBohr(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    var orbits = [20, 35, 50, 65];
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var cx = W/2, cy = H/2;
      // Nucleus
      ctx.fillStyle = '#ffdd55';
      ctx.beginPath(); ctx.arc(cx, cy, 5, 0, Math.PI*2); ctx.fill();
      orbits.forEach(function (r, i) {
        ctx.strokeStyle = 'rgba(0,207,255,' + (0.15+i*0.05) + ')';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI*2); ctx.stroke();
        // Electron
        var speed = 1/(r*0.03);
        var a = f * 0.02 * speed;
        var ex = cx + r*Math.cos(a);
        var ey = cy + r*Math.sin(a);
        ctx.fillStyle = '#00cfff';
        ctx.beginPath(); ctx.arc(ex, ey, 3, 0, Math.PI*2); ctx.fill();
      });
      ctx.fillStyle = '#ffaa33';
      ctx.font = '9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('E_k = −1/(4k²)', cx, H-6);
      ctx.textAlign = 'left';
    });
  }

  function previewGenerations(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.015;
      var cols = ['#00cfff','#44ff88','#ffdd55'];
      var labels = ['Gen I','Gen II','Gen III'];
      cols.forEach(function(col, i) {
        var cx = W*(0.22+i*0.28), cy = H*0.45;
        var r = 22 + 3*Math.sin(t + i*Math.PI*2/3);
        var rVal = parseInt(col.slice(1, 3), 16);
        var gVal = parseInt(col.slice(3, 5), 16);
        var bVal = parseInt(col.slice(5, 7), 16);
        var grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, r * 1.8);
        grd.addColorStop(0, 'rgba(' + rVal + ',' + gVal + ',' + bVal + ', 0.3)');
        grd.addColorStop(1, 'rgba(' + rVal + ',' + gVal + ',' + bVal + ', 0)');
        ctx.fillStyle = grd;
        ctx.beginPath(); ctx.arc(cx, cy, r * 1.5, 0, Math.PI * 2); ctx.fill();
        // simpler:
        ctx.strokeStyle = col+'99';
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.stroke();
        ctx.fillStyle = col;
        ctx.beginPath(); ctx.arc(cx,cy,5,0,Math.PI*2); ctx.fill();
        ctx.fillStyle = col;
        ctx.font = '9px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(labels[i], cx, cy+r+12);
      });
      ctx.fillStyle = '#ffaa33';
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('Q(3) = 2/3  →  N = 3', W/2, H-6);
      ctx.textAlign = 'left';
    });
  }

  function previewGodEquation(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.01;
      // Scale cascade visualization
      var scales = ['Planck','QCD','EW','Human'];
      var ys = [H*0.2, H*0.4, H*0.6, H*0.8];
      var cols = ['#ffdd55','#ff9944','#ffaa33','#00cfff'];
      scales.forEach(function(lbl, i) {
        var x = W*0.15 + W*0.7*Math.abs(Math.sin(t*0.3+i*0.8))*0.15;
        ctx.fillStyle = cols[i];
        ctx.font = '10px monospace';
        ctx.fillText(lbl, x, ys[i]+4);
        ctx.strokeStyle = cols[i]+'55';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(x+50, ys[i]);
        ctx.lineTo(W*0.85, ys[i]);
        ctx.stroke();
        if (i < scales.length-1) {
          ctx.strokeStyle = 'rgba(255,255,255,.15)';
          ctx.beginPath(); ctx.moveTo(W*0.85, ys[i]); ctx.lineTo(W*0.85, ys[i+1]); ctx.stroke();
        }
      });
      var pulse = 0.5+0.5*Math.sin(t*2);
      ctx.fillStyle = 'rgba(255,170,51,'+pulse+')';
      ctx.font = 'bold 11px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('λ_c = √2·l_P·e^(4π²N^(D/2)/b₀)', W/2, H*0.92);
      ctx.textAlign = 'left';
    });
  }

  function previewFoundations(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.008;
      // Three concentric expanding rings — one per axiom
      [[W*0.3,H*0.5,'#00cfff',0],[W*0.5,H*0.5,'#00cfff',1],[W*0.7,H*0.5,'#44ff88',2]].forEach(function(item) {
        var cx=item[0],cy=item[1],col=item[2],phase=item[3];
        for (var ring=0; ring<3; ring++) {
          var r = ((t*30+phase*40+ring*30)%90)+5;
          var alpha = (1-r/90)*0.6;
          ctx.strokeStyle = col.replace('#','').length===6 ?
            ('rgba('+parseInt(col.slice(1,3),16)+','+parseInt(col.slice(3,5),16)+','+parseInt(col.slice(5,7),16)+','+alpha+')') :
            col;
          ctx.lineWidth = 1.5;
          ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.stroke();
        }
        ctx.fillStyle = col;
        ctx.beginPath(); ctx.arc(cx,cy,4,0,Math.PI*2); ctx.fill();
      });
      ctx.fillStyle = '#00cfff';
      ctx.font = '9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('Propagate · Bound · Cohere', W/2, H-6);
      ctx.textAlign = 'left';
    });
  }

  function previewConsciousness(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.02;
      // Self-referential loop
      var cx = W/2, cy = H/2, r = Math.min(W,H)*0.3;
      var points = 64;
      ctx.beginPath();
      for (var i = 0; i <= points; i++) {
        var a = (i/points)*Math.PI*2;
        var wobble = 1 + 0.12*Math.sin(a*3+t) + 0.07*Math.sin(a*7-t*1.3);
        var x = cx + r*wobble*Math.cos(a);
        var y = cy + r*wobble*Math.sin(a);
        i===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
      }
      ctx.closePath();
      ctx.strokeStyle = 'rgba(160,80,255,0.5)';
      ctx.lineWidth = 2;
      ctx.stroke();
      // Center arrow (self-reference)
      ctx.fillStyle = 'rgba(160,80,255,0.8)';
      ctx.font = '28px serif';
      ctx.textAlign = 'center';
      ctx.fillText('∞', cx, cy+10);
      ctx.fillStyle = 'rgba(255,255,255,.3)';
      ctx.font = '9px monospace';
      ctx.fillText('INTUITION · 0.48', cx, H-6);
      ctx.textAlign = 'left';
    });
  }

  function previewBeltTrick(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.015;
      // Rotating band — topology visualization
      var cx = W/2, cy = H/2;
      ctx.strokeStyle = '#ffaa33';
      ctx.lineWidth = 3;
      for (var seg = 0; seg < 20; seg++) {
        var a1 = (seg/20)*Math.PI*2 + t;
        var a2 = ((seg+1)/20)*Math.PI*2 + t;
        var twist = Math.sin(a1*2+t)*0.3;
        var r = 35 + 10*Math.sin(a1+t);
        var x1 = cx + r*Math.cos(a1), y1 = cy + r*Math.sin(a1);
        var x2 = cx + r*Math.cos(a2), y2 = cy + r*Math.sin(a2);
        var alpha = 0.3 + 0.7*Math.abs(Math.sin(a1*0.5));
        ctx.strokeStyle = 'rgba(255,170,51,' + alpha + ')';
        ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
      }
      ctx.fillStyle = 'rgba(255,255,255,.5)';
      ctx.font = '9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('720° to return — click to explore ↗', W/2, H-6);
      ctx.textAlign = 'left';
    });
  }

  function previewPlayground(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    var sources = [{x:W*0.3,y:H*0.5,phase:0},{x:W*0.7,y:H*0.5,phase:Math.PI}];
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.04;
      // Interference pattern — use regular draw calls (avoid ImageData DPR issue)
      var step = 8;
      for (var py = 0; py < H; py += step) {
        for (var px = 0; px < W; px += step) {
          var val = 0;
          sources.forEach(function(s) {
            val += Math.sin(Math.hypot(px-s.x, py-s.y)*0.15 - t + s.phase);
          });
          val = (val/2 + 1)/2;
          ctx.fillStyle = 'rgba(0,' + Math.round(val*180) + ',255,' + (val*0.7) + ')';
          ctx.fillRect(px, py, step, step);
        }
      }
      sources.forEach(function(s) {
        ctx.fillStyle = '#ffdd55';
        ctx.beginPath(); ctx.arc(s.x,s.y,5,0,Math.PI*2); ctx.fill();
      });
      ctx.fillStyle = 'rgba(255,255,255,.5)';
      ctx.font = '9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('Interactive · drag sources ↗', W/2, H-6);
      ctx.textAlign = 'left';
    });
  }

  function previewScaleLadder(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    var labels = ['10⁻³⁵','10⁻¹⁸','10⁻¹⁵','10⁻¹⁰','10⁻⁶','10⁰','10⁹','10²⁶'];
    var cols   = ['#ffdd55','#ff9944','#ff4455','#00cfff','#44ff88','#ffffff','#ffaa33','#00cfff'];
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.005;
      var active = Math.floor(((Math.sin(t)+1)/2) * labels.length);
      // Vertical rail
      var railX = W*0.2, railTop = 10, railBot = H-20;
      ctx.strokeStyle = 'rgba(255,255,255,.12)';
      ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(railX,railTop); ctx.lineTo(railX,railBot); ctx.stroke();
      labels.forEach(function(lbl,i) {
        var y = railTop + (i/(labels.length-1))*(railBot-railTop);
        var isActive = i === active;
        ctx.fillStyle = isActive ? cols[i] : 'rgba(255,255,255,.3)';
        ctx.beginPath(); ctx.arc(railX, y, isActive?5:3, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = isActive ? cols[i] : 'rgba(255,255,255,.25)';
        ctx.font = (isActive?'bold ':'')+' 9px monospace';
        ctx.fillText(lbl, railX+10, y+4);
        if (isActive) {
          // Glow ring
          ctx.strokeStyle = cols[i]+'55';
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.arc(railX,y,12+3*Math.sin(f*0.15),0,Math.PI*2); ctx.stroke();
        }
      });
      ctx.fillStyle = '#00cfff';
      ctx.font = '9px monospace';
      ctx.textAlign = 'right';
      ctx.fillText('61 orders of magnitude ↗', W-8, H-6);
      ctx.textAlign = 'left';
    });
  }

  function previewJourney(canvas) {
    var c = setupCanvas(canvas);
    var ctx = c.ctx, W = c.w, H = c.h;
    var steps = ['Object is process','Force is geometry','Particle is mode','Failure is evidence'];
    return animLoop(function (f) {
      ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = '#070712';
      ctx.fillRect(0, 0, W, H);
      var t = f * 0.008;
      var idx = Math.floor(t) % steps.length;
      var progress = t - Math.floor(t);
      // Progress dots
      steps.forEach(function(_, i) {
        ctx.fillStyle = i < idx ? '#ffdd55' : (i===idx ? ('rgba(255,221,85,'+progress+')') : 'rgba(255,255,255,.15)');
        ctx.beginPath(); ctx.arc(W*0.15+i*(W*0.22), H*0.35, i===idx?5:3, 0, Math.PI*2); ctx.fill();
      });
      // Path line
      ctx.strokeStyle = 'rgba(255,221,85,.3)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(W*0.15, H*0.35);
      ctx.lineTo(W*0.15 + Math.min(idx+(progress),steps.length-1)*(W*0.22), H*0.35);
      ctx.stroke();
      // Current step text
      ctx.fillStyle = '#ffdd55';
      ctx.font = 'bold 11px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(steps[idx], W/2, H*0.6);
      ctx.fillStyle = 'rgba(255,255,255,.3)';
      ctx.font = '9px monospace';
      ctx.fillText('Guided story journey ↗', W/2, H-6);
      ctx.textAlign = 'left';
    });
  }

  // ── DOM builder ─────────────────────────────────────────────────────────
  function buildObservatory() {
    var data   = window.PFClaimsData || {};
    var claims = data.CLAIMS || [];
    var defs   = data.DEFINITIONS || [];
    var nogos  = data.NOGOS || [];
    var derived = claims.filter(function(c){ return c.status && c.status.label==='DERIVED'; });
    var auditedCount = claims.length;

    var scales = [
      { id: 'planck', label: 'Planck', value: '10⁻³⁵m' },
      { id: 'nuclear', label: 'Nuclear', value: '10⁻¹⁵m' },
      { id: 'atomic', label: 'Atomic', value: '10⁻¹⁰m' },
      { id: 'cellular', label: 'Cellular', value: '10⁻⁶m' },
      { id: 'human', label: 'Human', value: '10⁰m' },
      { id: 'planetary', label: 'Planetary', value: '10⁷m' },
      { id: 'galactic', label: 'Galactic', value: '10²¹m' },
      { id: 'cosmic', label: 'Cosmic', value: '10²⁶m' }
    ];

    var html = [
      '<div class="obs-instrument-surface">',

        // --- Pane 1: Scale Rail ---
        '<div class="obs-rail-pane">',
          '<div class="obs-rail">',
            '<div class="obs-wave-front" id="obsWaveFront"></div>',
            scales.map(function(s, i) {
              var pos = (i / (scales.length - 1)) * 100;
              return '<div class="obs-rail-tick" style="top: '+pos+'%;" data-scale="'+s.id+'"></div>' +
                     '<div class="obs-rail-label" style="top: '+pos+'%;">'+s.label+' '+s.value+'</div>';
            }).join(''),
          '</div>',
        '</div>',

        // --- Pane 2: Stat Deck & Featured Proof ---
        '<div class="obs-center-pane">',
          '<div class="obs-header">',
            '<h1>Observatory</h1>',
            '<p>Live interactive preview of the Propagation Framework. Explore claims, derivations, and open questions through propagation-based reasoning.</p>',
          '</div>',
          '<div class="obs-credibility-deck">',
            '<div class="obs-credibility-card obs-credibility-card--derived">',
              '<div class="obs-cred-title">What is Derived</div>',
              '<ul class="obs-cred-list">',
                '<li>Gravity as refraction (static/Randers) <span class="obs-badge-lean">Lean 4 Verified</span></li>',
                '<li>Charged-lepton Koide geometry (Q = 2/3) <span class="obs-badge-lean">Lean 4 Verified</span></li>',
                '<li>Weinberg mixing angle (sin²θ_W ≈ 0.22310) <span class="obs-badge-lean">Lean 4 Verified</span></li>',
                '<li>Casimir polynomial unique positive root <span class="obs-badge-lean">Lean 4 Verified</span> <span class="obs-badge-premise">Sub-Certificate</span></li>',
                '<li>Three Generations algebraic lock (N = 3) <span class="obs-badge-lean">Lean 4 Verified</span> <span class="obs-badge-premise">Premises Conditional</span></li>',
                '<li>SO(2) rotation group structure (ℝ/2πℤ ≅ SO(2)) <span class="obs-badge-lean">Lean 4 Verified</span> <span class="obs-badge-premise">Algebraic Foundation</span></li>',
                '<li>SO(3) double cover (UnitQuaternion → SO(3), ker = {±1}) <span class="obs-badge-lean">Lean 4 Verified</span> <span class="obs-badge-premise">Algebraic Foundation</span></li>',
              '</ul>',
            '</div>',
            '<div class="obs-credibility-card obs-credibility-card--conditional">',
              '<div class="obs-cred-title">What is Conditional</div>',
              '<ul class="obs-cred-list">',
                '<li>God Equation matter scale (1.48% error, open H_prod)</li>',
                '<li>Three Generations N = 3 count (depends on T1/T2)</li>',
                '<li>Scalar-tensor Propagation Lagrangian structure</li>',
              '</ul>',
            '</div>',
            '<div class="obs-credibility-card obs-credibility-card--open">',
              '<div class="obs-cred-title">What remains Open</div>',
              '<ul class="obs-cred-list">',
                '<li>Analytical fine structure constant α derivation</li>',
                '<li>Koide phase δ₀ ≈ 2/9 rational selector</li>',
                '<li>Self-referential dynamic consciousness metrics</li>',
              '</ul>',
            '</div>',
            '<div class="obs-credibility-card obs-credibility-card--falsify">',
              '<div class="obs-cred-title">What would Falsify</div>',
              '<ul class="obs-cred-list">',
                '<li>Precision tau g−2 mismatch beyond QED</li>',
                '<li>Discovery of a 4th-generation fermion</li>',
                '<li>JUNO confirmation of neutrino mass universality</li>',
              '</ul>',
            '</div>',
          '</div>',
          '<div class="obs-stats-deck">',
            '<div class="obs-stat-card" style="border-top: 2px solid #44ff88;">',
              '<div class="obs-stat-val">'+derived.length+'</div>',
              '<div class="obs-stat-lbl">Derived Claims</div>',
            '</div>',
            '<div class="obs-stat-card" style="border-top: 2px solid #ffdd55;">',
              '<div class="obs-stat-val">'+defs.length+'</div>',
              '<div class="obs-stat-lbl">Definitions</div>',
            '</div>',
            '<div class="obs-stat-card" style="border-top: 2px solid #ff4455;">',
              '<div class="obs-stat-val">'+nogos.length+'</div>',
              '<div class="obs-stat-lbl">No-gos</div>',
            '</div>',
            '<div class="obs-stat-card" style="border-top: 2px solid rgba(255,255,255,0.4);">',
              '<div class="obs-stat-val">'+auditedCount+'</div>',
              '<div class="obs-stat-lbl">Audited</div>',
            '</div>',
          '</div>',
          '<div class="obs-featured-proof" id="obsFeaturedKoide" tabindex="0">',
            '<div class="obs-fp-status">DERIVED · CONFIDENCE 95%</div>',
            '<h2 class="obs-fp-title">Koide Resonance (Q = 2/3)</h2>',
            '<p style="color: rgba(255,255,255,0.7); font-size: 14px; line-height: 1.6; margin-bottom: 20px;">',
              'The electron, muon, and tau masses are locked in an exact geometric phase relationship dictated by Axiom 3.',
            '</p>',
            '<div class="obs-fp-bar">',
              '<div class="obs-fp-fill"></div>',
            '</div>',
            '<div class="obs-fp-markers">',
              '<span>Theoretical: 0.666666</span>',
              '<span>Measured: 0.666659</span>',
            '</div>',
          '</div>',
          '<div class="obs-manuscript-link" style="margin-top:auto; padding-top: 20px;">',
             '<a href="PROPAGATION_FRAMEWORK_v1.pdf" target="_blank" style="color:#00cfff; text-decoration:none; font-size:13px; font-weight:600;">READ THE FULL MANUSCRIPT ↗</a>',
          '</div>',
        '</div>',

        // --- Pane 3: Interactive Grid ---
        '<div class="obs-right-pane">',
          '<h3>Interactive Experiments</h3>',
          '<div class="obs-demo-grid" id="obsDemoGrid">',
            DEMOS.map(function(d, i) {
              // Resolve status from generated data for claim-backed demos
              var statusInfo;
              if (d._fallbackStatus) {
                statusInfo = lookupStatus(d.id, d._fallbackStatus, d._fallbackColor);
              } else {
                statusInfo = { status: d.status, statusColor: d.statusColor, badge: d.status };
              }
              var statusText = statusInfo.badge || statusInfo.status;
              var statusColor = statusInfo.statusColor;
              var statusClass = (statusInfo.status || 'unknown').toLowerCase().replace(/[^a-z0-9]+/g, '-');
              var inner = '<div class="obs-demo-canvas-wrap"><canvas class="obs-demo-canvas" width="280" height="140"></canvas></div>' +
                '<div class="obs-demo-info">' +
                  '<div class="obs-demo-status" style="color:'+statusColor+'">'+statusText+'</div>' +
                  '<div class="obs-demo-label">'+d.label+'</div>' +
                  '<div class="obs-demo-tagline">'+d.tagline+'</div>' +
                '</div>';
              if (d.href) {
                return '<a class="obs-demo-card obs-demo-card--'+statusClass+' obs-demo-card--link" ' +
                  'href="'+d.href+'" target="_blank" rel="noopener" data-demo-idx="'+i+'" tabindex="0">' +
                  inner + '</a>';
              }
              return '<div class="obs-demo-card obs-demo-card--'+statusClass+'" data-demo-idx="'+i+'" tabindex="0">' +
                inner + '</div>';
            }).join(''),
          '</div>',
        '</div>',

      '</div>'
    ].join('');

    return html;
  }

  // ── Injected styles ──────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById('obs2-styles')) return;
    var el = document.createElement('style'); el.id = 'obs2-styles';
    el.textContent = [
      '/* Observatory Dashboard World-Class Theme */',
      '.obs-instrument-surface {',
      '  display: grid;',
      '  grid-template-columns: 240px 1fr 340px;',
      '  height: 100%;',
      '  background: #070712;',
      '  color: #fff;',
      '  font-family: "DM Sans", -apple-system, sans-serif;',
      '  overflow: hidden;',
      '}',
      '/* Scale Rail Pane */',
      '.obs-rail-pane {',
      '  border-right: 1px solid rgba(255,255,255,0.08);',
      '  position: relative;',
      '  padding: 40px 20px;',
      '  display: flex;',
      '  flex-direction: column;',
      '  background: rgba(255,255,255,0.01);',
      '}',
      '.obs-rail {',
      '  flex: 1;',
      '  border-left: 1px solid rgba(255,255,255,0.12);',
      '  margin-left: 30px;',
      '  position: relative;',
      '}',
      '.obs-rail-tick {',
      '  position: absolute;',
      '  left: -4px;',
      '  width: 7px; height: 7px; border-radius: 50%;',
      '  background: rgba(255,255,255,0.3);',
      '  transition: background 0.3s;',
      '}',
      '.obs-rail-label {',
      '  position: absolute;',
      '  left: 15px;',
      '  font-family: "JetBrains Mono", monospace;',
      '  font-size: 11px;',
      '  color: rgba(255,255,255,0.5);',
      '  transform: translateY(-4px);',
      '  white-space: nowrap;',
      '  transition: color 0.3s;',
      '}',
      '.obs-wave-front {',
      '  position: absolute;',
      '  left: -10px;',
      '  width: 19px;',
      '  height: 4px;',
      '  background: #00cfff;',
      '  box-shadow: 0 0 10px #00cfff, 0 0 20px #00cfff;',
      '  animation: scanRail 12s infinite linear alternate;',
      '}',
      '@keyframes scanRail {',
      '  0% { top: 0%; }',
      '  100% { top: 100%; }',
      '}',
      '/* Center Pane */',
      '.obs-center-pane {',
      '  padding: 40px;',
      '  overflow-y: auto;',
      '  display: flex;',
      '  flex-direction: column;',
      '  gap: 30px;',
      '  background: radial-gradient(circle at center, rgba(0,207,255,0.03) 0%, transparent 60%);',
      '}',
      '.obs-header h1 {',
      '  font-family: "Spectral", serif;',
      '  font-size: 42px;',
      '  font-weight: 300;',
      '  margin: 0 0 10px;',
      '  letter-spacing: -0.5px;',
      '}',
      '.obs-header p {',
      '  color: rgba(255,255,255,0.6);',
      '  font-size: 15px;',
      '  max-width: 540px;',
      '  line-height: 1.6;',
      '  margin: 0 0 20px 0;',
      '}',
      '/* Credibility Deck */',
      '.obs-credibility-deck {',
      '  display: grid;',
      '  grid-template-columns: repeat(4, 1fr);',
      '  gap: 16px;',
      '  margin-bottom: 10px;',
      '}',
      '.obs-credibility-card {',
      '  background: rgba(255, 255, 255, 0.02);',
      '  border: 1px solid rgba(255, 255, 255, 0.06);',
      '  border-radius: 12px;',
      '  padding: 16px;',
      '  backdrop-filter: blur(16px);',
      '  transition: transform 0.25s cubic-bezier(0.165, 0.84, 0.44, 1), border-color 0.25s, box-shadow 0.25s;',
      '}',
      '.obs-credibility-card:hover {',
      '  transform: translateY(-2px);',
      '  box-shadow: 0 8px 24px rgba(0,0,0,0.3);',
      '}',
      '.obs-credibility-card--derived { border-top: 3px solid #44ff88; }',
      '.obs-credibility-card--derived:hover { border-color: rgba(68,255,136,0.6); box-shadow: 0 8px 24px rgba(68,255,136,0.06); }',
      '.obs-credibility-card--conditional { border-top: 3px solid #ffaa33; }',
      '.obs-credibility-card--conditional:hover { border-color: rgba(255,170,51,0.6); box-shadow: 0 8px 24px rgba(255,170,51,0.06); }',
      '.obs-credibility-card--open { border-top: 3px solid #00cfff; }',
      '.obs-credibility-card--open:hover { border-color: rgba(0,207,255,0.6); box-shadow: 0 8px 24px rgba(0,207,255,0.06); }',
      '.obs-credibility-card--falsify { border-top: 3px solid #ff4455; }',
      '.obs-credibility-card--falsify:hover { border-color: rgba(255,68,85,0.6); box-shadow: 0 8px 24px rgba(255,68,85,0.06); }',
      '.obs-cred-title {',
      '  font-family: "Spectral", serif;',
      '  font-size: 16px;',
      '  font-weight: 500;',
      '  margin-bottom: 12px;',
      '  letter-spacing: -0.2px;',
      '}',
      '.obs-credibility-card--derived .obs-cred-title { color: #44ff88; }',
      '.obs-credibility-card--conditional .obs-cred-title { color: #ffaa33; }',
      '.obs-credibility-card--open .obs-cred-title { color: #00cfff; }',
      '.obs-credibility-card--falsify .obs-cred-title { color: #ff4455; }',
      '.obs-cred-list {',
      '  list-style: none;',
      '  padding: 0;',
      '  margin: 0;',
      '  display: flex;',
      '  flex-direction: column;',
      '  gap: 8px;',
      '}',
      '.obs-cred-list li {',
      '  font-size: 11.5px;',
      '  line-height: 1.4;',
      '  color: rgba(255,255,255,0.7);',
      '  position: relative;',
      '  padding-left: 10px;',
      '}',
      '.obs-cred-list li::before {',
      '  content: "•";',
      '  position: absolute;',
      '  left: 0;',
      '  color: rgba(255,255,255,0.3);',
      '}',
      '.obs-badge-lean {',
      '  display: inline-block;',
      '  font-family: "JetBrains Mono", monospace;',
      '  font-size: 8px;',
      '  background: rgba(68,255,136,0.15);',
      '  color: #44ff88;',
      '  border: 1px solid rgba(68,255,136,0.3);',
      '  border-radius: 4px;',
      '  padding: 1px 4px;',
      '  margin-left: 4px;',
      '  vertical-align: middle;',
      '  text-transform: uppercase;',
      '  letter-spacing: 0.05em;',
      '}',
      '.obs-badge-premise {',
      '  display: inline-block;',
      '  font-family: "JetBrains Mono", monospace;',
      '  font-size: 8px;',
      '  background: rgba(255,221,85,0.15);',
      '  color: #ffdd55;',
      '  border: 1px solid rgba(255,221,85,0.3);',
      '  border-radius: 4px;',
      '  padding: 1px 4px;',
      '  margin-left: 4px;',
      '  vertical-align: middle;',
      '  text-transform: uppercase;',
      '  letter-spacing: 0.05em;',
      '}',
      '.obs-stats-deck {',
      '  display: flex;',
      '  gap: 20px;',
      '  flex-wrap: wrap;',
      '}',
      '.obs-stat-card {',
      '  flex: 1;',
      '  min-width: 100px;',
      '  background: rgba(255,255,255,0.03);',
      '  border: 1px solid rgba(255,255,255,0.08);',
      '  border-radius: 12px;',
      '  padding: 20px;',
      '  backdrop-filter: blur(16px);',
      '  display: flex;',
      '  flex-direction: column;',
      '}',
      '.obs-stat-val { font-size: 32px; font-weight: 700; margin-bottom: 4px; }',
      '.obs-stat-lbl { font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.4); }',
      '/* Featured Proof */',
      '.obs-featured-proof {',
      '  background: rgba(255,255,255,0.03);',
      '  border: 1px solid rgba(68,255,136,0.2);',
      '  border-radius: 16px;',
      '  padding: 30px;',
      '  backdrop-filter: blur(16px);',
      '  box-shadow: 0 10px 40px rgba(0,0,0,0.5);',
      '  cursor: pointer;',
      '  transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.2s, box-shadow 0.2s;',
      '}',
      '.obs-featured-proof:hover, .obs-featured-proof:focus {',
      '  transform: translateY(-4px) scale(1.01);',
      '  border-color: rgba(68,255,136,0.6);',
      '  box-shadow: 0 15px 50px rgba(68,255,136,0.15);',
      '  outline: none;',
      '}',
      '.obs-fp-status { color: #44ff88; font-family: "JetBrains Mono", monospace; font-size: 12px; margin-bottom: 10px; letter-spacing: 0.1em; }',
      '.obs-fp-title { font-family: "Spectral", serif; font-size: 28px; margin: 0 0 15px; font-weight: 400; }',
      '.obs-fp-bar { height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; position: relative; margin: 25px 0 15px; }',
      '.obs-fp-fill { position: absolute; left: 0; top: 0; height: 100%; background: #44ff88; border-radius: 3px; width: 99.998%; box-shadow: 0 0 10px #44ff88; }',
      '.obs-fp-markers { display: flex; justify-content: space-between; font-family: "JetBrains Mono", monospace; font-size: 10px; color: rgba(255,255,255,0.5); }',
      '/* Right Pane */',
      '.obs-right-pane {',
      '  border-left: 1px solid rgba(255,255,255,0.08);',
      '  padding: 30px 20px;',
      '  overflow-y: auto;',
      '  display: flex;',
      '  flex-direction: column;',
      '  gap: 16px;',
      '  background: rgba(255,255,255,0.01);',
      '}',
      '.obs-right-pane h3 {',
      '  font-size: 12px;',
      '  text-transform: uppercase;',
      '  letter-spacing: 0.15em;',
      '  color: rgba(255,255,255,0.4);',
      '  margin: 0 0 10px 10px;',
      '}',
      '.obs-demo-grid {',
      '  display: flex;',
      '  flex-direction: column;',
      '  gap: 16px;',
      '  padding: 0 10px 40px;',
      '}',
      '.obs-demo-card {',
      '  border-radius: 12px;',
      '  overflow: hidden;',
      '  border: 1px solid rgba(255,255,255,0.08);',
      '  background: rgba(255,255,255,0.02);',
      '  cursor: pointer;',
      '  transition: border-color .2s, transform .2s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow .2s;',
      '}',
      '.obs-demo-card:hover, .obs-demo-card:focus {',
      '  transform: translateX(-4px) scale(1.02);',
      '  box-shadow: -8px 8px 30px rgba(0,0,0,.5);',
      '  outline: none;',
      '}',
      '.obs-demo-card--derived { border-color: rgba(68,255,136,.15); }',
      '.obs-demo-card--derived:hover { border-color: rgba(68,255,136,.45); box-shadow: -8px 8px 30px rgba(68,255,136,.08); }',
      '.obs-demo-card--conditional { border-color: rgba(255,170,51,.12); }',
      '.obs-demo-card--conditional:hover { border-color: rgba(255,170,51,.4); }',
      '.obs-demo-card--axioms { border-color: rgba(0,207,255,.15); }',
      '.obs-demo-card--axioms:hover { border-color: rgba(0,207,255,.45); }',
      '.obs-demo-card--intuition { border-color: rgba(160,80,255,.1); }',
      '.obs-demo-card--intuition:hover { border-color: rgba(160,80,255,.35); }',
      '.obs-demo-card--demo, .obs-demo-card--interactive, .obs-demo-card--journey, .obs-demo-card--narrative { border-color: rgba(255,221,85,.1); }',
      '.obs-demo-card--demo:hover, .obs-demo-card--interactive:hover, .obs-demo-card--journey:hover, .obs-demo-card--narrative:hover { border-color: rgba(255,221,85,.4); }',
      '.obs-demo-canvas-wrap { width: 100%; height: 100px; background: #070712; overflow: hidden; }',
      '.obs-demo-canvas { width: 100%; height: 140px; display: block; transform: translateY(-20px); }',
      '.obs-demo-info { padding: 12px 14px; background: rgba(0,0,0,0.2); }',
      '.obs-demo-status { font-size: 9px; font-weight: 700; letter-spacing: .12em; font-family: "JetBrains Mono", monospace; margin-bottom: 4px; text-transform: uppercase; }',
      '.obs-demo-label { font-size: 14px; font-weight: 600; color: #fff; margin-bottom: 4px; }',
      '.obs-demo-tagline { font-size: 11.5px; color: rgba(255,255,255,.45); line-height: 1.45; }',
      '.obs-demo-card--link { text-decoration: none; color: inherit; display: block; }',
      '/* Responsive */',
      '@media(max-width:1200px) {',
      '  .obs-credibility-deck { grid-template-columns: repeat(2, 1fr); }',
      '}',
      '@media(max-width:1024px) {',
      '  .obs-instrument-surface { grid-template-columns: 80px 1fr 280px; }',
      '  .obs-rail-label { display: none; }',
      '}',
      '@media(max-width:768px) {',
      '  .obs-instrument-surface { grid-template-columns: 1fr; overflow-y: auto; display: block; }',
      '  .obs-rail-pane { display: none; }',
      '  .obs-credibility-deck { grid-template-columns: 1fr; }',
      '}'
    ].join('\n');
    document.head.appendChild(el);
  }

  // ── Panel registration ───────────────────────────────────────────────────
  var _anims = [];
  var _waveObserver = null;
  var _waveInterval = null;

  PFExplorer.registerPanel({
    id: 'observatory',
    title: 'Observatory',

    mount: function (ctx) {
      injectStyles();
      ctx.stage.innerHTML = buildObservatory();
      // Remove any padding applied by framework so we go full screen
      ctx.stage.style.cssText = 'padding:0; height:100%;';

      // Wire click → navigate for panel-route cards
      ctx.stage.querySelectorAll('.obs-demo-card:not(.obs-demo-card--link)').forEach(function (card) {
        var idx  = parseInt(card.getAttribute('data-demo-idx'), 10);
        var demo = DEMOS[idx];
        if (!demo || !demo.id) return;
        function launch() {
          if (window.AudioEngine) window.AudioEngine.playInteraction('click');
          PFExplorer.navigate(demo.id);
        }
        card.addEventListener('click', launch);
        card.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); launch(); }
        });
        // Add hover sound effect
        card.addEventListener('mouseenter', function() {
          if (window.AudioEngine) window.AudioEngine.playInteraction('pop');
        });
      });

      // Koide panel click
      var koideFp = ctx.stage.querySelector('#obsFeaturedKoide');
      if (koideFp) {
        koideFp.addEventListener('click', function() {
          if (window.AudioEngine) window.AudioEngine.playInteraction('explore');
          PFExplorer.navigate('koide');
        });
        koideFp.addEventListener('mouseenter', function() {
          if (window.AudioEngine) window.AudioEngine.playInteraction('whoosh');
        });
      }

      // Track wave pulse for audio interactions
      var wave = ctx.stage.querySelector('#obsWaveFront');
      var ticks = ctx.stage.querySelectorAll('.obs-rail-tick');
      if (wave && ticks.length > 0 && window.AudioEngine) {
        // Simple polling to see if the wave passes a tick (since it's a CSS animation)
        var activeTickIndex = -1;
        _waveInterval = setInterval(function() {
          var waveRect = wave.getBoundingClientRect();
          var waveCenterY = waveRect.top + waveRect.height / 2;

          ticks.forEach(function(tick, idx) {
            var tickRect = tick.getBoundingClientRect();
            var tickCenterY = tickRect.top + tickRect.height / 2;

            // If wave is crossing tick
            if (Math.abs(waveCenterY - tickCenterY) < 10) {
              if (activeTickIndex !== idx) {
                activeTickIndex = idx;
                // Highlight tick
                tick.style.background = '#00cfff';
                tick.style.boxShadow = '0 0 10px #00cfff';
                setTimeout(function(){
                   tick.style.background = 'rgba(255,255,255,0.3)';
                   tick.style.boxShadow = 'none';
                }, 300);

                // Play sound
                if (window.AudioEngine) window.AudioEngine.playInteraction('pop');
              }
            }
          });
        }, 100);
      }

      // Defer canvas animations by one rAF
      requestAnimationFrame(function () {
        ctx.stage.querySelectorAll('.obs-demo-card').forEach(function (card) {
          var idx  = parseInt(card.getAttribute('data-demo-idx'), 10);
          var demo = DEMOS[idx];
          var cvs  = card.querySelector('canvas');
          if (cvs && demo && demo.preview) {
            try {
              var anim = demo.preview(cvs);
              if (anim) _anims.push(anim);
            } catch (e) {
              console.error('[Observatory] preview failed for', demo.id || demo.label, e);
            }
          }
        });
      });
    },

    resize: function (ctx) {
      // Nothing needs manual resizing, pure CSS grid
    },

    unmount: function (ctx) {
      _anims.forEach(function (a) { if (a && a.stop) a.stop(); });
      _anims = [];
      if (_waveInterval) { clearInterval(_waveInterval); _waveInterval = null; }
      ctx.stage.style.cssText = '';
    },
  });

  // ── Scale Ladder iframe panel ────────────────────────────────────────────
  PFExplorer.registerPanel({
    id: 'scale-ladder-panel',
    title: 'Scale Ladder',
    mount: function (ctx) {
      ctx.stage.innerHTML =
        '<div class="iframe-panel-wrap">' +
          '<iframe src="scale-ladder.html" title="Scale Ladder — 61 orders of magnitude" allowfullscreen></iframe>' +
        '</div>';
      ctx.stage.style.cssText = 'padding:0;overflow:hidden;height:100%;';
    },
    unmount: function (ctx) {
      ctx.stage.innerHTML = '';
      ctx.stage.style.cssText = '';
    },
  });

}());
