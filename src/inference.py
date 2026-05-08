"""Inference helpers for failure probability + failure category.

Loads the two models trained by `src/train_model.py` and exposes a single
`predict(rows)` API that accepts a dict, list of dicts, or DataFrame
(matching the feature columns in models/model_meta.json).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Mapping

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / "models"
META_PATH = MODELS_DIR / "model_meta.json"


class FailurePredictor:
    """Two-stage predictor: P(failure) + most-likely failure category."""

    def __init__(self) -> None:
        if not META_PATH.exists():
            raise FileNotFoundError(
                "Model metadata missing. Run: python src/train_model.py"
            )
        self.meta = json.loads(META_PATH.read_text())
        self.features: list[str] = self.meta["features"]

        prob_path = MODELS_DIR / self.meta["failure_prob_model"]
        self.prob_model = joblib.load(prob_path)

        self.class_model = None
        if self.meta.get("failure_class_model"):
            self.class_model = joblib.load(MODELS_DIR / self.meta["failure_class_model"])

    # ---------- Input handling ----------
    def _to_frame(self, rows) -> pd.DataFrame:
        if isinstance(rows, pd.DataFrame):
            df = rows.copy()
        elif isinstance(rows, Mapping):
            df = pd.DataFrame([rows])
        elif isinstance(rows, Iterable):
            df = pd.DataFrame(list(rows))
        else:
            raise TypeError(f"Unsupported input type: {type(rows)}")

        missing = [c for c in self.features if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required feature columns: {missing}")
        return df[self.features].astype(float)

    # ---------- Predict ----------
    def predict(self, rows) -> pd.DataFrame:
        """Return a DataFrame with: failure_probability, predicted_category, category_confidence."""
        X = self._to_frame(rows)
        p_fail = self.prob_model.predict_proba(X)[:, list(self.prob_model.classes_).index(1)] \
            if 1 in self.prob_model.classes_ else self.prob_model.predict_proba(X).max(axis=1)

        out = pd.DataFrame({"failure_probability": p_fail})

        if self.class_model is not None:
            cls_proba = self.class_model.predict_proba(X)
            top_idx = np.argmax(cls_proba, axis=1)
            out["predicted_category"] = [self.class_model.classes_[i] for i in top_idx]
            out["category_confidence"] = cls_proba[np.arange(len(X)), top_idx]
        else:
            out["predicted_category"] = "Unknown"
            out["category_confidence"] = 0.0

        out["health_score"] = (1 - out["failure_probability"]) * 100
        return out

    def predict_one(self, row: Mapping) -> dict:
        return self.predict(row).iloc[0].to_dict()


# Convenience CLI: `python src/inference.py datasets/predictive_maintenance.csv`
if __name__ == "__main__":
    import sys
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "datasets" / "predictive_maintenance.csv"
    df = pd.read_csv(src).head(5)
    pred = FailurePredictor().predict(df)
    print(pd.concat([df.reset_index(drop=True), pred], axis=1).to_string(index=False))
