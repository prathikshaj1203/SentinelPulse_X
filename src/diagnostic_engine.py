"""Hybrid diagnostic engine: rule-based scoring + ML failure predictor."""
from __future__ import annotations

from src.inference import FailurePredictor


class DiagnosticEngine:
    def __init__(self) -> None:
        try:
            self.predictor: FailurePredictor | None = FailurePredictor()
        except FileNotFoundError:
            self.predictor = None

    # ---------- Rule engine ----------
    def rule_score(self, machine: dict, answers: dict[str, bool]) -> tuple[float, dict]:
        failure_scores: dict[str, float] = {f["name"]: 0.0 for f in machine["common_failures"]}
        total_weight = sum(q["weight"] for q in machine["questions"])
        triggered = 0.0
        for q in machine["questions"]:
            if answers.get(q["id"]):
                triggered += q["weight"]
                share = q["weight"] / max(len(q["maps_to"]), 1)
                for f in q["maps_to"]:
                    if f in failure_scores:
                        failure_scores[f] += share
        prob = triggered / total_weight if total_weight else 0.0
        return prob, failure_scores

    # ---------- ML engine ----------
    def ml_predict(self, sensors: dict) -> dict:
        if not self.predictor:
            return {"failure_probability": 0.0, "predicted_category": "Unknown",
                    "category_confidence": 0.0}
        return self.predictor.predict_one(sensors)

    # ---------- Fusion ----------
    def diagnose(self, machine: dict, answers: dict[str, bool], sensors: dict | None = None):
        rule_prob, per_failure = self.rule_score(machine, answers)
        top_failure = max(per_failure, key=per_failure.get) if per_failure else "Unknown"

        ml = self.ml_predict(sensors) if sensors else {
            "failure_probability": 0.0, "predicted_category": "N/A", "category_confidence": 0.0
        }

        # Combined risk: weighted average of rule probability and ML failure probability
        risk = 0.55 * rule_prob + 0.45 * ml["failure_probability"]
        health_score = max(0.0, min(100.0, (1 - risk) * 100))

        severity = next((f["severity"] for f in machine["common_failures"]
                         if f["name"] == top_failure), "Low")
        component = next((f["component"] for f in machine["common_failures"]
                          if f["name"] == top_failure), "Unknown")
        recommendations = machine.get("recommendations", {}).get(top_failure, [])

        return {
            "top_failure": top_failure,
            "component": component,
            "severity": severity,
            "rule_probability": rule_prob,
            "ml_class": ml["predicted_category"],
            "ml_confidence": ml["category_confidence"],
            "ml_failure_probability": ml["failure_probability"],
            "health_score": health_score,
            "per_failure_scores": per_failure,
            "recommendations": recommendations,
        }
