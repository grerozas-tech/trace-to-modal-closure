# PORTABLE_ADAPTATION: path-only adaptation of TRANSCRIPT_RECOVERED source.
import numpy as np, pandas as pd, importlib.util
from pathlib import Path

OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("loopop",OUT/"reactor_full_loop_operator_gain_diagnostic.py")
loopop=importlib.util.module_from_spec(spec); spec.loader.exec_module(loopop)

HALF=24
NQ=6
TUPLES=[
    (-135.,-45.,45.),
    (-45.,45.,135.),
    (45.,135.,-135.),
    (135.,-135.,-45.)
]

def unit(v):
    v=np.asarray(v,float)
    return v/(np.linalg.norm(v)+1e-15)

def orthogonal_q(rng,v):
    q=rng.normal(size=v.shape)
    q=q-v*np.dot(q,v)
    if np.linalg.norm(q)<1e-12:
        q=np.roll(v,1); q=q-v*np.dot(q,v)
    return unit(q)

def fit_weights(mix,ref_v,ref_q):
    U=np.column_stack([unit(ref_v),unit(ref_q)])
    coeff=np.linalg.pinv(U)@mix
    recon=U@coeff
    resid=float(np.linalg.norm(mix-recon)/(np.linalg.norm(mix)+1e-15))
    ratio=float(abs(coeff[0])/(abs(coeff[1])+1e-15))
    share=float(ratio/(1+ratio))
    return coeff,ratio,share,resid

def evolve(st,noise,cfg,shared,target):
    return loopop.rollout(st,noise,cfg,shared,target,False,False)

def collect_seed(seed):
    Adeg,Bdeg,Cdeg=TUPLES[seed%4]
    A=np.deg2rad(Adeg); B=np.deg2rad(Bdeg); C=np.deg2rad(Cdeg)

    cfg,shared,target,orig=loopop.origin(seed)
    start=loopop.make_history(seed,[A,B,None],cfg,shared,target,orig)
    intact0,ctrl0=loopop.build_turn(seed,start,C,cfg,shared,target)

    # G1 carrier.
    nw0=loopop.nz(seed,HALF,3401)
    nr0=loopop.nz(seed,HALF,3402)
    iw=loopop.rollout(intact0,nw0,cfg,shared,target,False,False)
    intact1=loopop.rollout(iw,nr0,cfg,shared,target,False,False)
    cw=loopop.rollout(ctrl0,nw0,cfg,shared,target,False,False)
    ctrl1=loopop.rollout(cw,nr0,cfg,shared,target,False,False)

    # Full-loop optimal mode.
    aw=loopop.nz(seed,HALF,3403)
    ar=loopop.nz(seed,HALF,3404)
    T,_,_=loopop.estimate_T(ctrl1,aw,ar,cfg,shared,target)
    _,S,Vt=np.linalg.svd(T,full_matrices=False)
    v=unit(Vt[0])

    amp=float(np.linalg.norm(intact1["x"]-ctrl1["x"]))
    if amp<1e-10: amp=1.0
    comp_amp=amp/np.sqrt(2.0)

    write_noise=loopop.nz(seed,HALF,3405)
    return_noise=loopop.nz(seed,HALF,3406)
    ctrl_w=evolve(ctrl1,write_noise,cfg,shared,target)
    ctrl_r=evolve(ctrl_w,return_noise,cfg,shared,target)

    rng=np.random.default_rng(seed*761+181)
    rows=[]

    for qi in range(NQ):
        q=orthogonal_q(rng,v)

        # Pure component branches at exactly the component amplitude used in the mixture.
        pure_v=loopop.clone(ctrl1); pure_v["x"]=ctrl1["x"]+comp_amp*v
        pure_q=loopop.clone(ctrl1); pure_q["x"]=ctrl1["x"]+comp_amp*q
        pv_w=evolve(pure_v,write_noise,cfg,shared,target)
        pq_w=evolve(pure_q,write_noise,cfg,shared,target)
        mv=pv_w["m"]-ctrl_w["m"]
        mq=pq_w["m"]-ctrl_w["m"]

        # Return references.
        mv_state=loopop.clone(ctrl_w); mv_state["m"]=ctrl_w["m"]+mv
        mq_state=loopop.clone(ctrl_w); mq_state["m"]=ctrl_w["m"]+mq
        xv=evolve(mv_state,return_noise,cfg,shared,target)["x"]-ctrl_r["x"]
        xq=evolve(mq_state,return_noise,cfg,shared,target)["x"]-ctrl_r["x"]

        for phase in (+1,-1):
            d=comp_amp*(v+phase*q)
            mix=loopop.clone(ctrl1); mix["x"]=ctrl1["x"]+d
            mix_w=evolve(mix,write_noise,cfg,shared,target)
            mmix=mix_w["m"]-ctrl_w["m"]

            # Native return using the actual mixed m packet.
            mm_state=loopop.clone(ctrl_w); mm_state["m"]=ctrl_w["m"]+mmix
            xmix=evolve(mm_state,return_noise,cfg,shared,target)["x"]-ctrl_r["x"]

            cm,rm,sm,resm=fit_weights(mmix,mv,mq)
            cx,rx,sx,resx=fit_weights(xmix,xv,xq)

            rows.append({
                "seed":seed,"q_index":qi,"phase":phase,
                "sigma1":float(S[0]),
                "input_v_norm":float(comp_amp),
                "input_q_norm":float(comp_amp),
                "input_ratio":1.0,
                "pure_m_gain_v":float(np.linalg.norm(mv)/(comp_amp+1e-15)),
                "pure_m_gain_q":float(np.linalg.norm(mq)/(comp_amp+1e-15)),
                "pure_x_gain_v":float(np.linalg.norm(xv)/(comp_amp+1e-15)),
                "pure_x_gain_q":float(np.linalg.norm(xq)/(comp_amp+1e-15)),
                "m_coeff_v":float(cm[0]),"m_coeff_q":float(cm[1]),
                "m_ratio":rm,"m_share":sm,"m_residual":resm,
                "x_coeff_v":float(cx[0]),"x_coeff_q":float(cx[1]),
                "x_ratio":rx,"x_share":sx,"x_residual":resx,
                "x_minus_m_ratio":rx-rm
            })
    return pd.DataFrame(rows)

def run(seeds):
    return pd.concat([collect_seed(s) for s in seeds],ignore_index=True)
