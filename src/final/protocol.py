"""Shared evaluation protocol for the three final models (docs/RENCANA-ML-COLAB.md section 5).

For every (feature set, validation scheme, model):
    outer loop   : leave-one-group-out (experiment / donor / figure / plate) or StratifiedKFold(k) per cell (leakage comparison)
    inner loop   : GridSearchCV on the training part only, scoring balanced accuracy;
                   StratifiedGroupKFold(3) when the training part has >= 3 groups, else StratifiedKFold(3)
    prediction   : argmax of predicted class probabilities (SVM is refitted with probability=True after the search)
Outputs per evaluation: per-fold metrics, mean +- sd over folds, pooled metrics over all out-of-fold predictions,
bootstrap 95% CI of the pooled metrics, permutation feature importance on the outer test folds.
A separate label-permutation test (labels shuffled within groups) checks that the score is not chance.
"""
from __future__ import annotations

import time
from collections import Counter

import numpy as np
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, average_precision_score, balanced_accuracy_score, confusion_matrix,
                             f1_score, matthews_corrcoef, roc_auc_score)
from sklearn.model_selection import GridSearchCV, LeaveOneGroupOut, StratifiedGroupKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

CI_METRICS = ["balanced_accuracy", "mcc", "roc_auc", "sensitivity", "specificity"]


def build_models(seed: int) -> dict:
    """Same model families and grids as the pilots (src/wo14_kfold_heidata.models) so results stay comparable."""
    imp = ("imp", SimpleImputer(strategy="median"))
    return {
        "logreg": (Pipeline([imp, ("sc", StandardScaler()),
                             ("clf", LogisticRegression(class_weight="balanced", max_iter=5000))]),
                   {"clf__C": [0.01, 0.1, 1, 10]}),
        "rf": (Pipeline([imp, ("clf", RandomForestClassifier(n_estimators=200, class_weight="balanced",
                                                             random_state=seed, n_jobs=-1))]),
               {"clf__max_depth": [None, 5], "clf__min_samples_leaf": [1, 3, 5]}),
        "svm": (Pipeline([imp, ("sc", StandardScaler()),
                          ("clf", SVC(kernel="rbf", class_weight="balanced", random_state=seed))]),
                {"clf__C": [0.1, 1, 10], "clf__gamma": ["scale", 0.01, 0.1]}),
    }


def outer_splits(X, y, groups, scheme: str, seed: int) -> list:
    """scheme 'group' = leave-one-group-out on `groups`; 'kfoldK' = StratifiedKFold(K) on cells."""
    if scheme == "group":
        return list(LeaveOneGroupOut().split(X, y, groups))
    k = int(scheme.replace("kfold", ""))
    return list(StratifiedKFold(k, shuffle=True, random_state=seed).split(X, y))


def stratified_subsample(idx: np.ndarray, y: np.ndarray, max_n: int | None, seed: int) -> np.ndarray:
    """Class-proportional random subsample of indices (used to keep RBF-SVM training tractable)."""
    if not max_n or len(idx) <= max_n:
        return idx
    rng = np.random.default_rng(seed)
    keep = []
    for c in np.unique(y[idx]):
        ic = idx[y[idx] == c]
        keep.append(rng.choice(ic, max(1, int(round(max_n * len(ic) / len(idx)))), replace=False))
    return np.sort(np.concatenate(keep))


def _inner_cv(groups_tr, seed):
    if groups_tr is not None and len(set(groups_tr)) >= 3:
        return StratifiedGroupKFold(3, shuffle=True, random_state=seed), groups_tr
    return StratifiedKFold(3, shuffle=True, random_state=seed), None


def _proba_full(est, X, K):
    """Probabilities with one column per class 0..K-1 even if a class was missing in training."""
    P = est.predict_proba(X)
    if P.shape[1] == K:
        return P
    full = np.zeros((len(X), K))
    full[:, est.classes_.astype(int)] = P
    return full


def metric_set(y, pred, P, K) -> dict:
    cm = confusion_matrix(y, pred, labels=list(range(K)))
    tot = cm.sum()
    row, col, diag = cm.sum(1), cm.sum(0), np.diag(cm)
    sens = [float(diag[c] / row[c]) if row[c] else None for c in range(K)]
    spec = [float((tot - row[c] - col[c] + diag[c]) / (tot - row[c])) if (tot - row[c]) else None for c in range(K)]
    present = len(np.unique(y)) == K
    out = {"n": int(len(y)), "accuracy": float(accuracy_score(y, pred)),
           "balanced_accuracy": float(balanced_accuracy_score(y, pred)) if len(np.unique(y)) > 1 else None,
           "mcc": float(matthews_corrcoef(y, pred)) if len(np.unique(y)) > 1 else None,
           "sensitivity_per_class": sens, "specificity_per_class": spec, "cm": cm.tolist()}
    if K == 2:
        tn, fp, fn, tp = cm.ravel()
        out.update(sensitivity=sens[1], specificity=sens[0],
                   precision=float(tp / (tp + fp)) if (tp + fp) else None,
                   npv=float(tn / (tn + fn)) if (tn + fn) else None,
                   f1=float(f1_score(y, pred, zero_division=0)),
                   roc_auc=float(roc_auc_score(y, P[:, 1])) if present else None,
                   pr_auc=float(average_precision_score(y, P[:, 1])) if present else None)
    else:
        out.update(sensitivity=None, specificity=None,
                   roc_auc=float(roc_auc_score(y, P, multi_class="ovr", average="macro", labels=list(range(K))))
                   if present else None)
    return out


def bootstrap_ci(y, pred, P, K, n_boot: int, seed: int) -> dict:
    """Percentile 95% CI of pooled metrics, resampling cells with replacement."""
    if not n_boot:
        return {}
    rng = np.random.default_rng(seed)
    vals = {m: [] for m in CI_METRICS}
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        if len(np.unique(y[i])) < K:
            continue
        m = metric_set(y[i], pred[i], P[i], K)
        for k in CI_METRICS:
            if m.get(k) is not None:
                vals[k].append(m[k])
    return {k: [round(float(np.percentile(v, 2.5)), 3), round(float(np.percentile(v, 97.5)), 3)]
            for k, v in vals.items() if v}


def _round(d):
    if isinstance(d, dict):
        return {k: _round(v) for k, v in d.items()}
    if isinstance(d, list):
        return [_round(v) for v in d]
    if isinstance(d, float):
        return round(d, 3)
    return d


def evaluate(name, model, grid, X, y, groups, splits, K, *, seed, svm_max_train=None, n_boot=0,
             importance=None, feature_names=None, log=print) -> dict:
    """Nested evaluation of one model; returns metrics + out-of-fold arrays (keys starting with '_')."""
    t0 = time.time()
    n = len(y)
    oof_pred, oof_P = np.full(n, -1), np.full((n, K), np.nan)
    folds, params, imps = [], [], []
    for f, (tr, te) in enumerate(splits):
        tr_fit = stratified_subsample(tr, y, svm_max_train, seed + f) if name == "svm" else tr
        cv, g = _inner_cv(groups[tr_fit] if groups is not None else None, seed)
        search = GridSearchCV(clone(model), grid, scoring="balanced_accuracy", cv=cv, error_score=np.nan)
        search.fit(X[tr_fit], y[tr_fit], groups=g)
        best = search.best_estimator_
        if name == "svm":
            best = clone(best).set_params(clf__probability=True).fit(X[tr_fit], y[tr_fit])
        P = _proba_full(best, X[te], K)
        pred = P.argmax(1)
        oof_P[te], oof_pred[te] = P, pred
        m = metric_set(y[te], pred, P, K)
        m.update(n_train=int(len(tr_fit)), test_group=str(groups[te][0]) if groups is not None and
                 len(set(groups[te])) == 1 else None, best_params=search.best_params_)
        folds.append(m)
        params.append(tuple(sorted(search.best_params_.items(), key=lambda kv: kv[0])))
        if importance:
            sub = stratified_subsample(te, y, importance.get("max_test"), seed + f)
            pi = permutation_importance(best, X[sub], y[sub], scoring="balanced_accuracy",
                                        n_repeats=importance.get("n_repeats", 10), random_state=seed)
            imps.append(pi.importances_mean)
        log(f"      fold {f + 1}/{len(splits)} bAcc={m['balanced_accuracy']} AUC={m['roc_auc']} "
            f"params={search.best_params_}")
    tested = np.concatenate([te for _, te in splits])
    yt, pt, Pt = y[tested], oof_pred[tested], oof_P[tested]
    scal = ["accuracy", "balanced_accuracy", "mcc", "roc_auc", "sensitivity", "specificity"]
    mean_sd = {}
    for k in scal:
        v = [fm[k] for fm in folds if fm.get(k) is not None]
        mean_sd[k] = {"mean": float(np.mean(v)) if v else None, "sd": float(np.std(v, ddof=1)) if len(v) > 1 else None}
    res = {"model": name, "n_folds": len(splits), "per_fold_mean_sd": mean_sd, "pooled": metric_set(yt, pt, Pt, K),
           "ci95_pooled": bootstrap_ci(yt, pt, Pt, K, n_boot, seed), "folds": folds,
           "most_common_params": dict(Counter(params).most_common(1)[0][0]), "seconds": round(time.time() - t0, 1)}
    if imps:
        a = np.vstack(imps)
        res["importance"] = {fn: {"mean": float(a[:, j].mean()), "sd": float(a[:, j].std(ddof=1)) if len(a) > 1 else None}
                             for j, fn in enumerate(feature_names)}
    res = _round(res)
    res.update(_tested=tested, _pred=pt, _P=Pt, _y=yt)
    return res


def permutation_test(model, params, X, y, groups, splits, *, n_perm, seed, svm_max_train=None, is_svm=False,
                     log=print) -> dict:
    """Pooled balanced accuracy with fixed hyperparameters vs labels shuffled within each group."""
    est = clone(model).set_params(**params)
    rng = np.random.default_rng(seed)

    def score(yy):
        pred = np.full(len(yy), -1)
        for f, (tr, te) in enumerate(splits):
            trf = stratified_subsample(tr, yy, svm_max_train, seed + f) if is_svm else tr
            pred[te] = clone(est).fit(X[trf], yy[trf]).predict(X[te])
        t = np.concatenate([te for _, te in splits])
        return balanced_accuracy_score(yy[t], pred[t])

    t0 = time.time()
    obs = score(y)
    null = []
    for b in range(n_perm):
        yp = y.copy()
        for g in np.unique(groups):
            i = np.where(groups == g)[0]
            yp[i] = rng.permutation(y[i])
        null.append(score(yp))
        if (b + 1) % 10 == 0:
            log(f"      permutation {b + 1}/{n_perm}")
    null = np.array(null)
    return {"params": params, "observed_balanced_accuracy": round(float(obs), 3),
            "null_mean": round(float(null.mean()), 3), "null_p95": round(float(np.percentile(null, 95)), 3),
            "n_perm": n_perm, "p_value": round(float((1 + (null >= obs).sum()) / (1 + n_perm)), 4),
            "seconds": round(time.time() - t0, 1)}
