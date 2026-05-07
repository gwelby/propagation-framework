/**
 * panels/observatory.js — Observatory: Visual Launch Pad
 *
 * This is the entry point. It shows LIVE ANIMATED PREVIEWS of every demo,
 * not walls of text. Click any card to launch the full interactive experience.
 *
 * Codex gates (unchanged):
 * - Only 3 DERIVED results: gravity-optical, koide-leptons, weinberg-angle
 * - Consciousness is INTUITION
 * - Status colors are data, not decoration
 */
(function () {
  'use strict';

  // ── Demo catalogue ──────────────────────────────────────────────────────
  // Each entry drives a card. preview: function that draws onto a canvas.
  var DEMOS = [
    {
      id: 'refraction',
      label: 'Gravity = Refraction',
      status: 'DERIVED',
      statusColor: '#44ff88',
      tagline: 'Light bends because space has a refractive index. Not a metaphor — a theorem.',
      preview: previewRefraction,
    },
    {
      id: 'koide',
      label: 'Koide Resonance',
      status: 'DERIVED',
      statusColor: '#44ff88',
      tagline: 'Three charged leptons locked at 120°. Q = 2/3 exactly. Zero free parameters.',
      preview: previewKoide,
    },
    {
      id: 'weinberg',
      label: 'Weinberg Angle',
      status: 'DERIVED',
      statusColor: '#44ff88',
      tagline: 'sin²θ_W from a Casimir polynomial. Matches experiment to 0.13σ.',
      preview: previewWeinberg,
    },
    {
      id: 'bohr',
      label: 'Bohr Spectrum',
      status: 'CONDITIONAL',
      statusColor: '#ffaa33',
      tagline: 'Phase closure in the Coulomb field selects the hydrogen energy levels.',
      preview: previewBohr,
    },
    {
      id: 'generations',
      label: 'Three Generations',
      status: 'CONDITIONAL',
      statusColor: '#ffaa33',
      tagline: 'Why exactly three families of matter? Q(N)=2/3 has one solution: N=3.',
      preview: previewGenerations,
    },
    {
      id: 'god-equation',
      label: 'God Equation',
      status: 'CONDITIONAL',
      statusColor: '#ffaa33',
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
      status: 'INTUITION',
      statusColor: 'rgba(255,255,255,.3)',
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

    var html = [
      // Hero — minimal, visual-first
      '<div class="obs-hero-compact">',
        '<div class="obs-hero-sig">',
          '<span class="obs-sig-glyph">∇λΣ∞</span>',
          '<div class="obs-sig-text">',
            '<strong>Propagation Framework</strong>',
            '<span>Physics from three axioms — every demo is a live experiment</span>',
          '</div>',
        '</div>',
        '<div class="obs-hero-counts">',
          '<span class="obs-count obs-count--green"><strong>'+derived.length+'</strong> Derived</span>',
          '<span class="obs-count obs-count--gold"><strong>'+defs.length+'</strong> Definitions</span>',
          '<span class="obs-count obs-count--red"><strong>'+nogos.length+'</strong> No-go</span>',
          '<span class="obs-count"><strong>'+claims.length+'</strong> Audited claims</span>',
        '</div>',
      '</div>',

      // Big propagation canvas
      '<div class="obs-field-hero">',
        '<canvas id="obsFieldCanvas" class="obs-field-full" aria-label="Live propagation field"></canvas>',
        '<div class="obs-field-caption">',
          '<span class="obs-field-tag obs-field-tag--1">Axiom 1 · Propagation</span>',
          '<span class="obs-field-tag obs-field-tag--2">Axiom 2 · Causal Bound</span>',
          '<span class="obs-field-tag obs-field-tag--3">Axiom 3 · Coherence</span>',
          '<span class="obs-field-tag obs-field-tag--legend">● Derived &nbsp; ● Conditional &nbsp; ● Empirical</span>',
        '</div>',
      '</div>',

      // Demo grid
      '<div class="obs-demo-head">',
        '<h2>Interactive Experiments</h2>',
        '<p>Click any card to launch the full interactive demo. Hover to see it animate.</p>',
      '</div>',
      '<div class="obs-demo-grid" id="obsDemoGrid">',
        DEMOS.map(function(d, i) {
          // href-based cards use a real <a> so popup-blockers can't intercept
          var inner = '<div class="obs-demo-canvas-wrap"><canvas class="obs-demo-canvas" width="280" height="140"></canvas></div>' +
            '<div class="obs-demo-info">' +
              '<div class="obs-demo-status" style="color:'+d.statusColor+'">'+d.status+'</div>' +
              '<div class="obs-demo-label">'+d.label+'</div>' +
              '<div class="obs-demo-tagline">'+d.tagline+'</div>' +
            '</div>';
          if (d.href) {
            return '<a class="obs-demo-card obs-demo-card--'+d.status.toLowerCase().replace(' ','-')+' obs-demo-card--link" ' +
              'href="'+d.href+'" target="_blank" rel="noopener" data-demo-idx="'+i+'" tabindex="0">' +
              inner + '</a>';
          }
          return '<div class="obs-demo-card obs-demo-card--'+d.status.toLowerCase().replace(' ','-')+'" data-demo-idx="'+i+'" tabindex="0">' +
            inner + '</div>';
        }).join(''),
      '</div>',
    ].join('');

    return html;
  }

  // ── Propagation field (large hero) ───────────────────────────────────────
  function PropagationField(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.waves = []; this.nodes = [];
    this.frame = 0; this.running = false; this._raf = null;
    this.W = 0; this.H = 0;
  }

  PropagationField.prototype.resize = function () {
    var dpr = Math.min(window.devicePixelRatio||1,2);
    var w = this.canvas.offsetWidth; var h = this.canvas.offsetHeight;
    this.canvas.width = w*dpr; this.canvas.height = h*dpr;
    this.ctx.scale(dpr,dpr);
    this.W = w; this.H = h;
    this.nodes = [
      {x:w*.50,y:h*.50,c:'#00cfff',p:0},
      {x:w*.20,y:h*.35,c:'#44ff88',p:60},
      {x:w*.80,y:h*.35,c:'#44ff88',p:30},
      {x:w*.65,y:h*.72,c:'#44ff88',p:90},
      {x:w*.35,y:h*.72,c:'#ffaa33',p:45},
      {x:w*.10,y:h*.60,c:'#ffdd55',p:75},
      {x:w*.90,y:h*.60,c:'#ff4455',p:15},
      {x:w*.50,y:h*.15,c:'#00cfff',p:20},
    ];
  };

  PropagationField.prototype.spawnFrom = function (n) {
    this.waves.push({x:n.x,y:n.y,r:0,maxR:Math.max(this.W,this.H)*.7,c:n.c,s:.8+Math.random()*.4});
  };

  function hexRgba(hex,a) {
    var r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
    return 'rgba('+r+','+g+','+b+','+a.toFixed(3)+')';
  }

  PropagationField.prototype.tick = function () {
    if (!this.running) return;
    var ctx=this.ctx,W=this.W,H=this.H;
    ctx.fillStyle='rgba(8,8,20,.15)'; ctx.fillRect(0,0,W,H);
    // Grid
    ctx.strokeStyle='rgba(0,207,255,.025)'; ctx.lineWidth=.5;
    for(var xi=0;xi<W;xi+=48){ctx.beginPath();ctx.moveTo(xi,0);ctx.lineTo(xi,H);ctx.stroke();}
    for(var yi=0;yi<H;yi+=48){ctx.beginPath();ctx.moveTo(0,yi);ctx.lineTo(W,yi);ctx.stroke();}
    // Waves
    this.waves=this.waves.filter(function(w){return w.r<w.maxR;});
    this.waves.forEach(function(w){
      w.r+=w.s*2; var alpha=(1-w.r/w.maxR)*(1-w.r/w.maxR)*.6;
      ctx.beginPath(); ctx.arc(w.x,w.y,w.r,0,Math.PI*2);
      ctx.strokeStyle=hexRgba(w.c,alpha); ctx.lineWidth=1.2; ctx.stroke();
    });
    // Connection lines
    var nodes=this.nodes;
    ctx.lineWidth=.4;
    for(var i=0;i<nodes.length;i++){
      for(var j=i+1;j<nodes.length;j++){
        var d=Math.hypot(nodes[j].x-nodes[i].x,nodes[j].y-nodes[i].y);
        if(d<W*.5){ctx.strokeStyle='rgba(0,207,255,'+((.5-d/(W*.5))*.1)+')';ctx.beginPath();ctx.moveTo(nodes[i].x,nodes[i].y);ctx.lineTo(nodes[j].x,nodes[j].y);ctx.stroke();}
      }
    }
    // Nodes
    nodes.forEach(function(n){
      var phase=(this.frame+n.p)%120/120;
      var pulse=.5+.5*Math.sin(phase*Math.PI*2);
      var grd=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,18+pulse*5);
      grd.addColorStop(0,hexRgba(n.c,.4*pulse)); grd.addColorStop(1,'rgba(0,0,0,0)');
      ctx.fillStyle=grd; ctx.beginPath(); ctx.arc(n.x,n.y,18+pulse*5,0,Math.PI*2); ctx.fill();
      ctx.fillStyle=hexRgba(n.c,.95); ctx.beginPath(); ctx.arc(n.x,n.y,3.5+pulse,0,Math.PI*2); ctx.fill();
    },this);
    this.frame++;
    if(this.waves.length<50){
      nodes.forEach(function(n,idx){if(this.frame%60===(idx*7)%60)this.spawnFrom(n);},this);
    }
    var self=this; this._raf=requestAnimationFrame(function(){self.tick();});
  };

  PropagationField.prototype.start=function(){this.running=true;this.resize();this.nodes.forEach(function(n,i){var self=this;setTimeout(function(){self.spawnFrom(n);},i*80);},this);this.tick();};
  PropagationField.prototype.stop=function(){this.running=false;if(this._raf)cancelAnimationFrame(this._raf);};

  // ── Injected styles ──────────────────────────────────────────────────────
  function injectStyles() {
    if (document.getElementById('obs2-styles')) return;
    var el = document.createElement('style'); el.id = 'obs2-styles';
    el.textContent = [
      '.obs-hero-compact{display:flex;align-items:center;justify-content:space-between;padding:16px 32px;gap:16px;border-bottom:1px solid rgba(255,255,255,.05);flex-wrap:wrap;}',
      '.obs-hero-sig{display:flex;align-items:center;gap:14px;}',
      '.obs-sig-glyph{font-family:serif;font-size:28px;color:#00cfff;letter-spacing:.05em;}',
      '.obs-sig-text{display:flex;flex-direction:column;gap:2px;}',
      '.obs-sig-text strong{font-size:14px;color:#fff;}',
      '.obs-sig-text span{font-size:11px;color:rgba(255,255,255,.4);}',
      '.obs-hero-counts{display:flex;gap:16px;flex-wrap:wrap;}',
      '.obs-count{font-size:12px;color:rgba(255,255,255,.45);}',
      '.obs-count strong{display:block;font-size:20px;font-weight:700;}',
      '.obs-count--green strong{color:#44ff88;}',
      '.obs-count--gold strong{color:#ffdd55;}',
      '.obs-count--red strong{color:#ff4455;}',
      // Hero field — bigger
      '.obs-field-hero{position:relative;height:clamp(240px,35vw,420px);background:#08080f;overflow:hidden;}',
      '.obs-field-full{position:absolute;inset:0;width:100%;height:100%;}',
      '.obs-field-caption{position:absolute;inset:0;pointer-events:none;display:flex;align-items:flex-end;gap:10px;padding:14px 20px;flex-wrap:wrap;}',
      '.obs-field-tag{font-size:10px;letter-spacing:.08em;padding:3px 8px;border-radius:3px;}',
      '.obs-field-tag--1{color:#00cfff;background:rgba(0,207,255,.1);border:1px solid rgba(0,207,255,.2);}',
      '.obs-field-tag--2{color:#00cfff;background:rgba(0,207,255,.07);border:1px solid rgba(0,207,255,.12);}',
      '.obs-field-tag--3{color:#44ff88;background:rgba(68,255,136,.07);border:1px solid rgba(68,255,136,.18);}',
      '.obs-field-tag--legend{color:rgba(255,255,255,.4);margin-left:auto;font-size:9px;}',
      // Demo grid
      '.obs-demo-head{padding:28px 32px 8px;}',
      '.obs-demo-head h2{font-family:Georgia,serif;font-size:20px;font-weight:400;color:#fff;margin:0 0 6px;}',
      '.obs-demo-head p{font-size:13px;color:rgba(255,255,255,.4);margin:0;}',
      '.obs-demo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;padding:16px 32px 40px;}',
      '@media(max-width:640px){.obs-demo-grid{grid-template-columns:1fr;padding:12px 16px 32px;}}',
      '.obs-demo-card{border-radius:12px;overflow:hidden;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.02);cursor:pointer;transition:border-color .2s,transform .18s,box-shadow .2s;}',
      '.obs-demo-card:hover,.obs-demo-card:focus{transform:translateY(-3px);box-shadow:0 8px 30px rgba(0,0,0,.4);}',
      '.obs-demo-card:focus{outline:2px solid #00cfff;}',
      '.obs-demo-card--derived{border-color:rgba(68,255,136,.15);}',
      '.obs-demo-card--derived:hover{border-color:rgba(68,255,136,.45);box-shadow:0 8px 30px rgba(68,255,136,.08);}',
      '.obs-demo-card--conditional{border-color:rgba(255,170,51,.12);}',
      '.obs-demo-card--conditional:hover{border-color:rgba(255,170,51,.4);}',
      '.obs-demo-card--axioms{border-color:rgba(0,207,255,.15);}',
      '.obs-demo-card--axioms:hover{border-color:rgba(0,207,255,.45);}',
      '.obs-demo-card--intuition{border-color:rgba(160,80,255,.1);}',
      '.obs-demo-card--intuition:hover{border-color:rgba(160,80,255,.35);}',
      '.obs-demo-card--demo,.obs-demo-card--interactive,.obs-demo-card--journey,.obs-demo-card--narrative{border-color:rgba(255,221,85,.1);}',
      '.obs-demo-card--demo:hover,.obs-demo-card--interactive:hover,.obs-demo-card--journey:hover,.obs-demo-card--narrative:hover{border-color:rgba(255,221,85,.4);}',
      '.obs-demo-canvas-wrap{width:100%;height:140px;background:#070712;overflow:hidden;}',
      '.obs-demo-canvas{width:100%;height:140px;display:block;}',
      '.obs-demo-info{padding:12px 14px;}',
      '.obs-demo-status{font-size:9px;font-weight:700;letter-spacing:.12em;font-family:monospace;margin-bottom:4px;text-transform:uppercase;}',
      '.obs-demo-label{font-size:14px;font-weight:600;color:#fff;margin-bottom:4px;}',
      '.obs-demo-tagline{font-size:11.5px;color:rgba(255,255,255,.45);line-height:1.45;}',
      // Link cards (href-based) look identical — just remove default <a> styling
      '.obs-demo-card--link{text-decoration:none;color:inherit;display:block;}',
    ].join('\n');
    document.head.appendChild(el);
  }

  // ── Panel registration ───────────────────────────────────────────────────
  var _field = null;
  var _anims = [];

  PFExplorer.registerPanel({
    id: 'observatory',
    title: 'Observatory',

    mount: function (ctx) {
      injectStyles();
      ctx.stage.innerHTML = buildObservatory();
      ctx.stage.style.cssText = 'overflow-y:auto;padding:0;';

      // Start big field
      var canvas = ctx.stage.querySelector('#obsFieldCanvas');
      if (canvas) { _field = new PropagationField(canvas); _field.start(); }

      // Wire click → navigate for panel-route cards (href cards are real <a> links, no handler needed)
      ctx.stage.querySelectorAll('.obs-demo-card:not(.obs-demo-card--link)').forEach(function (card) {
        var idx  = parseInt(card.getAttribute('data-demo-idx'), 10);
        var demo = DEMOS[idx];
        if (!demo || !demo.id) return;
        function launch() { PFExplorer.navigate(demo.id); }
        card.addEventListener('click', launch);
        card.addEventListener('keydown', function (e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); launch(); }
        });
      });

      // Defer canvas animations by one rAF so grid layout is committed before
      // setupCanvas reads offsetWidth (avoids all cards getting 0-width buffers)
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
      if (_field) _field.resize();
    },

    unmount: function (ctx) {
      if (_field) { _field.stop(); _field = null; }
      _anims.forEach(function (a) { if (a && a.stop) a.stop(); });
      _anims = [];
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
