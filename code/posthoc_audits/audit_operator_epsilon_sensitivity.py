# POSTCONFIRMATORY_AUDIT: numerical epsilon sensitivity; not part of frozen C07 criteria.
from pathlib import Path
import sys,numpy as np,pandas as pd
from multiprocessing import Pool
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
PORTABLE=REPO/'code'/'portable'
sys.path.insert(0,str(PORTABLE))
import reactor_dynamic_half_channel_closure_map_diagnostic as d
HALF=24; EPS=[1e-3,1e-4,1e-5]

def ab_context(seed,which,eps,cfg,shared,target,orig):
    if which=='A': tup=(-135,-45,45); gen=0; tags=(4301,4302)
    else: tup=(45,135,-135); gen=1; tags=(4305,4306)
    A,B,C=np.deg2rad(tup); start=d.loopop.make_history(seed,[A,B,None],cfg,shared,target,orig); _,ctrl=d.loopop.build_turn(seed,start,C,cfg,shared,target)
    if gen:
        cw=d.loopop.rollout(ctrl,d.loopop.nz(seed,HALF,4303),cfg,shared,target,False,False)
        ctrl=d.loopop.rollout(cw,d.loopop.nz(seed,HALF,4304),cfg,shared,target,False,False)
    return d.fac.estimate_A_B(ctrl,d.loopop.nz(seed,HALF,tags[0]),d.loopop.nz(seed,HALF,tags[1]),cfg,shared,target,epsilon=eps)[:2]

def worker(seed):
    cfg,shared,target,orig=d.loopop.origin(seed); out=[]
    for eps in EPS:
        Aa,Ba=ab_context(seed,'A',eps,cfg,shared,target,orig); Ab,Bb=ab_context(seed,'B',eps,cfg,shared,target,orig)
        C,uA,vA,sA,_=d.closure_from_AB(Aa,Ba); _,uB,vB,sB,_=d.closure_from_AB(Ab,Bb)
        out.append(dict(seed=seed,eps=eps,align=d.abs_cos(C@uB,vB),sigmaA=sA,sigmaB=sB,uA=uA,vA=vA,uB=uB,vB=vB))
    # compare modes against 1e-4 baseline
    base=out[1]
    slim=[]
    for r in out:
        slim.append(dict(seed=seed,eps=r['eps'],align=r['align'],sigmaA=r['sigmaA'],sigmaB=r['sigmaB'],
                         uA_vs_base=d.abs_cos(r['uA'],base['uA']),vA_vs_base=d.abs_cos(r['vA'],base['vA']),
                         uB_vs_base=d.abs_cos(r['uB'],base['uB']),vB_vs_base=d.abs_cos(r['vB'],base['vB'])))
    return slim
if __name__=='__main__':
    with Pool(8) as p: nest=p.map(worker,range(184000,184016))
    df=pd.DataFrame([r for rr in nest for r in rr]); OUT=REPO/'results'/'robustness'/'operator_epsilon_robustness_16.csv'; df.to_csv(OUT,index=False); print(f'wrote {OUT}')
    for e,g in df.groupby('eps'):
        print(e,'align',g['align'].mean(),g['align'].min(),'sigA rel',((g.sigmaA-df[df.eps==1e-4].set_index('seed').loc[g.seed].sigmaA.values)/df[df.eps==1e-4].set_index('seed').loc[g.seed].sigmaA.values).abs().mean(),
              'uA',g.uA_vs_base.mean(),'vA',g.vA_vs_base.mean(),'uB',g.uB_vs_base.mean(),'vB',g.vB_vs_base.mean())
