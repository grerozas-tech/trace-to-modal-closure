# Paper IV — Methods Audit v0.1

## Audit status

The core base reactor equations are verified directly from `reactor_v012.py`. The central confirmatory result tables are present. Several late-stage designs are recoverable exactly from the frozen tool code in this conversation but their standalone `.py`/prereg `.json` files are not currently mounted; these are treated as reproducibility gaps, not silently reconstructed facts.

## 1. Base C4 reactor verified from source

Dimensions: recurrent state \(x\in\mathbb R^{32}\), four modules of eight units; body/environment/action vectors \(s,e,a\in\mathbb R^4\); context \(c\in\mathbb R^8\); slow memory \(m\in\mathbb R^8\); plasticity \(\theta\in\mathbb R^4\); relevance \(r\in\mathbb R^{12}\); trace matrix \(K\in\mathbb R^{8\times4}\); boundary readout \(b\in\mathbb R^8\).

The base C4 update implemented in `reactor_v012.py` is:

\[
e_{t+1}=0.95e_t+0.03\eta^{env}_t+\mu_t,
\]

\[
c_t=S_e e_t+S_a a_t+\eta^c_t,\qquad u_t=[s_t;c_t],
\]

\[
V_t=\exp\!\left[-\frac{\|s_t\|^2}{2(0.35)^2}-0.05\|a_t\|^2\right],
\]

\[
r_t=0.98r_{t-1}+0.02\,u_{t-1}\Delta V_t,
\]

with normalized magnitude \(rr=|r|/\max|r|\) when nonzero and \(u^{eff}=u(1+0.5rr)\).

\[
W(\theta)=W_0+\sum_{k=1}^{4}\theta_k A_k,
\]

\[
K_t=0.98K_{t-1}+0.02\,c_t\zeta_{t-1}^{\top},
\]

\[
b_i=\sigma\!\left(12\left[\|K_i\|-\operatorname{median}_j\|K_j\|\right]\right),
\]

and \(p_t\) is an exponentially weighted summary of the last at most five module-mean vectors \(g\), with weights proportional to \(e^{-\mathrm{lag}/2}\).

\[
z_t=W(\theta_t)x_t+B u^{eff}_t+Mm_t+J_p p_t+J_r r_t+J_b b_t,
\]

\[
x_{t+1}=0.75x_t+0.25\tanh(z_t),
\]

\[
a_t=\operatorname{clip}\left[\tanh(0.8s_t)+0.25\tanh(g_t)+\zeta_t,-1,1\right],
\]

\[
m_{t+1}=0.98m_t+0.02P_mx_t.
\]

For C4 plasticity,

\[
\theta_{t+1}=
\operatorname{clip}\left[
\theta_t+0.002(v^\star-v_t)-0.004\theta_t+0.0005\,\Delta V_t p_t,\,
-0.25,0.25
\right].
\]

The base body update is

\[
s_{t+1}=A_s s_t-0.40a_t+0.25e_t+\eta^s_t.
\]

Paper IV uses the later rotational-relation branch in which the action term is replaced by the previously frozen \(R_4(\phi)a_t\) relation. The exact standalone source implementing \(R_4(\phi)\) is **not currently mounted** and must be restored before final Methods text is locked.

Fixed random matrices are generated independently per master seed. `W0` is sparse modular and rescaled to spectral radius 0.75. `M` and `Pm` are independently drawn, which is important for later write/read asymmetry experiments.

Noise scales in the verified base source are: environment standard normal before filtering; body noise SD 0.005; context noise SD 0.02; action noise \(\zeta\) SD 0.02.

## 2. Common-present intervention

The best-documented common-present protocol is T01. After 80-step exposures to 12 relations, the carrier from \(\phi=0\) supplies exactly common fast/current variables

\[
[s,e,x,a,\mathrm{prev\_u},\mathrm{prev\_z},\mathrm{prev\_v}],
\]

while the donor supplies only

\[
[m,\theta,r,K,b,gh].
\]

All branches then receive the same future relation \(\phi=0\) and identical future noise for eight steps. The response concatenates eight action vectors and eight recurrent increments \(dx\).

Later common-present experiments use related but not always identical retained/transplanted sets. A per-experiment variable table remains a required source-audit item.

## 3. Isolated reentry operators

The final Paper IV operator branch uses 24-step write and 24-step return windows.

The effective write operator is

\[
A_{\mathrm{eff}}
=
\frac{\partial m_{t+24}}{\partial x_t}
\in\mathbb R^{8\times32},
\]

and the effective return operator is

\[
B_{\mathrm{eff}}
=
\frac{\partial x_{t+48}}{\partial m_{t+24}}
\in\mathbb R^{32\times8}.
\]

They are estimated by central finite differences with \(\epsilon=10^{-4}\), using matched control branches and matched write/return noise. The full local loop is

\[
T_{\mathrm{eff}}=B_{\mathrm{eff}}A_{\mathrm{eff}}.
\]

Singular vectors are compared sign-invariantly using absolute cosine or projector distance.

## 4. Modal closure construction

With

\[
A=U_A\Sigma_A V_A^\top,\qquad
B=U_B\Sigma_B V_B^\top,
\]

define

\[
H=\Sigma_BV_B^\top U_A\Sigma_A.
\]

If

\[
H=U_H\Sigma_HV_H^\top,
\]

the externally reconstructed instance-specific closure is

\[
C_{\mathrm{dyn}}
=
V_AV_HU_H^\top U_B^\top.
\]

In Paper IV, this map is learned once in context A and tested in a distinct context B. It is not estimated or applied natively by the reactor.

## 5. Gain compensation and finite nonlinear relay

For the final regenerative intervention,

\[
\gamma_A=\frac{1}{\sigma_1(T_A)}
\]

is learned once in context A. In each test generation, the native 24-step write is run, only the written memory increment \(\Delta m\) is multiplied by fixed \(\gamma_A\), then the native 24-step return is run. The fixed closure map is applied to the returned \(x\) packet and renormalized to preserve that returned packet norm. No per-generation SVD, gain recalibration or closure recomputation is allowed.

The final confirmatory relay is tested for four generations, so manuscript language should say **finite-horizon regenerative reentry over four tested generations**, not asymptotic or autonomous stability.

## 6. Statistical practice

Paper IV does not use one universal inferential test. Designs are experiment-specific and frozen in advance of fresh confirmatory cohorts.

Common elements are:
- fresh 64-seed confirmatory cohorts after separate diagnostics for most major experiments;
- seed-level summaries as the experimental unit for many hypotheses;
- one-sided sign-flip tests with Holm correction in several earlier multi-hypothesis blocks;
- nonparametric bootstrap 95% intervals;
- preregistered effect-size thresholds and favorable-seed fractions;
- sign-invariant modal comparisons.

The final transcript-coded analyses often use 150,000 bootstrap resamples; exact resample counts and randomization algorithms for every earlier branch still require script-level audit.

## 7. Scope locks

Paper IV supports:
1. distributed, path-dependent historical traces;
2. contextual and relational readout;
3. causal x↔m reentry;
4. differential mode selection;
5. input-output mismatch and non-normality;
6. an externally identified instance-specific closure;
7. sufficiency of fixed closure plus fixed critical gain for four-generation regenerative reentry;
8. a projective basin for pre-existing compatible components.

Paper IV does **not** show that the native reactor learns \(C_i\), estimates \(\gamma_i\), autonomously regulates energy, is autopoietic, or is conscious.

The question of learning \(C_i,\gamma_i\) from lived causal consequences is Paper V.
