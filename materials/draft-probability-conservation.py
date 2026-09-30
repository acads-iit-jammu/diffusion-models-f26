"""Particle simulations of fixed-interval flux and moving-interval conservation."""
from pathlib import Path
from math import erf
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out=Path(__file__).resolve().parents[1]/'tutorials'/'figs'
rng=np.random.default_rng(20260930)
n=80000
x0=rng.standard_normal(n)
t=np.linspace(0,1,201)
left,right=-.75,.75
cdf=lambda x: .5*(1+np.vectorize(erf)(np.asarray(x)/np.sqrt(2)))
phi=lambda x: np.exp(-np.asarray(x)**2/2)/np.sqrt(2*np.pi)
plt.rcParams.update({'font.size':11,'svg.fonttype':'none','svg.hashsalt':'conservation-simulation','axes.spines.top':False,'axes.spines.right':False})
for name in ['translation','contraction']:
    def flow(x,t): return x+2*t if name=='translation' else x*np.exp(-t)
    def pdf(x,t): return phi(x-2*t) if name=='translation' else np.exp(t)*phi(np.exp(t)*x)
    def velocity(x): return 2 if name=='translation' else -x
    moving=[]; fixed=[]; net=[]
    prev=None
    for instant in t:
        x=flow(x0,instant)
        inside=(x>=left)&(x<=right)
        fixed.append(inside.mean())
        moving.append(((x>=flow(left,instant))&(x<=flow(right,instant))).mean())
        if prev is not None:
            # Signed net crossings at each boundary; exact for these monotone paths.
            left_cross=np.count_nonzero((prev<left)&(x>=left))-np.count_nonzero((prev>=left)&(x<left))
            right_cross=np.count_nonzero((prev<right)&(x>=right))-np.count_nonzero((prev>=right)&(x<right))
            net.append((left_cross-right_cross)/n)
        prev=x
    fixed=np.array(fixed); moving=np.array(moving)
    cumulative=np.r_[0,np.cumsum(net)]
    flux=pdf(left,t)*velocity(left)-pdf(right,t)*velocity(right)
    integrated=np.r_[0,np.cumsum((flux[:-1]+flux[1:])*np.diff(t)/2)]
    assert np.ptp(moving)==0
    assert np.max(np.abs(cumulative-(fixed-fixed[0])))<1e-12
    assert np.max(np.abs(integrated-cumulative))<.012
    if name=='translation': exact=cdf(right-2*t)-cdf(left-2*t)
    else: exact=cdf(right*np.exp(t))-cdf(left*np.exp(t))
    assert np.max(abs(exact-fixed))<.012
    fig,ax=plt.subplots(2,2,figsize=(11,7.8),layout='constrained')
    grid=np.linspace(-4,5,1001)
    for a,instant in zip(ax[0],[0,1]):
        x=flow(x0,instant)
        a.hist(x,bins=np.linspace(-5,6,160),density=True,color='#777777',alpha=.25,label='Particle histogram')
        a.plot(grid,pdf(grid,instant),color='#222222',lw=1.6,label='Exact PDF')
        a.axvspan(left,right,color='#0072B2',alpha=.12,label='Fixed interval')
        ml,mr=flow(left,instant),flow(right,instant)
        a.fill_between(grid,0,pdf(grid,instant),where=(grid>=ml)&(grid<=mr),color='#D55E00',alpha=.35,label='Moving interval')
        for edge in [left,right]: a.axvline(edge,color='#0072B2',ls='--',lw=1)
        for edge in [ml,mr]: a.axvline(edge,color='#D55E00',ls=':',lw=1.5)
        a.set(title=f'Density and intervals at t = {instant}',xlabel='Position x',ylabel='Density',xlim=(-3.5,4.5),ylim=(0,1.2 if name=='contraction' else .48))
    ax[0,0].legend(frameon=False,fontsize=8,loc='upper right')
    ax[1,0].plot(t,fixed,color='#0072B2',lw=2,label='Fixed interval: simulated fraction')
    ax[1,0].plot(t,exact,'k--',lw=1,label='Fixed interval: exact probability')
    ax[1,0].plot(t,moving,color='#D55E00',lw=2,label='Moving interval: simulated fraction')
    ax[1,0].set(title='Probability contained in each interval',xlabel='Time t',ylabel='Probability',xlim=(0,1),ylim=(0,1))
    ax[1,0].legend(frameon=False,fontsize=8,loc='best')
    ax[1,1].plot(t,integrated,color='#009E73',lw=2.5,label='Integrated boundary flux')
    ax[1,1].plot(t,cumulative,color='#0072B2',ls='--',lw=1.5,label='Net crossings / particle count')
    ax[1,1].axhline(0,color='gray',lw=.6)
    ax[1,1].set(title='Change in fixed-interval probability',xlabel='Time t',ylabel='Change since t = 0',xlim=(0,1))
    ax[1,1].legend(frameon=False,fontsize=8,loc='best')
    for a in ax.flat: a.grid(alpha=.12)
    fig.suptitle('Constant field v(x) = 2' if name=='translation' else 'Contraction field v(x) = −x',fontsize=15)
    fig.savefig(out/f'draft-conservation-{name}.svg',metadata={'Date':None})
    fig.savefig(f'/tmp/draft-conservation-{name}.png',dpi=130)
    plt.close(fig)
    print(name, {'initial_fraction':fixed[0],'final_fixed_fraction':fixed[-1],'moving_fraction':moving[-1],'max_flux_discrepancy':float(np.max(abs(integrated-cumulative)))})
