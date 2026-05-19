// renderer_sized_pass: WebGLRenderer created AND renderer.setSize present
// Expected: check_renderer_sized -> True
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(640, 400, false);
