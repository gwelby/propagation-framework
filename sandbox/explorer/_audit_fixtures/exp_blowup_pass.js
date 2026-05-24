// exp_blowup_pass: Math.exp with negative argument (bounded by 1)
// Expected: check_exp_blowup -> True
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const t = 2.5;
const y = Math.exp(-t * t);
