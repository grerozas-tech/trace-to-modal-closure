# PORTABLE_ADAPTATION: path-only adaptation of TRANSCRIPT_RECOVERED source.
import numpy as np, pandas as pd, importlib.util
from pathlib import Path

OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("loopop",OUT/"reactor_full_loop_operator_gain_diagnostic.py")
loopop=importlib.util.module_from_spec(spec); spec.loader.exec_module(loopop)

TUPLES=[
    (-135.,-45.,45.),
    (-45.,45.,135.),
    (45.,135.,-135.),
    (135.,-135.,-45.)
]

def abs_cos(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(abs(a@b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-15))

def audit(seed):
    Adeg,Bdeg,Cdeg=TUPLES[seed%4]
    A=np.deg2rad(Adeg); B=np.deg2rad(Bdeg); C=np.deg2rad(Cdeg)

    cfg,shared,target,orig=loopop.origin(seed)
    start=loopop.make_history(seed,[A,B,None],cfg,shared,target,orig)
    intact0,ctrl0=loopop.build_turn(seed,start,C,cfg,shared,target)

    # advance to G1
    nw0=loopop.nz(seed,loopop.HALF,3501)
    nr0=loopop.nz(seed,loopop.HALF,3502)
    iw=loopop.rollout(intact0,nw0,cfg,shared,target,False,False)
    intact1=loopop.rollout(iw,nr0,cfg,shared,target,False,False)
    cw=loopop.rollout(ctrl0,nw0,cfg,shared,target,False,False)
    ctrl1=loopop.rollout(cw,nr0,cfg,shared,target,False,False)

    aw=loopop.nz(seed,loopop.HALF,3503)
    ar=loopop.nz(seed,loopop.HALF,3504)
    T,cw1,cr1=loopop.estimate_T(ctrl1,aw,ar,cfg,shared,target)
    U,S,Vt=np.linalg.svd(T,full_matrices=False)
    u1=U[:,0]; v1=Vt[0]

    eig=np.linalg.eigvals(T)
    rho=float(np.max(np.abs(eig)))
    sigma1=float(S[0])
    nonnorm=float(np.linalg.norm(T.T@T-T@T.T,"fro")/(np.linalg.norm(T,"fro")**2+1e-15))

    amp=float(np.linalg.norm(intact1["x"]-ctrl1["x"]))
    if amp<1e-10: amp=1.0
    out=loopop.loop_map(ctrl1,cw1,cr1,aw,ar,amp*v1,cfg,shared,target)

    return {
        "seed":seed,
        "u1_v1_abs_cos":abs_cos(u1,v1),
        "u1_v1_angle_deg":float(np.degrees(np.arccos(np.clip(abs_cos(u1,v1),0,1)))),
        "sigma1":sigma1,
        "spectral_radius":rho,
        "sigma1_over_spectral_radius":sigma1/(rho+1e-15),
        "normalized_nonnormality":nonnorm,
        "finite_output_cos_u1":abs_cos(out,u1),
        "finite_output_cos_v1":abs_cos(out,v1),
        "finite_output_u1_minus_v1":abs_cos(out,u1)-abs_cos(out,v1)
    }

def run(seeds):
    return pd.DataFrame([audit(s) for s in seeds])
