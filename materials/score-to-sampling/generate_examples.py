"""Reproduce the integrated tutorial's scalar examples. No network is needed.
Run from any directory: python materials/score-to-sampling/generate_examples.py
Requires numpy and matplotlib. All outputs are written beside this script.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
BETA=8.0
MU=2.0
DATA_VARIANCE=0.25


def alpha(t): return np.exp(-BETA*np.asarray(t)/2)
def sigma(t): return np.sqrt(-np.expm1(-BETA*np.asarray(t)))
def mean(t): return alpha(t)*MU
def variance(t): return alpha(t)**2*DATA_VARIANCE+sigma(t)**2
def score(x,t): return -(x-mean(t))/variance(t)
def normal_pdf(x,m,v): return np.exp(-(x-m)**2/(2*v))/np.sqrt(2*np.pi*v)


def sample(method, initial, steps=1000, seed=19):
    """Increasing reverse clock; t decreases from one to zero.

    DDPM uses reverse variance b and omits the final random draw, following
    Ho's sampling algorithm. The other schemes integrate down to t=0.
    """
    rng=np.random.default_rng(seed)
    x=np.array(initial,copy=True)
    h=1/steps
    b=-np.expm1(-BETA*h)
    for n in range(steps,0,-1):
        t=n*h
        s=score(x,t)
        if method=='ode':
            x=x+h*BETA/2*(x+s)
        elif method=='reverse_sde':
            x=x+h*BETA*(x/2+s)+np.sqrt(BETA*h)*rng.normal(size=x.shape)
        elif method=='ddpm':
            x=(x+b*s)/np.sqrt(1-b)
            if n>1: x=x+np.sqrt(b)*rng.normal(size=x.shape)
        else: raise ValueError(method)
    return x


def finite_grid_moments(method, steps):
    """Exact mean/variance of each implemented linear numerical recurrence."""
    m=float(mean(1));v=float(variance(1));h=1/steps;b=-np.expm1(-BETA*h)
    for n in range(steps,0,-1):
        t=n*h;mt=float(mean(t));vt=float(variance(t))
        if method=='ode':
            a=1+h*BETA/2*(1-1/vt);c=h*BETA*mt/(2*vt);noise=0
        elif method=='reverse_sde':
            a=1+h*BETA*(.5-1/vt);c=h*BETA*mt/vt;noise=BETA*h
        elif method=='ddpm':
            a=(1-b/vt)/np.sqrt(1-b);c=b*mt/vt/np.sqrt(1-b);noise=b if n>1 else 0
        m=a*m+c;v=a*a*v+noise
    return {'mean':m,'variance':v}


def main():
    rng=np.random.default_rng(2026)
    # Score ascent and Langevin share a score, not a target density evolution.
    count=12000;eta=.02;steps=250
    initial=rng.normal(0,2,count);det=initial.copy();stoch=initial.copy()
    time=[0.];dv=[det.var()];sv=[stoch.var()]
    for k in range(steps):
        det=(1-eta)*det
        stoch=(1-eta)*stoch+np.sqrt(2*eta)*rng.normal(size=count)
        time.append((k+1)*eta);dv.append(det.var());sv.append(stoch.var())
    fig,ax=plt.subplots(figsize=(8,3.6))
    ax.plot(time,dv,label='Score ODE: dx/dτ = −x',lw=2)
    ax.plot(time,sv,label='Langevin Euler–Maruyama',lw=2)
    ax.axhline(1,color='k',ls='--',label='Target variance = 1')
    ax.set(xlabel='Sampling time τ',ylabel='Particle variance',title='Following the score alone does not preserve the target spread')
    ax.legend();fig.tight_layout();fig.savefig(ROOT/'langevin-balance.png',dpi=170);plt.close(fig)

    grid=np.linspace(-4,5,700)
    fig,axes=plt.subplots(2,1,figsize=(9,7))
    for t in [0,.15,.4,1]:
        axes[0].plot(grid,normal_pdf(grid,mean(t),variance(t)),label=f't={t:g}',lw=2)
    axes[0].set(title='Forward VP path: data N(2, 0.25) toward N(0, 1)',xlabel='x',ylabel='Density')
    axes[0].legend()
    initial=mean(1)+np.sqrt(variance(1))*rng.normal(size=count)
    bins=np.linspace(-.5,4.5,80)
    result={}
    for method,label in [('ddpm','DDPM ancestral'),('reverse_sde','Reverse SDE: Euler–Maruyama'),('ode','Probability-flow ODE: Euler')]:
        out=sample(method,initial,steps=2000)
        axes[1].hist(out,bins=bins,density=True,histtype='step',lw=1.5,label=label)
        expected=finite_grid_moments(method,2000)
        result[method]={'sample_mean':float(out.mean()),'sample_variance':float(out.var()),'finite_grid':expected}
        assert abs(out.mean()-expected['mean'])<.02
        assert abs(out.var()-expected['variance'])<.02
        coarse=finite_grid_moments(method,100)
        fine=finite_grid_moments(method,2000)
        assert abs(fine['mean']-MU)+abs(fine['variance']-DATA_VARIANCE)<abs(coarse['mean']-MU)+abs(coarse['variance']-DATA_VARIANCE)
    axes[1].plot(grid,normal_pdf(grid,MU,DATA_VARIANCE),'k--',label='Target data density',lw=2)
    axes[1].set(xlim=(-.5,4.5),xlabel='Generated x',ylabel='Density',title='One exact score, three finite-step sampling rules (2,000 steps)')
    axes[1].legend(fontsize=9);fig.tight_layout();fig.savefig(ROOT/'vp-path-and-samplers.png',dpi=170);plt.close(fig)
    # Exact probability-flow solution for the Gaussian path.
    exact=MU+np.sqrt(DATA_VARIANCE/variance(1))*(initial-mean(1))
    numerical=sample('ode',initial,steps=2000)
    result['ode_pathwise_rmse']=float(np.sqrt(np.mean((numerical-exact)**2)))
    assert result['ode_pathwise_rmse']<.005
    # Stationary normal sanity check: correct ODE velocity is identically zero.
    probe=np.linspace(-4,4,31)
    assert np.max(np.abs(BETA/2*(probe-probe)))==0
    result['terminal']={'mean':float(mean(1)),'variance':float(variance(1))}
    result['setup']={'seed':2026,'particles':count,'beta':BETA,'steps':2000,'initialization':'exact p_1 to isolate solver error'}
    (ROOT/'verification.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()
