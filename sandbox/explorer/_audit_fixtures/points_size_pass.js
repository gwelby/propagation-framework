// points_size_pass: PointsMaterial with visible point size
// Expected: check_points_size -> True
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const mat = new THREE.PointsMaterial({ size: 0.08, color: 0xffffff });
