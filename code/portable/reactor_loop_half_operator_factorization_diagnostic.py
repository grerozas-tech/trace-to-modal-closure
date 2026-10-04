"""
Reconstructed Paper-IV half-channel operator factorization.

PROVENANCE
----------
API-compatible reconstruction from the frozen conversation, the exact
confirmatory preregistration, archived result schema, and the reconstructed
full-loop module. It is not claimed to be byte-identical to the transient
original runner.
"""

from __future__ import annotations
from pathlib import Path
import importlib.util
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CANDIDATES = [HERE / "reactor_full_loop_operator_gain_diagnostic.py",
              Path("/mnt/data/reactor_full_loop_operator_gain_diagnostic.py")]
for p in CANDIDATES:
    if p.exists():
        spec = importlib.util.spec_from_file_location("loopdiag", p)
        loopdiag = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(loopdiag)
        break
else:
    raise FileNotFoundError("reactor_full_loop_operator_gain_diagnostic.py not found")

HALF = loopdiag.HALF
EPS = loopdiag.EPS
TUPLES = loopdiag.TUPLES


def estimate_A_B(control, noise_w, noise_r, cfg, shared, target_v,
                 epsilon=EPS):
    """Estimate the two isolated half-channel local operators.

    A : x_t -> m_(t+24), shape (8,32)
    B : m_(t+24) -> x_(t+48), shape (32,8)

    Returns (A, B, ctrl_w, ctrl_r).
    """
    ctrl_w = loopdiag.rollout(control, noise_w, cfg, shared, target_v,
                              False, False, phi=0.0)
    ctrl_r = loopdiag.rollout(ctrl_w, noise_r, cfg, shared, target_v,
                              False, False, phi=0.0)

    A = np.zeros((cfg.memory_dim, cfg.N), dtype=float)
    for j in range(cfg.N):
        d = np.zeros(cfg.N); d[j] = epsilon
        p = loopdiag.clone(control); p["x"] = p["x"] + d
        m = loopdiag.clone(control); m["x"] = m["x"] - d
        pw = loopdiag.rollout(p, noise_w, cfg, shared, target_v,
                              False, False, phi=0.0)
        mw = loopdiag.rollout(m, noise_w, cfg, shared, target_v,
                              False, False, phi=0.0)
        A[:, j] = (pw["m"] - mw["m"]) / (2.0*epsilon)

    B = np.zeros((cfg.N, cfg.memory_dim), dtype=float)
    for j in range(cfg.memory_dim):
        d = np.zeros(cfg.memory_dim); d[j] = epsilon
        p = loopdiag.clone(ctrl_w); p["m"] = p["m"] + d
        m = loopdiag.clone(ctrl_w); m["m"] = m["m"] - d
        pr = loopdiag.rollout(p, noise_r, cfg, shared, target_v,
                              False, False, phi=0.0)
        mr = loopdiag.rollout(m, noise_r, cfg, shared, target_v,
                              False, False, phi=0.0)
        B[:, j] = (pr["x"] - mr["x"]) / (2.0*epsilon)

    return A, B, ctrl_w, ctrl_r


def _abs_cos(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(abs(a @ b)/(np.linalg.norm(a)*np.linalg.norm(b) + 1e-15))


def stage_metrics(control, noise_w, noise_r, cfg, shared, target_v):
    A, B, _, _ = estimate_A_B(control, noise_w, noise_r, cfg, shared, target_v)
    T = B @ A

    Ua, Sa, Vta = np.linalg.svd(A, full_matrices=False)
    Ub, Sb, Vtb = np.linalg.svd(B, full_matrices=False)
    Ut, St, Vtt = np.linalg.svd(T, full_matrices=False)

    perfect = float(Sa[0]*Sb[0])
    efficiency = float(St[0]/(perfect + 1e-15))
    # A's top output mode and B's top input mode both live in memory space.
    alignment = _abs_cos(Ua[:,0], Vtb[0])

    return {
        "sigmaA": float(Sa[0]),
        "sigmaB": float(Sb[0]),
        "perfect_interface_bound": perfect,
        "sigmaT": float(St[0]),
        "interface_efficiency": efficiency,
        "top_mode_alignment": alignment,
        "sigmaA2": float(Sa[1]),
        "sigmaB2": float(Sb[1]),
        "sigmaT2": float(St[1]),
    }


def audit(seed: int):
    Adeg, Bdeg, Cdeg = TUPLES[seed % 4]
    Aang, Bang, Cang = np.deg2rad([Adeg, Bdeg, Cdeg])
    cfg, shared, target, orig = loopdiag.origin(seed)
    start = loopdiag.make_history(seed, [Aang, Bang, None], cfg, shared, target, orig)
    intact0, ctrl0 = loopdiag.build_turn(seed, start, Cang, cfg, shared, target)

    g0 = stage_metrics(ctrl0,
                       loopdiag.nz(seed, HALF, 3001),
                       loopdiag.nz(seed, HALF, 3002),
                       cfg, shared, target)

    nw = loopdiag.nz(seed, HALF, 3003)
    nr = loopdiag.nz(seed, HALF, 3004)
    intact1 = loopdiag.rollout(loopdiag.rollout(intact0, nw, cfg, shared, target, False, False),
                               nr, cfg, shared, target, False, False)
    ctrl1 = loopdiag.rollout(loopdiag.rollout(ctrl0, nw, cfg, shared, target, False, False),
                             nr, cfg, shared, target, False, False)

    g1 = stage_metrics(ctrl1,
                       loopdiag.nz(seed, HALF, 3005),
                       loopdiag.nz(seed, HALF, 3006),
                       cfg, shared, target)

    row = {"seed": seed}
    for prefix, vals in (("G0",g0),("G1",g1)):
        for k,v in vals.items():
            row[f"{prefix}_{k}"] = v
    row.update({
        "G0_geometry_loss_fraction": 1.0-g0["interface_efficiency"],
        "G1_geometry_loss_fraction": 1.0-g1["interface_efficiency"],
        "A_deg": Adeg, "B_deg": Bdeg, "C_deg": Cdeg,
        "G0_sigmaB_over_sigmaA": g0["sigmaB"]/(g0["sigmaA"]+1e-15),
        "G1_sigmaB_over_sigmaA": g1["sigmaB"]/(g1["sigmaA"]+1e-15),
    })
    return row


def run(seeds):
    return pd.DataFrame([audit(int(s)) for s in seeds])


if __name__ == "__main__":
    df = run(range(153000, 153008))
    cols = ["seed","G0_sigmaA","G0_sigmaB","G0_sigmaT","G0_interface_efficiency",
            "G1_sigmaA","G1_sigmaB","G1_sigmaT","G1_interface_efficiency"]
    print(df[cols].to_string(index=False))
