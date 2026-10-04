"""
Reconstructed Paper-IV full-loop causal operator scaffold.

PROVENANCE
----------
API-compatible reconstruction from the frozen research transcript, recovered
preregistrations, downstream scripts, reactor_v012.py, and archived result
schemas. It is not claimed to be byte-identical to the original transient
runner. The core local operator construction was independently audited against
archived confirmatory tables (see validation report delivered with this file).

The isolated loop is:
    delta x --24 native steps--> delta m
            --isolate delta m-->
            --24 native steps--> delta x'

Central finite differences use epsilon=1e-4.
"""

from __future__ import annotations
import copy
from collections import deque
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BASE_CANDIDATES = [HERE / "reactor_v012.py", Path("/mnt/data/reactor_v012.py")]
ROT_CANDIDATES = [HERE / "reactor_relational_rotation.py", Path("/mnt/data/reactor_relational_rotation.py")]


def _load_module(name, candidates):
    for p in candidates:
        if p.exists():
            spec = importlib.util.spec_from_file_location(name, p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise FileNotFoundError(f"Could not find dependency {name}: {candidates}")


base = _load_module("reactor_v012", BASE_CANDIDATES)
rot = _load_module("reactor_relational_rotation", ROT_CANDIDATES)

HALF = 24
EPS = 1e-4
HISTORY_BLOCK = 24
ORIGIN_WARMUP = 160

TUPLES = [
    (-135.0, -45.0, 45.0),
    (-45.0, 45.0, 135.0),
    (45.0, 135.0, -135.0),
    (135.0, -135.0, -45.0),
]


def clone(st):
    """Deep-copy a reactor state while preserving deque semantics."""
    out = {}
    for k, v in st.items():
        if isinstance(v, np.ndarray):
            out[k] = v.copy()
        elif isinstance(v, deque):
            out[k] = deque(
                [x.copy() if isinstance(x, np.ndarray) else copy.deepcopy(x) for x in v],
                maxlen=v.maxlen,
            )
        else:
            out[k] = copy.deepcopy(v)
    return out


def zero_state(cfg):
    return {
        "s": np.zeros(cfg.body_dim),
        "e": np.zeros(cfg.body_dim),
        "x": np.zeros(cfg.N),
        "a": np.zeros(cfg.body_dim),
        "m": np.zeros(cfg.memory_dim),
        "theta": np.zeros(cfg.modules),
        "r": np.zeros(cfg.body_dim + cfg.context_dim),
        "K": np.zeros((cfg.context_dim, cfg.body_dim)),
        "b": np.full(cfg.context_dim, 0.5),
        "gh": deque(maxlen=5),
        "prev_u": np.zeros(cfg.body_dim + cfg.context_dim),
        # Historical scripts call this prev_z; it is the previous action-noise vector.
        "prev_z": np.zeros(cfg.body_dim),
        "prev_v": 1.0,
    }


def nz(seed: int, n: int, tag: int):
    """Deterministic matched noise block.

    The exact original seed mixer was not archived. This replacement keeps the
    defining property required by the experiments: branches sharing (seed,tag)
    receive exactly identical noise.
    """
    rng = np.random.default_rng(int(seed) * 1_000_003 + int(tag))
    return {
        "eta_env": rng.normal(0.0, 1.0, size=(n, 4)),
        "eta_body": rng.normal(0.0, 0.005, size=(n, 4)),
        "eta_context": rng.normal(0.0, 0.02, size=(n, 8)),
        "zeta": rng.normal(0.0, 0.02, size=(n, 4)),
    }


def rollout(st, noise, cfg, shared, target_v,
            credit_r=True, credit_theta=True, phi=0.0):
    """Evolve C4 under a fixed hidden action-body relation phi.

    credit_r=False suppresses the new DeltaV relevance term but retains decay.
    credit_theta=False suppresses only the C4 DeltaV*p credit term; the native
    homeostatic/decay terms remain active.
    """
    q = clone(st)
    n = len(noise["eta_env"])
    R = rot.R4(float(phi))

    for t in range(n):
        q["e"] = 0.95*q["e"] + 0.03*noise["eta_env"][t]
        c = shared["Se"] @ q["e"] + shared["Sa"] @ q["a"] + noise["eta_context"][t]
        u = np.r_[q["s"], c]
        vhat = base.viability(q["s"], q["a"], cfg)
        delta_v = vhat - q["prev_v"]

        if credit_r:
            q["r"] = base.relevance_update(q["r"], q["prev_u"], delta_v, cfg)
        else:
            q["r"] = cfg.rel_decay * q["r"]

        rr = np.abs(q["r"])
        if np.max(rr) > 1e-12:
            rr = rr / np.max(rr)
        u_eff = u * (1.0 + 0.5*rr)

        W = base.W_from_theta(shared, q["theta"])
        z = W @ q["x"] + shared["B"] @ u_eff + shared["M"] @ q["m"]

        q["K"] = base.boundary_update(q["K"], c, q["prev_z"], cfg)
        scores = np.linalg.norm(q["K"], axis=1)
        q["b"] = base.sigmoid(12.0*(scores - np.median(scores)))
        p = np.zeros(cfg.modules) if len(q["gh"]) == 0 else base.temporal_summary(q["gh"])
        z += shared["Jp"] @ p + shared["Jr"] @ q["r"] + shared["Jb"] @ q["b"]

        q["x"] = 0.75*q["x"] + 0.25*np.tanh(z)
        g = base.module_means(q["x"], cfg)
        q["gh"].append(g.copy())

        q["a"] = np.clip(
            np.tanh(0.8*q["s"]) + 0.25*np.tanh(g) + noise["zeta"][t],
            -1.0, 1.0,
        )
        q["s"] = (
            shared["As"] @ q["s"]
            - 0.40*(R @ q["a"])
            + 0.25*q["e"]
            + noise["eta_body"][t]
        )

        q["m"] = base.memory_update(q["m"], q["x"], shared, cfg)
        p2 = base.temporal_summary(q["gh"])
        q["theta"] = base.theta_update(
            q["theta"], q["x"], target_v, shared, cfg,
            delta_v=(delta_v if credit_theta else 0.0), p=p2, c4=True,
        )

        q["prev_u"] = u.copy()
        q["prev_z"] = noise["zeta"][t].copy()
        q["prev_v"] = float(vhat)

    return q


def origin(seed: int):
    """Construct the common neutral origin used by late Paper-IV operator audits."""
    cfg = base.Config(T=1200, intervention_t=800, warmup_end=400, baseline_end=800)
    shared = base.make_shared(seed, cfg)
    world = base.precompute_world(seed, shared, cfg)
    target = base.run_fixed_reference(shared, world, cfg)
    st = zero_state(cfg)
    st = rollout(st, nz(seed, ORIGIN_WARMUP, 1001), cfg, shared, target,
                 True, True, phi=0.0)
    return cfg, shared, target, st


def make_history(seed, sequence, cfg, shared, target_v, orig,
                 block_steps=HISTORY_BLOCK):
    """Apply a prospective relation history; None denotes neutral phi=0."""
    st = clone(orig)
    for j, phi in enumerate(sequence):
        p = 0.0 if phi is None else float(phi)
        st = rollout(st, nz(seed, block_steps, 1100+j), cfg, shared, target_v,
                     True, True, phi=p)
    return st


def build_turn(seed, start, phi, cfg, shared, target_v,
               steps=HISTORY_BLOCK):
    """Create an intact relation-C branch and its matched neutral control."""
    noise = nz(seed, steps, 1201)
    intact = rollout(start, noise, cfg, shared, target_v, True, True, phi=float(phi))
    control = rollout(start, noise, cfg, shared, target_v, True, True, phi=0.0)
    return intact, control


def loop_map(control, ctrl_w, ctrl_r, noise_w, noise_r,
             dx, cfg, shared, target_v):
    """Apply the isolated x->m->x loop to one x perturbation dx."""
    p = clone(control)
    p["x"] = p["x"] + np.asarray(dx, float)
    pw = rollout(p, noise_w, cfg, shared, target_v, False, False, phi=0.0)
    dm = pw["m"] - ctrl_w["m"]

    mp = clone(ctrl_w)
    mp["m"] = ctrl_w["m"] + dm
    pr = rollout(mp, noise_r, cfg, shared, target_v, False, False, phi=0.0)
    return pr["x"] - ctrl_r["x"]


def estimate_T(control, noise_w, noise_r, cfg, shared, target_v,
               epsilon=EPS):
    """Estimate the 32x32 isolated full-loop operator by central differences."""
    ctrl_w = rollout(control, noise_w, cfg, shared, target_v, False, False, phi=0.0)
    ctrl_r = rollout(ctrl_w, noise_r, cfg, shared, target_v, False, False, phi=0.0)

    T = np.zeros((cfg.N, cfg.N), dtype=float)
    for j in range(cfg.N):
        d = np.zeros(cfg.N)
        d[j] = epsilon
        yp = loop_map(control, ctrl_w, ctrl_r, noise_w, noise_r,
                      d, cfg, shared, target_v)
        ym = loop_map(control, ctrl_w, ctrl_r, noise_w, noise_r,
                      -d, cfg, shared, target_v)
        T[:, j] = (yp - ym) / (2.0*epsilon)
    return T, ctrl_w, ctrl_r


def _abs_cos(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(abs(a @ b)/(np.linalg.norm(a)*np.linalg.norm(b) + 1e-15))


def _stage_metrics(control, hist_dx, noise_w, noise_r,
                   cfg, shared, target_v):
    T, cw, cr = estimate_T(control, noise_w, noise_r, cfg, shared, target_v)
    U, S, Vt = np.linalg.svd(T, full_matrices=False)
    v1 = Vt[0]
    u1 = U[:, 0]

    hnorm = float(np.linalg.norm(hist_dx))
    hout = loop_map(control, cw, cr, noise_w, noise_r, hist_dx, cfg, shared, target_v)
    hgain = float(np.linalg.norm(hout)/(hnorm + 1e-15))
    # A descriptive projection gain; H4 uses norm gain, not this auxiliary column.
    hproj = float(abs(hout @ u1)/(hnorm + 1e-15))
    hcos = _abs_cos(hist_dx, v1)

    amp = hnorm if hnorm > 1e-10 else 1.0
    yp = loop_map(control, cw, cr, noise_w, noise_r, amp*v1, cfg, shared, target_v)
    ym = loop_map(control, cw, cr, noise_w, noise_r, -amp*v1, cfg, shared, target_v)
    gp = float(np.linalg.norm(yp)/(amp + 1e-15))
    gm = float(np.linalg.norm(ym)/(amp + 1e-15))

    return {
        "sigma1": float(S[0]),
        "sigma2": float(S[1]),
        "sigma3": float(S[2]),
        "hist_norm_gain": hgain,
        "hist_proj_gain": hproj,
        "hist_topv_abs_cos": hcos,
        "finite_top_gain_mean": 0.5*(gp+gm),
        "finite_top_gain_plus": gp,
        "finite_top_gain_minus": gm,
        "hist_norm": hnorm,
    }


def audit(seed: int):
    """Run a G0/G1 audit with the archived Paper-IV result schema."""
    Adeg, Bdeg, Cdeg = TUPLES[seed % 4]
    A, B, C = np.deg2rad([Adeg, Bdeg, Cdeg])
    cfg, shared, target, orig = origin(seed)
    start = make_history(seed, [A, B, None], cfg, shared, target, orig)
    intact0, ctrl0 = build_turn(seed, start, C, cfg, shared, target)

    g0 = _stage_metrics(
        ctrl0, intact0["x"]-ctrl0["x"],
        nz(seed, HALF, 2001), nz(seed, HALF, 2002), cfg, shared, target,
    )

    # Advance intact and matched control through one neutral 48-step generation.
    nw = nz(seed, HALF, 2003)
    nr = nz(seed, HALF, 2004)
    intact1 = rollout(rollout(intact0, nw, cfg, shared, target, False, False),
                      nr, cfg, shared, target, False, False)
    ctrl1 = rollout(rollout(ctrl0, nw, cfg, shared, target, False, False),
                    nr, cfg, shared, target, False, False)

    g1 = _stage_metrics(
        ctrl1, intact1["x"]-ctrl1["x"],
        nz(seed, HALF, 2005), nz(seed, HALF, 2006), cfg, shared, target,
    )

    row = {"seed": seed}
    for prefix, vals in (("G0", g0), ("G1", g1)):
        for k, v in vals.items():
            row[f"{prefix}_{k}"] = v
    row.update({
        "sigma1_change_G1_minus_G0": g1["sigma1"]-g0["sigma1"],
        "hist_gain_change_G1_minus_G0": g1["hist_norm_gain"]-g0["hist_norm_gain"],
        "A_deg": Adeg, "B_deg": Bdeg, "C_deg": Cdeg,
        "G0_opt_gap": g0["sigma1"]-g0["hist_norm_gain"],
        "G1_opt_gap": g1["sigma1"]-g1["hist_norm_gain"],
    })
    return row


def run(seeds):
    return pd.DataFrame([audit(int(s)) for s in seeds])


if __name__ == "__main__":
    df = run(range(151000, 151008))
    print(df[["seed","G0_sigma1","G1_sigma1","G0_finite_top_gain_mean","G1_finite_top_gain_mean"]].to_string(index=False))
