import numpy as np, pandas as pd, importlib.util
from pathlib import Path

OUT=Path("/mnt/data")
spec=importlib.util.spec_from_file_location("fic",OUT/"reactor_fixed_instance_closure_multigeneration_diagnostic.py")
fic=importlib.util.module_from_spec(spec); spec.loader.exec_module(fic)
loopop=fic.loopop

HALF=24
NGEN=4
ANGLES=[22.5,45.0,67.5,90.0]
NQ=3

def unit_to_norm(v,n):
    v=np.asarray(v,float); nv=np.linalg.norm(v)
    if nv<1e-15: return np.zeros_like(v)
    return v*(n/nv)

def orthogonal_q(rng,v):
    q=rng.normal(size=v.shape)
    q=q-v*np.dot(q,v)
    n=np.linalg.norm(q)
    if n<1e-12:
        q=np.roll(v,1); q=q-v*np.dot(q,v); n=np.linalg.norm(q)
    return q/(n+1e-15)

def share(dx,v):
    dx=np.asarray(dx,float); v=np.asarray(v,float)
    c=float(abs(dx@v)/(np.linalg.norm(dx)*np.linalg.norm(v)+1e-15))
    return c*c

def run_prepared(preps):
    rows=[]
    n=len(preps)

    for idx,P in enumerate(preps):
        wrong=preps[(idx+1)%n]["Cdyn"]
        maps={
            "UNCORRECTED":None,
            "WRONG_SEED":wrong,
            "FIXED_DYNAMIC":P["Cdyn"]
        }

        rng=np.random.default_rng(P["seed"]*839+251)
        branches={}
        initial=P["amp"]

        for angle_deg in ANGLES:
            a=np.deg2rad(angle_deg)
            for qi in range(NQ):
                q=orthogonal_q(rng,P["vA"])
                dx0=initial*(np.cos(a)*P["vA"]+np.sin(a)*q)
                for cond in maps:
                    branches[(angle_deg,qi,cond)]=dx0.copy()
                    rows.append({
                        "seed":P["seed"],"angle_deg":angle_deg,"q_index":qi,
                        "condition":cond,"generation":0,
                        "share":share(dx0,P["vA"]),
                        "norm_rel_initial":float(np.linalg.norm(dx0)/(initial+1e-15)),
                        "generation_gain":np.nan,
                        "preclosure_share":share(dx0,P["vA"])
                    })

        control=loopop.clone(P["ctrlB"])

        for g in range(1,NGEN+1):
            nw=loopop.nz(P["seed"],HALF,4510+2*g)
            nr=loopop.nz(P["seed"],HALF,4511+2*g)

            ctrl_w=loopop.rollout(control,nw,P["cfg"],P["shared"],P["target"],False,False)
            ctrl_r=loopop.rollout(ctrl_w,nr,P["cfg"],P["shared"],P["target"],False,False)

            newbranches={}
            for key,dx in branches.items():
                angle_deg,qi,cond=key
                prev=np.linalg.norm(dx)+1e-15

                p=loopop.clone(control)
                p["x"]=p["x"]+dx
                pw=loopop.rollout(p,nw,P["cfg"],P["shared"],P["target"],False,False)
                dm=pw["m"]-ctrl_w["m"]

                mp=loopop.clone(ctrl_w)
                mp["m"]=ctrl_w["m"]+P["gammaA"]*dm
                pr=loopop.rollout(mp,nr,P["cfg"],P["shared"],P["target"],False,False)
                raw=pr["x"]-ctrl_r["x"]

                pre=share(raw,P["vA"])
                raw_norm=np.linalg.norm(raw)
                C=maps[cond]
                if C is None:
                    nxt=raw
                else:
                    nxt=unit_to_norm(C@raw,raw_norm)

                newbranches[key]=nxt
                rows.append({
                    "seed":P["seed"],"angle_deg":angle_deg,"q_index":qi,
                    "condition":cond,"generation":g,
                    "share":share(nxt,P["vA"]),
                    "norm_rel_initial":float(np.linalg.norm(nxt)/(initial+1e-15)),
                    "generation_gain":float(np.linalg.norm(nxt)/prev),
                    "preclosure_share":pre
                })

            branches=newbranches
            control=ctrl_r

    return pd.DataFrame(rows)

def run(seeds):
    preps=[fic.prepare(s) for s in seeds]
    return run_prepared(preps)
