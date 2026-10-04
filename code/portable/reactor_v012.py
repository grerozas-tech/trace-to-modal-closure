
import numpy as np
from dataclasses import dataclass
from collections import deque

@dataclass
class Config:
    N: int = 32
    modules: int = 4
    module_size: int = 8
    body_dim: int = 4
    context_dim: int = 8
    memory_dim: int = 8
    lambda_x: float = 0.25
    sigma_s: float = 0.35
    lambda_a: float = 0.05
    theta_eta: float = 0.002
    theta_decay: float = 0.004
    theta_lim: float = 0.25
    mem_decay: float = 0.98
    mem_rate: float = 0.02
    rel_decay: float = 0.98
    rel_rate: float = 0.02
    boundary_decay: float = 0.98
    boundary_rate: float = 0.02
    T: int = 2000
    intervention_t: int = 800
    warmup_end: int = 400
    baseline_end: int = 800

def spectral_radius(W):
    vals = np.linalg.eigvals(W)
    return float(np.max(np.abs(vals)))

def make_shared(seed=0, cfg=Config()):
    rng = np.random.default_rng(seed)
    W = np.zeros((cfg.N, cfg.N))
    for i in range(cfg.N):
        mi = i // cfg.module_size
        for j in range(cfg.N):
            if i == j:
                continue
            mj = j // cfg.module_size
            p = 0.35 if mi == mj else 0.05
            if rng.random() < p:
                W[i, j] = rng.normal(0, 0.35)
    rho = spectral_radius(W)
    if rho > 0:
        W *= 0.75 / rho

    B = rng.normal(0, 0.18, size=(cfg.N, cfg.body_dim + cfg.context_dim))
    M = rng.normal(0, 0.12, size=(cfg.N, cfg.memory_dim))
    Pm = rng.normal(0, 1/np.sqrt(cfg.N), size=(cfg.memory_dim, cfg.N))

    A = np.zeros((cfg.modules, cfg.N, cfg.N))
    for k in range(cfg.modules):
        sl = slice(k*cfg.module_size, (k+1)*cfg.module_size)
        Ak = rng.normal(0, 0.10, size=(cfg.N, cfg.N))
        mask = np.zeros((cfg.N, cfg.N))
        mask[sl, sl] = 1.0
        mask[sl, :] = np.maximum(mask[sl, :], (rng.random((cfg.module_size, cfg.N)) < 0.08))
        mask[:, sl] = np.maximum(mask[:, sl], (rng.random((cfg.N, cfg.module_size)) < 0.08))
        Ak *= mask
        norm = np.linalg.norm(Ak)
        if norm > 0:
            Ak /= norm
        A[k] = Ak

    Se = rng.normal(0, 0.18, size=(cfg.context_dim, cfg.body_dim))
    causal_idx = np.sort(rng.choice(cfg.context_dim, size=cfg.body_dim, replace=False))
    Sa = np.zeros((cfg.context_dim, cfg.body_dim))
    Sa[causal_idx] = rng.normal(0, 0.30, size=(cfg.body_dim, cfg.body_dim))

    Jp = rng.normal(0, 0.04, size=(cfg.N, cfg.modules))
    Jr = rng.normal(0, 0.025, size=(cfg.N, cfg.body_dim + cfg.context_dim))
    Jb = rng.normal(0, 0.025, size=(cfg.N, cfg.context_dim))

    As = 0.94*np.eye(cfg.body_dim)
    for i in range(cfg.body_dim):
        As[i, (i+1) % cfg.body_dim] += 0.015

    return dict(W0=W, B=B, M=M, Pm=Pm, A=A, Se=Se, Sa=Sa,
                causal_idx=causal_idx, Jp=Jp, Jr=Jr, Jb=Jb, As=As)

def module_means(x, cfg):
    return np.array([np.mean(x[k*cfg.module_size:(k+1)*cfg.module_size]) for k in range(cfg.modules)])

def module_activity(x, cfg):
    return np.array([np.mean(x[k*cfg.module_size:(k+1)*cfg.module_size]**2) for k in range(cfg.modules)])

def W_from_theta(shared, theta):
    W = shared["W0"].copy()
    for k, th in enumerate(theta):
        W += th * shared["A"][k]
    return W

def viability(s, a, cfg):
    return float(np.exp(-np.dot(s,s)/(2*cfg.sigma_s**2) - cfg.lambda_a*np.dot(a,a)))

def memory_update(m, x, shared, cfg):
    return cfg.mem_decay*m + cfg.mem_rate*(shared["Pm"] @ x)

def theta_update(theta, x, target_v, shared, cfg, delta_v=0.0, p=None, c4=False):
    v = module_activity(x, cfg)
    drive = cfg.theta_eta*(target_v - v) - cfg.theta_decay*theta
    if c4 and p is not None:
        drive = drive + 0.0005*delta_v*p
    return np.clip(theta + drive, -cfg.theta_lim, cfg.theta_lim)

def relevance_update(r, prev_u, delta_v, cfg):
    return cfg.rel_decay*r + cfg.rel_rate*prev_u*delta_v

def boundary_update(K, c_t, prev_zeta, cfg):
    return cfg.boundary_decay*K + cfg.boundary_rate*np.outer(c_t, prev_zeta)

def temporal_summary(hist):
    L = min(5, len(hist))
    arr = np.array(list(hist)[-L:])
    lags = np.arange(L-1, -1, -1)
    w = np.exp(-lags/2.0); w /= w.sum()
    return (arr*w[:,None]).sum(axis=0)

def sigmoid(x):
    return 1/(1+np.exp(-np.clip(x,-40,40)))

def precompute_world(master_seed, shared, cfg):
    rng = np.random.default_rng(master_seed + 10_000)
    eta_env = rng.normal(0, 1, size=(cfg.T, cfg.body_dim))
    eta_body = rng.normal(0, 0.005, size=(cfg.T, cfg.body_dim))
    eta_context = rng.normal(0, 0.02, size=(cfg.T, cfg.context_dim))
    zeta = rng.normal(0, 0.02, size=(cfg.T, cfg.body_dim))
    shock_dir = rng.normal(size=cfg.body_dim); shock_dir /= np.linalg.norm(shock_dir)
    lesion_idx = np.sort(rng.choice(cfg.N, size=cfg.N//4, replace=False))
    perm = rng.permutation(cfg.context_dim)
    return dict(eta_env=eta_env, eta_body=eta_body, eta_context=eta_context,
                zeta=zeta, shock_dir=shock_dir, lesion_idx=lesion_idx, p5_perm=perm)

def run_fixed_reference(shared, world, cfg):
    s = np.zeros(cfg.body_dim); e = np.zeros(cfg.body_dim)
    x = np.zeros(cfg.N); m = np.zeros(cfg.memory_dim); a = np.zeros(cfg.body_dim)
    acts = []
    for t in range(cfg.baseline_end):
        e = 0.95*e + 0.03*world["eta_env"][t]
        c = shared["Se"]@e + shared["Sa"]@a + world["eta_context"][t]
        u = np.r_[s,c]
        z = shared["W0"]@x + shared["B"]@u + shared["M"]@m
        x = 0.75*x + 0.25*np.tanh(z)
        g = module_means(x,cfg)
        a = np.clip(np.tanh(0.8*s) + 0.25*np.tanh(g) + world["zeta"][t], -1,1)
        s = shared["As"]@s - 0.40*a + 0.25*e + world["eta_body"][t]
        m = memory_update(m,x,shared,cfg)
        if t >= cfg.warmup_end:
            acts.append(module_activity(x,cfg))
    return np.mean(np.array(acts),axis=0)

def perturbation_terms(kind, t, shared, world, cfg):
    mu = np.zeros(cfg.body_dim)
    body_kick = None
    lesion = None
    Sa = shared["Sa"]
    if kind == "P1" and t == cfg.intervention_t:
        body_kick = 0.8*world["shock_dir"]
    elif kind == "P2" and cfg.intervention_t <= t < cfg.intervention_t+20:
        lesion = world["lesion_idx"]
    elif kind == "P3" and cfg.intervention_t <= t < cfg.intervention_t+100:
        mu = 0.04*world["shock_dir"]
    elif kind == "P4" and cfg.intervention_t <= t < cfg.intervention_t+400:
        frac = (t-cfg.intervention_t)/399.0
        mu = 0.04*frac*world["shock_dir"]
    elif kind == "P5" and t >= cfg.intervention_t:
        Sa = shared["Sa"][world["p5_perm"]]
    return mu, body_kick, lesion, Sa

def run_architecture(arch, perturbation, master_seed=0, cfg=Config()):
    shared = make_shared(master_seed, cfg)
    world = precompute_world(master_seed, shared, cfg)
    target_v = run_fixed_reference(shared, world, cfg)

    s = np.zeros(cfg.body_dim); e = np.zeros(cfg.body_dim)
    x = np.zeros(cfg.N); a = np.zeros(cfg.body_dim)
    m = np.zeros(cfg.memory_dim)
    theta = np.zeros(cfg.modules)
    r = np.zeros(cfg.body_dim+cfg.context_dim)
    K = np.zeros((cfg.context_dim,cfg.body_dim))
    b = np.full(cfg.context_dim,0.5)
    ghist = deque(maxlen=5)
    prev_u = np.zeros(cfg.body_dim+cfg.context_dim)
    prev_zeta = np.zeros(cfg.body_dim)
    prev_vhat = 1.0

    V = np.zeros(cfg.T)
    theta_hist=np.zeros((cfg.T,cfg.modules))
    x_max=0.; s_max=0.; m_max=0.; r_max=0.; b_min=1.; b_max=0.

    for t in range(cfg.T):
        mu, body_kick, lesion, Sa_now = perturbation_terms(perturbation,t,shared,world,cfg)
        e = 0.95*e + 0.03*world["eta_env"][t] + mu
        if body_kick is not None:
            s = s + body_kick

        c = shared["Se"]@e + Sa_now@a + world["eta_context"][t]
        u = np.r_[s,c]
        vhat_now = viability(s,a,cfg)
        delta_v = vhat_now - prev_vhat

        if arch == "C0":
            x_new = np.tanh(shared["B"]@u)
        else:
            W = shared["W0"] if arch in ("C1","C2") else W_from_theta(shared,theta)
            z = W@x + shared["B"]@u
            if arch in ("C2","C3","C4"):
                z += shared["M"]@m
            if arch == "C4":
                r = relevance_update(r, prev_u, delta_v, cfg)
                rr = np.abs(r)
                if np.max(rr) > 1e-12:
                    rr = rr/np.max(rr)
                u_eff = u*(1+0.5*rr)
                z = W@x + shared["B"]@u_eff + shared["M"]@m
                K = boundary_update(K,c,prev_zeta,cfg)
                scores = np.linalg.norm(K,axis=1)
                thresh = np.median(scores)
                b = sigmoid(12*(scores-thresh))
                p = np.zeros(cfg.modules) if len(ghist)==0 else temporal_summary(ghist)
                z += shared["Jp"]@p + shared["Jr"]@r + shared["Jb"]@b
            x_new = 0.75*x + 0.25*np.tanh(z)

        if lesion is not None:
            x_new = x_new.copy()
            x_new[lesion] = 0.0

        x = x_new
        g = module_means(x,cfg)
        ghist.append(g)
        a = np.clip(np.tanh(0.8*s) + 0.25*np.tanh(g) + world["zeta"][t], -1,1)
        s = shared["As"]@s - 0.40*a + 0.25*e + world["eta_body"][t]

        if arch in ("C2","C3","C4"):
            m = memory_update(m,x,shared,cfg)
        if arch == "C3":
            theta = theta_update(theta,x,target_v,shared,cfg,c4=False)
        elif arch == "C4":
            p = temporal_summary(ghist)
            theta = theta_update(theta,x,target_v,shared,cfg,delta_v=delta_v,p=p,c4=True)

        V[t]=viability(s,a,cfg)
        theta_hist[t]=theta
        x_max=max(x_max,float(np.max(np.abs(x))))
        s_max=max(s_max,float(np.max(np.abs(s))))
        m_max=max(m_max,float(np.max(np.abs(m))))
        r_max=max(r_max,float(np.max(np.abs(r))))
        b_min=min(b_min,float(np.min(b))); b_max=max(b_max,float(np.max(b)))

        prev_u = u
        prev_zeta = world["zeta"][t]
        prev_vhat = vhat_now

    base = float(np.mean(V[cfg.warmup_end:cfg.baseline_end]))
    late = float(np.mean(V[1600:2000]))
    th_base = theta_hist[cfg.warmup_end:cfg.baseline_end]
    th_late = theta_hist[1600:2000]
    return {
        "arch":arch, "perturbation":perturbation, "seed":master_seed,
        "base_V":base, "late_V":late,
        "min_V_post":float(np.min(V[cfg.intervention_t:])),
        "max_abs_x":x_max, "max_abs_s":s_max, "max_abs_m":m_max,
        "max_abs_r":r_max, "b_min":b_min, "b_max":b_max,
        "theta_base_mean_abs":float(np.mean(np.abs(th_base))),
        "theta_late_mean_abs":float(np.mean(np.abs(th_late))),
        "theta_max_abs":float(np.max(np.abs(theta_hist))),
        "nan_count":int(np.isnan(V).sum()+np.isnan(theta_hist).sum()),
        "target_v":target_v.tolist(),
        "world_signature":(
            float(world["eta_env"][0,0]),
            float(world["eta_body"][10,1]),
            tuple(world["lesion_idx"].tolist()),
            tuple(world["p5_perm"].tolist())
        )
    }
