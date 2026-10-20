export const PHASES = [
  "recon",
  "scan",
  "enum",
  "exploit",
  "privesc",
  "lateral",
  "exfil",
  "report",
];

export const PHASE_LABELS = [
  "Reconnaissance",
  "Scanning",
  "Enumeration",
  "Exploitation",
  "Privilege Escalation",
  "Lateral Movement",
  "Exfiltration",
  "Reporting",
];

export const STAGES = [
  "scope",
  "enrich",
  "trigger",
  "plan",
  "claim",
  "work",
  "record",
  "settle",
];

export const LIMITS = {
  rounds: 10,
  toolcalls: 200,
  findings: 50,
  intentsPerRound: 4,
  workers: 2,
  stepsPerIntent: 6,
};

export const GUARD_PATTERN = [
  "allow",
  "allow",
  "ask",
  "allow",
  "deny",
  "allow",
  "allow",
  "ask",
  "allow",
  "allow",
  "deny",
  "allow",
];

export const GOAL = "gain initial access on 10.10.11.5";

const MILESTONE = [4, 7, 11, 15];

export function simulate(seed = 11) {
  let state = seed >>> 0;
  const rnd = () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 4294967296;
  };
  const ticks = [];
  let phaseIndex = 0;
  let toolcalls = 0;
  let facts = 0;
  let findings = 0;
  let assets = 1;
  let tested = 0;
  let intentsOpen = 0;
  let claimed = 0;
  let worked = 0;
  let goalMet = false;
  let stopReason = "rounds";
  let round = 0;

  for (round = 1; round <= LIMITS.rounds && !goalMet; round += 1) {
    for (let stageIndex = 0; stageIndex < STAGES.length; stageIndex += 1) {
      const stage = STAGES[stageIndex];
      let guard = "allow";
      let steps = 0;

      if (stage === "enrich") {
        toolcalls += 1;
        if (rnd() < 0.45) {
          assets += 1;
        }
      }

      if (stage === "plan") {
        const emitted = Math.min(LIMITS.intentsPerRound, 1 + Math.floor(rnd() * LIMITS.intentsPerRound));
        intentsOpen += emitted;
      }

      if (stage === "claim") {
        claimed = Math.min(LIMITS.workers, intentsOpen);
        intentsOpen -= claimed;
      }

      if (stage === "work") {
        guard = GUARD_PATTERN[(round * 3 + stageIndex * 5) % GUARD_PATTERN.length];
        if (guard === "allow") {
          steps = Math.min(LIMITS.stepsPerIntent, 1 + Math.floor(rnd() * LIMITS.stepsPerIntent));
        } else if (guard === "ask") {
          steps = Math.min(LIMITS.stepsPerIntent, Math.ceil((1 + Math.floor(rnd() * LIMITS.stepsPerIntent)) / 2));
        } else {
          steps = 0;
        }
        toolcalls += steps * claimed;
        worked = steps > 0 ? claimed : 0;
        for (let step = 0; step < steps; step += 1) {
          facts += 1;
          if (rnd() < 0.25) {
            assets += 1;
          }
        }
      }

      if (stage === "record") {
        tested = Math.min(assets, tested + worked);
        if (worked > 0 && rnd() < 0.3) {
          findings += 1;
        }
      }

      if (stage === "settle") {
        const need = MILESTONE[phaseIndex] ?? 99;
        if (phaseIndex < PHASES.length - 1 && facts + findings >= need) {
          phaseIndex += 1;
        }
        if (phaseIndex >= 3 && findings >= 1) {
          goalMet = true;
          stopReason = "goal_met";
        }
      }

      ticks.push({
        index: ticks.length,
        round,
        stage,
        stageIndex,
        phase: PHASES[phaseIndex],
        phaseIndex,
        guard,
        steps,
        claimed,
        toolcalls,
        facts,
        findings,
        assets,
        tested,
        coverage: assets ? Math.round((100 * tested) / assets) : 0,
        goalMet,
      });

      if (toolcalls >= LIMITS.toolcalls) {
        stopReason = "budget";
        round = LIMITS.rounds;
        break;
      }
      if (goalMet) {
        break;
      }
    }
  }

  const coverage = assets ? Math.round((100 * tested) / assets) : 0;
  const verdict = goalMet ? "achieved" : facts > 0 || tested > 0 ? "partial" : "failed";
  return {
    goal: GOAL,
    ticks,
    final: {
      verdict,
      stopReason,
      rounds: ticks.length ? ticks[ticks.length - 1].round : 0,
      phase: PHASES[phaseIndex],
      phaseIndex,
      toolcalls,
      facts,
      findings,
      assets,
      tested,
      coverage,
    },
  };
}
