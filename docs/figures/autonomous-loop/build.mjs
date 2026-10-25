import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { homedir } from "node:os";

const HERE = dirname(fileURLToPath(import.meta.url));
const SKILL = process.env.ANATOMY_SKILL || join(homedir(), ".config/opencode/skills/anatomy");
const k = await import(pathToFileURL(join(SKILL, "kit/iso-kit.mjs")).href);
const G = await import(pathToFileURL(join(SKILL, "kit/lathe.mjs")).href);
const { kitScript } = await import(pathToFileURL(join(SKILL, "scripts/inline-kit.mjs")).href);

const solidSvg = k.solidSvg;
const cylinder = k.cylinder;
const extrude = k.extrude;
const slabOf = k.slabOf;
const lineOnTop = k.lineOnTop;
const planOutline = k.planOutline;
const iso = k.iso;
const faceTextSvg = k.faceTextSvg;
const translateAlong = k.translateAlong;
const lineSvg = k.lineSvg;

const theme = process.argv.includes("--light") ? "light" : "dark";
const WIDTH = 740;
const HEIGHT = 500;

const BASE = { x: -138, y: -92, w: 280, d: 172, r: 12 };
const BASE_BOTTOM = -12;
const BASE_H = 12;
const FOOT_H = 5;

const AXIS = [-25, -10];
const RING_R = 56;
const TABLE_R = 46;
const ORBIT_R = 36;
const TABLE_Z = 30;
const TABLE_H = 8;
const TABLE_TOP = TABLE_Z + TABLE_H;
const ARM_Z = 62;
const ARM_H = 4.6;
const COLUMN_TOP = ARM_Z;
const BLOCK_BOTTOM = 40;
const BLOCK_TOP = 50;
const TOOL_UP = 58;
const TOOL_TRAVEL = TOOL_UP - BLOCK_TOP;
const TOOL_TOP = 74;

const DIAL = [98, -52];
const DIAL_R = 20;
const DIAL_Z = 72;
const DIAL_H = 10;
const DIAL_TOP = DIAL_Z + DIAL_H;
const DIAL_ZERO = Math.PI;
const DIAL_SPAN = Math.PI * 1.5;

const GLASS = [130, -36];
const GLASS_BOTTOM = 18;
const GLASS_TOP = 70;

const DRUM = [98, -2];
const DRUM_R = 13;
const DRUM_Z = 44;
const DRUM_H = 9;

const RACK = [-104, 30];
const CARD_X = [-123, -113, -103, -93];
const GUARD = [58, 50];

const P = k.fitProjection(
  [
    ...k.boxCorners(BASE, BASE_BOTTOM - FOOT_H, 0),
    [AXIS[0], AXIS[1], TOOL_TOP + 4],
    [DIAL[0], DIAL[1], DIAL_TOP + 2],
    [DRUM[0], DRUM[1], DRUM_Z + DRUM_H + 6],
    [GLASS[0], GLASS[1], GLASS_TOP + 4],
    [RACK[0] + 24, RACK[1], 26],
  ],
  WIDTH,
  HEIGHT,
  { pad: 30, azimuth: 45 },
);

const GEO = {
  AXIS,
  RING_R,
  TABLE_R,
  ORBIT_R,
  TABLE_Z,
  TABLE_H,
  TABLE_TOP,
  ARM_Z,
  ARM_H,
  BLOCK_BOTTOM,
  BLOCK_TOP,
  TOOL_UP,
  TOOL_TRAVEL,
  TOOL_TOP,
  DIAL,
  DIAL_R,
  DIAL_Z,
  DIAL_H,
  DIAL_TOP,
  DIAL_ZERO,
  DIAL_SPAN,
  GLASS,
  GLASS_BOTTOM,
  GLASS_TOP,
  DRUM,
  DRUM_R,
  DRUM_Z,
  DRUM_H,
  RACK,
  CARD_X,
  GUARD,
};

const S = (paths, style) => solidSvg(paths, style);
const L = (d, style) => k.lineSvg(d, style);
const D = (points, style) => k.dotsSvg(points, style);
const byDepth = (points) =>
  [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

function rotPlan(cx, cy, length, width, angle) {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  const hx = length / 2;
  const hy = width / 2;
  return [
    [cx - hx * c + hy * s, cy - hx * s - hy * c],
    [cx + hx * c + hy * s, cy + hx * s - hy * c],
    [cx + hx * c - hy * s, cy + hx * s + hy * c],
    [cx - hx * c - hy * s, cy - hx * s + hy * c],
  ];
}

function headAngle(index) {
  return (Math.PI / 4) * index + Math.PI / 8;
}

function headPoint(index, radius) {
  const a = headAngle(index);
  return [AXIS[0] + radius * Math.cos(a), AXIS[1] + radius * Math.sin(a)];
}

function headDepth(index) {
  const [x, y] = headPoint(index, RING_R);
  return k.depthOf([x, y, 0], P);
}

function basePlate() {
  const out = [`<path class="iso-halo" d="${k.haloOf(BASE, BASE_BOTTOM - FOOT_H, BASE_H, P)}"/>`];
  for (const [x, y] of byDepth(k.corners(BASE, 24))) {
    out.push(S(k.cylinder(x, y, 7.5, BASE_BOTTOM - FOOT_H, 1.8, P, 28), { tone: "lo" }));
    out.push(S(k.cylinder(x, y, 5.6, BASE_BOTTOM - FOOT_H + 1.8, FOOT_H - 1.8, P, 28), { tone: "mid" }));
  }
  out.push(S(slabOf(BASE, BASE_BOTTOM, BASE_H, P, 10, 1.6), { tone: "mid" }));
  out.push(L(planOutline(k.insetPlan(BASE, 6), 0, P), { tone: "lo" }));
  out.push(L(planOutline(k.insetPlan(BASE, 15), 0, P), { tone: "faint" }));
  const screws = k.corners(BASE, 11);
  out.push(L(screws.map(([x, y]) => k.ring(x, y, 2.3, 0, P, 16)).join(""), { tone: "lo" }));
  out.push(D(screws.map(([x, y]) => iso([x, y, 0], P)), { size: 0.5 }));
  return out.join("");
}

function rulerStrip() {
  const strip = { x: -46, y: BASE.y + BASE.d - 15, w: 132, d: 7, r: 1 };
  const out = [S(slabOf(strip, 0, 0.7, P, 3), { tone: "lo", crease: "none" })];
  const ticks = k.topTicks(strip.x + 5, strip.x + strip.w - 5, 5, 5, strip.y + 1, 0.7, [2, 3.6], P);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  out.push(D([iso([strip.x + 3, strip.y + 3.5, 0.7], P), iso([strip.x + strip.w - 3, strip.y + 3.5, 0.7], P)], { size: 0.45 }));
  return out.join("");
}

function namePlate() {
  const plate = { x: -130, y: BASE.y + BASE.d - 19, w: 56, d: 19, r: 2 };
  const out = [S(slabOf(plate, 0, 1.2, P, 4, 0.4), { tone: "lo" })];
  out.push(L(planOutline(k.insetPlan(plate, 2.4), 1.2, P), { tone: "faint" }));
  out.push(k.faceTextSvg(k.topMatrix([plate.x + 28, plate.y + 11], 1.2, P, "x"), "10.10.11.5", { size: 3.6, tone: "mid", anchor: "middle" }));
  out.push(L(lineOnTop([plate.x + 5, plate.y + 5], [plate.x + 46, plate.y + 5], 1.2, P), { tone: "lo", free: true }));
  out.push(L(lineOnTop([plate.x + 5, plate.y + 16], [plate.x + 38, plate.y + 16], 1.2, P), { tone: "lo", free: true }));
  out.push(D([iso([plate.x + 3, plate.y + 3, 1.2], P), iso([plate.x + plate.w - 3, plate.y + plate.d - 3, 1.2], P)], { size: 0.45 }));
  return out.join("");
}

function driveTrain() {
  const out = [];
  out.push(S(k.cylinder(AXIS[0], AXIS[1], 17, 0, 13, P, 40, 0.8), { tone: "mid" }));
  out.push(S(k.cylinder(AXIS[0], AXIS[1], 13.5, 13, 4, P, 32, 0.6), { tone: "lo" }));
  out.push(L(k.sideArc(AXIS[0], AXIS[1], 17, 6, P, 28), { tone: "faint" }));
  out.push(S(k.cylinder(AXIS[0], AXIS[1], 6.6, 17, TABLE_Z - 17, P, 24), { tone: "mid", crease: "none" }));
  out.push(L(k.sideArc(AXIS[0], AXIS[1], 6.6, 22, P, 16), { tone: "faint" }));
  return out.join("");
}

function tableDisc() {
  const out = [];
  out.push(S(k.cylinder(AXIS[0], AXIS[1], TABLE_R, TABLE_Z, TABLE_H, P, 72, 0.8), { tone: "mid" }));
  out.push(S(k.cylinder(AXIS[0], AXIS[1], TABLE_R - 7, TABLE_TOP, 0.6, P, 64), { tone: "lo", crease: "none" }));
  out.push(L(k.ring(AXIS[0], AXIS[1], TABLE_R - 2.6, TABLE_TOP + 0.6, P, 72), { tone: "faint" }));
  out.push(S(k.cylinder(AXIS[0], AXIS[1], 13, TABLE_TOP, 5, P, 40, 0.6), { tone: "mid" }));
  out.push(S(k.cylinder(AXIS[0], AXIS[1], 8, TABLE_TOP + 5, 2.6, P, 28, 0.5), { tone: "lo" }));
  const marks = [];
  for (let index = 0; index < 8; index += 1) {
    const a = headAngle(index);
    marks.push(iso([AXIS[0] + (TABLE_R - 3) * Math.cos(a), AXIS[1] + (TABLE_R - 3) * Math.sin(a), TABLE_TOP + 0.6], P));
  }
  out.push(D(marks, { size: 0.5, tone: "lo" }));
  return out.join("");
}

function bedBeam(index) {
  const a = headAngle(index);
  const mid = a + Math.PI / 8;
  const cx = AXIS[0] + RING_R * Math.cos(mid);
  const cy = AXIS[1] + RING_R * Math.sin(mid);
  const out = [S(extrude(rotPlan(cx, cy, 44, 11, mid + Math.PI / 2), 0, 9, P, { convex: true, bevel: 0.7 }), { tone: "mid" })];
  const bolts = [];
  for (const sign of [-1, 1]) {
    const bx = cx + sign * 17 * Math.cos(mid + Math.PI / 2);
    const by = cy + sign * 17 * Math.sin(mid + Math.PI / 2);
    bolts.push([bx, by]);
  }
  out.push(D(bolts.map(([x, y]) => iso([x, y, 9], P)), { size: 0.5 }));
  return out.join("");
}

function column(index) {
  const [x, y] = headPoint(index, RING_R);
  const out = [];
  out.push(S(k.cylinder(x, y, 5.6, 9, 4.5, P, 24, 0.5), { tone: "lo" }));
  out.push(S(k.cylinder(x, y, 3.8, 13.5, COLUMN_TOP - 13.5, P, 24), { tone: "mid", crease: "none" }));
  out.push(L(k.sideArc(x, y, 3.8, 40, P, 16), { tone: "faint" }));
  return out.join("");
}

function arm(index) {
  const a = headAngle(index);
  const cx = AXIS[0] + 45 * Math.cos(a);
  const cy = AXIS[1] + 45 * Math.sin(a);
  const out = [S(extrude(rotPlan(cx, cy, 22, 7.4, a + Math.PI / 2), ARM_Z, ARM_H, P, { convex: true, bevel: 0.6 }), { tone: "mid" })];
  const [tx, ty] = headPoint(index, ORBIT_R);
  out.push(S(k.cylinder(tx, ty, 3.6, ARM_Z - 1.5, 3, P, 20, 0.4), { tone: "lo" }));
  const [hx, hy] = headPoint(index, RING_R);
  const ex = cx + 6 * Math.cos(a + Math.PI / 2);
  const ey = cy + 6 * Math.sin(a + Math.PI / 2);
  out.push(D([iso([hx, hy, ARM_Z + ARM_H], P), iso([ex, ey, ARM_Z + ARM_H], P)], { size: 0.45 }));
  return out.join("");
}

function tool(index) {
  const [x, y] = headPoint(index, ORBIT_R);
  const a = headAngle(index);
  const tangent = a + Math.PI / 2;
  const at_ = (d) => [x + d * Math.cos(tangent), y + d * Math.sin(tangent)];
  const out = [];
  const ram = (z0) => S(k.cylinder(x, y, 1.4, z0, 60.4 - z0, P, 14), { tone: "mid", crease: "none" });
  if (index === 0) {
    for (const sign of [-1, 1]) {
      const [jx, jy] = at_(sign * 3.4);
      out.push(S(extrude(rotPlan(jx, jy, 1.8, 9, tangent), TOOL_UP, 8, P, { convex: true, bevel: 0.3 }), { tone: "mid" }));
    }
    out.push(ram(TOOL_UP + 8));
  } else if (index === 1) {
    out.push(S(k.cylinder(x, y, 1.3, TOOL_UP + 2.5, 60.4 - TOOL_UP - 2.5, P, 16), { tone: "mid", crease: "none" }));
    out.push(S(G.sphereOf([x, y, TOOL_UP + 0.4], 2, P), { tone: "mid" }));
  } else if (index === 2) {
    out.push(S(k.cylinder(x, y, 3.4, TOOL_UP - 4, 4, P, 20, 0.5), { tone: "mid" }));
    out.push(ram(TOOL_UP));
  } else if (index === 3) {
    out.push(S(extrude(rotPlan(x, y, 5, 1.8, tangent), TOOL_UP - 8, 8, P, { convex: true, bevel: 0.3 }), { tone: "mid" }));
    out.push(ram(TOOL_UP));
  } else if (index === 4) {
    for (const sign of [-1, 1]) {
      const [jx, jy] = at_(sign * 2.6);
      out.push(S(extrude(rotPlan(jx, jy, 2.6, 4, tangent), TOOL_UP - 5, 5, P, { convex: true, bevel: 0.3 }), { tone: "mid" }));
    }
    out.push(ram(TOOL_UP));
  } else if (index === 5) {
    const frame = G.frameAlong([x, y, TOOL_UP - 9], [0, 0, 1]);
    out.push(S(G.solidOf([[0, 0.9, 1], [7, 3.4, 1]], frame, P), { tone: "mid" }));
    out.push(ram(TOOL_UP - 2));
    out.push(L(lineOnTop([x - 3, y - 3], [x + 3, y + 3], TOOL_UP - 6.6, P), { tone: "lo" }));
  } else if (index === 6) {
    out.push(S(k.cylinder(x, y, 4, TOOL_UP - 5, 5, P, 24, 0.5), { tone: "mid" }));
    out.push(S(k.cylinder(x, y, 4.8, TOOL_UP - 6.4, 1.4, P, 24), { tone: "mid" }));
    out.push(ram(TOOL_UP));
  } else {
    out.push(S(extrude(rotPlan(x, y, 7, 7, tangent), TOOL_UP - 8, 8, P, { convex: true, bevel: 0.4 }), { tone: "mid" }));
    out.push(ram(TOOL_UP));
  }
  return `<g data-part="tool-${index}" data-tool="${index}">${out.join("")}</g>`;
}

function toolTop(index) {
  const [x, y] = headPoint(index, ORBIT_R);
  const out = [S(k.cylinder(x, y, 1.4, 66.8, TOOL_TOP - 66.8, P, 14), { tone: "mid", crease: "none" })];
  if (index === 1) {
    out.push(S(k.cylinder(x, y, 1.3, 66.8, TOOL_TOP - 66.8, P, 16), { tone: "mid", crease: "none" }));
  }
  if (index === 7) {
    out.push(S(k.cylinder(x, y, 3.2, TOOL_TOP - 3, 3, P, 18, 0.4), { tone: "lo" }));
  }
  return `<g data-part="tool-${index}-top" data-tool="${index}">${out.join("")}</g>`;
}

function instruments() {
  const out = [];
  out.push(S(k.cylinder(DIAL[0], DIAL[1], 13, 0, 7, P, 32, 0.6), { tone: "lo" }));
  out.push(S(k.cylinder(DIAL[0], DIAL[1], 6.2, 7, DIAL_Z - 7, P, 24), { tone: "mid", crease: "none" }));
  out.push(L(k.sideArc(DIAL[0], DIAL[1], 6.2, 40, P, 16), { tone: "faint" }));
  out.push(S(k.cylinder(DIAL[0], DIAL[1], DIAL_R, DIAL_Z, DIAL_H, P, 64, 0.8), { tone: "hi", crease: "lo" }));
  out.push(L(k.knurl(DIAL[0], DIAL[1], DIAL_R, DIAL_TOP - 3.4, DIAL_TOP, 84, P, 0.3), { tone: "lo" }));
  out.push(L(k.sideArc(DIAL[0], DIAL[1], DIAL_R, DIAL_TOP - 3.4, P, 40), { tone: "faint" }));
  out.push(L(k.ring(DIAL[0], DIAL[1], DIAL_R - 2.4, DIAL_TOP, P, 64), { tone: "lo" }));
  const scaleOuter = DIAL_R - 2.4;
  const scaleMid = scaleOuter - 1.6;
  const scaleInner = scaleOuter - 2.9;
  out.push(L(k.ring(DIAL[0], DIAL[1], scaleMid, DIAL_TOP, P, 64), { tone: "faint" }));
  out.push(L(k.ring(DIAL[0], DIAL[1], scaleInner, DIAL_TOP, P, 64), { tone: "faint" }));
  const ticks = k.radialTicks(DIAL[0], DIAL[1], scaleOuter, 40, 4, DIAL_TOP, [1.6, 2.9], P, DIAL_ZERO, DIAL_SPAN);
  out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));
  for (const zero of [DIAL_ZERO, DIAL_ZERO + DIAL_SPAN]) {
    out.push(
      L(
        lineOnTop(
          [DIAL[0] + Math.sin(zero) * scaleInner, DIAL[1] - Math.cos(zero) * scaleInner],
          [DIAL[0] + Math.sin(zero) * scaleOuter, DIAL[1] - Math.cos(zero) * scaleOuter],
          DIAL_TOP,
          P,
        ),
        { tone: "hi" },
      ),
    );
  }
  out.push(L(k.ring(DIAL[0], DIAL[1], 1.8, DIAL_TOP, P, 16), { tone: "mid" }));
  out.push(S(extrude(rotPlan(DIAL[0] + DIAL_R - 1.6, DIAL[1], 7, 5.4, 0), DIAL_Z + 2, 5, P, { convex: true, bevel: 0.4 }), { tone: "mid" }));
  out.push(S(extrude(rotPlan(DIAL[0] + DIAL_R + 2.4, DIAL[1], 3.4, 6.4, 0), DIAL_Z + 1, 7, P, { convex: true, bevel: 0.4 }), { tone: "mid" }));

  out.push(S(k.cylinder(DRUM[0], DRUM[1], 11, 0, 5, P, 28, 0.6), { tone: "lo" }));
  out.push(S(k.cylinder(DRUM[0], DRUM[1], 4.6, 5, DRUM_Z - 5, P, 20), { tone: "mid", crease: "none" }));
  out.push(S(k.cylinder(DRUM[0], DRUM[1], DRUM_R, DRUM_Z, DRUM_H, P, 48, 0.7), { tone: "hi", crease: "lo" }));
  out.push(L(k.ring(DRUM[0], DRUM[1], DRUM_R - 2, DRUM_Z + DRUM_H, P, 48), { tone: "lo" }));
  for (let index = 0; index < 8; index += 1) {
    const a = headAngle(index);
    const x = DRUM[0] + (DRUM_R - 0.6) * Math.cos(a);
    const y = DRUM[1] + (DRUM_R - 0.6) * Math.sin(a);
    out.push(S(extrude(rotPlan(x, y, 2.4, 4, a + Math.PI / 2), DRUM_Z + 1, 3, P, { convex: true, bevel: 0.3 }), { tone: "lo" }));
  }

  out.push(S(extrude(rotPlan(GLASS[0] - 7, GLASS[1] + 3, 14, 12, 0), 0, 4, P, { convex: true, bevel: 0.4 }), { tone: "mid" }));
  out.push(S(k.cylinder(GLASS[0], GLASS[1], 4.6, 4, 3, P, 24, 0.5), { tone: "lo" }));
  out.push(S(k.cylinder(GLASS[0], GLASS[1], 3.8, GLASS_BOTTOM - 2, GLASS_TOP - GLASS_BOTTOM + 4, P, 24), { tone: "mid", crease: "none" }));
  out.push(S(k.cylinder(GLASS[0], GLASS[1], 4.8, GLASS_TOP + 2, 4, P, 24, 0.5), { tone: "lo" }));
  const marks = [];
  for (let z = GLASS_BOTTOM; z <= GLASS_TOP; z += 5) {
    marks.push(L(k.sideArc(GLASS[0], GLASS[1], 3.9, z, P, 20), { tone: (z - GLASS_BOTTOM) % 20 === 0 ? "mid" : "lo" }));
  }
  out.push(marks.join(""));
  return out.join("");
}

function rack() {
  const out = [];
  const base = { x: RACK[0] - 20, y: RACK[1] - 16, w: 44, d: 34, r: 3 };
  out.push(S(slabOf(base, 0, 4, P, 4, 0.6), { tone: "mid" }));
  out.push(S(slabOf({ x: base.x, y: base.y + base.d - 4, w: base.w, d: 4, r: 1 }, 4, 13, P, 3, 0.5), { tone: "lo" }));
  out.push(L(lineOnTop([base.x + 4, base.y + base.d - 5.4], [base.x + base.w - 4, base.y + base.d - 5.4], 15, P), { tone: "faint" }));
  out.push(D([iso([base.x + 4, base.y + base.d - 6, 15], P), iso([base.x + base.w - 4, base.y + base.d - 6, 15], P)], { size: 0.45 }));
  out.push(S(slabOf({ x: base.x, y: base.y, w: base.w, d: 3.4, r: 1 }, 4, 6, P, 3, 0.4), { tone: "lo" }));
  out.push(S(extrude(rotPlan(RACK[0] + 25, RACK[1] - 4, 24, 3.4, 0.35), 4, 3, P, { convex: true, bevel: 0.3 }), { tone: "mid" }));
  out.push(S(k.cylinder(RACK[0] + 25, RACK[1] - 14, 2.6, 0, 18, P, 18), { tone: "mid" }));
  const tray = { x: RACK[0] - 18, y: RACK[1] - 30, w: 40, d: 13, r: 2 };
  out.push(S(slabOf(tray, 0, 3, P, 3, 0.4), { tone: "lo" }));
  out.push(L(planOutline(k.insetPlan(tray, 1.8), 3, P), { tone: "faint" }));
  for (let index = 0; index < 3; index += 1) {
    out.push(
      S(extrude(rotPlan(tray.x + 9 + index * 9, tray.y + 6, 8, 5, 0.06 * index), 3, 1.2, P, { convex: true, bevel: 0.2 }), { tone: "lo" }),
    );
  }
  return out.join("");
}

function terminalBlock() {
  const out = [];
  const plan = { x: -64, y: 52, w: 40, d: 15, r: 2 };
  out.push(S(slabOf(plan, 0, 7, P, 4, 0.7), { tone: "mid" }));
  out.push(L(planOutline(k.insetPlan(plan, 2), 7, P), { tone: "faint" }));
  const sockets = [];
  for (let index = 0; index < 4; index += 1) {
    const x = plan.x + 7 + index * 8.6;
    const y = plan.y + plan.d / 2;
    sockets.push(S(k.cylinder(x, y, 2.8, 7, 1.6, P, 20), { tone: "lo" }));
    sockets.push(L(k.ring(x, y, 3.2, 8.6, P, 20), { tone: "mid" }));
  }
  out.push(sockets.join(""));
  out.push(D([iso([plan.x + 3, plan.y + 3, 7], P), iso([plan.x + plan.w - 3, plan.y + plan.d - 3, 7], P)], { size: 0.45 }));
  return out.join("");
}

function guardStand() {
  const out = [];
  const [gx, gy] = GUARD;
  out.push(S(slabOf({ x: gx - 12, y: gy - 10, w: 24, d: 20, r: 2 }, 0, 4, P, 4, 0.6), { tone: "mid" }));
  out.push(S(k.cylinder(gx, gy, 3.4, 4, 10, P, 20), { tone: "mid", crease: "none" }));
  out.push(S(k.cylinder(gx, gy, 11, 14, 1.6, P, 40, 0.5), { tone: "hi", crease: "lo" }));
  out.push(L(k.ring(gx, gy, 9.4, 15.6, P, 40), { tone: "faint" }));
  const marks = [];
  for (let index = 0; index < 3; index += 1) {
    const angle = (-60 + index * 60) * (Math.PI / 180);
    const mx = gx + 8.4 * Math.sin(angle);
    const my = gy - 8.4 * Math.cos(angle);
    marks.push(S(extrude(rotPlan(mx, my, 2.6, 4, angle), 15.6, 1.4, P, { convex: true, bevel: 0.2 }), { tone: "lo" }));
  }
  out.push(marks.join(""));
  out.push(D([iso([gx, gy, 15.6], P)], { size: 0.5, tone: "mid" }));
  return out.join("");
}

function guardSvg(verdict, P) {
  const index = verdict === "allow" ? 0 : verdict === "ask" ? 1 : 2;
  const angle = (-60 + index * 60) * (Math.PI / 180);
  const gx = GEO.GUARD[0];
  const gy = GEO.GUARD[1];
  const dx = Math.sin(angle);
  const dy = -Math.cos(angle);
  const out = [];
  out.push(solidSvg(extrude(rotPlan(gx + dx * 6.5, gy + dy * 6.5, 13, 3.4, angle), 15.6, 2.2, P, { convex: true, bevel: 0.3 }), { tone: "hi" }));
  out.push(solidSvg(cylinder(gx + dx * 12.6, gy + dy * 12.6, 2.8, 15.6, 4.4, P, 18, 0.4), { tone: "mid" }));
  out.push(solidSvg(cylinder(gx, gy, 2.4, 15.6, 3, P, 16, 0.3), { tone: "lo" }));
  return out.join("");
}

function cards() {
  const out = [];
  CARD_X.forEach((x, index) => {
    const plan = { x, y: RACK[1] - 8, w: 9, d: 1.4, r: 0.4 };
    const solid = S(slabOf(plan, 4, 20, P, 3, 0.4), { tone: index === 0 ? "hi" : "lo" });
    out.push(index === 0 ? `<g data-part="card-0">${solid}</g>` : solid);
  });
  return out.join("");
}

function rotorSvg(angle, P) {
  const x = GEO.AXIS[0] + GEO.ORBIT_R * Math.cos(angle);
  const y = GEO.AXIS[1] + GEO.ORBIT_R * Math.sin(angle);
  const out = [];
  out.push(solidSvg(cylinder(x, y, 7, GEO.TABLE_TOP, 2, P, 24, 0.4), { tone: "mid" }));
  out.push(solidSvg(slabOf({ x: x - 7, y: y - 7, w: 14, d: 14, r: 1.6 }, GEO.BLOCK_BOTTOM, GEO.BLOCK_TOP - GEO.BLOCK_BOTTOM, P, 5, 0.7), { tone: "mid" }));
  const tangent = angle + Math.PI / 2;
  out.push(
    lineSvg(
      lineOnTop(
        [x - 7 * Math.cos(tangent), y - 7 * Math.sin(tangent)],
        [x + 7 * Math.cos(tangent), y + 7 * Math.sin(tangent)],
        GEO.BLOCK_TOP,
        P,
      ),
      { tone: "faint" },
    ),
  );
  const tangent2 = angle + Math.PI / 2;
  out.push(
    lineSvg(
      lineOnTop(
        [x - 5 * Math.cos(tangent2), y - 5 * Math.sin(tangent2)],
        [x + 5 * Math.cos(tangent2), y + 5 * Math.sin(tangent2)],
        GEO.BLOCK_TOP,
        P,
      ),
      { tone: "faint" },
    ),
  );
  const barX = GEO.AXIS[0] + 22 * Math.cos(angle);
  const barY = GEO.AXIS[1] + 22 * Math.sin(angle);
  out.push(
    solidSvg(extrude(rotPlan(barX, barY, 17, 4, angle + Math.PI / 2), GEO.TABLE_TOP + 0.6, 1.6, P, { convex: true, bevel: 0.3 }), { tone: "mid" }),
  );
  return out.join("");
}

const HEAD_ORDER = [0, 1, 2, 3, 4, 5, 6, 7].sort((a, b) => headDepth(a) - headDepth(b));
const BACK = HEAD_ORDER.filter((index) => headDepth(index) < 0);
const FRONT = HEAD_ORDER.filter((index) => headDepth(index) >= 0);

const svg = k.figureSvg({
  width: WIDTH,
  height: HEIGHT,
  label:
    "A bench-top rotary indexing machine. A block clamped to a turntable is carried under eight fixed tool heads, one for each stage of a round, while a dial, a phase drum and a sight glass report coverage, kill-chain phase and remaining budget.",
  body: [
    basePlate(),
    rulerStrip(),
    namePlate(),
    driveTrain(),
    ...BACK.map((index) => bedBeam(index)),
    ...BACK.map((index) => column(index)),
    tableDisc(),
    `<g data-part="rotor">${rotorSvg(headAngle(0), P)}</g>`,
    ...FRONT.map((index) => bedBeam(index)),
    ...FRONT.map((index) => column(index)),
    ...HEAD_ORDER.map((index) => tool(index)),
    ...HEAD_ORDER.map((index) => arm(index)),
    ...HEAD_ORDER.map((index) => toolTop(index)),
    instruments(),
    rack(),
    terminalBlock(),
    guardStand(),
    cards(),
    `<path data-part="needle" class="iso-line" data-tone="hi" data-free="start" d=""/>`,
    `<g data-part="phase-pointer"></g>`,
    `<g data-part="level"></g>`,
    `<g data-part="guard"></g>`,
  ],
});

const live = `
const P = ${JSON.stringify(P)};
const GEO = ${JSON.stringify(GEO)};
const SIM = simulate(11);
const TICKS = SIM.ticks;
const STAGE_SECONDS = 1.55;
const ROTATE_SECONDS = 0.62;
const DIVE_SECONDS = 0.34;
const clamp = (value, low, high) => Math.min(high, Math.max(low, value));
const ease = (t) => (t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t));
const rotPlan = ${rotPlan.toString()};
const rotorSvg = ${rotorSvg.toString()};
const guardSvg = ${guardSvg.toString()};
const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const rotor = svg.querySelector('[data-part="rotor"]');
const readout = document.querySelector("[data-readout]");
const needle = svg.querySelector('[data-part="needle"]');
const pointer = svg.querySelector('[data-part="phase-pointer"]');
const level = svg.querySelector('[data-part="level"]');
const guard = svg.querySelector('[data-part="guard"]');
const card = svg.querySelector('[data-part="card-0"]');
const toolGroups = [0, 1, 2, 3, 4, 5, 6, 7].flatMap((index) => [
  svg.querySelector('[data-part="tool-' + index + '"]'),
  svg.querySelector('[data-part="tool-' + index + '-top"]'),
]);
const still = matchMedia("(prefers-reduced-motion: reduce)");
let clock = 0;
let manual = false;
let manualStage = 5;
let visible = false;
let frame = 0;
let last = 0;
let idleTimer = 0;
let restartTimer = 0;

const headAngle = (index) => (Math.PI / 4) * index + Math.PI / 8;

function tickFor(time) {
  if (manual) {
    const round = TICKS[clamp(Math.floor(time / STAGE_SECONDS), 0, TICKS.length - 1)].round;
    const match = TICKS.find((tick) => tick.round === round && tick.stageIndex === manualStage);
    return match || TICKS.find((tick) => tick.stageIndex === manualStage) || TICKS[0];
  }
  return TICKS[clamp(Math.floor(time / STAGE_SECONDS), 0, TICKS.length - 1)];
}

function needleAt(coverage) {
  const angle = GEO.DIAL_ZERO + GEO.DIAL_SPAN * clamp(coverage, 0, 1);
  const dx = Math.sin(angle);
  const dy = -Math.cos(angle);
  return lineOnTop(
    [GEO.DIAL[0] - dx * 3.6, GEO.DIAL[1] - dy * 3.6],
    [GEO.DIAL[0] + dx * (GEO.DIAL_R - 4.6), GEO.DIAL[1] + dy * (GEO.DIAL_R - 4.6)],
    GEO.DIAL_TOP + 0.2,
    P,
  );
}

function pointerAt(phaseIndex) {
  const angle = headAngle(phaseIndex);
  const dx = Math.cos(angle);
  const dy = Math.sin(angle);
  const cx = GEO.DRUM[0];
  const cy = GEO.DRUM[1];
  const z = GEO.DRUM_Z + GEO.DRUM_H;
  const out = [];
  out.push(solidSvg(extrude(rotPlan(cx + dx * 6.5, cy + dy * 6.5, 12, 3.4, angle + Math.PI / 2), z, 2.4, P, { convex: true, bevel: 0.4 }), { tone: "mid" }));
  out.push(solidSvg(cylinder(cx, cy, 2.6, z, 3.4, P, 20, 0.4), { tone: "mid" }));
  return out.join("");
}

function levelAt(used) {
  const top = GEO.GLASS_TOP - 2;
  const bottom = GEO.GLASS_BOTTOM + 1;
  const height = (top - bottom) * (1 - clamp(used, 0, 1));
  return solidSvg(cylinder(GEO.GLASS[0], GEO.GLASS[1], 2.6, bottom, Math.max(0.6, height), P, 20), { tone: "mid", crease: "none" });
}

function draw() {
  const tick = tickFor(clock);
  const within = clock - Math.floor(clock / STAGE_SECONDS) * STAGE_SECONDS;
  const spin = manual ? 1 : ease(clamp(within / ROTATE_SECONDS, 0, 1));
  const angle = headAngle(0) + (Math.PI / 4) * (tick.index + spin);
  rotor.innerHTML = rotorSvg(angle, P);

  const aligned = ((Math.round((angle - headAngle(0)) / (Math.PI / 4)) % 8) + 8) % 8;
  const diveIn = manual ? 1 : clamp((within - ROTATE_SECONDS) / DIVE_SECONDS, 0, 1);
  const diveOut = manual ? 0 : clamp((within - (STAGE_SECONDS - DIVE_SECONDS)) / DIVE_SECONDS, 0, 1);
  const dive = diveIn * (1 - diveOut);
  const depth = tick.guard === "deny" ? 0 : tick.guard === "ask" ? 0.5 : 1;
  const travel = GEO.TOOL_TRAVEL * depth * dive;
  toolGroups.forEach((group, index) => {
    if (!group) return;
    const active = Math.floor(index / 2) === aligned;
    group.setAttribute("transform", active ? translateAlong(P, [0, 0, -travel]) : "");
    group.querySelectorAll(".iso-solid").forEach((solid) => {
      if (active) solid.setAttribute("data-lit", "");
      else solid.removeAttribute("data-lit");
    });
  });

  const lift = tick.stage === "claim" ? 5 * dive : tick.stage === "work" ? 5 : tick.stage === "record" ? 5 * (1 - dive) : 0;
  card.setAttribute("transform", translateAlong(P, [0, 0, lift]));

  needle.setAttribute("d", needleAt(tick.coverage / 100));
  pointer.innerHTML = pointerAt(tick.phaseIndex);
  level.innerHTML = levelAt(tick.toolcalls / 200);
  guard.innerHTML = guardSvg(tick.guard, P);

  const text =
    "r" + tick.round + "/10 \\u00b7 " + tick.stage + " \\u00b7 " + tick.phase +
    " \\u00b7 " + tick.toolcalls + "/200 \\u00b7 " + tick.coverage + "% \\u00b7 " + tick.guard;
  if (readout.textContent !== text) readout.textContent = text;
  stage.setAttribute("aria-valuenow", String(tick.coverage));
  stage.setAttribute("aria-valuetext", text);
}

function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  if (!manual) clock += dt;
  draw();
  const finished = !manual && clock > TICKS.length * STAGE_SECONDS;
  frame = visible && !finished ? requestAnimationFrame(tick) : 0;
  if (finished) {
    const text =
      "goal " + SIM.final.verdict + " \\u00b7 " + SIM.final.rounds + " rounds \\u00b7 " + SIM.final.phase +
      " \\u00b7 " + SIM.final.coverage + "% \\u00b7 " + SIM.final.toolcalls + "/200";
    if (readout.textContent !== text) readout.textContent = text;
    clearTimeout(restartTimer);
    restartTimer = setTimeout(() => {
      clock = 0;
      if (!frame && visible) frame = requestAnimationFrame(tick);
    }, 2800);
  }
}

const run = () => {
  if (!frame && visible) {
    last = 0;
    frame = requestAnimationFrame(tick);
  }
};

const steer = (stageIndex) => {
  manual = true;
  manualStage = clamp(stageIndex, 0, 7);
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => {
    manual = false;
    run();
  }, 3200);
  run();
};

new IntersectionObserver(
  (entries) => {
    visible = entries[entries.length - 1].isIntersecting;
    if (visible) run();
  },
  { rootMargin: "120px 0px" },
).observe(stage);

stage.addEventListener("pointermove", (event) => {
  const box = svg.getBoundingClientRect();
  const share = clamp((event.clientX - box.left) / box.width, 0, 1);
  steer(Math.min(7, Math.floor(share * 8)));
});

stage.addEventListener("pointerleave", () => {
  manual = false;
});

stage.addEventListener("keydown", (event) => {
  let to = null;
  if (event.key === "ArrowRight" || event.key === "ArrowDown") to = manualStage + 1;
  if (event.key === "ArrowLeft" || event.key === "ArrowUp") to = manualStage - 1;
  if (event.key === "Home") to = 0;
  if (event.key === "End") to = 7;
  if (to === null) return;
  event.preventDefault();
  steer(to);
});

if (still.matches) clock = 0;
draw();
`;

const MODEL = readFileSync(join(HERE, "model.mjs"), "utf8").replace(/^export /gm, "");

const body = k.plateHtml({
  fig: "Fig 1",
  title: "LazyOwn autonomous loop",
  hint: "Hover or arrows to step",
  readout: "r1/10 · scope · recon · 0/200 · 0% · allow",
  keys: [
    { mark: "lit", label: "The head working the block now: the stage that touches the target" },
    { mark: "raised", label: "The block on the table: the engagement, carried round the ring" },
    { mark: "edge", label: "Eight heads, one per stage of a round" },
    { mark: "dim", label: "Dial: coverage · drum: phase · sight glass: budget" },
  ],
  caption:
    "A bench-top round engine. The block clamped on the turntable is the engagement. The table turns it under eight fixed heads — scope, enrich, trigger, plan, claim, work, record, settle — and one full turn is one round of the loop. The head over the block does that stage's work, and the guard decides whether it may touch: allow, ask or deny. The dial reads the share of assets the loop has tested, the pointer on the drum reads the kill-chain phase, and the level in the sight glass falls as the 200-call budget is spent. The cards in the rack are the planner's intents; a worker claims one at a time.",
  body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="LazyOwn autonomous loop: arrow keys step the table through the eight stages of a round" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">${svg}</div>`,
});

const script = kitScript() + MODEL + live;
writeFileSync(join(HERE, theme === "light" ? "autonomous-loop-light.html" : "autonomous-loop.html"), k.pageHtml({ title: "LazyOwn autonomous loop", theme, body, script }));
console.log("wrote", theme === "light" ? "autonomous-loop-light.html" : "autonomous-loop.html");
