
import argparse, json, pickle
from pathlib import Path
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, brier_score_loss
import matplotlib.pyplot as plt

from eda import cramers_v_matrix, num_corr, linear_probability_model

def main(data_path: str, out_dir: str):
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)
    df = df.dropna(subset=["Churn"]).copy()
    df["target"] = (df["Churn"] == "Evasão").astype(int)

    # -------- EDA: numeric correlations --------
    X_all = df.drop(columns=["Churn","target","customerID"])
    cat_cols = [c for c in X_all.columns if X_all[c].dtype == "object"]
    num_cols = [c for c in X_all.columns if c not in cat_cols]

    if len(num_cols) >= 2:
        corr = num_corr(df, num_cols)
        corr.to_csv(out/"corr_numeric.csv")
        plt.figure(figsize=(7,6))
        plt.imshow(corr, aspect='auto')
        plt.xticks(range(len(num_cols)), num_cols, rotation=90, fontsize=8)
        plt.yticks(range(len(num_cols)), num_cols, fontsize=8)
        plt.colorbar()
        plt.title("Correlação (Pearson) - Numéricas")
        plt.tight_layout()
        plt.savefig(out/"corr_numeric.png")
        plt.close()

    # -------- EDA: Cramer's V for categoricals --------
    if len(cat_cols) >= 2:
        cvm = cramers_v_matrix(df, cat_cols)
        cvm.to_csv(out/"cramers_v.csv")
        plt.figure(figsize=(7,6))
        plt.imshow(cvm.values, aspect='auto', vmin=0, vmax=1)
        plt.xticks(range(len(cat_cols)), cat_cols, rotation=90, fontsize=8)
        plt.yticks(range(len(cat_cols)), cat_cols, fontsize=8)
        plt.colorbar()
        plt.title("Associação categórica (Cramer's V)")
        plt.tight_layout()
        plt.savefig(out/"cramers_v.png")
        plt.close()

    # -------- EDA: Linear Probability Model (OLS) for interpretability --------
    # pick a compact feature set: all numerics + up to 6 categorical cols (to keep X small)
    lpm_features = num_cols + cat_cols[:6]
    try:
        model_lpm, lpm_cols = linear_probability_model(df.assign(y=df["target"]), "y", lpm_features)
        (out/"lpm_summary.txt").write_text(model_lpm.summary().as_text(), encoding="utf-8")
    except Exception as e:
        (out/"lpm_summary.txt").write_text(f"Falha ao ajustar LPM: {e}", encoding="utf-8")

    # -------- ML Pipeline --------
    X = X_all
    y = df["target"]

    numeric = Pipeline([("impute", SimpleImputer(strategy="median")),
                        ("scale", StandardScaler())])
    categoric = Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))])

    preprocess = ColumnTransformer([("num", numeric, num_cols),
                                    ("cat", categoric, cat_cols)])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe_lr = Pipeline([("prep", preprocess),
                        ("clf", LogisticRegression(max_iter=400, n_jobs=1))])
    pipe_rf = Pipeline([("prep", preprocess),
                        ("clf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=1))])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    auc_lr_cv = cross_val_score(pipe_lr, X_train, y_train, cv=cv, scoring="roc_auc").mean()
    auc_rf_cv = cross_val_score(pipe_rf, X_train, y_train, cv=cv, scoring="roc_auc").mean()

    pipe_lr.fit(X_train, y_train)
    pipe_rf.fit(X_train, y_train)

    proba_lr = pipe_lr.predict_proba(X_test)[:, 1]
    proba_rf = pipe_rf.predict_proba(X_test)[:, 1]
    auc_lr = roc_auc_score(y_test, proba_lr)
    auc_rf = roc_auc_score(y_test, proba_rf)

    base_best_name = "LogisticRegression" if auc_lr >= auc_rf else "RandomForest"
    base_best_pipe = pipe_lr if base_best_name == "LogisticRegression" else pipe_rf
    base_best_proba = proba_lr if base_best_name == "LogisticRegression" else proba_rf
    base_best_auc = max(auc_lr, auc_rf)

    # -------- Calibration --------
    Xc, yc = X_train, y_train
    if len(Xc) > 2500:
        idx = np.random.RandomState(42).choice(Xc.index, size=2500, replace=False)
        Xc, yc = Xc.loc[idx], yc.loc[idx]
    cal_sig = CalibratedClassifierCV(base_best_pipe, method="sigmoid", cv=3)
    cal_iso = CalibratedClassifierCV(base_best_pipe, method="isotonic", cv=3)
    cal_sig.fit(Xc, yc)
    cal_iso.fit(Xc, yc)

    proba_sig = cal_sig.predict_proba(X_test)[:,1]
    proba_iso = cal_iso.predict_proba(X_test)[:,1]
    auc_sig = roc_auc_score(y_test, proba_sig)
    auc_iso = roc_auc_score(y_test, proba_iso)
    brier_base = brier_score_loss(y_test, base_best_proba)
    brier_sig  = brier_score_loss(y_test, proba_sig)
    brier_iso  = brier_score_loss(y_test, proba_iso)

    candidates = [
        ("raw", base_best_pipe, base_best_proba, base_best_auc, brier_base),
        ("sigmoid", cal_sig, proba_sig, auc_sig, brier_sig),
        ("isotonic", cal_iso, proba_iso, auc_iso, brier_iso),
    ]
    # choose highest AUC, tiebreaker lowest Brier
    candidates = sorted(candidates, key=lambda t: (t[3], -t[4]), reverse=True)
    calib_name, best_model, best_proba, best_auc, best_brier = candidates[0]

    with open(out/"model.pkl", "wb") as f:
        pickle.dump(best_model, f)

    # Save predictions holdout
    (pd.DataFrame({
        "y_true": y_test.values,
        "proba_raw": base_best_proba,
        "proba_sigmoid": proba_sig,
        "proba_isotonic": proba_iso
    })).to_csv(out/"holdout_predictions.csv", index=False)

    # Save metrics
    metrics = {
        "cv_roc_auc": {"LogisticRegression": float(auc_lr_cv), "RandomForest": float(auc_rf_cv)},
        "holdout_roc_auc": {"LogisticRegression": float(auc_lr), "RandomForest": float(auc_rf)},
        "selected_base_model": base_best_name,
        "calibration_choice": calib_name,
        "selected_auc": float(best_auc),
        "selected_brier": float(best_brier),
        "n_rows": int(df.shape[0]),
        "n_features": int(X.shape[1]),
        "cat_features": cat_cols,
        "num_features": num_cols
    }
    (out/"metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")

    # -------- Feature importance proxy (coef or RF importances) --------
    prep = base_best_pipe.named_steps["prep"]
    clf  = base_best_pipe.named_steps["clf"]
    prep.fit(X_train, y_train)
    cat_features = prep.named_transformers_["cat"].named_steps["onehot"].get_feature_names_out(cat_cols).tolist()
    feature_names = num_cols + cat_features

    if base_best_name == "RandomForest":
        importances = clf.feature_importances_
    else:
        importances = np.abs(clf.coef_[0])
        importances = importances / (importances.sum() + 1e-9)

    importances = importances[:len(feature_names)]
    imp = pd.DataFrame({"feature": feature_names, "importance": importances}).sort_values("importance", ascending=False)
    imp.to_csv(out/"feature_importance.csv", index=False)

    # Top20 barplot
    top = imp.head(20)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,6))
    plt.barh(top["feature"][::-1], top["importance"][::-1])
    plt.title("Top 20 Features (coef/importances proxy)")
    plt.tight_layout()
    plt.savefig(out/"shap_top20.png")
    plt.close()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--data", type=str, required=True)
    p.add_argument("--out", type=str, required=True)
    args = p.parse_args()
    main(args.data, args.out)
