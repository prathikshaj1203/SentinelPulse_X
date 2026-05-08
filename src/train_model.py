"""Train two scikit-learn models from a CSV dataset:

  1. Failure-probability model  (binary classifier: failure vs. healthy)
  2. Failure-category model     (multiclass classifier: which failure)

Reads:  datasets/predictive_maintenance.csv  (or any CSV passed via --csv)
Writes: models/rf_failure_prob.joblib
        models/rf_failure_class.joblib
        models/model_meta.json

Expected CSV columns (defaults — override via --features / --label):
  vibration, temperature, noise, current, rpm, pressure, label

`label` may be either:
  - a class string (e.g. "Healthy", "Bearing Wear")  → "Healthy" is treated as no-failure
  - or 0/1                                            → 1 = failure
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CSV = ROOT / "datasets" / "predictive_maintenance.csv"
MODELS_DIR = ROOT / "models"
PROB_PATH = MODELS_DIR / "rf_failure_prob.joblib"
CLASS_PATH = MODELS_DIR / "rf_failure_class.joblib"
META_PATH = MODELS_DIR / "model_meta.json"
LEGACY_PATH = MODELS_DIR / "rf_model.joblib"     # kept for back-compat

DEFAULT_FEATURES = ["vibration", "temperature", "noise", "current", "rpm", "pressure"]
HEALTHY_LABELS = {"healthy", "ok", "normal", "0", 0}


# ---------- Synthetic dataset (used if no CSV present) ----------
def _generate_synthetic(n: int = 4000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    classes = ["Healthy", "Bearing Wear", "Overheating", "Misalignment", "Valve/Leak"]
    rows = []
    for _ in range(n):
        cls = rng.choice(classes, p=[0.45, 0.15, 0.15, 0.12, 0.13])
        if cls == "Healthy":
            row = [rng.normal(2, .5), rng.normal(55, 5), rng.normal(60, 5),
                   rng.normal(10, 1), rng.normal(1480, 20), rng.normal(6, .4)]
        elif cls == "Bearing Wear":
            row = [rng.normal(7, 1.2), rng.normal(70, 6), rng.normal(85, 6),
                   rng.normal(12, 1.5), rng.normal(1450, 30), rng.normal(5.8, .4)]
        elif cls == "Overheating":
            row = [rng.normal(3, .8), rng.normal(95, 6), rng.normal(65, 5),
                   rng.normal(14, 1.5), rng.normal(1400, 40), rng.normal(5.5, .4)]
        elif cls == "Misalignment":
            row = [rng.normal(6, 1), rng.normal(65, 5), rng.normal(75, 5),
                   rng.normal(11, 1), rng.normal(1430, 30), rng.normal(5.9, .4)]
        else:
            row = [rng.normal(3, .7), rng.normal(72, 6), rng.normal(70, 6),
                   rng.normal(13, 1.2), rng.normal(1460, 25), rng.normal(4.2, .5)]
        rows.append(row + [cls])
    return pd.DataFrame(rows, columns=DEFAULT_FEATURES + ["label"])


def _to_binary(series: pd.Series) -> pd.Series:
    """Convert any label column to 0 (healthy) / 1 (failure)."""
    def _is_fail(v) -> int:
        s = str(v).strip().lower()
        return 0 if s in {str(x) for x in HEALTHY_LABELS} else 1
    return series.apply(_is_fail).astype(int)


def load_dataset(csv_path: Path) -> pd.DataFrame:
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        print(f"[data] loaded {len(df)} rows from {csv_path}")
        return df
    print(f"[data] {csv_path} not found — generating synthetic dataset")
    df = _generate_synthetic()
    csv_path.parent.mkdir(exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"[data] wrote synthetic CSV -> {csv_path}")
    return df


def train(csv_path: Path, features: list[str], label_col: str) -> None:
    MODELS_DIR.mkdir(exist_ok=True)
    df = load_dataset(csv_path)

    missing = [c for c in features + [label_col] if c not in df.columns]
    if missing:
        raise SystemExit(f"CSV is missing required columns: {missing}")

    X = df[features].astype(float)
    y_class = df[label_col].astype(str)
    y_bin = _to_binary(df[label_col])

    # ---------- 1. Failure probability (binary) ----------
    Xtr, Xte, ytr, yte = train_test_split(X, y_bin, test_size=.2, random_state=42, stratify=y_bin)
    prob_model = RandomForestClassifier(n_estimators=250, max_depth=14,
                                        random_state=42, n_jobs=-1, class_weight="balanced")
    prob_model.fit(Xtr, ytr)
    p = prob_model.predict_proba(Xte)[:, 1]
    auc = roc_auc_score(yte, p) if yte.nunique() > 1 else float("nan")
    acc_p = prob_model.score(Xte, yte)
    print(f"\n[failure-prob] accuracy={acc_p:.3f}  ROC-AUC={auc:.3f}")
    print(classification_report(yte, prob_model.predict(Xte), target_names=["healthy", "failure"]))

    # ---------- 2. Failure category (multiclass) ----------
    fail_mask = y_bin == 1
    Xc, yc = X[fail_mask], y_class[fail_mask]
    if yc.nunique() < 2:
        print("[failure-class] not enough categories — skipping multiclass model")
        class_model = None
        acc_c = None
        classes_ = []
    else:
        Xtr, Xte, ytr, yte = train_test_split(Xc, yc, test_size=.2, random_state=42, stratify=yc)
        class_model = RandomForestClassifier(n_estimators=300, max_depth=16,
                                             random_state=42, n_jobs=-1)
        class_model.fit(Xtr, ytr)
        acc_c = class_model.score(Xte, yte)
        classes_ = sorted(class_model.classes_.tolist())
        print(f"\n[failure-class] accuracy={acc_c:.3f}")
        print(classification_report(yte, class_model.predict(Xte)))

    # ---------- Optional baseline (Decision Tree) for comparison ----------
    dt = DecisionTreeClassifier(max_depth=10, random_state=42).fit(X, y_bin)
    print(f"[baseline]    decision tree binary accuracy (in-sample): {dt.score(X, y_bin):.3f}")

    # ---------- Persist ----------
    joblib.dump(prob_model, PROB_PATH)
    if class_model is not None:
        joblib.dump(class_model, CLASS_PATH)
        # legacy alias used by older diagnostic_engine
        joblib.dump(class_model, LEGACY_PATH)

    META_PATH.write_text(json.dumps({
        "features": features,
        "label_column": label_col,
        "failure_prob_model": str(PROB_PATH.name),
        "failure_class_model": str(CLASS_PATH.name) if class_model else None,
        "classes": classes_,
        "metrics": {
            "failure_prob_accuracy": acc_p,
            "failure_prob_auc": auc,
            "failure_class_accuracy": acc_c,
        },
        "source_csv": str(csv_path),
    }, indent=2))
    print(f"\n[models] saved -> {PROB_PATH.name}, {CLASS_PATH.name if class_model else '(no class model)'}")
    print(f"[meta]   saved -> {META_PATH}")


def main() -> None:
    p = argparse.ArgumentParser(description="Train Sentinel Pulse failure models from a CSV.")
    p.add_argument("--csv", type=Path, default=DEFAULT_CSV, help="Path to training CSV.")
    p.add_argument("--features", nargs="+", default=DEFAULT_FEATURES, help="Feature column names.")
    p.add_argument("--label", default="label", help="Label column name.")
    args = p.parse_args()
    train(args.csv, args.features, args.label)


if __name__ == "__main__":
    main()
