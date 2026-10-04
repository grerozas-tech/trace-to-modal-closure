import numpy as np, pandas as pd, importlib.util
from pathlib import Path

OUT=Path("/mnt/data")
spec=importlib.util.spec_from_file_location("dhc",OUT/"reactor_dynamic_half_channel_closure_map_diagnostic.py")
dhc=importlib.util.module_from_spec(spec); spec.loader.exec_module(dhc)
fac=dhc.fac
loopop=dhc.loopop

HALF=24
NGEN=4

def unit_to_norm(v,n):
    v=np.asarray(v,float)
    nv=np.linalg.norm(v)
    if nv<1e-15:
        return np.zeros_like(v)
    return v*(n/nv)

def abs_cos(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(abs(a@b)/(np.linalg.norm(a)*np.linalg.norm(b)+1e-15))

def scaled_loop(control,dx,gamma,nw,nr,cfg,shared,target):
    ctrl_w=loopop.rollout(control,nw,cfg,shared,target,False,False)
    ctrl_r=loopop.rollout(ctrl_w,nr,cfg,shared,target,False,False)

    p=loopop.clone(control)
    p["x"]=p["x"]+dx
    pw=loopop.rollout(p,nw,cfg,shared,target,False,False)
    dm=pw["m"]-ctrl_w["m"]

    mp=loopop.clone(ctrl_w)
    mp["m"]=ctrl_w["m"]+gamma*dm
    pr=loopop.rollout(mp,nr,cfg,shared,target,False,False)
    return pr["x"]-ctrl_r["x"], ctrl_r

def prepare(seed):
    cfg,shared,target,orig=loopop.origin(seed)

    # Learn context A.
    Aa,Ba=dhc.context_A(seed,cfg,shared,target,orig)
    Cdyn,uA,vA,sA,_=dhc.closure_from_AB(Aa,Ba)
    Cstatic=dhc.static_closure(shared)
    gammaA=1.0/(sA+1e-15)

    # Build test context B, including intact reference for amplitude.
    A=np.deg2rad(45.); B=np.deg2rad(135.); C=np.deg2rad(-135.)
    start=loopop.make_history(seed,[A,B,None],cfg,shared,target,orig)
    intact,ctrl=loopop.build_turn(seed,start,C,cfg,shared,target)

    nw0=loopop.nz(seed,HALF,4401)
    nr0=loopop.nz(seed,HALF,4402)
    iw=loopop.rollout(intact,nw0,cfg,shared,target,False,False)
    intactB=loopop.rollout(iw,nr0,cfg,shared,target,False,False)
    cw=loopop.rollout(ctrl,nw0,cfg,shared,target,False,False)
    ctrlB=loopop.rollout(cw,nr0,cfg,shared,target,False,False)

    amp=float(np.linalg.norm(intactB["x"]-ctrlB["x"]))
    if amp<1e-10:
        amp=1.0

    return {
        "seed":seed,"cfg":cfg,"shared":shared,"target":target,
        "Cdyn":Cdyn,"Cstatic":Cstatic,"gammaA":gammaA,"vA":vA,
        "ctrlB":ctrlB,"amp":amp,"sigmaA":sA
    }

def run_prepared(preps):
    rows=[]
    n=len(preps)
    for idx,P in enumerate(preps):
        wrong=preps[(idx+1)%n]["Cdyn"]
        Cmaps={
            "UNCORRECTED":None,
            "STATIC":P["Cstatic"],
            "WRONG_SEED":wrong,
            "FIXED_DYNAMIC":P["Cdyn"]
        }

        dx0=P["amp"]*P["vA"]
        branches={name:dx0.copy() for name in Cmaps}
        control=loopop.clone(P["ctrlB"])
        initial=np.linalg.norm(dx0)+1e-15

        # initial record
        for name,dx in branches.items():
            rows.append({
                "seed":P["seed"],"condition":name,"generation":0,
                "norm_rel_initial":float(np.linalg.norm(dx)/initial),
                "postclosure_align_vA":abs_cos(dx,P["vA"]),
                "preclosure_align_vA":abs_cos(dx,P["vA"]),
                "generation_gain":np.nan,
                "gammaA":P["gammaA"],"sigmaA":P["sigmaA"]
            })

        for g in range(1,NGEN+1):
            nw=loopop.nz(P["seed"],HALF,4410+2*g)
            nr=loopop.nz(P["seed"],HALF,4411+2*g)

            # control evolution identical for all branches.
            ctrl_w=loopop.rollout(control,nw,P["cfg"],P["shared"],P["target"],False,False)
            ctrl_r=loopop.rollout(ctrl_w,nr,P["cfg"],P["shared"],P["target"],False,False)

            newbranches={}
            for name,dx in branches.items():
                prev=np.linalg.norm(dx)+1e-15

                p=loopop.clone(control)
                p["x"]=p["x"]+dx
                pw=loopop.rollout(p,nw,P["cfg"],P["shared"],P["target"],False,False)
                dm=pw["m"]-ctrl_w["m"]

                mp=loopop.clone(ctrl_w)
                mp["m"]=ctrl_w["m"]+P["gammaA"]*dm
                pr=loopop.rollout(mp,nr,P["cfg"],P["shared"],P["target"],False,False)
                raw=pr["x"]-ctrl_r["x"]

                prealign=abs_cos(raw,P["vA"])
                rawnorm=np.linalg.norm(raw)

                C=Cmaps[name]
                if C is None:
                    nxt=raw
                else:
                    nxt=unit_to_norm(C@raw,rawnorm)

                newbranches[name]=nxt
                rows.append({
                    "seed":P["seed"],"condition":name,"generation":g,
                    "norm_rel_initial":float(np.linalg.norm(nxt)/initial),
                    "postclosure_align_vA":abs_cos(nxt,P["vA"]),
                    "preclosure_align_vA":prealign,
                    "generation_gain":float(np.linalg.norm(nxt)/prev),
                    "gammaA":P["gammaA"],"sigmaA":P["sigmaA"]
                })

            branches=newbranches
            control=ctrl_r

    return pd.DataFrame(rows)

def run(seeds):
    preps=[prepare(s) for s in seeds]
    return run_prepared(preps)
