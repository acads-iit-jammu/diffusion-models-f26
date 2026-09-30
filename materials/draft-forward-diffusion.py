"""Forward Gaussian transition: exact densities and reproducible simulation."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parents[1] / 'tutorials' / 'figs'
rng = np.random.default_rng(20260930)
h, steps, n = .005, 200, 30000
beta = 8.0
x = rng.choice([-2., 2.], n) + .5*rng.standard_normal(n)
paths = [x[:12].copy()]
for _ in range(steps):
    x = np.exp(-beta*h/2)*x + np.sqrt(1-np.exp(-beta*h))*rng.standard_normal(n)
    paths.append(x[:12].copy())
expected_var = 1 + 3.25*np.exp(-beta*steps*h)
assert abs(x.mean()) < .035
assert abs(x.var()-expected_var) < .035

def normal(x, mu, var):
    return np.exp(-(x-mu)**2/(2*var))/np.sqrt(2*np.pi*var)
def density(x, t):
    var = 1-.75*np.exp(-beta*t)
    return .5*normal(x,-2*np.exp(-beta*t/2),var)+.5*normal(x,2*np.exp(-beta*t/2),var)

plt.rcParams.update({'font.size':11, 'svg.fonttype':'none',
 'svg.hashsalt':'draft-forward-diffusion', 'axes.spines.top':False,
 'axes.spines.right':False})
fig, axes = plt.subplots(1,3,figsize=(13,4),layout='constrained')
grid = np.linspace(-5,5,1201)
for t in [0,.075,.25,1]:
    axes[0].plot(grid,density(grid,t),label=f't = {t:g}')
axes[0].plot(grid,normal(grid,0,1),'k--',lw=1.4,label='Standard normal')
axes[0].set(title='Exact marginal densities',xlabel='Position x',ylabel='Density',xlim=(-4,4))
axes[0].legend(frameon=False,fontsize=9)
axes[1].plot(np.arange(steps+1)*h,np.array(paths),lw=.8,alpha=.8)
axes[1].set(title='12 simulated particle paths',xlabel='Time t',ylabel='Position',xlim=(0,1))
axes[2].hist(x,bins=65,density=True,color='#0072B2',alpha=.45,label='30,000 particles at t = 1')
axes[2].plot(grid,density(grid,1),color='#D55E00',label='Exact density at t = 1')
axes[2].plot(grid,normal(grid,0,1),'k--',label='Standard normal')
axes[2].set(title='Terminal population',xlabel='Position x',ylabel='Density',xlim=(-4,4))
axes[2].legend(frameon=False,fontsize=8)
for ax in axes: ax.grid(alpha=.15)
fig.savefig(out/'draft-forward-diffusion.svg',metadata={'Date':None})
fig.savefig('/tmp/draft-forward-diffusion.png',dpi=140)
print(f'Terminal mean: {x.mean():.5f}; variance: {x.var():.5f}; exact variance: {expected_var:.5f}')
