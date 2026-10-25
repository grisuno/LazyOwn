import { pathToFileURL } from "node:url";
import { join } from "node:path";
import { homedir } from "node:os";

const SKILL = process.env.ANATOMY_SKILL || join(homedir(), ".config/opencode/skills/anatomy");
const k = await import(pathToFileURL(join(SKILL, "kit/iso-kit.mjs")).href);
const A = await import(pathToFileURL(join(SKILL, "kit/audit.mjs")).href);

const BASE = { x: -138, y: -92, w: 280, d: 172, r: 12 };
const BASE_BOTTOM = -12;
const BASE_H = 12;
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
const TOOL_TOP = 74;

const P = k.fitProjection(
  [
    ...k.boxCorners(BASE, BASE_BOTTOM - 5, 0),
    [AXIS[0], AXIS[1], TOOL_TOP + 4],
    [98, -52, 84],
    [98, -2, 53],
    [130, -36, 74],
    [-79, 30, 26],
  ],
  740,
  500,
  { pad: 30, azimuth: 45 },
);

const headAngle = (index) => (Math.PI / 4) * index + Math.PI / 8;
const headPoint = (index, radius) => {
  const a = headAngle(index);
  return [AXIS[0] + radius * Math.cos(a), AXIS[1] + radius * Math.sin(a)];
};
const headDepth = (index) => k.depthOf([...headPoint(index, RING_R), 0], P);
const HEAD_ORDER = [0, 1, 2, 3, 4, 5, 6, 7].sort((a, b) => headDepth(a) - headDepth(b));
const BACK = HEAD_ORDER.filter((index) => headDepth(index) < 0);
const FRONT = HEAD_ORDER.filter((index) => headDepth(index) >= 0);

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

const along = (angle) => [Math.cos(angle), Math.sin(angle)];
const across = (angle) => [-Math.sin(angle), Math.cos(angle)];
const up = [0, 0, 1];

const R = A.recorder(P, { order: [] });
const { items, nameFor } = R;

let ORDER = 0;
function put(at, shapes, label) {
  R.put({ at, bias: 0, svg: "", shapes, key: ORDER++, name: nameFor(label) });
}

for (const [x, y] of k.corners(BASE, 24)) {
  put([x, y, BASE_BOTTOM - 3], [R.solid(A.cylinder(x, y, 5.6, BASE_BOTTOM - 5, 5, { name: "base.foot" }))], "base.foot");
}
put([AXIS[0], AXIS[1], BASE_BOTTOM + BASE_H / 2], [R.solid(A.slab(BASE, BASE_BOTTOM, BASE_H, { name: "base.plate" }))], "base");
put([AXIS[0], AXIS[1], 6], [R.solid(A.cylinder(AXIS[0], AXIS[1], 17, 0, 13, { name: "drive.box" }))], "drive");
put([AXIS[0], AXIS[1], 22], [R.solid(A.cylinder(AXIS[0], AXIS[1], 6.6, 17, TABLE_Z - 17, { name: "drive.shaft" }))], "drive.shaft");

function beam(index) {
  const a = headAngle(index);
  const mid = a + Math.PI / 8;
  const cx = AXIS[0] + RING_R * Math.cos(mid);
  const cy = AXIS[1] + RING_R * Math.sin(mid);
  const dir = along(mid + Math.PI / 2);
  put(
    [cx, cy, 4.5],
    [R.solid(A.orientedBox([cx, cy, 4.5], [dir, across(mid + Math.PI / 2), up], [22, 5.5, 4.5], { name: "bed.beam" }))],
    "bed.beam",
  );
}

function column(index) {
  const [x, y] = headPoint(index, RING_R);
  put([x, y, 11], [R.solid(A.cylinder(x, y, 5.6, 9, 4.5, { name: "head.collar" }))], "head.collar");
  put([x, y, 37], [R.solid(A.cylinder(x, y, 3.8, 13.5, COLUMN_TOP - 13.5, { name: "head.column" }))], "head.column");
}

function ramOf(index) {
  const [x, y] = headPoint(index, ORBIT_R);
  return { x, y, lower: A.cylinder(x, y, 1.4, 58, 2.4, { name: "tool.ram.lower" }), upper: A.cylinder(x, y, 1.4, 66.8, TOOL_TOP - 66.8, { name: "tool.ram.upper" }) };
}

function arm(index) {
  const a = headAngle(index);
  const cx = AXIS[0] + 45 * Math.cos(a);
  const cy = AXIS[1] + 45 * Math.sin(a);
  const dir = along(a + Math.PI / 2);
  const ram = ramOf(index);
  put(
    [cx, cy, ARM_Z + ARM_H / 2],
    [
      R.solid(
        A.orientedBox([cx, cy, ARM_Z + ARM_H / 2], [dir, across(a + Math.PI / 2), up], [11, 3.7, ARM_H / 2], {
          name: "head.arm",
          cut: [ram.upper],
        }),
      ),
    ],
    "head.arm",
  );
  const [tx, ty] = headPoint(index, ORBIT_R);
  put(
    [tx, ty, ARM_Z],
    [R.solid(A.cylinder(tx, ty, 3.6, ARM_Z - 1.5, 3, { name: "head.bush" }))],
    "head.bush",
  );
}

function tool(index) {
  const [x, y] = headPoint(index, ORBIT_R);
  const a = headAngle(index);
  const tangent = a + Math.PI / 2;
  const at_ = (d) => [x + d * Math.cos(tangent), y + d * Math.sin(tangent)];
  const box = (cx, cy, length, width, z, h, label) => {
    const dir = along(tangent);
    put([cx, cy, z + h / 2], [R.solid(A.orientedBox([cx, cy, z + h / 2], [dir, across(tangent), up], [length / 2, width / 2, h / 2], { name: label }))], label);
  };
  const lower = (z0) => {
    if (z0 >= 60.4) return;
    put([x, y, (z0 + 60.4) / 2], [R.solid(A.cylinder(x, y, 1.4, z0, 60.4 - z0, { name: "tool.ram.lower" }))], "tool.ram.lower");
  };
  if (index === 0) {
    for (const sign of [-1, 1]) {
      const [jx, jy] = at_(sign * 3.4);
      box(jx, jy, 1.8, 9, TOOL_UP, 8, "tool.jaw");
    }
  } else if (index === 1) {
    put(
      [x, y, (TOOL_UP + 2.5 + 60.4) / 2],
      [
        R.solid(A.cylinder(x, y, 1.3, TOOL_UP + 2.5, 60.4 - TOOL_UP - 2.5, { name: "tool.probe" })),
        R.solid(A.ball([x, y, TOOL_UP + 0.4], 2, { name: "tool.ball" })),
      ],
      "tool.probe",
    );
  } else if (index === 2) {
    put([x, y, TOOL_UP - 2], [R.solid(A.cylinder(x, y, 3.4, TOOL_UP - 4, 4, { name: "tool.hammer" }))], "tool.hammer");
    lower(TOOL_UP);
  } else if (index === 3) {
    box(x, y, 5, 1.8, TOOL_UP - 8, 8, "tool.blade");
    lower(TOOL_UP);
  } else if (index === 4) {
    for (const sign of [-1, 1]) {
      const [jx, jy] = at_(sign * 2.6);
      box(jx, jy, 2.6, 4, TOOL_UP - 5, 5, "tool.jaw");
    }
    lower(TOOL_UP);
  } else if (index === 5) {
    put([x, y, TOOL_UP - 5], [R.solid(A.cylinder(x, y, 2.6, TOOL_UP - 9, 7, { name: "tool.drill" }))], "tool.drill");
    lower(TOOL_UP - 2);
  } else if (index === 6) {
    put(
      [x, y, TOOL_UP - 3],
      [
        R.solid(A.cylinder(x, y, 4, TOOL_UP - 5, 5, { name: "tool.stamp" })),
        R.solid(A.cylinder(x, y, 4.8, TOOL_UP - 6.4, 1.4, { name: "tool.face" })),
      ],
      "tool.stamp",
    );
    lower(TOOL_UP);
  } else {
    box(x, y, 7, 7, TOOL_UP - 8, 8, "tool.press");
    lower(TOOL_UP);
  }
}

function rotor(angle) {
  const x = AXIS[0] + ORBIT_R * Math.cos(angle);
  const y = AXIS[1] + ORBIT_R * Math.sin(angle);
  put([x, y, TABLE_TOP + 1], [R.solid(A.cylinder(x, y, 7, TABLE_TOP, 2, { name: "rotor.boss" }))], "rotor.boss");
  put(
    [x, y, (BLOCK_BOTTOM + BLOCK_TOP) / 2],
    [R.solid(A.box([x - 10, y - 10, BLOCK_BOTTOM], [x + 10, y + 10, BLOCK_TOP], { name: "rotor.block" }))],
    "rotor.block",
  );
}

for (const index of BACK) beam(index);
for (const index of BACK) column(index);
put([AXIS[0], AXIS[1], TABLE_Z + TABLE_H / 2], [R.solid(A.cylinder(AXIS[0], AXIS[1], TABLE_R, TABLE_Z, TABLE_H, { name: "table" }))], "table");
put([AXIS[0], AXIS[1], TABLE_TOP + 2.5], [R.solid(A.cylinder(AXIS[0], AXIS[1], 13, TABLE_TOP, 5, { name: "table.hub" }))], "table.hub");
rotor(headAngle(0));
for (const index of FRONT) beam(index);
for (const index of FRONT) column(index);
for (const index of HEAD_ORDER) tool(index);
for (const index of HEAD_ORDER) arm(index);
for (const index of HEAD_ORDER) {
  const [x, y] = headPoint(index, ORBIT_R);
  const top = [R.solid(A.cylinder(x, y, 1.4, 66.8, TOOL_TOP - 66.8, { name: "tool.ram.top" }))];
  if (index === 1) {
    top.push(R.solid(A.cylinder(x, y, 1.3, 66.8, TOOL_TOP - 66.8, { name: "tool.probe.top" })));
  }
  if (index === 7) {
    top.push(R.solid(A.cylinder(x, y, 3.2, TOOL_TOP - 3, 3, { name: "tool.weight" })));
  }
  put([x, y, (66.8 + TOOL_TOP) / 2], top, "tool.top");
}

items.sort((a, b) => a.key - b.key);
const overlaps = A.overlapsOf(items, P, { step: 0.25 });
const depth = A.depthOrder(items, P, { overlaps, solved: false });
console.log(`items ${items.length} · overlapping pairs ${overlaps.length ?? overlaps.pairs?.length ?? 0} · depth problems ${depth.problems.length}`);
for (const problem of depth.problems.slice(0, 30)) {
  console.log("  ", JSON.stringify(problem));
}
