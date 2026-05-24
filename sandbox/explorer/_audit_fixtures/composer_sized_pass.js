// composer_sized_pass: EffectComposer + composer.setSize
// Expected: check_composer_sized -> True
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const composer = new THREE.EffectComposer(renderer);
composer.setSize(640, 400);
composer.render();
