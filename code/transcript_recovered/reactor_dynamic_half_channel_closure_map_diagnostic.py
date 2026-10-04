import numpy as np, pandas as pd, importlib.util
from pathlib import Path

OUT=Path("/mnt/data")
spec=importlib.util.spec_from_file_location("fac",OUT/"reactor_loop_half_operator_factorization_diagnostic.py")
fac=importlib.util.module_from_spec(spec); spec.loader.exec_module(fac)
loopop=fac.loopdiag

HALF=24

def canonical_pair(u,v):
    u=np.asarray(u,float).copy(); v=np.asarray(v,float).copy()
    j=int(np.argmax(np.abs(v)))
    if v[j] < 0:
        u=-u; v=-v
    return u/(np.linalg.norm(u)+1e-15), v/(np.linalg.norm(v)+1e-15)

def abs_cos(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(abs(a@b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-15))

def closure_from_AB(A,B):
    Ua,Sa,Vta=np.linalg.svd(A,full_matrices=False)
    Ub,Sb,Vtb=np.linalg.svd(B,full_matrices=False)
    H=np.diag(Sb) @ (Vtb @ Ua) @ np.diag(Sa)
    Uh,Sh,Vth=np.linalg.svd(H,full_matrices=False)

    Va=Vta.T
    # V_H columns = Vth.T; U_H columns = Uh
    C=Va @ Vth.T @ Uh.T @ Ub.T

    T=B@A
    Ut,St,Vtt=np.linalg.svd(T,full_matrices=False)
    u,v=canonical_pair(Ut[:,0],Vtt[0])
    return C,u,v,float(St[0]),float(Sh[0])

def static_closure(shared):
    A=shared["Pm"]           # 8x32
    B=shared["M"]            # 32x8
    return closure_from_AB(A,B)[0]

def context_A(seed,cfg,shared,target,orig):
    A=np.deg2rad(-135.); B=np.deg2rad(-45.); C=np.deg2rad(45.)
    start=loopop.make_history(seed,[A,B,None],cfg,shared,target,orig)
    _,ctrl=loopop.build_turn(seed,start,C,cfg,shared,target)
    nw=loopop.nz(seed,HALF,4301); nr=loopop.nz(seed,HALF,4302)
    Aeff,Beff,_,_=fac.estimate_A_B(ctrl,nw,nr,cfg,shared,target)
    return Aeff,Beff

def context_B(seed,cfg,shared,target,orig):
    A=np.deg2rad(45.); B=np.deg2rad(135.); C=np.deg2rad(-135.)
    start=loopop.make_history(seed,[A,B,None],cfg,shared,target,orig)
    _,ctrl=loopop.build_turn(seed,start,C,cfg,shared,target)
    # advance one generation
    nw0=loopop.nz(seed,HALF,4303); nr0=loopop.nz(seed,HALF,4304)
    cw=loopop.rollout(ctrl,nw0,cfg,shared,target,False,False)
    ctrl=loopop.rollout(cw,nr0,cfg,shared,target,False,False)
    nw=loopop.nz(seed,HALF,4305); nr=loopop.nz(seed,HALF,4306)
    Aeff,Beff,_,_=fac.estimate_A_B(ctrl,nw,nr,cfg,shared,target)
    return Aeff,Beff

def collect_seed(seed):
    cfg,shared,target,orig=loopop.origin(seed)

    Aa,Ba=context_A(seed,cfg,shared,target,orig)
    Ab,Bb=context_B(seed,cfg,shared,target,orig)

    CdynA,uA,vA,sA,hA=closure_from_AB(Aa,Ba)
    CdynB,uB,vB,sB,hB=closure_from_AB(Ab,Bb)
    Cstat=static_closure(shared)

    pred_dyn=CdynA@uB
    pred_stat=Cstat@uB
    pred_id=uB

    actual_need=1-abs_cos(uB,vB)
    pred_need_dyn=1-abs_cos(uB,pred_dyn)
    pred_need_stat=1-abs_cos(uB,pred_stat)

    return {
        "seed":seed,
        "identity_abs_cos":abs_cos(pred_id,vB),
        "static_own_abs_cos":abs_cos(pred_stat,vB),
        "dynamic_own_abs_cos":abs_cos(pred_dyn,vB),
        "uA_uB_abs_cos":abs_cos(uA,uB),
        "vA_vB_abs_cos":abs_cos(vA,vB),
        "actual_need":actual_need,
        "pred_need_dynamic":pred_need_dyn,
        "pred_need_static":pred_need_stat,
        "dynamic_need_abs_error":abs(pred_need_dyn-actual_need),
        "static_need_abs_error":abs(pred_need_stat-actual_need),
        "sigmaAcontext":sA,
        "sigmaBcontext":sB,
        "HsigmaA":hA,
        "HsigmaB":hB,
        "CdynA":CdynA,
        "uB":uB,
        "vB":vB
    }

def collect(seeds):
    return [collect_seed(s) for s in seeds]
