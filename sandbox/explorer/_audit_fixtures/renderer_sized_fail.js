// renderer_sized_fail: WebGLRenderer created but no setSize anywhere
// Expected: check_renderer_sized -> False
const renderer = new THREE.WebGLRenderer({ antialias: true });
// (bug) no renderer.setSize call anywhere in this file
renderer.render(scene, camera);
