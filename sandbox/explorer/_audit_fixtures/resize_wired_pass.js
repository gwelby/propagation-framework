// resize_wired_pass: resize() method defined AND invoked from mount path
// Expected: check_resize_wired -> True
const renderer = new THREE.WebGLRenderer();
renderer.setSize(640, 400, false);
const panel = {
  resize: function (ctx) {
    renderer.setSize(ctx.stage.clientWidth, ctx.stage.clientHeight, false);
  },
  mount: function (ctx) {
    this.resize(ctx);
  },
};
