"""
PXOL Real Engine Adapter
Validation harness v0.3

This adapter targets the executable PXOLModel in tpnandakumar/LLM-DEV.

It deliberately does NOT fake P5D[zD], VCG or DvD. Those capabilities must
be explicitly exposed by the engine before their ablation tests are enabled.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any
import json
import time


@dataclass
class EngineTelemetry:
    turn_id: str
    confidence: float
    guidance_kind: str
    guidance_strength: float
    selected_guide_id: str | None
    guide_conflict: bool
    pump_prime_count: int
    competence_stage: str | None
    learning_phase: str | None
    autonomy: float
    reflection_required: bool
    verification_required: bool
    latency_ms: float
    reactivated_atoms: int
    unresolved_conflicts: int


class PXOLRealEngineAdapter:
    """Thin validation adapter around the real PXOLModel API."""

    REQUIRED_NEW_INTERFACES = {
        "p5d_state": "P5D[zD] dimensional state/telemetry",
        "vector_guidance": "VCG higher-to-lower vector guidance telemetry",
        "vector_decision": "DvD decision telemetry",
    }

    def __init__(self, model: Any):
        self.model = model

    @classmethod
    def cold_start(cls, **kwargs):
        from pxol.model import PXOLModel
        return cls(PXOLModel.cold_start(**kwargs))

    @classmethod
    def pflox_backed(cls, package, **kwargs):
        from pxol.model import PXOLModel
        return cls(PXOLModel.pflox_backed(package, **kwargs))

    def observe(
        self,
        content: str,
        *,
        context: dict[str, object] | None = None,
        situation: dict[str, object] | None = None,
        ecology: dict[str, object] | None = None,
        confidence: float = 0.7,
    ):
        return self.model.observe(
            content,
            context=context,
            situation=situation,
            ecology=ecology,
            confidence=confidence,
        )

    def solve(
        self,
        query: str,
        *,
        context: dict[str, object] | None = None,
        situation: dict[str, object] | None = None,
        ecology: dict[str, object] | None = None,
    ):
        start = time.perf_counter()
        turn = self.model.respond(
            query,
            context=context,
            situation=situation,
            ecology_observation=ecology,
        )
        latency_ms = (time.perf_counter() - start) * 1000.0

        response = turn.response
        meaning = response.meaning

        telemetry = EngineTelemetry(
            turn_id=turn.turn_id,
            confidence=float(meaning.confidence),
            guidance_kind=str(getattr(turn.guidance_kind, "value", turn.guidance_kind)),
            guidance_strength=float(turn.guidance_strength),
            selected_guide_id=turn.selected_guide_id,
            guide_conflict=bool(turn.guide_conflict),
            pump_prime_count=len(turn.pump_prime_records),
            competence_stage=(
                str(getattr(turn.competence_stage, "value", turn.competence_stage))
                if turn.competence_stage is not None else None
            ),
            learning_phase=(
                str(getattr(turn.learning_phase, "value", turn.learning_phase))
                if turn.learning_phase is not None else None
            ),
            autonomy=float(turn.autonomy),
            reflection_required=bool(turn.reflection_required),
            verification_required=bool(turn.verification_required),
            latency_ms=latency_ms,
            reactivated_atoms=len(getattr(response, "reactivated_atoms", ()) or ()),
            unresolved_conflicts=len(getattr(meaning, "unresolved_conflicts", ()) or ()),
        )
        return turn, telemetry

    def positive_outcome(self, turn_id: str, note: str = "validation success"):
        return self.model.success(turn_id, note=note, source="validation")

    def negative_outcome(self, turn_id: str, note: str = "validation failure"):
        return self.model.failure(turn_id, note=note, source="validation")

    def neutral_or_unknown_outcome(self, turn_id: str):
        """
        Do not manufacture negative evidence.

        The current public API provides explicit success/failure methods.
        Until a neutral/unknown feedback constructor is confirmed, this adapter
        leaves the turn unapplied instead of converting absence of evidence
        into failure.
        """
        return None

    def capability_report(self) -> dict[str, object]:
        report = {
            "real_engine": type(self.model).__name__,
            "implemented": {
                "respond": hasattr(self.model, "respond"),
                "feedback": hasattr(self.model, "feedback"),
                "success": hasattr(self.model, "success"),
                "failure": hasattr(self.model, "failure"),
                "pump_prime": hasattr(self.model, "pump_prime"),
                "multi_guide": hasattr(self.model, "multi_guide"),
                "memory_revision": hasattr(self.model, "memory_revision"),
                "strategy": hasattr(self.model, "strategy"),
                "self_model": hasattr(self.model, "self_model"),
            },
            "new_architecture_interfaces": {},
        }
        for attr, description in self.REQUIRED_NEW_INTERFACES.items():
            report["new_architecture_interfaces"][attr] = {
                "present": hasattr(self.model, attr),
                "description": description,
            }
        return report


def smoke_test() -> dict[str, object]:
    adapter = PXOLRealEngineAdapter.cold_start()
    adapter.observe(
        "A validated observation can be learned locally after real outcome feedback.",
        context={"domain": "validation"},
        ecology={"source": "smoke-test"},
        confidence=0.85,
    )
    turn, telemetry = adapter.solve(
        "What can be learned after validated outcome feedback?",
        context={"domain": "validation"},
        ecology={"source": "smoke-test"},
    )
    adapter.positive_outcome(turn.turn_id)

    return {
        "capabilities": adapter.capability_report(),
        "telemetry": asdict(telemetry),
        "turn_learned_after_feedback": bool(adapter.model.turns[turn.turn_id].learned),
    }


if __name__ == "__main__":
    print(json.dumps(smoke_test(), indent=2))
