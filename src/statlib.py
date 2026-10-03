"""Minimal dependency-free stats helpers (no scipy available in this env)."""
import math
import numpy as np


# ---------------------------------------------------------------- distributions
def _norm_cdf(z):
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _betacf(a, b, x, itmax=300, eps=3e-16):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < 1e-300:
        d = 1e-300
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-300:
            d = 1e-300
        c = 1.0 + aa / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-300:
            d = 1e-300
        c = 1.0 + aa / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def betainc(a, b, x):
    """Regularized incomplete beta I_x(a,b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = (math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
             + a * math.log(x) + b * math.log1p(-x))
    front = math.exp(lbeta)
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
        + b * math.log1p(-x) + a * math.log(x)) * _betacf(b, a, 1.0 - x) / b


def t_sf2(t, df):
    """Two-sided p-value for Student's t."""
    if df <= 0 or not np.isfinite(t):
        return float("nan")
    return betainc(df / 2.0, 0.5, df / (df + t * t))


def norm_sf2(z):
    return 2.0 * (1.0 - _norm_cdf(abs(z)))


# ---------------------------------------------------------------- correlations
def rankdata(a):
    a = np.asarray(a, float)
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), float)
    ranks[order] = np.arange(1, len(a) + 1)
    # average ties
    sa = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sa[j + 1] == sa[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = ranks[order[i:j + 1]].mean()
        i = j + 1
    return ranks


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    n = len(x)
    if n < 4 or x.std() == 0 or y.std() == 0:
        return float("nan"), float("nan"), n
    r = float(np.corrcoef(x, y)[0, 1])
    r = min(max(r, -0.999999), 0.999999)
    t = r * math.sqrt((n - 2) / (1 - r * r))
    return r, t_sf2(t, n - 2), n


def spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    m = np.isfinite(x) & np.isfinite(y)
    x, y = x[m], y[m]
    if len(x) < 4:
        return float("nan"), float("nan"), len(x)
    return pearson(rankdata(x), rankdata(y))


def fisher_z(r):
    r = np.clip(np.asarray(r, float), -0.999999, 0.999999)
    return np.arctanh(r)


def ttest_1samp(a, popmean=0.0):
    a = np.asarray(a, float)
    a = a[np.isfinite(a)]
    n = len(a)
    if n < 3:
        return float("nan"), float("nan"), n
    sd = a.std(ddof=1)
    if sd == 0:
        return float("nan"), float("nan"), n
    t = (a.mean() - popmean) / (sd / math.sqrt(n))
    return float(t), t_sf2(t, n - 1), n


def mannwhitney(x, y):
    """Two-sided Mann-Whitney U with normal approximation + tie correction."""
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    y = np.asarray(y, float); y = y[np.isfinite(y)]
    n1, n2 = len(x), len(y)
    if n1 < 3 or n2 < 3:
        return float("nan"), float("nan")
    allv = np.concatenate([x, y])
    r = rankdata(allv)
    u1 = r[:n1].sum() - n1 * (n1 + 1) / 2.0
    mu = n1 * n2 / 2.0
    n = n1 + n2
    _, counts = np.unique(allv, return_counts=True)
    tie = (counts ** 3 - counts).sum()
    sd = math.sqrt(n1 * n2 / 12.0 * ((n + 1) - tie / (n * (n - 1))))
    if sd == 0:
        return float("nan"), float("nan")
    z = (u1 - mu) / sd
    # rank-biserial effect size
    return 2 * u1 / (n1 * n2) - 1, norm_sf2(z)


def bh_fdr(p):
    """Benjamini-Hochberg adjusted p-values."""
    p = np.asarray(p, float)
    ok = np.isfinite(p)
    out = np.full(len(p), np.nan)
    pv = p[ok]
    n = len(pv)
    if n == 0:
        return out
    order = np.argsort(pv)
    adj = np.empty(n)
    prev = 1.0
    for i in range(n - 1, -1, -1):
        prev = min(prev, pv[order[i]] * n / (i + 1))
        adj[order[i]] = prev
    out[ok] = np.clip(adj, 0, 1)
    return out


# ---------------------------------------------------------------- modelling
def ridge_fit(X, y, lam):
    Xb = np.column_stack([np.ones(len(X)), X])
    p = Xb.shape[1]
    I = np.eye(p); I[0, 0] = 0.0
    return np.linalg.solve(Xb.T @ Xb + lam * I, Xb.T @ y)


def ridge_pred(beta, X):
    return np.column_stack([np.ones(len(X)), X]) @ beta
