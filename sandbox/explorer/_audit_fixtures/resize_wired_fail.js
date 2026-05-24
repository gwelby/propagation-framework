// resize_wired_fail: resize method defined but never invoked from mount path.
// Expected: check_resize_wired -> False
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const panel = {
  resize: function (ctx) {
    renderer.setSize(ctx.stage.clientWidth, ctx.stage.clientHeight, false);
  },
  mount: function (ctx) {
    // bug: mount forgets to wire the resize call after renderer creation
  },
};
