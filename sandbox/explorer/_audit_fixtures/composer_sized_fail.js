// composer_sized_fail: EffectComposer but no composer.setSize anywhere
// Expected: check_composer_sized -> False
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const composer = new THREE.EffectComposer(renderer);
// (bug) composer never gets a setSize call
composer.render();
