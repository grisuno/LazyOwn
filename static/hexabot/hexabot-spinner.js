/**
 * HEXABOT spinner: interactive WebGL loading mascot (three.js ES module).
 *
 *   import { createHexabotSpinner } from './hexabot-spinner.js';
 *   const bot = createHexabotSpinner(document.getElementById('hexabot'), {
 *     modelUrl: '/static/hexabot/hexabot.glb',
 *   });
 *   bot.setProgress(0.42, 'escaneando');   // 0..1, shows a bar on the tablet
 *   bot.log('[ OK ] paso 3 terminado');    // prints a line in the terminal
 *   bot.run('nmap -sV 10.0.0.1', ['...'])   // types a command, then prints output lines
 *   bot.happy(2000); bot.trick();          // ^^ eyes / barrel roll
 *   bot.dispose();                         // when the process finishes
 *
 * Requires an importmap exposing "three" and "three/addons/" (see index.html).
 *
 * Options:
 *   modelUrl      GLB path (default './hexabot.glb')
 *   background    CSS color, or null for a transparent canvas (bloom disabled then)
 *   bloom         true/false (default true)
 *   commands      [{cmd, out: [lines]}] terminal script (loops); default: built-in
 *   autoScript    keep typing the script while idle (default true)
 *   user, host    terminal prompt (default 'hexabot', 'solarpunk')
 *   autoOrbit     camera tours around the robot when the user is idle (default true)
 */
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const DEFAULT_COMMANDS = [
  { cmd: 'neofetch --short', out: ['hexabot v1.0 @ solarpunk-os', 'kernel 6.6-solar  rotors: 6', 'energy: UNLIMITED  mood: :)'] },
  { cmd: 'sudo systemctl start fusion-core', out: ['[ OK ] Started Fusion Core.', '[ OK ] Reached target Infinite Energy.'] },
  { cmd: 'ping -c 2 sun.local', out: ['64 bytes from sun.local: ttl=64 time=0.42 ms', '64 bytes from sun.local: ttl=64 time=0.39 ms'] },
  { cmd: './rotors --sync --all', out: ['rotor[0..5] ......... nominal', 'hover lock ........... OK'] },
  { cmd: 'cat /proc/energy', out: ['solar: 98.7%   wind: 12 kW', 'battery: inf   co2: 0 g'] },
  { cmd: 'git pull origin main', out: ['Already up to date.'] },
  { cmd: 'make coffee', out: ["make: *** No rule to make target 'coffee'.", 'hexabot: brewing anyway...'] },
  { cmd: 'htop --tree | head -3', out: ['  1 init', '  ├─ hover-daemon  2.1%', '  └─ your-process  97.9%'] },
  { cmd: 'echo "ya casi..."', out: ['ya casi...'] },
];

const rand = (a, b) => a + Math.random() * (b - a);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

class Terminal {
  constructor({ commands, autoScript = true, user = 'hexabot', host = 'solarpunk' }) {
    this.W = 1024;
    this.H = 700;
    this.canvas = document.createElement('canvas');
    this.canvas.width = this.W;
    this.canvas.height = this.H;
    this.ctx = this.canvas.getContext('2d');
    this.texture = new THREE.CanvasTexture(this.canvas);
    this.texture.flipY = false;
    this.texture.colorSpace = THREE.SRGBColorSpace;
    this.texture.anisotropy = 8;
    this.font = 'bold 38px "JetBrains Mono","Fira Code","DejaVu Sans Mono",monospace';
    this.lineH = 47;
    this.ctx.font = this.font;
    this.charW = this.ctx.measureText('M').width;
    this.cols = Math.floor((this.W - 40) / this.charW);
    this.user = user;
    this.host = host;
    this.commands = commands || DEFAULT_COMMANDS;
    this.auto = autoScript;
    this.idx = 0;
    this.lines = [];
    this.pending = [];
    this.userQueue = [];
    this.typing = null;
    this.wait = 0.6;
    this.paused = false;
    this.progress = null;
    this.label = '';
    this.blink = 0;
    this.dirty = true;
    this.draw();
  }

  push(text, color) {
    const chunks = [];
    for (let i = 0; i < Math.max(1, text.length); i += this.cols) chunks.push(text.slice(i, i + this.cols));
    chunks.forEach((t) => this.lines.push({ text: t, color }));
    if (this.lines.length > 200) this.lines.splice(0, this.lines.length - 200);
    this.dirty = true;
  }

  log(text) { String(text).split('\n').forEach((l) => this.push(l, null)); }

  run(cmd, out = []) { this.userQueue.push({ cmd, out }); }

  setProgress(p, label) {
    this.progress = p == null ? null : clamp(p, 0, 1);
    if (label !== undefined) this.label = label;
    this.dirty = true;
  }

  startCommand(item) {
    this.typing = { text: item.cmd, shown: 0 };
    this.pending = item.out.slice();
  }

  update(dt) {
    this.blink += dt;
    if (this.blink > 0.5) { this.blink = 0; this.cursorOn = !this.cursorOn; this.dirty = true; }
    this.wait -= dt;
    while (this.wait <= 0) {
      if (this.typing) {
        this.typing.shown++;
        this.dirty = true;
        if (this.typing.shown >= this.typing.text.length) {
          this.lines.push({ prompt: true, text: this.typing.text });
          this.typing = null;
          this.wait += 0.3;
        } else {
          this.wait += rand(0.035, 0.11);
        }
      } else if (this.pending.length) {
        this.push(this.pending.shift(), null);
        this.wait += rand(0.06, 0.18);
      } else if (!this.paused) {
        this.paused = true;
        this.wait += rand(0.9, 1.8);
      } else {
        this.paused = false;
        if (this.userQueue.length) this.startCommand(this.userQueue.shift());
        else if (this.auto) { this.startCommand(this.commands[this.idx % this.commands.length]); this.idx++; }
        else { this.wait = 0.5; break; }
        this.wait += 0.05;
      }
    }
    if (this.dirty) { this.draw(); this.texture.needsUpdate = true; this.dirty = false; }
  }

  colorFor(text) {
    if (/^\[ ?OK ?\]/.test(text)) return '#5dff7a';
    if (/error|fail|\*\*\*/i.test(text)) return '#ff5577';
    if (/warn|casi/i.test(text)) return '#ffc64a';
    return '#39ffb0';
  }

  drawPrompt(ctx, x, y, text, cursor) {
    const parts = [[`${this.user}@${this.host}`, '#ff3fa4'], [':', '#cfe'], ['~', '#00e5ff'], ['$ ', '#cfe'], [text, '#effff8']];
    for (const [t, c] of parts) { ctx.fillStyle = c; ctx.fillText(t, x, y); x += ctx.measureText(t).width; }
    if (cursor && this.cursorOn) { ctx.fillStyle = '#39ffb0'; ctx.fillRect(x + 2, y - 33, this.charW * 0.8, 40); }
  }

  draw() {
    const { ctx, W, H } = this;
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, '#04140f');
    g.addColorStop(1, '#020806');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    ctx.fillStyle = '#0c2620';
    ctx.fillRect(0, 0, W, 56);
    [['#ff5f56', 30], ['#ffbd2e', 62], ['#27c93f', 94]].forEach(([c, x]) => {
      ctx.fillStyle = c; ctx.beginPath(); ctx.arc(x, 28, 11, 0, Math.PI * 2); ctx.fill();
    });
    ctx.font = 'bold 24px "JetBrains Mono","DejaVu Sans Mono",monospace';
    ctx.fillStyle = '#9fe';
    ctx.textAlign = 'center';
    ctx.fillText(`${this.user}@${this.host}: ~`, W / 2, 37);
    ctx.textAlign = 'left';

    ctx.font = this.font;
    const bottom = this.progress != null ? H - 82 : H - 18;
    const rows = Math.floor((bottom - 70) / this.lineH);
    const view = this.lines.slice(-(rows - 1));
    let y = 56 + this.lineH;
    for (const l of view) {
      if (l.prompt) this.drawPrompt(ctx, 20, y, l.text, false);
      else { ctx.fillStyle = l.color || this.colorFor(l.text); ctx.fillText(l.text, 20, y); }
      y += this.lineH;
    }
    if (this.typing) this.drawPrompt(ctx, 20, y, this.typing.text.slice(0, this.typing.shown), true);
    else this.drawPrompt(ctx, 20, y, '', true);

    if (this.progress != null) {
      const by = H - 58;
      ctx.fillStyle = '#0c2620';
      ctx.fillRect(0, by - 16, W, 74);
      ctx.fillStyle = '#ffc64a';
      ctx.font = 'bold 30px "JetBrains Mono","DejaVu Sans Mono",monospace';
      const pct = `${Math.round(this.progress * 100)}%`;
      ctx.fillText(this.label || 'loading', 20, by + 10);
      ctx.textAlign = 'right';
      ctx.fillText(pct, W - 20, by + 10);
      ctx.textAlign = 'left';
      const bx = 20, bw = W - 40, bh = 16, cells = 40;
      const filled = Math.round(this.progress * cells);
      for (let i = 0; i < cells; i++) {
        ctx.fillStyle = i < filled ? (i % 2 ? '#00ffd5' : '#39ffb0') : '#123a30';
        ctx.fillRect(bx + (i * bw) / cells + 1, by + 24, bw / cells - 3, bh);
      }
    }
    ctx.fillStyle = 'rgba(0,0,0,0.18)';
    for (let sy = 0; sy < H; sy += 4) ctx.fillRect(0, sy, W, 1);
  }

  dispose() { this.texture.dispose(); }
}

function radialTexture(inner, outer) {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const ctx = c.getContext('2d');
  const g = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
  g.addColorStop(0, inner);
  g.addColorStop(1, outer);
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

export function createHexabotSpinner(container, opts = {}) {
  const o = {
    modelUrl: './hexabot.glb', background: '#07040f', bloom: true, autoOrbit: true, ...opts,
  };
  const transparent = o.background == null;
  const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: transparent });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 0.9;
  const canvas = renderer.domElement;
  Object.assign(canvas.style, { width: '100%', height: '100%', display: 'block', touchAction: 'none', cursor: 'grab' });
  if (getComputedStyle(container).position === 'static') container.style.position = 'relative';
  container.appendChild(canvas);

  const scene = new THREE.Scene();
  if (!transparent) {
    scene.background = new THREE.Color(o.background);
    scene.fog = new THREE.Fog(o.background, 7, 16);
  }
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environment = envTex;
  scene.environmentIntensity = 0.35;

  const camera = new THREE.PerspectiveCamera(36, 1, 0.1, 60);
  camera.position.set(1.2, 0.5, 3.7);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.enablePan = false;
  controls.minDistance = 2.2;
  controls.maxDistance = 8;
  controls.target.set(0, -0.2, 0);
  controls.update();

  scene.add(new THREE.HemisphereLight(0x8fa6ff, 0x1a0820, 0.35));
  const key = new THREE.DirectionalLight(0xffd6a0, 1.5);
  key.position.set(3, 4, 4);
  scene.add(key);
  const rimC = new THREE.PointLight(0x00ffd5, 30, 12, 2);
  rimC.position.set(-3, 1.2, -2);
  const rimM = new THREE.PointLight(0xff2a8a, 30, 12, 2);
  rimM.position.set(3, 0.4, -2.5);
  scene.add(rimC, rimM);

  const robot = new THREE.Group();
  const bobber = new THREE.Group();
  robot.add(bobber);
  scene.add(robot);
  const underLight = new THREE.PointLight(0x00ffd5, 6, 4, 2);
  underLight.position.set(0, -1.0, 0.2);
  bobber.add(underLight);

  const floorY = -1.45;
  const glowTex = radialTexture('rgba(0,255,213,0.14)', 'rgba(0,255,213,0)');
  const floorGlow = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 3.2),
    new THREE.MeshBasicMaterial({ map: glowTex, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }));
  floorGlow.rotation.x = -Math.PI / 2;
  floorGlow.position.y = floorY;
  const ring = new THREE.Mesh(new THREE.RingGeometry(1.15, 1.19, 6, 1),
    new THREE.MeshBasicMaterial({ color: 0xff2a8a, transparent: true, opacity: 0.45, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
  ring.rotation.x = -Math.PI / 2;
  ring.position.y = floorY + 0.01;
  const ring2 = new THREE.Mesh(new THREE.RingGeometry(0.7, 0.72, 64, 1), ring.material.clone());
  ring2.material.color.set(0x00ffd5);
  ring2.rotation.x = -Math.PI / 2;
  ring2.position.y = floorY + 0.01;
  scene.add(floorGlow, ring, ring2);

  const MOTES = 140;
  const motePos = new Float32Array(MOTES * 3);
  const moteSpeed = new Float32Array(MOTES);
  for (let i = 0; i < MOTES; i++) {
    const r = rand(1.0, 2.7), a = rand(0, Math.PI * 2);
    motePos.set([Math.cos(a) * r, rand(-1.5, 2.5), Math.sin(a) * r], i * 3);
    moteSpeed[i] = rand(0.05, 0.25);
  }
  const moteGeo = new THREE.BufferGeometry();
  moteGeo.setAttribute('position', new THREE.BufferAttribute(motePos, 3));
  const moteTex = radialTexture('rgba(255,210,120,1)', 'rgba(255,160,40,0)');
  const motes = new THREE.Points(moteGeo, new THREE.PointsMaterial({
    size: 0.05, map: moteTex, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending, color: 0xffc070,
  }));
  scene.add(motes);

  let composer = null, bloomPass = null;
  if (o.bloom && !transparent) {
    composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    bloomPass = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.32, 0.4, 0.9);
    composer.addPass(bloomPass);
    composer.addPass(new OutputPass());
  }

  const term = new Terminal(o);
  const st = {
    mixer: null, props: [], eyes: [], happyEyes: [], face: null, model: null,
    happyUntil: 0, trickT: -1, vel: new THREE.Vector3(), target: new THREE.Vector3(),
    dragging: false, downXY: null, dragOffset: new THREE.Vector3(), dragPlane: new THREE.Plane(),
    pointer: new THREE.Vector2(), pointerActive: 0, lastInteract: -10, look: new THREE.Vector2(),
  };

  let resolveReady, rejectReady;
  const ready = new Promise((res, rej) => { resolveReady = res; rejectReady = rej; });

  new GLTFLoader().load(o.modelUrl, (gltf) => {
    const model = gltf.scene;
    st.model = model;
    bobber.add(model);
    model.traverse((n) => {
      if (n.isMesh) {
        const mats = Array.isArray(n.material) ? n.material : [n.material];
        mats.forEach((m) => {
          if (m.emissive && m.emissiveIntensity > 1) m.emissiveIntensity = Math.min(m.emissiveIntensity * 0.4, 5);
        });
      }
      if (n.name === 'TabletScreen') {
        n.material = new THREE.MeshBasicMaterial({ map: term.texture, toneMapped: false, color: new THREE.Color(0.82, 0.82, 0.82) });
      }
      if (/^HappyEye_[LR]$/.test(n.name)) { n.visible = false; st.happyEyes.push(n); }
      if (/^Eye_[LR]$/.test(n.name)) st.eyes.push(n);
      if (n.name === 'FaceRig') st.face = n;
      const pm = n.name.match(/^Prop_(\d+)$/);
      if (pm) {
        const idx = +pm[1];
        const disc = new THREE.Mesh(new THREE.CircleGeometry(0.23, 48), new THREE.MeshBasicMaterial({
          color: idx % 2 ? 0xff2a8a : 0x00ffd5, transparent: true, opacity: 0.13,
          blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide,
        }));
        disc.rotation.x = -Math.PI / 2;
        n.add(disc);
        st.props.push({ node: n, dir: idx % 2 ? 1 : -1 });
      }
    });
    if (gltf.animations.length) {
      st.mixer = new THREE.AnimationMixer(model);
      st.mixer.clipAction(gltf.animations[0]).play();
    }
    resolveReady(api);
  }, undefined, (err) => { console.error('[hexabot] model load failed', err); rejectReady(err); });

  const setHappy = (on) => {
    st.happyEyes.forEach((n) => { n.visible = on; });
    st.eyes.forEach((n) => { n.visible = !on; });
  };

  const raycaster = new THREE.Raycaster();
  const ndc = (e) => {
    const r = canvas.getBoundingClientRect();
    return new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
  };
  const now = () => performance.now() / 1000;

  const onDown = (e) => {
    st.lastInteract = now();
    if (!st.model) return;
    const p = ndc(e);
    raycaster.setFromCamera(p, camera);
    const hit = raycaster.intersectObject(st.model, true)[0];
    if (!hit) return;
    controls.enabled = false;
    st.dragging = true;
    st.downXY = [e.clientX, e.clientY];
    const n = camera.getWorldDirection(new THREE.Vector3()).negate();
    st.dragPlane.setFromNormalAndCoplanarPoint(n, robot.position);
    const pt = new THREE.Vector3();
    raycaster.ray.intersectPlane(st.dragPlane, pt);
    st.dragOffset.copy(pt).sub(robot.position);
    canvas.style.cursor = 'grabbing';
    canvas.setPointerCapture?.(e.pointerId);
  };
  const onMove = (e) => {
    st.pointer.copy(ndc(e));
    st.pointerActive = now();
    if (!st.dragging) return;
    raycaster.setFromCamera(st.pointer, camera);
    const pt = new THREE.Vector3();
    if (raycaster.ray.intersectPlane(st.dragPlane, pt)) {
      st.target.copy(pt.sub(st.dragOffset));
      if (st.target.length() > 1.6) st.target.setLength(1.6);
      st.target.y = Math.max(st.target.y, floorY + 1.0);
    }
  };
  const onUp = (e) => {
    if (!st.dragging) return;
    st.dragging = false;
    controls.enabled = true;
    canvas.style.cursor = 'grab';
    st.lastInteract = now();
    const moved = Math.hypot(e.clientX - st.downXY[0], e.clientY - st.downXY[1]);
    if (moved < 6) api.trick();
    else { st.target.set(0, 0, 0); api.happy(1200); }
  };
  container.addEventListener('pointerdown', onDown, { capture: true });
  window.addEventListener('pointermove', onMove);
  window.addEventListener('pointerup', onUp);
  controls.addEventListener('start', () => { st.lastInteract = now(); });
  controls.addEventListener('end', () => { st.lastInteract = now(); });

  const resize = () => {
    const w = Math.max(1, container.clientWidth), h = Math.max(1, container.clientHeight);
    renderer.setSize(w, h, false);
    composer?.setSize(w, h);
    camera.aspect = w / h;
    camera.fov = w / h < 1 ? 48 : 36;
    camera.updateProjectionMatrix();
  };
  const ro = new ResizeObserver(resize);
  ro.observe(container);
  resize();

  const sph = new THREE.Spherical();
  const tmp = new THREE.Vector3();
  const clock = new THREE.Clock();

  const loop = () => {
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;
    term.update(dt);
    st.mixer?.update(dt);

    tmp.copy(st.target).sub(robot.position).multiplyScalar(28 * dt);
    st.vel.add(tmp).multiplyScalar(Math.exp(-5 * dt));
    robot.position.addScaledVector(st.vel, dt * 1.0);
    robot.rotation.z = THREE.MathUtils.lerp(robot.rotation.z, clamp(-st.vel.x * 0.18, -0.6, 0.6), 0.15);
    robot.rotation.x = THREE.MathUtils.lerp(robot.rotation.x, clamp(st.vel.z * 0.18, -0.6, 0.6), 0.15);

    bobber.position.y = 0.07 * Math.sin(t * 1.7) + 0.02 * Math.sin(t * 4.3);
    if (st.trickT >= 0) {
      st.trickT += dt / 1.1;
      const k = clamp(st.trickT, 0, 1);
      const e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
      bobber.rotation.z = e * Math.PI * 2;
      bobber.position.y += Math.sin(k * Math.PI) * 0.35;
      if (st.trickT >= 1) { st.trickT = -1; bobber.rotation.z = 0; }
    }

    const looking = now() - st.pointerActive < 2.5 && !st.dragging;
    const lx = looking ? clamp(st.pointer.x, -1, 1) : 0;
    const ly = looking ? clamp(st.pointer.y, -1, 1) : 0;
    st.look.x += (lx - st.look.x) * Math.min(1, dt * 4);
    st.look.y += (ly - st.look.y) * Math.min(1, dt * 4);
    bobber.rotation.y = st.look.x * 0.3;
    if (st.face) { st.face.position.x += st.look.x * 0.06; st.face.position.y += st.look.y * 0.05; }

    if (st.happyUntil && now() > st.happyUntil) { st.happyUntil = 0; setHappy(false); }

    for (const p of st.props) p.node.rotation.y += p.dir * 30 * dt;

    const h = robot.position.y + bobber.position.y - floorY;
    floorGlow.position.x = ring.position.x = ring2.position.x = robot.position.x;
    floorGlow.position.z = ring.position.z = ring2.position.z = robot.position.z;
    floorGlow.material.opacity = clamp(1.4 / h, 0.25, 0.9);
    ring.rotation.z = t * 0.3;
    ring2.scale.setScalar(1 + 0.08 * Math.sin(t * 3));

    const pos = moteGeo.attributes.position;
    for (let i = 0; i < MOTES; i++) {
      let y = pos.getY(i) + moteSpeed[i] * dt;
      if (y > 2.6) y = -1.5;
      pos.setY(i, y);
    }
    pos.needsUpdate = true;

    if (o.autoOrbit && !reduceMotion && !st.dragging && now() - st.lastInteract > 3.5) {
      tmp.copy(camera.position).sub(controls.target);
      sph.setFromVector3(tmp);
      sph.theta += dt * 0.22;
      sph.phi += (1.38 + 0.2 * Math.sin(t * 0.35) - sph.phi) * Math.min(1, dt * 0.6);
      sph.radius += (3.7 + 0.5 * Math.sin(t * 0.21) - sph.radius) * Math.min(1, dt * 0.4);
      camera.position.setFromSpherical(sph).add(controls.target);
    }
    controls.update();

    if (composer) composer.render(); else renderer.render(scene, camera);
  };
  renderer.setAnimationLoop(loop);

  const api = {
    ready,
    log: (text) => term.log(text),
    run: (cmd, out) => term.run(cmd, out),
    setProgress: (p, label) => term.setProgress(p, label),
    setStatus: (label) => term.setProgress(term.progress ?? 0, label),
    clearProgress: () => term.setProgress(null),
    happy: (ms = 1500) => { setHappy(true); st.happyUntil = now() + ms / 1000; },
    trick: () => {
      if (st.trickT >= 0) return;
      st.trickT = 0;
      api.happy(1800);
      term.run('sudo barrel-roll', ['wheeeee! \\o/']);
    },
    dispose: () => {
      renderer.setAnimationLoop(null);
      ro.disconnect();
      container.removeEventListener('pointerdown', onDown, { capture: true });
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      controls.dispose();
      term.dispose();
      envTex.dispose();
      pmrem.dispose();
      scene.traverse((n) => {
        n.geometry?.dispose();
        const mats = n.material ? (Array.isArray(n.material) ? n.material : [n.material]) : [];
        mats.forEach((m) => { m.map?.dispose(); m.dispose(); });
      });
      composer?.dispose();
      renderer.dispose();
      canvas.remove();
    },
  };
  return api;
}
