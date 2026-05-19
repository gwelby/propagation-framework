// exp_blowup_fail: Math.exp of an unbounded positive value, no guard nearby.
// Expected: check_exp_blowup -> False
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const bigPositive = 50;
const y = Math.exp(bigPositive);
