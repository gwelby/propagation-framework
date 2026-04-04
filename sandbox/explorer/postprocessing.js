/**
 * PostFX — Propagation Framework Shared Post-Processing Pipeline
 * 
 * Provides unified post-processing across all Three.js scenes:
 *   - Propagation bloom (coherent regions glow)
 *   - Volumetric medium fog (space is not empty)
 *   - Depth of Field / Bokeh (lens-style focus)
 *   - Film grain (subtle imperfection)
 *   - Color grading (unified design system palette)
 * 
 * Usage:
 *   var PostFX = window.PostFX;
 *   var composer = PostFX.createComposer(renderer, scene, camera);
 *   composer.render(); // in animation loop
 * 
 *   // Fog on a specific scene:
 *   PostFX.addFog(scene, { color: 0x020408, density: 0.008 });
 * 
 *   // DOF available via PostFX.createComposer options:
 *   //   dof: false to disable
 *   //   dofFocus, dofAperture, dofMaxblur for parameters
 */

(function () {
  'use strict';

  var DEFAULTS = {
    bloom: {
      strength: 0.55,
      radius: 0.38,
      threshold: 0.82
    },
    grain: {
      strength: 0.04,
      size: 1.2
    },
    colorGrade: {
      lift: 0.008,
      gamma: 1.0,
      gain: 1.0,
      saturation: 1.08
    },
    fog: {
      color: 0x020408,
      density: 0.008
    },
    dof: {
      focus: 0.5,       // normalized focus distance (0 = near, 1 = infinity)
      aperture: 0.025,  // bokeh strength
      maxblur: 0.01     // max blur radius in screen-space units
    }
  };

  function getThreeAddon(name) {
    return THREE[name] || window[name];
  }

  function createBloomPass(size, options) {
    var opts = options || DEFAULTS.bloom;
    var UnrealBloomPassCtor = getThreeAddon('UnrealBloomPass');
    if (!UnrealBloomPassCtor) {
      throw new Error('UnrealBloomPass addon not available');
    }
    return new UnrealBloomPassCtor(
      new THREE.Vector2(size.width || size, size.height || size),
      opts.strength,
      opts.radius,
      opts.threshold
    );
  }

  function createGrainPass(options) {
    var opts = options || DEFAULTS.grain;
    return {
      strength: opts.strength,
      size: opts.size,
      render: function (renderer, writeBuffer) {
        // Grain is applied via the color grade pass shader
        // This is a marker for PostFX.addGrain to find
      }
    };
  }

  /**
   * Grain + Color Grade combined shader pass
   */
  function createColorGradeShaderPass(options) {
    var opts = options || DEFAULTS.colorGrade;
    var grainOpts = DEFAULTS.grain;

    var mat = new THREE.ShaderMaterial({
      uniforms: {
        tDiffuse: { value: null },
        uTime: { value: 0 },
        uGrainStrength: { value: grainOpts.strength },
        uGrainSize: { value: grainOpts.size },
        uLift: { value: opts.lift },
        uGamma: { value: opts.gamma },
        uGain: { value: opts.gain },
        uSaturation: { value: opts.saturation }
      },
      vertexShader: [
        'varying vec2 vUv;',
        'void main() {',
        '  vUv = uv;',
        '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform sampler2D tDiffuse;',
        'uniform float uTime;',
        'uniform float uGrainStrength;',
        'uniform float uGrainSize;',
        'uniform float uLift;',
        'uniform float uGamma;',
        'uniform float uGain;',
        'uniform float uSaturation;',
        'varying vec2 vUv;',

        'float hash(vec2 p) {',
        '  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);',
        '}',

        'vec3 acesFilm(vec3 x) {',
        '  float a = 2.51;',
        '  float b = 0.03;',
        '  float c = 2.43;',
        '  float d = 0.59;',
        '  float e = 0.14;',
        '  return clamp((x*(a*x+b))/(x*(c*x+d)+e), 0.0, 1.0);',
        '}',

        'vec3 grade(vec3 c) {',
        '  // Lift (shadows)',
        '  c = c + uLift * (1.0 - c);',
        '  // Gamma',
        '  c = pow(max(c, 0.0), vec3(1.0 / uGamma));',
        '  // Gain (highlights)',
        '  c = c * uGain;',
        '  // Saturation',
        '  float lum = dot(c, vec3(0.2126, 0.7152, 0.0722));',
        '  c = mix(vec3(lum), c, uSaturation);',
        '  return c;',
        '}',

        'void main() {',
        '  vec4 texel = texture2D(tDiffuse, vUv);',
        '  vec3 color = texel.rgb;',

        '  // Film grain',
        '  float t = uTime * 0.07;',
        '  vec2 grainUv = vUv * uGrainSize + fract(t) * 100.0;',
        '  float grain = hash(floor(grainUv * 512.0)) * 2.0 - 1.0;',
        '  color += grain * uGrainStrength;',

        '  // ACES filmic tone mapping (already applied by renderer, but reinforce)',
        '  color = acesFilm(color);',

        '  // Color grade',
        '  color = grade(color);',

        '  gl_FragColor = vec4(clamp(color, 0.0, 1.0), texel.a);',
        '}'
      ].join('\n'),
      transparent: false
    });

    var ShaderPassCtor = getThreeAddon('ShaderPass');
    if (!ShaderPassCtor) {
      throw new Error('ShaderPass addon not available');
    }
    var pass = new ShaderPassCtor(mat);
    pass.uniforms = mat.uniforms;
    return pass;
  }

  /**
   * Add volumetric-style medium fog to a scene.
   * Uses Three.js FogExp2 for depth-based fog.
   * Call on scene.activate() for cosmic/planck scenes.
   */
  function addFog(scene, options) {
    var opts = options || DEFAULTS.fog;
    scene.fog = new THREE.FogExp2(opts.color, opts.density);
    return scene.fog;
  }

  /**
   * Remove fog from a scene.
   */
  function removeFog(scene) {
    scene.fog = null;
  }

  /**
   * Create a full PostFX composer pipeline for a given renderer/scene/camera.
   * 
   * Options:
   *   bloom: false to disable bloom
   *   grain: false to disable grain
   *   colorGrade: false to disable color grading
   *   bloomStrength / bloomRadius / bloomThreshold: bloom params
   * 
   * Returns { composer, bloomPass, colorPass, update(time) }
   */
  function createComposer(renderer, scene, camera, options) {
    options = options || {};

    var enableBloom = options.bloom !== false;
    var enableGrain = options.grain !== false;
    var enableColorGrade = options.colorGrade !== false;

    var size = renderer.getSize(new THREE.Vector2());

    var EffectComposerCtor = getThreeAddon('EffectComposer');
    var RenderPassCtor = getThreeAddon('RenderPass');
    if (!EffectComposerCtor || !RenderPassCtor) {
      throw new Error('EffectComposer or RenderPass addon not available');
    }

    var composer = new EffectComposerCtor(renderer);
    composer.addPass(new RenderPassCtor(scene, camera));

    var bloomPass = null;
    if (enableBloom) {
      var bloomOpts = {
        strength: options.bloomStrength !== undefined ? options.bloomStrength : DEFAULTS.bloom.strength,
        radius: options.bloomRadius !== undefined ? options.bloomRadius : DEFAULTS.bloom.radius,
        threshold: options.bloomThreshold !== undefined ? options.bloomThreshold : DEFAULTS.bloom.threshold
      };
      bloomPass = createBloomPass(size, bloomOpts);
      composer.addPass(bloomPass);
    }

    var dofPass = null;
    var BokehPassCtor = getThreeAddon('BokehPass');
    if (options.dof !== false && typeof BokehPassCtor !== 'undefined') {
      var dofOpts = {
        focus: options.dofFocus !== undefined ? options.dofFocus : DEFAULTS.dof.focus,
        aperture: options.dofAperture !== undefined ? options.dofAperture : DEFAULTS.dof.aperture,
        maxblur: options.dofMaxblur !== undefined ? options.dofMaxblur : DEFAULTS.dof.maxblur
      };
      dofPass = new BokehPassCtor(scene, camera, {
        focus: dofOpts.focus,
        aperture: dofOpts.aperture * 0.00001,
        maxblur: dofOpts.maxblur
      });
      composer.addPass(dofPass);
    }

    var colorPass = null;
    if (enableGrain || enableColorGrade) {
      var gradeOpts = enableColorGrade ? options : {};
      var grainOpts = enableGrain ? options : {};
      colorPass = createColorGradeShaderPass(gradeOpts);
      if (enableGrain) {
        colorPass.uniforms.uGrainStrength.value = grainOpts.grainStrength !== undefined ? grainOpts.grainStrength : DEFAULTS.grain.strength;
        colorPass.uniforms.uGrainSize.value = grainOpts.grainSize !== undefined ? grainOpts.grainSize : DEFAULTS.grain.size;
      }
      composer.addPass(colorPass);
    }

    return {
      composer: composer,
      bloomPass: bloomPass,
      colorPass: colorPass,
      dofPass: dofPass,

      update: function (time) {
        if (colorPass && colorPass.uniforms && colorPass.uniforms.uTime) {
          colorPass.uniforms.uTime.value = time;
        }
      },

      setBloomStrength: function (strength) {
        if (bloomPass) bloomPass.strength = strength;
      },

      setBloomRadius: function (radius) {
        if (bloomPass) bloomPass.radius = radius;
      },

      setBloomThreshold: function (threshold) {
        if (bloomPass) bloomPass.threshold = threshold;
      },

      setGrainStrength: function (strength) {
        if (colorPass && colorPass.uniforms && colorPass.uniforms.uGrainStrength) {
          colorPass.uniforms.uGrainStrength.value = strength;
        }
      },

      setDOFFocus: function (focus) {
        if (dofPass && dofPass.uniforms) dofPass.uniforms.focus.value = focus;
      },

      setDOFAperture: function (aperture) {
        if (dofPass && dofPass.uniforms) dofPass.uniforms.aperture.value = aperture * 0.00001;
      },

      resize: function (w, h) {
        composer.setSize(w, h);
      }
    };
  }

  /**
   * Add PostFX to an existing scene that uses its own composer.
   * Patches the render loop to go through PostFX.
   * Returns the PostFX handle so you can call .update(time) in your loop.
   * 
   * Usage:
   *   var pf = PostFX.patchRenderer(existingRenderer, scene, camera, canvasEl);
   *   // in animation loop:
   *   pf.composer.render();
   *   pf.update(time);
   */
  function patchRenderer(renderer, scene, camera, canvasEl, options) {
    var pf = createComposer(renderer, scene, camera, options);
    var w = canvasEl ? canvasEl.clientWidth : renderer.getSize(new THREE.Vector2()).width;
    var h = canvasEl ? canvasEl.clientHeight : renderer.getSize(new THREE.Vector2()).height;
    pf.resize(w, h);
    return pf;
  }

  /**
   * Create a lightweight fog-only scene enhancement.
   * Call scene.fog = PostFX.createFog(scene, options) directly.
   */
  function createFog(options) {
    var opts = options || DEFAULTS.fog;
    return new THREE.FogExp2(opts.color, opts.density);
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.PostFX = {
    createComposer: createComposer,
    patchRenderer: patchRenderer,
    addFog: addFog,
    removeFog: removeFog,
    createFog: createFog,
    createBloomPass: createBloomPass,
    createColorGradePass: createColorGradeShaderPass,
    DEFAULTS: DEFAULTS,

    /**
     * Create a consistent PBR material with scale-appropriate defaults.
     * 
     * Presets:
     *   'coherent'  — emissive glow for coherent standing wave regions (cyan/lime)
     *   'filament'  — cosmic web filaments (violet)
     *   'plasma'    — hot stellar/nuclear matter (red/orange)
     *   'quantum'   — Planck/GUT scale discrete geometry (gold)
     *   'neural'    — neural/neural-like oscillations (yellow/amber)
     *   'virus'     — organic coherent structures (lime/green)
     *   'generic'   — neutral default
     */
    createMaterial: function (preset, options) {
      var opts = options || {};
      var mat;

      var presets = {
        coherent: {
          color: opts.color || 0x00e5ff,
          emissive: opts.emissive || opts.color || 0x00e5ff,
          emissiveIntensity: opts.emissiveIntensity !== undefined ? opts.emissiveIntensity : 0.55,
          metalness: opts.metalness !== undefined ? opts.metalness : 0.7,
          roughness: opts.roughness !== undefined ? opts.roughness : 0.25,
          transparent: opts.transparent !== undefined ? opts.transparent : false,
          opacity: opts.opacity
        },
        filament: {
          color: opts.color || 0x7c5cbf,
          emissive: opts.emissive || opts.color || 0x7c5cbf,
          emissiveIntensity: opts.emissiveIntensity !== undefined ? opts.emissiveIntensity : 0.22,
          metalness: opts.metalness !== undefined ? opts.metalness : 0.7,
          roughness: opts.roughness !== undefined ? opts.roughness : 0.3,
          transparent: true,
          opacity: opts.opacity !== undefined ? opts.opacity : 0.7
        },
        plasma: {
          color: opts.color || 0xff6b6b,
          emissive: opts.emissive || opts.color || 0xff6b6b,
          emissiveIntensity: opts.emissiveIntensity !== undefined ? opts.emissiveIntensity : 0.8,
          metalness: opts.metalness !== undefined ? opts.metalness : 0.2,
          roughness: opts.roughness !== undefined ? opts.roughness : 0.4,
          transparent: opts.transparent !== undefined ? opts.transparent : false
        },
        quantum: {
          color: opts.color || 0xffd700,
          emissive: opts.emissive || opts.color || 0xffd700,
          emissiveIntensity: opts.emissiveIntensity !== undefined ? opts.emissiveIntensity : 0.5,
          metalness: opts.metalness !== undefined ? opts.metalness : 0.6,
          roughness: opts.roughness !== undefined ? opts.roughness : 0.3,
          transparent: true,
          opacity: opts.opacity !== undefined ? opts.opacity : 0.92
        },
        neural: {
          color: opts.color || 0xffdd55,
          emissive: opts.emissive || opts.color || 0xffdd55,
          emissiveIntensity: opts.emissiveIntensity !== undefined ? opts.emissiveIntensity : 0.6,
          metalness: opts.metalness !== undefined ? opts.metalness : 0.3,
          roughness: opts.roughness !== undefined ? opts.roughness : 0.5,
          transparent: true,
          opacity: opts.opacity !== undefined ? opts.opacity : 0.85
        },
        virus: {
          color: opts.color || 0x69ff94,
          emissive: opts.emissive || opts.color || 0x69ff94,
          emissiveIntensity: opts.emissiveIntensity !== undefined ? opts.emissiveIntensity : 0.4,
          metalness: opts.metalness !== undefined ? opts.metalness : 0.6,
          roughness: opts.roughness !== undefined ? opts.roughness : 0.35,
          transparent: true,
          opacity: opts.opacity !== undefined ? opts.opacity : 0.8
        },
        generic: {
          color: opts.color || 0x4488aa,
          emissive: opts.emissive || 0x000000,
          emissiveIntensity: opts.emissiveIntensity !== undefined ? opts.emissiveIntensity : 0.1,
          metalness: opts.metalness !== undefined ? opts.metalness : 0.5,
          roughness: opts.roughness !== undefined ? opts.roughness : 0.5,
          transparent: opts.transparent !== undefined ? opts.transparent : false
        }
      };

      var config = presets[preset] || presets.generic;
      mat = new THREE.MeshStandardMaterial({
        color: config.color,
        emissive: config.emissive,
        emissiveIntensity: config.emissiveIntensity,
        metalness: config.metalness,
        roughness: config.roughness,
        transparent: config.transparent
      });
      if (config.opacity !== undefined) mat.opacity = config.opacity;

      return mat;
    }
  };

}());
