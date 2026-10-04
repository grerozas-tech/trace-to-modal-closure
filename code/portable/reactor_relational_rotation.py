"""
Reconstructed Paper-IV relation scaffold.

PROVENANCE
----------
This file was reconstructed from the frozen research conversation and the
prospectively frozen causal-relation preregistration. It is intended as the
missing executable implementation of the Paper-IV 4-D relation R4(phi).
It is not claimed to be byte-identical to the original transient file.

The sign convention is fixed by the preregistered causal signature:
    y = -[s_post - As@s_pre - 0.25*e_post] / 0.40 ~= R4(phi) @ a
and
    phi_hat = atan2(sum planar_cross(a,y), sum dot(a,y)).
For this estimator to return +phi, each 2-D block must use the standard
counter-clockwise rotation [[cos,-sin],[sin,cos]].
"""

from __future__ import annotations
import numpy as np


def R2(phi: float) -> np.ndarray:
    """Standard counter-clockwise 2-D rotation."""
    c = float(np.cos(phi))
    s = float(np.sin(phi))
    return np.array([[c, -s], [s, c]], dtype=float)


def R4(phi: float) -> np.ndarray:
    """Shared 4-D block rotation used by the continuous relation branch.

    The same R2(phi) acts on body/action coordinates (0,1) and (2,3).
    """
    r = R2(phi)
    out = np.zeros((4, 4), dtype=float)
    out[:2, :2] = r
    out[2:, 2:] = r
    return out


def rotate_action(a: np.ndarray, phi: float) -> np.ndarray:
    """Apply the hidden causal relation to a 4-D action vector."""
    a = np.asarray(a, dtype=float)
    if a.shape != (4,):
        raise ValueError(f"expected action shape (4,), got {a.shape}")
    return R4(phi) @ a


def body_step(s: np.ndarray, e_post: np.ndarray, a: np.ndarray,
              As: np.ndarray, eta_body: np.ndarray, phi: float) -> np.ndarray:
    """Paper-IV body update for a fixed relation phi."""
    return As @ s - 0.40 * rotate_action(a, phi) + 0.25 * e_post + eta_body


def recover_relation_signature(a_seq: np.ndarray, y_seq: np.ndarray,
                               min_action_norm: float = 0.05) -> float:
    """Recover phi from action->consequence pairs using the preregistered signature.

    Parameters
    ----------
    a_seq, y_seq : arrays of shape (T,4)
        y should approximate R4(phi)@a.
    min_action_norm : float
        Samples below this action norm are ignored.
    """
    a_seq = np.asarray(a_seq, float)
    y_seq = np.asarray(y_seq, float)
    if a_seq.shape != y_seq.shape or a_seq.ndim != 2 or a_seq.shape[1] != 4:
        raise ValueError("a_seq and y_seq must both have shape (T,4)")

    dot_sum = 0.0
    cross_sum = 0.0
    used = 0
    for a, y in zip(a_seq, y_seq):
        if np.linalg.norm(a) < min_action_norm:
            continue
        for j in (0, 2):
            av = a[j:j+2]
            yv = y[j:j+2]
            dot_sum += float(av @ yv)
            cross_sum += float(av[0]*yv[1] - av[1]*yv[0])
        used += 1
    if used == 0:
        return float("nan")
    return float(np.arctan2(cross_sum, dot_sum))


if __name__ == "__main__":
    # Deterministic self-check of the sign convention.
    rng = np.random.default_rng(0)
    for deg in (-135, -90, -45, 0, 45, 90, 135, 180):
        phi = np.deg2rad(deg)
        a = rng.normal(size=(64, 4))
        y = np.array([R4(phi) @ ai for ai in a])
        phat = recover_relation_signature(a, y, min_action_norm=0.0)
        err = np.angle(np.exp(1j*(phat-phi)))
        if abs(err) > 1e-10:
            raise SystemExit(f"R4 self-check failed at {deg} deg: error={err}")
    print("R4 self-check: PASS")
