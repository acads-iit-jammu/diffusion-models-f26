"""Reproduce the four one-dimensional tutorial figures and numerical checks.

Requirements: Python 3, numpy, matplotlib.
Run from the repository root: python materials/one-dimensional-score-examples.py
Output: tutorials/figs/one-dimensional-*.svg
Brownian increments below are exact at grid times; the ODE paths are analytic.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / 'tutorials' / 'figs'
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False,
                     'axes.spines.right': False, 'svg.fonttype': 'none'})
COLORS = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']

def normal(x, mean=0., variance=1.):
    return np.exp(-(x-mean)**2/(2*variance))/np.sqrt(2*np.pi*variance)

def save(fig, name):
    fig.savefig(OUT / f'one-dimensional-{name}.svg', bbox_inches='tight')
    plt.close(fig)

# 1. Local arrows, trajectories, and the exactly transported density.
t = np.linspace(0, 2, 300)
x = np.linspace(-4, 4, 800)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), layout='constrained')
points = np.linspace(-3, 3, 13)
ax[0].quiver(points, np.zeros_like(points), -points, np.zeros_like(points),
             angles='xy', scale_units='xy', scale=4, color=COLORS[0], width=.008)
ax[0].axhline(0, color='0.7', lw=.7)
ax[0].set(xlim=(-3.5,3.5), ylim=(-.5,.5), yticks=[], xlabel='position x', title='Local arrows: v(x) = −x')
for x0 in [-3,-2,-1,1,2,3]: ax[1].plot(t, x0*np.exp(-t), lw=1.8)
ax[1].set(xlabel='time t', ylabel='position', title='Exact particle trajectories')
for time, color in zip([0,.5,1.], COLORS):
    ax[2].plot(x, normal(x, variance=np.exp(-2*time)), color=color, label=f't = {time:g}')
ax[2].set(xlabel='position x', ylabel='density qₜ(x)', title='Same mass, less spread')
ax[2].legend(frameon=False)
save(fig, 'ode')

# 2. Gaussian mixture density and its analytic marginal score.
m, a = 2., .8
x = np.linspace(-4, 4, 1000)
p = .5*normal(x,m,a*a)+.5*normal(x,-m,a*a)
s = (m*np.tanh(m*x/(a*a))-x)/(a*a)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6), layout='constrained')
ax[0].plot(x,p,color=COLORS[0]); ax[0].set(xlabel='position x',ylabel='target density p(x)',title='Two modes, nonzero spread')
ax[1].plot(x,s,color=COLORS[1]); ax[1].axhline(0,color='0.5',lw=.7)
ax[1].set(xlabel='position x',ylabel='score s(x)',title='Positive: right; negative: left')
save(fig, 'mixture')

# 3. Start both dynamics with N(0,4), target N(0,1).
t = np.linspace(0, 3, 400)
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8), layout='constrained')
ax[0].plot(t, 4*np.exp(-2*t),label='Score ODE',color=COLORS[1])
ax[0].plot(t, 1+3*np.exp(-2*t),label='Langevin SDE',color=COLORS[0])
ax[0].axhline(1,color='0.4',ls='--',label='Target variance')
ax[0].set(xlabel='time t',ylabel='population variance',title='Contraction versus balance')
ax[0].legend(frameon=False)
x = np.linspace(-6,6,1000)
for time,color in zip([0,.5,1.5],COLORS):
    ax[1].plot(x,normal(x,variance=4*np.exp(-2*time)),color=color,label=f't = {time:g}')
    ax[2].plot(x,normal(x,variance=1+3*np.exp(-2*time)),color=color,label=f't = {time:g}')
for pane,title in zip(ax[1:],['ODE density narrows','SDE density approaches target']):
    pane.plot(x,normal(x),color='0.25',ls='--',label='Target')
    pane.set(xlabel='position x',ylabel='density',title=title)
    pane.legend(frameon=False,fontsize=9)
save(fig, 'langevin')

# 4. Both start from N(0,1), with dX=dW and V_t=1+t.
rng = np.random.default_rng(20260929)
t = np.linspace(0,2,501); h=t[1]-t[0]
x0 = rng.normal(size=16)
paths = x0[:,None]+np.column_stack([np.zeros(16),np.cumsum(rng.normal(size=(16,len(t)-1))*np.sqrt(h),axis=1)])
flows = x0[:,None]*np.sqrt(1+t)
fig,ax=plt.subplots(1,3,figsize=(13,3.8),layout='constrained')
for i in range(16):
    ax[0].plot(t,paths[i],lw=.7,alpha=.7)
    ax[1].plot(t,flows[i],lw=.9,alpha=.7)
for pane,title in zip(ax[:2],['Brownian sample paths','Exact probability-flow paths']):
    pane.set(xlabel='time t',ylabel='position',title=title,ylim=(-5,5))
x=np.linspace(-6,6,1000)
for time,color in zip([0,1,2],COLORS): ax[2].plot(x,normal(x,variance=1+time),color=color,label=f't = {time}')
ax[2].set(xlabel='position x',ylabel='density pₜ(x)',title='Shared theoretical marginals')
ax[2].legend(frameon=False)
save(fig,'probability-flow')

# Independent numerical checks: density-PDE residual, score derivative,
# Monte Carlo Gaussian law, and Euler stationary variance recurrence.
x=np.linspace(-3,3,301); time=.4; eps=1e-5
mu,a,m0,V0=1.2,.8,-.3,1.7
m_t=lambda t:mu+np.exp(-t/a**2)*(m0-mu)
V_t=lambda t:a*a+(V0-a*a)*np.exp(-2*t/a**2)
q=lambda t:normal(x,m_t(t),V_t(t))
qt=(q(time+eps)-q(time-eps))/(2*eps)
z=x-m_t(time); V=V_t(time)
rhs=q(time)*(1/a**2-(x-mu)*z/(a*a*V)+z*z/V**2-1/V)
assert np.max(np.abs(qt-rhs))<1e-7
m,a=2.,.8
logp=lambda y:np.log(.5*normal(y,m,a*a)+.5*normal(y,-m,a*a))
assert np.max(np.abs((logp(x+eps)-logp(x-eps))/(2*eps)-(m*np.tanh(m*x/a**2)-x)/a**2))<1e-7
n=200000
initial=rng.normal(m0,np.sqrt(V0),n)
a=.8
sample=mu+np.exp(-time/a**2)*(initial-mu)+a*np.sqrt(1-np.exp(-2*time/a**2))*rng.normal(size=n)
assert abs(sample.mean()-m_t(time))<.012
assert abs(sample.var()-V_t(time))<.012
step=.2; variance=0.
for _ in range(500): variance=(1-step)**2*variance+2*step
assert abs(variance-1/(1-step/2))<1e-12
print('Generated four SVG figures; Gaussian PDE, mixture score, Gaussian simulation, and ULA checks passed.')
