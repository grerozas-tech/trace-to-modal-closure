from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT=(Path(__file__).resolve().parents[2] / "results")
OUT=Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)


def summary(folder,name):
    return pd.read_csv(ROOT/folder/name)

def val(df,key,col='mean'):
    keycol=df.columns[0]
    r=df[df[keycol]==key]
    if len(r)!=1:
        raise KeyError((key,name if 'name' in globals() else ''))
    return float(r.iloc[0][col])

def panel(ax, letter, title):
    ax.text(-0.12,1.20,letter,transform=ax.transAxes,fontweight='bold',fontsize=11,va='top')
    ax.set_title(title,fontsize=8,pad=8)
    ax.tick_params(labelsize=8)

# FIG 1
fig,axs=plt.subplots(2,2,figsize=(7.2,5.8))
d=summary('main','reactor_same_present_history_geometry_confirmatory_summary.csv')
axs[0,0].bar(['history','shuffle'],[val(d,'true_rsa'),val(d,'label_shuffle_rsa')])
axs[0,0].set_ylabel('response RSA')
panel(axs[0,0],'A','Common-present history geometry')
d=summary('main','reactor_distributed_trace_architecture_confirmatory_summary.csv')
labels=['r amp','m RSA','K RSA','gh RSA']
vals=[val(d,'R_amp_ratio_over_MGH')/10,val(d,'M_rsa'),val(d,'K_rsa'),val(d,'GH_rsa')]
axs[0,1].bar(labels,vals); axs[0,1].axhline(0,linewidth=.8); axs[0,1].set_ylabel('scaled amplitude / RSA')
panel(axs[0,1],'B','Distributed historical support')
d=summary('main','reactor_contextual_trace_reactivation_confirmatory_summary.csv')
axs[1,0].bar(['full','r','K','m','gh'],[val(d,'FULL_interaction_fraction'),val(d,'R_interaction_fraction'),val(d,'K_interaction_fraction'),val(d,'M_interaction_fraction'),val(d,'GH_interaction_fraction')])
axs[1,0].set_ylabel('interaction fraction')
panel(axs[1,0],'C','History × present interaction')
d=summary('main','reactor_multi_trace_K_superposition_confirmatory_summary.csv')
axs[1,1].bar(['correct span','wrong span','older trace'],[val(d,'K_span_r2'),val(d,'K_wrong_span_r2'),val(d,'K_old_trace_fraction')])
axs[1,1].set_ylim(0,1.05); axs[1,1].set_ylabel('R² / coefficient fraction')
panel(axs[1,1],'D','Coexistence of two historical traces')
fig.tight_layout(); fig.savefig(OUT/'fig1_history_trace.pdf',bbox_inches='tight'); fig.savefig(OUT/'fig1_history_trace.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# FIG 2
fig,axs=plt.subplots(2,2,figsize=(7.2,5.8))
d=summary('main','reactor_K_storage_superposition_nonlinear_readout_confirmatory_summary.csv')
axs[0,0].bar(['state error','response error','nonadditivity'],[val(d,'state_error'),val(d,'response_match_error'),val(d,'actual_nonadditivity')]); axs[0,0].set_ylabel('relative magnitude')
panel(axs[0,0],'A','Additive K storage, nonlinear response')
d=summary('main','reactor_K_readout_nonlinearity_localization_confirmatory_summary.csv')
axs[0,1].bar(['row norm','centered','b'],[val(d,'scores_relres'),val(d,'centered_relres'),val(d,'b_relres')]); axs[0,1].set_ylabel('relative residual')
panel(axs[0,1],'B','Localization of readout nonlinearity')
axs[1,0].bar(['native action','additive-b'],[val(d,'a_relres'),val(d,'ADDB_a_relres')]); axs[1,0].set_yscale('log'); axs[1,0].set_ylabel('action residual (log)')
panel(axs[1,0],'C','Additive-b intervention collapses residual')
axs[1,1].axis('off'); axs[1,1].text(.5,.55,r'$b_i=\sigma\{12[\|K_i\|-\mathrm{median}_j\|K_j\|]\}$',ha='center',va='center',fontsize=12); axs[1,1].text(.5,.32,'approximately additive storage\n+ collective relative readout',ha='center',va='center',fontsize=9)
panel(axs[1,1],'D','Operational readout rule')
fig.tight_layout(); fig.savefig(OUT/'fig2_storage_readout.pdf',bbox_inches='tight'); fig.savefig(OUT/'fig2_storage_readout.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# FIG 3
fig,axs=plt.subplots(2,3,figsize=(9,5.8))
d=summary('main','reactor_native_written_field_hysteresis_confirmatory_summary.csv')
axs[0,0].bar(['cycle','flat','difference'],[val(d,'CYCLE_resp_mean_pair_dist'),val(d,'FLAT_resp_mean_pair_dist'),val(d,'CYCLE_minus_FLAT_resp_mean_pair_dist')]); axs[0,0].set_ylabel('pairwise response distance')
panel(axs[0,0],'A','Finite operational hysteresis')
d=summary('main','reactor_mx_memory_relay_confirmatory_summary.csv')
axs[0,1].bar(['x→m 12','x→m probe','m→x loss','asym.'],[val(d,'x_to_m_after12_relay'),val(d,'x_to_m_probe_relay'),val(d,'m_to_x_decay'),val(d,'directional_asymmetry')]); axs[0,1].set_ylabel('relay effect')
panel(axs[0,1],'B','Bidirectional causal relay')
d=summary('main','reactor_return_aligned_residual_attenuation_confirmatory_summary.csv')
axs[0,2].bar(['G1 rescue','G2 rescue','G3 norm','G3 direction'],[val(d,'g1_rescue'),val(d,'g2_rescue'),val(d,'g3_RETURN_ALIGNED_x_norm_ratio'),val(d,'g3_RETURN_ALIGNED_x_cosine')]); axs[0,2].set_ylabel('effect / ratio / cosine')
axs[0,2].tick_params(axis='x',rotation=20,labelsize=6)
panel(axs[0,2],'C','Direction can survive amplitude collapse')
d=summary('main','reactor_full_loop_operator_gain_confirmatory_summary.csv')
axs[1,0].bar(['q_cal σ₁(T)','q_test σ₁(T)','q_cal finite','q_test finite'],[val(d,'G0_sigma1'),val(d,'G1_sigma1'),val(d,'G0_finite_top_gain_mean'),val(d,'G1_finite_top_gain_mean')]); axs[1,0].axhline(1,linestyle='--',linewidth=.8); axs[1,0].set_ylim(0,1.05); axs[1,0].set_ylabel('gain')
raw=pd.read_csv(ROOT/'main'/'reactor_full_loop_operator_gain_confirmatory_results.csv')
for j,col in enumerate(['G0_sigma1','G1_sigma1','G0_finite_top_gain_mean','G1_finite_top_gain_mean']):
    x=j+np.linspace(-.10,.10,len(raw)); axs[1,0].scatter(x,raw[col],s=5,alpha=.35)
axs[1,0].tick_params(axis='x',rotation=25,labelsize=6)
panel(axs[1,0],'D','Native full-loop contraction')
d=summary('main','reactor_loop_half_operator_factorization_confirmatory_summary.csv')
axs[1,1].bar(['σ₁(A)','σ₁(B)','A·B','efficiency'],[val(d,'G0_sigmaA'),val(d,'G0_sigmaB'),val(d,'G0_perfect_interface_bound'),val(d,'G0_interface_efficiency')]); axs[1,1].set_ylabel('q_cal metric')
raw=pd.read_csv(ROOT/'main'/'reactor_loop_half_operator_factorization_confirmatory_results.csv')
for j,col in enumerate(['G0_sigmaA','G0_sigmaB','G0_perfect_interface_bound','G0_interface_efficiency']):
    x=j+np.linspace(-.10,.10,len(raw)); axs[1,1].scatter(x,raw[col],s=5,alpha=.30)
panel(axs[1,1],'E','Write bottleneck and interface loss')
axs[1,2].axis('off'); axs[1,2].annotate('',xy=(.82,.55),xytext=(.55,.55),arrowprops={'arrowstyle':'->'}); axs[1,2].annotate('',xy=(.45,.55),xytext=(.18,.55),arrowprops={'arrowstyle':'->'}); axs[1,2].text(.1,.55,'x',ha='center',va='center',fontsize=14); axs[1,2].text(.5,.55,'m',ha='center',va='center',fontsize=14); axs[1,2].text(.9,.55,"x'",ha='center',va='center',fontsize=14); axs[1,2].text(.31,.66,'A',ha='center'); axs[1,2].text(.68,.66,'B',ha='center'); axs[1,2].text(.5,.25,'causal return path ≠ regenerative recurrence',ha='center',fontsize=9)
panel(axs[1,2],'F','Operational decomposition')
fig.tight_layout(); fig.savefig(OUT/'fig3_reentry.pdf',bbox_inches='tight'); fig.savefig(OUT/'fig3_reentry.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# FIG 4
fig,axs=plt.subplots(2,3,figsize=(9,5.8))
d=summary('main','reactor_loop_mode_drift_confirmatory_summary.csv')
axs[0,0].plot(d['generation'],d['inherited_norm_mean'],marker='o',label='inherited'); axs[0,0].plot(d['generation'],d['reoriented_norm_mean'],marker='o',label='reoriented'); axs[0,0].legend(fontsize=7); axs[0,0].set_ylabel('packet norm'); axs[0,0].set_xlabel('generation')
panel(axs[0,0],'A','Gain alone does not preserve inherited packets')
d=summary('main','reactor_optimal_mode_stationarity_confirmatory_summary.csv')
axs[0,1].bar(d['generation'].astype(str),d['mean_abs_cos']); axs[0,1].set_ylim(.98,1.0); axs[0,1].set_ylabel('|cos(vg,vg+1)|')
panel(axs[0,1],'B','Dominant mode is nearly stationary')
d=summary('main','reactor_compatibility_imprint_operator_explanation_confirmatory_seed_summary.csv')
axs[0,2].bar(['norm corr','vector cos','rel norm err'],[d['norm_corr'].mean(),d['vector_cos'].mean(),d['mean_relative_norm_error'].mean()]); axs[0,2].set_ylim(0,1.05)
panel(axs[0,2],'C','Local operator predicts compatibility imprint')
d=pd.read_csv(ROOT/'main'/'reactor_native_m_mode_correction_diagnostic_replication.csv')
axs[1,0].bar(['native-no m','aligned-native'],[d['native_minus_no_m'].mean(),d['aligned_minus_native'].mean()]); axs[1,0].axhline(0,linewidth=.8); axs[1,0].set_ylabel('diagnostic effect')
for j,col in enumerate(['native_minus_no_m','aligned_minus_native']):
    x=j+np.linspace(-.08,.08,len(d)); axs[1,0].scatter(x,d[col],s=10,alpha=.6)
panel(axs[1,0],'D','No reliable native autocorrection')
d=summary('main','reactor_native_mode_competition_confirmatory_summary.csv')
axs[1,1].bar(['input','memory','return'],[float(d.iloc[0]['input_share']),float(d.iloc[0]['m_share_mean']),float(d.iloc[0]['x_share_mean'])]); axs[1,1].set_ylim(0,1); axs[1,1].set_ylabel('compatible share')
panel(axs[1,1],'E','Selection during one transit')
d=pd.read_csv(ROOT/'main'/'reactor_loop_input_output_mode_mismatch_confirmatory_diagnostics.csv')
axs[1,2].bar(['|u₁·v₁|','(σ₁/ρ)/3','nonnorm.'],[d.iloc[0]['mean_u1_v1_abs_cos'],d.iloc[0]['mean_sigma1_over_spectral_radius']/3,d.iloc[0]['mean_normalized_nonnormality']]); axs[1,2].set_ylabel('scaled metric')
panel(axs[1,2],'F','Input-output mismatch and non-normality')
fig.tight_layout(); fig.savefig(OUT/'fig4_selection.pdf',bbox_inches='tight'); fig.savefig(OUT/'fig4_selection.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# FIG 5
fig,axs=plt.subplots(2,2,figsize=(7.2,5.8))
d=summary('main','reactor_native_modal_closure_coproduct_confirmatory_summary.csv')
sub=d[d['condition'].isin(['ALL_NONX','ALL_SLOW'])]
axs[0,0].bar(sub['condition'],sub['mean_gain_ratio']); axs[0,0].axhline(1,linestyle='--',linewidth=.8); axs[0,0].set_ylim(.995,1.005); axs[0,0].set_ylabel('gain ratio')
panel(axs[0,0],'A','Native co-products do not rescue closure')
axs[0,1].axis('off'); axs[0,1].text(.5,.72,r'$A=U_A\Sigma_A V_A^T$',ha='center',fontsize=11); axs[0,1].text(.5,.53,r'$B=U_B\Sigma_B V_B^T$',ha='center',fontsize=11); axs[0,1].text(.5,.34,r'$H=\Sigma_B V_B^T U_A\Sigma_A$',ha='center',fontsize=11); axs[0,1].text(.5,.15,r'$C_{dyn}=V_A V_H U_H^T U_B^T$',ha='center',fontsize=11)
panel(axs[0,1],'B','Effective causal factorization')
d=summary('main','reactor_dynamic_half_channel_closure_map_confirmatory_summary.csv')
r=d.iloc[0]
raw=pd.read_csv(ROOT/'main'/'reactor_dynamic_half_channel_closure_map_confirmatory_results.csv')
labels=['identity','static','dynamic','wrong seed']; cols=['identity_abs_cos','static_own_abs_cos','dynamic_own_abs_cos','dynamic_wrong_abs_cos']
axs[1,0].bar(labels,[raw[c].mean() for c in cols]); axs[1,0].set_ylim(0,1.05); axs[1,0].set_ylabel('test-context |cos|')
for j,c in enumerate(cols):
    axs[1,0].scatter(j+np.linspace(-.11,.11,len(raw)),raw[c],s=5,alpha=.35)
panel(axs[1,0],'C','Calibration-to-test transfer')
cols2=['dynamic_minus_static','dynamic_minus_wrong','dynamic_need_abs_error']; labels2=['vs static','vs wrong','need MAE']
axs[1,1].bar(labels2,[raw[c].mean() for c in cols2]); axs[1,1].set_ylabel('advantage / error')
for j,c in enumerate(cols2):
    axs[1,1].scatter(j+np.linspace(-.11,.11,len(raw)),raw[c],s=5,alpha=.35)
panel(axs[1,1],'D','Specificity of dynamic closure')
fig.tight_layout(); fig.savefig(OUT/'fig5_closure.pdf',bbox_inches='tight'); fig.savefig(OUT/'fig5_closure.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# FIG 6
fig,axs=plt.subplots(2,2,figsize=(7.2,5.8))
d=summary('main','reactor_fixed_instance_closure_multigeneration_confirmatory_summary.csv')
raw=pd.read_csv(ROOT/'main'/'reactor_fixed_instance_closure_multigeneration_confirmatory_results.csv')
for cond,g in d.groupby('condition'):
    axs[0,0].plot(g['generation'],g['mean_norm_rel_initial'],marker='o',label=cond)
# show seedwise dispersion for the decisive same-gain contrast
for cond in ['FIXED_DYNAMIC','UNCORRECTED']:
    q=raw[raw['condition']==cond].groupby('generation')['norm_rel_initial'].quantile([.05,.95]).unstack()
    axs[0,0].fill_between(q.index,q[.05],q[.95],alpha=.10)
axs[0,0].set_xlabel('generation'); axs[0,0].set_ylabel('relative norm'); axs[0,0].legend(fontsize=6)
panel(axs[0,0],'A','Four-generation amplitude (5–95% bands)')
# fixed-dynamic pre/post closure alignment with seedwise 5–95% bands
g=d[d['condition']=='FIXED_DYNAMIC']; axs[0,1].plot(g['generation'][1:],g['mean_preclosure_align'][1:],marker='o',label='preclosure'); axs[0,1].plot(g['generation'][1:],g['mean_postclosure_align'][1:],marker='o',label='postclosure')
rf=raw[(raw['condition']=='FIXED_DYNAMIC') & (raw['generation']>0)]
for col in ['preclosure_align_vA','postclosure_align_vA']:
    q=rf.groupby('generation')[col].quantile([.05,.95]).unstack(); axs[0,1].fill_between(q.index,q[.05],q[.95],alpha=.10)
axs[0,1].set_ylim(0,1.05); axs[0,1].legend(fontsize=7); axs[0,1].set_xlabel('generation'); axs[0,1].set_ylabel('|cos|')
panel(axs[0,1],'B','Closure restores reusable geometry')
d2=summary('main','reactor_fixed_closure_modal_attractor_confirmatory_summary.csv')
raw2=pd.read_csv(ROOT/'main'/'reactor_fixed_closure_modal_attractor_confirmatory_results.csv')
for angle,g in d2[(d2['condition']=='FIXED_DYNAMIC') & (d2['angle_deg']<90)].groupby('angle_deg'):
    axs[1,0].plot(g['generation'],g['mean_share'],marker='o',label=f'{angle:g}°')
    rr=raw2[(raw2['condition']=='FIXED_DYNAMIC') & (raw2['angle_deg']==angle)]
    q=rr.groupby('generation')['share'].quantile([.05,.95]).unstack(); axs[1,0].fill_between(q.index,q[.05],q[.95],alpha=.08)
axs[1,0].set_ylim(0,1.02); axs[1,0].set_xlabel('generation'); axs[1,0].set_ylabel('compatible share'); axs[1,0].legend(fontsize=7)
panel(axs[1,0],'C','Projective purification (5–95% bands)')
g1=d2[(d2['condition']=='FIXED_DYNAMIC') & (d2['generation']==1) & (d2['angle_deg'].isin([67.5,90]))]
axs[1,1].bar([f'{x:g}°' for x in g1['angle_deg']],g1['mean_share']); axs[1,1].set_ylim(0,1); axs[1,1].set_ylabel('G1 compatible share')
seedangle=(raw2[(raw2['condition']=='FIXED_DYNAMIC') & (raw2['generation']==1) & (raw2['angle_deg'].isin([67.5,90]))].groupby(['seed','angle_deg'],as_index=False)['share'].mean())
for j,angle in enumerate([67.5,90]):
    yy=seedangle[seedangle['angle_deg']==angle]['share'].to_numpy(); axs[1,1].scatter(j+np.linspace(-.10,.10,len(yy)),yy,s=5,alpha=.35)
panel(axs[1,1],'D','Exact orthogonality is not immediately attracted')
fig.tight_layout(); fig.savefig(OUT/'fig6_regeneration.pdf',bbox_inches='tight'); fig.savefig(OUT/'fig6_regeneration.png',dpi=200,bbox_inches='tight'); plt.close(fig)

# Supplementary figures helper
# S1
fig,ax=plt.subplots(figsize=(5.5,3.6)); d=summary('supplementary','reactor_second_time_maladaptive_trace_confirmatory_summary.csv'); ax.bar(['intact same','no-r same','specificity'],[val(d,'INTACT_common_same_gain'),val(d,'NO_R_common_same_gain'),val(d,'INTACT_common_specificity')]); ax.axhline(0,linewidth=.8); ax.set_ylabel('second-encounter effect'); ax.set_title('Fig. S1 | Maladaptive second-encounter hypothesis fails',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS1_maladaptive_null.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS1_maladaptive_null.png',dpi=200,bbox_inches='tight'); plt.close(fig)
# S2
fig,ax=plt.subplots(figsize=(5.5,3.6)); d=summary('supplementary','reactor_trace_weight_continuation_confirmatory_summary.csv'); ax.bar(['max jump b','max jump a','median-rank b'],[val(d,'b_max_jump_fraction'),val(d,'a_max_jump_fraction'),val(d,'b_median_minus_rank_adv')*200]); ax.set_ylabel('scaled continuation metric'); ax.set_title('Fig. S2 | Collective readout is structured but continuous',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS2_continuation.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS2_continuation.png',dpi=200,bbox_inches='tight'); plt.close(fig)
# S3
fig,ax=plt.subplots(figsize=(5.5,3.6)); d=summary('supplementary','reactor_ascent_memory_at_turn_confirmatory_summary.csv'); ax.bar(['slow removed','fast removed','m removed','x removed'],[val(d,'RESET_SLOW_removed_fraction'),val(d,'RESET_FAST_removed_fraction'),val(d,'RESET_M_removed_fraction'),val(d,'RESET_X_removed_fraction')]); ax.set_ylabel('fraction removed'); ax.set_title('Fig. S3 | Turning-point support ablations',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS3_turn_ablation.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS3_turn_ablation.png',dpi=200,bbox_inches='tight'); plt.close(fig)
# S4
fig,ax=plt.subplots(figsize=(5.5,3.6)); d=summary('supplementary','reactor_m_to_x_return_alignment_confirmatory_summary.csv'); ax.bar(['write cos','write x','return x','return-scr.'],[val(d,'write_vs_native_cos_gain'),val(d,'write_vs_native_x_gain'),val(d,'return_vs_native_x_gain'),val(d,'return_vs_scrambled_x_gain')]); ax.set_ylabel('intervention effect'); ax.set_title('Fig. S4 | Partial alignment improves relay performance',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS4_partial_alignment.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS4_partial_alignment.png',dpi=200,bbox_inches='tight'); plt.close(fig)
# S5
fig,ax=plt.subplots(figsize=(5.5,3.6)); d=summary('supplementary','reactor_history_field_optimal_mode_stationarity_confirmatory_summary.csv'); ax.bar(['mean angle/10','max angle/10','projector','sigma spread'],[val(d,'mean_pairwise_angle_deg')/10,val(d,'max_pairwise_angle_deg')/10,val(d,'mean_projector_distance'),val(d,'sigma_rel_spread')]); ax.set_ylabel('scaled stationarity metric'); ax.set_title('Fig. S5 | Dominant mode is stable across historical fields',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS5_history_stationarity.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS5_history_stationarity.png',dpi=200,bbox_inches='tight'); plt.close(fig)
# S6
fig,ax=plt.subplots(figsize=(5.5,3.6)); d=summary('supplementary','reactor_m_compatibility_imprint_causal_decomposition_confirmatory_seed_summary.csv'); ax.bar(['native ρ','amp-only ρ','dir-only ρ'],[d['NATIVE_rho'].mean(),d['AMP_ONLY_rho'].mean(),d['DIR_ONLY_rho'].mean()]); ax.set_ylim(0,1); ax.set_ylabel('Spearman correlation'); ax.set_title('Fig. S6 | Compatibility signal is multiplexed',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS6_compatibility.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS6_compatibility.png',dpi=200,bbox_inches='tight'); plt.close(fig)
# S7
fig,axs=plt.subplots(1,2,figsize=(7.2,3.4)); common=[.230768,.127457,.160252,.118396]; axs[0].bar(['id','Proc.','ridge','state'],common); axs[0].set_ylabel('held-out |cos|'); axs[0].set_title('Common map diagnostic',fontsize=9); d=summary('supplementary','reactor_instance_specific_modal_closure_confirmatory_summary.csv'); r=d.iloc[0]; axs[1].bar(['own','identity','wrong'],[r.own_abs_cos_mean,r.identity_abs_cos_mean,r.wrong_seed_abs_cos_mean]); axs[1].set_ylim(0,1.05); axs[1].set_title('Instance-specific transfer',fontsize=9); fig.suptitle('Fig. S7 | Common closure fails; own-instance bridge transfers',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS7_common_vs_instance.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS7_common_vs_instance.png',dpi=200,bbox_inches='tight'); plt.close(fig)
# S8
fig,axs=plt.subplots(1,2,figsize=(7.2,3.4)); d=summary('supplementary','reactor_scale_invariant_write_read_reciprocity_confirmatory_summary.csv'); axs[0].bar(d['condition'],d['mean_closure_gain']); axs[0].tick_params(axis='x',rotation=25,labelsize=7); axs[0].set_ylabel('closure gain'); axs[0].set_title('Static reciprocity',fontsize=9); d=summary('supplementary','reactor_write_read_subspace_factorization_confirmatory_summary.csv'); axs[1].bar(d['condition'],d['mean_u1_v1_abs_cos']); axs[1].tick_params(axis='x',rotation=25,labelsize=7); axs[1].set_ylabel('|u₁·v₁|'); axs[1].set_title('Subspace / memory-basis matching',fontsize=9); fig.suptitle('Fig. S8 | Static architectural explanations are insufficient',fontsize=10); fig.tight_layout(); fig.savefig(OUT/'figS8_static_failures.pdf',bbox_inches='tight'); fig.savefig(OUT/'figS8_static_failures.png',dpi=200,bbox_inches='tight'); plt.close(fig)

print('generated',len(list(OUT.glob('*.pdf'))),'pdf figures')
