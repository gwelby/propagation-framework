// points_size_fail: PointsMaterial with sub-pixel point size
// Expected: check_points_size -> False
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const mat = new THREE.PointsMaterial({ size: 0.02, color: 0xffffff });
