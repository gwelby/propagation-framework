// camera_aspect_fail: PerspectiveCamera with hard-coded aspect of 1 and no
// projection-matrix refresh anywhere in the file.
// Expected: check_camera_aspect -> False
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
// bug: the projection stays at aspect=1 forever (no refresh call)
