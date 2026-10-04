# PORTABLE_ADAPTATION: path-only adaptation of TRANSCRIPT_RECOVERED source.
import numpy as np, pandas as pd, importlib.util
from pathlib import Path
from collections import deque

OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("loopop",OUT/"reactor_full_loop_operator_gain_diagnostic.py")
loopop=importlib.util.module_from_spec(spec); spec.loader.exec_module(loopop)

HALF=24
TUPLES=[
    (-135.,-45.,45.),
    (-45.,45.,135.),
    (45.,135.,-135.),
    (135.,-135.,-45.)
]

PACKAGES={
    "X_ONLY":[],
    "M":["m"],
    "THETA":["theta"],
    "R":["r"],
    "KB":["K","b"],
    "GH":["gh"],
    "FASTCTX":["s","e","a","prev_u","prev_z","prev_v"],
    "ALL_SLOW":["m","theta","r","K","b","gh"],
    "ALL_NONX":["s","e","a","m","theta","r","K","b","gh","prev_u","prev_z","prev_v"]
}

def clone(st):
    return loopop.clone(st)

def copy_delta(dst,base,full,key):
    if key=="gh":
        # represent gh co-product by direct full queue transplant.
        dst["gh"]=deque([g.copy() for g in full["gh"]],maxlen=full["gh"].maxlen)
    elif isinstance(base[key],np.ndarray):
        dst[key]=base[key]+(full[key]-base[key])
    else:
        dst[key]=full[key]
    return dst

def make_carrier(base,full,keys):
    s=clone(base)
    for k in keys:
        s=copy_delta(s,base,full,k)
    return s

def isolated_loop(control,dx,noise_w,noise_r,cfg,shared,target,return_full=False):
    ctrl_w=loopop.rollout(control,noise_w,cfg,shared,target,False,False)
    ctrl_r=loopop.rollout(ctrl_w,noise_r,cfg,shared,target,False,False)

    p=clone(control)
    p["x"]=p["x"]+dx
    pw=loopop.rollout(p,noise_w,cfg,shared,target,False,False)
    dm=pw["m"]-ctrl_w["m"]

    mp=clone(ctrl_w)
    mp["m"]=mp["m"]+dm
    pr=loopop.rollout(mp,noise_r,cfg,shared,target,False,False)
    out=pr["x"]-ctrl_r["x"]
    if return_full:
        return out,pr,ctrl_r
    return out

def abs_cos(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(abs(a@b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-15))

def audit(seed):
    Adeg,Bdeg,Cdeg=TUPLES[seed%4]
    A=np.deg2rad(Adeg); B=np.deg2rad(Bdeg); C=np.deg2rad(Cdeg)

    cfg,shared,target,orig=loopop.origin(seed)
    start=loopop.make_history(seed,[A,B,None],cfg,shared,target,orig)
    intact0,ctrl0=loopop.build_turn(seed,start,C,cfg,shared,target)

    # G1 common carrier.
    n0w=loopop.nz(seed,HALF,3601)
    n0r=loopop.nz(seed,HALF,3602)
    iw=loopop.rollout(intact0,n0w,cfg,shared,target,False,False)
    intact1=loopop.rollout(iw,n0r,cfg,shared,target,False,False)
    cw=loopop.rollout(ctrl0,n0w,cfg,shared,target,False,False)
    ctrl1=loopop.rollout(cw,n0r,cfg,shared,target,False,False)

    # First-loop operator and optimal input v1.
    n1w=loopop.nz(seed,HALF,3603)
    n1r=loopop.nz(seed,HALF,3604)
    T1,cw1,cr1=loopop.estimate_T(ctrl1,n1w,n1r,cfg,shared,target)
    U,S,Vt=np.linalg.svd(T1,full_matrices=False)
    v1=Vt[0]; u1=U[:,0]
    amp=float(np.linalg.norm(intact1["x"]-ctrl1["x"]))
    if amp<1e-10: amp=1.0

    # Run one native isolated loop at finite amplitude, retaining full post-return state.
    dx_in=amp*v1
    dx_out,full_post,base_post=isolated_loop(
        ctrl1,dx_in,n1w,n1r,cfg,shared,target,return_full=True
    )

    # Second-loop noise common to all package carriers.
    n2w=loopop.nz(seed,HALF,3605)
    n2r=loopop.nz(seed,HALF,3606)

    rows=[]
    baseline_gain=None
    for name,keys in PACKAGES.items():
        carrier=make_carrier(base_post,full_post,keys)

        # Matched carrier and packet differ only by inherited dx_out.
        out2=isolated_loop(carrier,dx_out,n2w,n2r,cfg,shared,target,return_full=False)
        gain=float(np.linalg.norm(out2)/(np.linalg.norm(dx_out)+1e-15))

        # projection on inherited input/output axes only as descriptive readouts
        proj_v=float(abs(out2@v1)/(np.linalg.norm(dx_out)+1e-15))
        proj_u=float(abs(out2@u1)/(np.linalg.norm(dx_out)+1e-15))

        if name=="X_ONLY":
            baseline_gain=gain

        rows.append({
            "seed":seed,"condition":name,
            "first_sigma1":float(S[0]),
            "first_u1_v1_abs_cos":abs_cos(u1,v1),
            "first_output_norm_gain":float(np.linalg.norm(dx_out)/(np.linalg.norm(dx_in)+1e-15)),
            "second_loop_gain":gain,
            "second_proj_on_v1":proj_v,
            "second_proj_on_u1":proj_u,
            "inherited_dx_norm":float(np.linalg.norm(dx_out))
        })

    # attach rescue relative to X_ONLY
    b=[r["second_loop_gain"] for r in rows if r["condition"]=="X_ONLY"][0]
    for r in rows:
        r["gain_rescue_vs_xonly"]=r["second_loop_gain"]-b
        r["gain_ratio_vs_xonly"]=r["second_loop_gain"]/(b+1e-15)
    return pd.DataFrame(rows)

def run(seeds):
    return pd.concat([audit(s) for s in seeds],ignore_index=True)
