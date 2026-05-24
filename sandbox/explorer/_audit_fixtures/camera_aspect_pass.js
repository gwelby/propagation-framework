// camera_aspect_pass: PerspectiveCamera with real aspect ratio (no hard-coded 1)
// Expected: check_camera_aspect -> True
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const w = 640;
const h = 400;
const camera = new THREE.PerspectiveCamera(60, w / h, 0.1, 1000);
camera.updateProjectionMatrix();
