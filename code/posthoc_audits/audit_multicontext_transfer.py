# POSTCONFIRMATORY_AUDIT: four symmetry-related context pairs; not part of frozen C07 criteria.
from pathlib import Path
import sys, numpy as np, pandas as pd
from multiprocessing import Pool
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
PORTABLE=REPO/'code'/'portable'
sys.path.insert(0,str(PORTABLE))
import reactor_dynamic_half_channel_closure_map_diagnostic as d
HALF=24
TUPLES=[(-135,-45,45),(-45,45,135),(45,135,-135),(135,-135,-45)]
PAIRS=[(0,2),(1,3),(2,0),(3,1)]

def context(seed,tup,generation,cfg,shared,target,orig):
    A,B,C=np.deg2rad(tup)
    start=d.loopop.make_history(seed,[A,B,None],cfg,shared,target,orig)
    _,ctrl=d.loopop.build_turn(seed,start,C,cfg,shared,target)
    if generation==1:
        nw0=d.loopop.nz(seed,HALF,4303); nr0=d.loopop.nz(seed,HALF,4304)
        cw=d.loopop.rollout(ctrl,nw0,cfg,shared,target,False,False)
        ctrl=d.loopop.rollout(cw,nr0,cfg,shared,target,False,False)
        nw=d.loopop.nz(seed,HALF,4305); nr=d.loopop.nz(seed,HALF,4306)
    else:
        nw=d.loopop.nz(seed,HALF,4301); nr=d.loopop.nz(seed,HALF,4302)
    return d.fac.estimate_A_B(ctrl,nw,nr,cfg,shared,target)[:2]

def worker(seed):
    cfg,shared,target,orig=d.loopop.origin(seed)
    Cstatic=d.static_closure(shared)
    out=[]
    for pair_id,(ia,ib) in enumerate(PAIRS):
        Aa,Ba=context(seed,TUPLES[ia],0,cfg,shared,target,orig)
        Ab,Bb=context(seed,TUPLES[ib],1,cfg,shared,target,orig)
        Cdyn,uA,vA,sA,_=d.closure_from_AB(Aa,Ba)
        _,uB,vB,sB,_=d.closure_from_AB(Ab,Bb)
        actual=1-d.abs_cos(uB,vB); pred=1-d.abs_cos(uB,Cdyn@uB)
        out.append(dict(seed=seed,pair=pair_id,cal=ia,test=ib,
                        own=d.abs_cos(Cdyn@uB,vB),identity=d.abs_cos(uB,vB),static=d.abs_cos(Cstatic@uB,vB),
                        u_stab=d.abs_cos(uA,uB),v_stab=d.abs_cos(vA,vB),need_err=abs(pred-actual)))
    return out

if __name__=='__main__':
    seeds=list(range(184000,184064))
    rows=[]
    # Chunking keeps memory bounded on modest machines while preserving the same deterministic calculation.
    for start in range(0,len(seeds),16):
        chunk=seeds[start:start+16]
        with Pool(min(8,len(chunk))) as pool:
            nested=pool.map(worker,chunk)
        rows.extend(r for rr in nested for r in rr)
    df=pd.DataFrame(rows)
    OUT=REPO/'results'/'robustness'/'dynamic_closure_multicontext_robustness_64x4.csv'
    df.to_csv(OUT,index=False)
    print(f'wrote {OUT}')
    for pid,g in df.groupby('pair'):
        ia,ib=PAIRS[pid]
        print(pid,TUPLES[ia],'->',TUPLES[ib],
              'own',g.own.mean(),'min',g.own.min(),'frac>0.99',np.mean(g.own>0.99),
              'adv static',(g.own-g.static).mean(),'frac+',np.mean(g.own>g.static),
              'need mae',g.need_err.mean(),'max',g.need_err.max(),
              'u',g.u_stab.mean(),'v',g.v_stab.mean())
    print('agg own',df.own.mean(),'min',df.own.min(),'frac>.99',np.mean(df.own>0.99))
    print('agg adv static',(df.own-df.static).mean(),'frac+',np.mean(df.own>df.static))
    print('agg need',df.need_err.mean(),'max',df.need_err.max(),'frac<.03',np.mean(df.need_err<.03))
