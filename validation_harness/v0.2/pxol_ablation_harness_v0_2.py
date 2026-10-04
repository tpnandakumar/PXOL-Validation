"""
PXOL/PFLOX VCG-P5D[zD] Ablation Validation Harness
Version 0.2

Adds:
- repeated-seed replication
- paired task sets across configurations
- mean, SD and 95% CI
- component contribution stability
- pass/watch/fail interpretation
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any
from pathlib import Path
import csv, json, random, statistics, math


@dataclass(frozen=True)
class AblationConfig:
    name: str
    p5d: bool = True
    vcg: bool = True
    dvd: bool = True
    frontload: bool = True
    memory: bool = True


@dataclass
class Task:
    task_id: str
    difficulty: int
    context_shift: bool
    contradiction: bool
    delayed_outcome: bool
    repeated: bool
    target: int


CONFIGS = [
    AblationConfig("FULL"),
    AblationConfig("NO_VCG", vcg=False),
    AblationConfig("NO_DVD", dvd=False),
    AblationConfig("NO_FRONTLOAD", frontload=False),
    AblationConfig("NO_MEMORY", memory=False),
    AblationConfig("NO_P5D", p5d=False),
    AblationConfig("BASELINE", p5d=False, vcg=False, dvd=False, frontload=False, memory=False),
]

ABLATION_MAP = {
    "VCG": "NO_VCG",
    "DvD": "NO_DVD",
    "PFLOX_frontload": "NO_FRONTLOAD",
    "Multidimensional_memory": "NO_MEMORY",
    "P5D_zD": "NO_P5D",
}


class SyntheticPXOLAgent:
    """Synthetic stand-in. Results validate only the harness."""

    def __init__(self, config: AblationConfig, seed: int):
        self.config = config
        self.rng = random.Random(seed)
        self.memory_store: Dict[str, float] = {}

    def _key(self, task: Task):
        return task.task_id.split("_r")[0]

    def solve(self, task: Task):
        cfg = self.config
        key = self._key(task)
        p = 0.82 - 0.075 * max(0, task.difficulty - 1)
        ops = 45 + 22 * task.difficulty
        dim = float(max(1, min(task.difficulty, 5)))
        mem_hits = vectors = escalations = 0

        if cfg.dvd:
            if task.difficulty <= 2:
                dim *= 0.72
                ops = int(ops * 0.82)
            elif task.difficulty >= 4:
                escalations += 1
                p += 0.035
        else:
            dim *= 1.20
            ops = int(ops * 1.18)

        if cfg.p5d:
            p += 0.03 * max(0, task.difficulty - 2)
            if task.context_shift:
                p += 0.05
        else:
            if task.difficulty >= 4:
                p -= 0.09
            if task.context_shift:
                p -= 0.07

        if cfg.vcg:
            if task.contradiction:
                p += 0.11
                vectors += 2
            elif task.difficulty >= 4:
                p += 0.035
                vectors += 1
        elif task.contradiction:
            p -= 0.13

        ms = self.memory_store.get(key, 0.0)
        if cfg.memory and ms > 0:
            mem_hits = 1
            p += 0.08 * ms
            ops = int(ops * (0.92 - 0.10 * min(ms, 1.0)))

        if cfg.frontload and cfg.memory and ms > 0:
            p += 0.05
            ops = int(ops * 0.78)
            dim *= 0.78

        if task.delayed_outcome:
            p -= 0.015

        p = max(0.03, min(0.98, p))
        return {
            "correct": int(self.rng.random() < p),
            "confidence": max(0.05, min(0.99, p + self.rng.uniform(-0.08, 0.08))),
            "dimensional_load": max(1.0, dim),
            "operations": max(1, ops),
            "memory_hits": mem_hits,
            "vector_events": vectors,
            "escalations": escalations,
        }

    def observe(self, task: Task, result: Dict[str, Any]):
        if not self.config.memory:
            return
        key = self._key(task)
        current = self.memory_store.get(key, 0.0)
        delta = 0.0 if task.delayed_outcome else (0.22 if result["correct"] else -0.12)
        self.memory_store[key] = max(0.0, min(1.0, current + delta))


def make_tasks(seed: int, n_base: int = 160) -> List[Task]:
    rng = random.Random(seed)
    tasks = []
    for i in range(n_base):
        d = rng.randint(1, 5)
        context = rng.random() < 0.25
        contradiction = rng.random() < 0.22
        delayed = rng.random() < 0.15
        target = rng.randint(0, 1)
        tid = f"T{i:03d}"
        tasks.append(Task(tid, d, context, contradiction, delayed, False, target))
        if rng.random() < 0.45:
            tasks.append(Task(
                f"{tid}_r1", d,
                context if rng.random() > 0.25 else not context,
                contradiction, False, True, target
            ))
    return tasks


def evaluate(config: AblationConfig, tasks: List[Task], seed: int) -> Dict[str, float]:
    agent = SyntheticPXOLAgent(config, seed * 1009 + sum(ord(c) for c in config.name))
    rows = []
    for task in tasks:
        r = agent.solve(task)
        rows.append((task, r))
        agent.observe(task, r)

    acc = statistics.mean(r["correct"] for _, r in rows)
    ops = statistics.mean(r["operations"] for _, r in rows)
    dim = statistics.mean(r["dimensional_load"] for _, r in rows)
    eff = acc / (ops * dim)
    first = [r for t, r in rows if not t.repeated]
    repeat = [r for t, r in rows if t.repeated]
    first_ops = statistics.mean(r["operations"] for r in first)
    repeat_ops = statistics.mean(r["operations"] for r in repeat) if repeat else first_ops

    return {
        "accuracy": acc,
        "operations": ops,
        "dimensional_load": dim,
        "cognitive_efficiency": eff,
        "compression_gain": (first_ops - repeat_ops) / first_ops if first_ops else 0.0,
    }


def ci95(values):
    n = len(values)
    mean = statistics.mean(values)
    if n < 2:
        return mean, 0.0, mean, mean
    sd = statistics.stdev(values)
    half = 1.96 * sd / math.sqrt(n)
    return mean, sd, mean - half, mean + half


def status_from_ci(low, high, practical):
    if low > practical:
        return "PASS"
    if high < -practical:
        return "FAIL"
    return "WATCH"


def main():
    seeds = list(range(30))
    per_seed = []

    for seed in seeds:
        tasks = make_tasks(seed)
        metrics_by_cfg = {cfg.name: evaluate(cfg, tasks, seed) for cfg in CONFIGS}
        row = {"seed": seed}
        full = metrics_by_cfg["FULL"]

        for component, ablation_name in ABLATION_MAP.items():
            abl = metrics_by_cfg[ablation_name]
            row[f"DELTA__{component}__accuracy"] = full["accuracy"] - abl["accuracy"]
            row[f"DELTA__{component}__efficiency"] = (
                full["cognitive_efficiency"] / abl["cognitive_efficiency"] - 1.0
            )

        base = metrics_by_cfg["BASELINE"]
        row["DELTA__FULL_vs_BASELINE__accuracy"] = full["accuracy"] - base["accuracy"]
        row["DELTA__FULL_vs_BASELINE__efficiency"] = (
            full["cognitive_efficiency"] / base["cognitive_efficiency"] - 1.0
        )
        per_seed.append(row)

    out = Path("validation_outputs_v0_2")
    out.mkdir(exist_ok=True)

    with (out / "replicated_seed_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(per_seed[0].keys()))
        writer.writeheader()
        writer.writerows(per_seed)

    stat_rows = []
    for key in [k for k in per_seed[0] if k.startswith("DELTA__")]:
        vals = [r[key] for r in per_seed]
        mean, sd, low, high = ci95(vals)
        practical = 0.01 if key.endswith("__accuracy") else 0.02
        stat_rows.append({
            "comparison": key,
            "mean": mean,
            "sd": sd,
            "ci95_low": low,
            "ci95_high": high,
            "status": status_from_ci(low, high, practical),
        })

    with (out / "statistical_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(stat_rows[0].keys()))
        writer.writeheader()
        writer.writerows(stat_rows)

    with (out / "statistical_summary.json").open("w", encoding="utf-8") as f:
        json.dump(stat_rows, f, indent=2)


if __name__ == "__main__":
    main()
