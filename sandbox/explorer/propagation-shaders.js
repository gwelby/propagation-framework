/**
 * Propagation Shaders — Shared GLSL for Scale Ladder Scenes
 * 
 * Every scale expresses the same mathematics: propagation, interference,
 * coherence. These shaders make that shared math visually concrete.
 * 
 * Three shader systems:
 *   1. WaveField — 2D wave interference, click to spawn sources
 *   2. StandingWave — 1D standing wave with node/antinode markers
 *   3. FieldDensity — volumetric field density, shows coherent regions
 */

window.PropagationShaders = {
  version: '1.0',

  // ── Shared GLSL snippets ─────────────────────────────────────────────────

  glsl: {
    PI: '#define PI 3.14159265359',
    TAU: '#define TAU 6.28318530718',
    E: '#define E 2.71828182845',

    // Standard wave equation helpers
    waveSum: [
      'float waveSum(vec2 p, float t, int nSources, vec2 sources[8], float freqs[8]) {',
      '  float v = 0.0;',
      '  for (int i = 0; i < 8; i++) {',
      '    if (i >= nSources) break;',
      '    float d = length(p - sources[i]);',
      '    v += sin(d * freqs[i] - t * freqs[i] * 0.6);',
      '  }',
      '  return v / float(nSources);',
      '}'
    ].join('\n'),

    // Fresnel for volumetric edge glow
    fresnel: [
      'float fresnel(vec3 viewDir, vec3 normal, float power) {',
      '  return pow(1.0 - clamp(dot(viewDir, normal), 0.0, 1.0), power);',
      '}'
    ].join('\n'),

    // Smooth noise
    smoothNoise: [
      'float hash(vec2 p) {',
      '  return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);',
      '}',
      'float noise(vec2 p) {',
      '  vec2 i = floor(p);',
      '  vec2 f = fract(p);',
      '  vec2 u = f * f * (3.0 - 2.0 * f);',
      '  return mix(mix(hash(i), hash(i + vec2(1.0,0.0)), u.x),',
      '              mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), u.x), u.y);',
      '}'
    ].join('\n')
  },

  // ── Wave Field ShaderMaterial ───────────────────────────────────────────
  // Used at: atomic, molecular, cellular scales
  // Shows: interference pattern from multiple wave sources

  createWaveFieldMaterial: function (opts) {
    opts = opts || {};
    return new THREE.ShaderMaterial({
      uniforms: {
        uTime:    { value: 0 },
        uScale:   { value: opts.scale || 1.0 },
        uDecay:   { value: opts.decay || 0.3 },
        uColor1:  { value: new THREE.Color(opts.color1 || 0x00e5ff) },
        uColor2:  { value: new THREE.Color(opts.color2 || 0x69ff94) },
        uBgColor: { value: new THREE.Color(opts.bgColor || 0x020408) }
      },
      vertexShader: [
        'varying vec2 vUv;',
        'void main() {',
        '  vUv = uv;',
        '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform float uTime;',
        'uniform float uScale;',
        'uniform float uDecay;',
        'uniform vec3 uColor1;',
        'uniform vec3 uColor2;',
        'uniform vec3 uBgColor;',
        'varying vec2 vUv;',

        // Distance field from center
        'float dist(vec2 p) { return length(p - vec2(0.5)); }',

        // Three wave sources at different positions
        'float waves(vec2 p, float t) {',
        '  vec2 s1 = vec2(0.3, 0.5);',
        '  vec2 s2 = vec2(0.7, 0.35);',
        '  vec2 s3 = vec2(0.5, 0.75);',
        '  float d1 = length(p - s1);',
        '  float d2 = length(p - s2);',
        '  float d3 = length(p - s3);',
        '  float w1 = sin(d1 * 18.0 - t * 2.5) * exp(-d1 * uDecay);',
        '  float w2 = sin(d2 * 14.0 - t * 2.0) * exp(-d2 * uDecay);',
        '  float w3 = sin(d3 * 22.0 - t * 3.2) * exp(-d3 * uDecay);',
        '  return (w1 + w2 + w3) / 3.0;',
        '}',

        'void main() {',
        '  vec2 p = vUv;',
        '  float t = uTime * uScale;',
        '  float w = waves(p, t);',

        // Standing wave nodes appear where waves cancel
        '  float standing = abs(w);',

        // Coherence = where waves constructively interfere
        '  float coherence = smoothstep(0.3, 0.9, w * w);',

        // Color mixing: cyan for propagating, lime for coherent
        '  vec3 propColor = uColor1;',
        '  vec3 cohColor  = uColor2;',
        '  vec3 color = mix(propColor * 0.5, cohColor, coherence);',
        '  color *= 0.4 + 0.6 * standing;',

        // Grid overlay for spatial reference
        '  vec2 grid = fract(vUv * 20.0);',
        '  float gridLine = step(0.94, grid.x) + step(0.94, grid.y);',
        '  color += vec3(gridLine * 0.06);',

        '  gl_FragColor = vec4(color, 0.9);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.DoubleSide
    });
  },

  // ── Standing Wave ShaderMaterial ────────────────────────────────────────
  // Used at: matter, nuclear scales
  // Shows: 1D standing wave with visible nodes and antinodes

  createStandingWaveMaterial: function (opts) {
    opts = opts || {};
    return new THREE.ShaderMaterial({
      uniforms: {
        uTime:         { value: 0 },
        uWavelength:  { value: opts.wavelength || 0.3 },
        uAmplitude:    { value: opts.amplitude || 1.0 },
        uNodeColor:    { value: new THREE.Color(opts.nodeColor || 0xff4757) },
        uAntinodeColor:{ value: new THREE.Color(opts.antinodeColor || 0x69ff94) },
        uBgColor:      { value: new THREE.Color(opts.bgColor || 0x020408) }
      },
      vertexShader: [
        'varying vec2 vUv;',
        'void main() {',
        '  vUv = uv;',
        '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform float uTime;',
        'uniform float uWavelength;',
        'uniform float uAmplitude;',
        'uniform vec3 uNodeColor;',
        'uniform vec3 uAntinodeColor;',
        'uniform vec3 uBgColor;',
        'varying vec2 vUv;',

        'void main() {',
        '  float x = vUv.x * PI * 4.0;',
        '  float t = uTime * 0.8;',

        // Standing wave: sin(kx) * cos(ωt)
        '  float wave = sin(x) * cos(t);',
        '  float y = (wave * 0.5 + 0.5) * uAmplitude;',

        // Node positions (zero crossing)
        '  float node = smoothstep(0.05, 0.0, abs(wave));',

        // Antinode positions (peaks)
        '  float antinode = smoothstep(0.1, 0.9, wave * wave);',

        '  vec3 color = uBgColor;',
        '  color = mix(color, uAntinodeColor, antinode * 0.7);',
        '  color = mix(color, uNodeColor, node * 0.5);',

        // Draw wave curve
        '  float waveLine = smoothstep(0.04, 0.0, abs(vUv.y - y * 0.8 - 0.1));',
        '  color = mix(color, vec3(0.9), waveLine);',

        '  gl_FragColor = vec4(color, 0.85);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.DoubleSide
    });
  },

  // ── Field Density ShaderMaterial ────────────────────────────────────────
  // Used at: planck, cosmic scales
  // Shows: volumetric field density — coherent regions glow green

  createFieldDensityMaterial: function (opts) {
    opts = opts || {};
    return new THREE.ShaderMaterial({
      uniforms: {
        uTime:       { value: 0 },
        uDensity:    { value: opts.density || 0.5 },
        uCoherence:  { value: opts.coherence || 0.6 },
        uFieldColor: { value: new THREE.Color(opts.fieldColor || 0x7c5cbf) },
        uCohColor:   { value: new THREE.Color(opts.cohColor || 0x69ff94) },
        uBgColor:    { value: new THREE.Color(opts.bgColor || 0x020408) }
      },
      vertexShader: [
        'varying vec3 vPosition;',
        'varying vec3 vNormal;',
        'void main() {',
        '  vPosition = position;',
        '  vNormal = normalMatrix * normal;',
        '  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);',
        '}'
      ].join('\n'),
      fragmentShader: [
        'uniform float uTime;',
        'uniform float uDensity;',
        'uniform float uCoherence;',
        'uniform vec3 uFieldColor;',
        'uniform vec3 uCohColor;',
        'uniform vec3 uBgColor;',
        'varying vec3 vPosition;',
        'varying vec3 vNormal;',

        // Noise for density variation
        'float hash(vec3 p) {',
        '  return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453);',
        '}',
        'float noise3(vec3 p) {',
        '  vec3 i = floor(p);',
        '  vec3 f = fract(p);',
        '  f = f * f * (3.0 - 2.0 * f);',
        '  return mix(',
        '    mix(mix(hash(i), hash(i+vec3(1,0,0)), f.x),',
        '        mix(hash(i+vec3(0,1,0)), hash(i+vec3(1,1,0)), f.x), f.y),',
        '    mix(mix(hash(i+vec3(0,0,1)), hash(i+vec3(1,0,1)), f.x),',
        '        mix(hash(i+vec3(0,1,1)), hash(i+vec3(1,1,1)), f.x), f.y),',
        '    f.z);',
        '}',

        'void main() {',
        '  vec3 p = vPosition * 0.8;',
        '  float t = uTime * 0.15;',

        // Layered noise for field density
        '  float field = noise3(p * 2.0 + t) * 0.5',
        '             + noise3(p * 4.0 - t * 0.7) * 0.3',
        '             + noise3(p * 8.0 + t * 0.4) * 0.2;',

        '  float density = field * uDensity;',

        // Coherence: regions where noise is smooth (low detail)
        '  float detail = abs(noise3(p * 4.0) - noise3(p * 8.0));',
        '  float coherence = smoothstep(0.05, 0.2, 0.2 - detail) * uCoherence;',

        // Fresnel edge glow
        '  float fresnel = pow(1.0 - abs(dot(normalize(vNormal), vec3(0.0, 0.0, 1.0))), 2.5);',

        '  vec3 color = uBgColor;',
        '  color = mix(color, uFieldColor, density * 0.6);',
        '  color = mix(color, uCohColor, coherence * 0.7);',
        '  color += uFieldColor * fresnel * 0.3;',

        '  gl_FragColor = vec4(color, 0.75 + fresnel * 0.2);',
        '}'
      ].join('\n'),
      transparent: true,
      side: THREE.FrontSide,
      depthWrite: false
    });
  },

  // ── Helix Ribbon — standing wave / coherent mode visualization ──────────
  // Used at: matter scale to show the helical standing wave

  createHelixRibbonGeometry: function (radius, pitch, turns, tubeRadius) {
    var segments = Math.max(32, Math.floor(turns * 32));
    var geo = new THREE.TubeGeometry(
      new THREE.CatmullRomCurve3(
        Array.from({ length: segments + 1 }, function (_, i) {
          var t = i / segments;
          var angle = t * turns * Math.PI * 2;
          return new THREE.Vector3(
            radius * Math.cos(angle),
            t * pitch - pitch / 2,
            radius * Math.sin(angle)
          );
        }),
        segments
      ),
      segments,
      tubeRadius,
      12,
      false
    );
    return geo;
  }
};
