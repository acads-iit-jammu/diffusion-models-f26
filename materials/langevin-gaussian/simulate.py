"""Reproduce the Gaussian Langevin tutorial figures. Requires numpy, matplotlib."""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT=Path(__file__).resolve().parent
MU, VAR, M, T = 2., 4., 20000, 40.
SEED=20261023

def pdf(x, mean=MU, var=VAR):
    return np.exp(-(x-mean)**2/(2*var))/np.sqrt(2*np.pi*var)
def cdf(x):
    return np.array([.5*(1+math.erf((float(v)-MU)/np.sqrt(2*VAR))) for v in x])
def dm(x):
    f=cdf(np.sort(x));i=np.arange(1,len(x)+1)
    return float(max(np.max(i/len(x)-f),np.max(f-(i-1)/len(x))))
def simulate(eta, seed):
    rng=np.random.default_rng(seed); x=rng.normal(-3,1,M); d=x.copy()
    steps=round(T/eta); snaps={0:x.copy()}; paths=[x[:8].copy()]; det=[d[:8].copy()]
    means=[x.mean()]; variances=[x.var()]; dv=[d.var()]
    for k in range(1,steps+1):
        x += -eta*(x-MU)/VAR + np.sqrt(2*eta)*rng.normal(size=M)
        d += -eta*(d-MU)/VAR
        paths.append(x[:8].copy());det.append(d[:8].copy())
        means.append(x.mean());variances.append(x.var());dv.append(d.var())
        if any(np.isclose(k*eta,t) for t in [2,8,40]): snaps[int(round(k*eta))]=x.copy()
    A=1-eta/VAR; expected_mean=MU+A**steps*(-3-MU)
    expected_var=A**(2*steps)+2*eta*(1-A**(2*steps))/(1-A*A)
    assert abs(x.mean()-expected_mean)<6*np.sqrt(expected_var/M)
    assert abs(x.var()-expected_var)<6*expected_var*np.sqrt(2/(M-1))
    return dict(x=x,d=d,snaps=snaps,paths=np.array(paths),det=np.array(det),means=means,variances=variances,dv=dv,
                expected_mean=expected_mean,expected_var=expected_var)

runs={eta:simulate(eta,SEED+j) for j,eta in enumerate([1.,.5,.1])}
r=runs[.1];times=np.arange(len(r['paths']))*.1
fig,ax=plt.subplots(1,2,figsize=(11,3.6),sharey=True)
ax[0].plot(times,r['det']);ax[1].plot(times,r['paths'],alpha=.7)
for a,title in zip(ax,['Score ODE: no diffusion','Langevin SDE: fresh noise each step']):
    a.axhline(MU,color='black',ls='--',lw=1);a.set(xlabel='Sampling time τ',ylabel='Position',title=title)
fig.tight_layout();fig.savefig(OUT/'trajectories.png',dpi=160);plt.close(fig)
grid=np.linspace(-10,12,1000);bins=np.linspace(-14,18,100)
fig,axes=plt.subplots(1,4,figsize=(13,3),sharey=True)
for ax,t in zip(axes,[0,2,8,40]):
    ax.hist(r['snaps'][t],bins=bins,density=True,alpha=.5,label='Simulated particles')
    ax.plot(grid,pdf(grid),'k',label='Target N(2,4)')
    if t==0: m,v=-3,1
    else: m=MU-5*np.exp(-t/VAR);v=VAR+(1-VAR)*np.exp(-2*t/VAR)
    ax.plot(grid,pdf(grid,m,v),'--',color='tab:red',label='Exact SDE density')
    ax.set(xlim=(-8,10),xlabel='x',title=f'τ = {t}')
axes[0].legend(fontsize=7);fig.tight_layout();fig.savefig(OUT/'density-evolution.png',dpi=160);plt.close(fig)
fig,ax=plt.subplots(1,2,figsize=(10,3.5))
ax[0].plot(times,r['means'],label='Euler–Maruyama');ax[0].plot(times,MU-5*np.exp(-times/VAR),'k--',label='Exact SDE')
ax[0].axhline(MU,color='gray',ls=':');ax[0].set(title='Mean',xlabel='τ');ax[0].legend()
ax[1].plot(times,r['variances'],label='Euler–Maruyama')
ax[1].plot(times,VAR+(1-VAR)*np.exp(-2*times/VAR),'k--',label='Exact SDE')
ax[1].plot(times,r['dv'],label='Euler without noise')
ax[1].axhline(VAR,color='gray',ls=':');ax[1].set(title='Variance',xlabel='τ');ax[1].legend()
fig.tight_layout();fig.savefig(OUT/'moments.png',dpi=160);plt.close(fig)
fig,axes=plt.subplots(1,3,figsize=(12,3.5),sharey=True)
rows=[]
for ax,(eta,r) in zip(axes,runs.items()):
    ax.hist(r['x'],bins=bins,density=True,alpha=.5,label='Generated samples')
    ax.plot(grid,pdf(grid),'k',label='Target density')
    ax.plot(grid,pdf(grid,MU,VAR/(1-eta/(2*VAR))),'--',color='tab:red',label='Euler stationary density')
    ax.set(xlim=(-6,10),xlabel='x',title=f'η = {eta}')
    rows.append(dict(eta=eta,mean=float(r['x'].mean()),variance=float(r['x'].var(ddof=1)),D_M=dm(r['x']),expected_variance=r['expected_var']))
axes[0].legend(fontsize=8);fig.tight_layout();fig.savefig(OUT/'sampler-comparison.png',dpi=160);plt.close(fig)
rng=np.random.default_rng(SEED+100);reference=[dm(rng.normal(MU,np.sqrt(VAR),M)) for _ in range(20)]
result=dict(seed=SEED,particles=M,final_time=T,rows=rows,reference=dict(median=float(np.median(reference)),min=min(reference),max=max(reference)))
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
