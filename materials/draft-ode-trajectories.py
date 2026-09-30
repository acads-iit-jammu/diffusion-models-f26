"""Generate the trajectory figures for the opening draft ODE section.
Run with Python, NumPy, and Matplotlib. Outputs go to tutorials/figs/.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = Path(__file__).resolve().parents[1] / 'tutorials' / 'figs'
t = np.linspace(0, 1, 400)
initial_positions = [-3, -2, -1, 0, 1, 2, 3]
colors = ['#0072B2', '#D55E00', '#009E73', '#555555', '#CC79A7', '#8C510A', '#6A3D9A']
plt.rcParams.update({'font.size': 12, 'svg.fonttype': 'none',
                     'svg.hashsalt': 'draft-ode-trajectories',
                     'axes.spines.top': False, 'axes.spines.right': False})
for name, title, solution in [
    ('constant', r'Constant velocity: $v(x)=2$, $x(t)=x_0+2t$', lambda x0: x0+2*t),
    ('contraction', r'Contraction: $v(x)=-x$, $x(t)=x_0e^{-t}$', lambda x0: x0*np.exp(-t)),
]:
    fig, ax = plt.subplots(figsize=(8.4, 4.5), layout='constrained')
    for x0, color in zip(initial_positions, colors):
        label = rf'$x_0={x0}$'
        if name == 'contraction' and x0 == 0:
            label += ' (equilibrium)'
        ax.plot(t, solution(x0), color=color, lw=2,
                ls='--' if x0 == 0 else '-', label=label)
        ax.scatter([0], [x0], color=color, s=28, zorder=3, clip_on=False)
    ax.set(title=title, xlabel=r'Time $t$', ylabel=r'Position $x(t)$', xlim=(0,1))
    ax.set_xticks(np.linspace(0,1,5))
    ax.grid(alpha=.18)
    ax.legend(title='Starting position', loc='center left', bbox_to_anchor=(1.01,.5), frameon=False)
    fig.savefig(out / f'draft-ode-{name}-trajectories.svg', metadata={'Date': None})
    plt.close(fig)

# Density induced by the same exact trajectories, starting from N(0,1).
from matplotlib.colors import Normalize
snapshots = [0., .25, .5, 1.]
time = np.linspace(0, 1, 301)

def mixture0(x):
    """Equal mixture with means -2, +2 and component standard deviation 0.5."""
    a = 0.5
    return 0.5 * (np.exp(-0.5*((x+2)/a)**2) + np.exp(-0.5*((x-2)/a)**2)) / (a*np.sqrt(2*np.pi))

for name, extent, density in [
    ('constant', (-4, 8), lambda x, t: np.exp(-(x-2*t)**2/2)/np.sqrt(2*np.pi)),
    ('contraction', (-4, 4), lambda x, t: np.exp(t)*np.exp(-np.exp(2*t)*x*x/2)/np.sqrt(2*np.pi)),
    ('mixture-constant', (-4, 8), lambda x, t: mixture0(x-2*t)),
    ('mixture-contraction', (-4, 4), lambda x, t: np.exp(t)*mixture0(np.exp(t)*x)),
]:
    x = np.linspace(*extent, 1201)
    field = density(x[:, None], time[None, :])
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2), layout='constrained')
    for instant, color in zip(snapshots, colors):
        axes[0].plot(x, density(x, instant), color=color, lw=2, label=rf'$t={instant:g}$')
    axes[0].set(xlabel=r'Position $x$', ylabel=r'Density $p_t(x)$',
                title='PDF snapshots', xlim=extent)
    axes[0].set_ylim(bottom=0)
    axes[0].legend(frameon=False)
    axes[0].grid(alpha=.18)
    im = axes[1].pcolormesh(time, x, field, shading='auto', cmap='viridis',
                            norm=Normalize(vmin=0, vmax=float(field.max())), rasterized=True)
    axes[1].set(xlabel=r'Time $t$', ylabel=r'Position $x$', title='Density over time')
    fig.colorbar(im, ax=axes[1], label=r'Density $p_t(x)$')
    fig.savefig(out / f'draft-ode-{name}-densities.svg', metadata={'Date': None})
    plt.close(fig)
