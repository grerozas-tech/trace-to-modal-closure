# POSTCONFIRMATORY_AUDIT: added during adversarial pre-release review; not part of frozen G01 criteria.
from pathlib import Path
import sys, numpy as np, pandas as pd
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
PORTABLE=REPO/'code'/'portable'
sys.path.insert(0,str(PORTABLE))
import reactor_fixed_instance_closure_multigeneration_diagnostic as fic

seeds=range(186000,186064)
preps=[fic.prepare(s) for s in seeds]
rows=[]
for idx,P in enumerate(preps):
    C=P['Cdyn']; dx=P['amp']*P['vA']; control=fic.loopop.clone(P['ctrlB']); initial=np.linalg.norm(dx)
    dx_nr=dx.copy(); dx_r=dx.copy()
    for g in range(1,fic.NGEN+1):
        nw=fic.loopop.nz(P['seed'],fic.HALF,4410+2*g); nr=fic.loopop.nz(P['seed'],fic.HALF,4411+2*g)
        ctrl_w=fic.loopop.rollout(control,nw,P['cfg'],P['shared'],P['target'],False,False)
        ctrl_r=fic.loopop.rollout(ctrl_w,nr,P['cfg'],P['shared'],P['target'],False,False)
        vals={}
        for label,cur,ren in [('RENORM',dx_r,True),('NO_RENORM',dx_nr,False)]:
            p=fic.loopop.clone(control); p['x']=p['x']+cur
            pw=fic.loopop.rollout(p,nw,P['cfg'],P['shared'],P['target'],False,False)
            dm=pw['m']-ctrl_w['m']
            mp=fic.loopop.clone(ctrl_w); mp['m']=ctrl_w['m']+P['gammaA']*dm
            pr=fic.loopop.rollout(mp,nr,P['cfg'],P['shared'],P['target'],False,False)
            raw=pr['x']-ctrl_r['x']; mapped=C@raw
            factor=np.linalg.norm(raw)/(np.linalg.norm(mapped)+1e-15)
            nxt=fic.unit_to_norm(mapped,np.linalg.norm(raw)) if ren else mapped
            vals[label]=nxt
            rows.append((P['seed'],g,label,np.linalg.norm(raw),np.linalg.norm(mapped),factor,np.linalg.norm(nxt)/initial,fic.abs_cos(nxt,P['vA']),fic.abs_cos(raw,P['vA'])))
        dx_r=vals['RENORM']; dx_nr=vals['NO_RENORM']; control=ctrl_r

df=pd.DataFrame(rows,columns=['seed','generation','condition','raw_norm','mapped_norm','renorm_factor','norm_rel_initial','post_align','pre_align'])
OUT=REPO/'results'/'robustness'/'fixed_dynamic_renorm_robustness_64.csv'
df.to_csv(OUT,index=False)
print(f'wrote {OUT}')
print('RENORM FACTORS based on RENORM branch raw packets:')
r=df[df.condition=='RENORM']
print(r.groupby('generation').renorm_factor.agg(['mean','std','min','max']).to_string())
print('all quantiles',r.renorm_factor.quantile([.01,.05,.5,.95,.99]).to_dict())
print('\nNO_RENORM norm by generation:')
n=df[df.condition=='NO_RENORM']
print(n.groupby('generation').norm_rel_initial.agg(['mean','std','min','max']).to_string())
print('\nNO_RENORM alignment:')
print(n.groupby('generation').post_align.agg(['mean','min']).to_string())
print('\nRENORM norm by generation:')
print(r.groupby('generation').norm_rel_initial.agg(['mean','std','min','max']).to_string())
