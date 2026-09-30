"""Teaching DDPM: train a small unconditional MNIST U-Net and sample.

See Lecture 16 for notation and limitations. Mathematical steps n=1..N
are stored at array indices i=n-1. No continuous-time interpolation is used.
"""
import argparse
import copy
import json
import math
from pathlib import Path
import time

import torch
from torch import nn
import torch.nn.functional as F


class Block(nn.Module):
    def __init__(self, inputs, outputs, time_dim=64):
        super().__init__()
        self.conv1 = nn.Conv2d(inputs, outputs, 3, padding=1)
        self.norm1 = nn.GroupNorm(4, outputs)
        self.time = nn.Linear(time_dim, outputs)
        self.conv2 = nn.Conv2d(outputs, outputs, 3, padding=1)
        self.norm2 = nn.GroupNorm(4, outputs)

    def forward(self, x, t):
        x = F.silu(self.norm1(self.conv1(x)))
        x = x + self.time(t)[:, :, None, None]
        return F.silu(self.norm2(self.conv2(x)))


class TinyUNet(nn.Module):
    """Two resolutions, a spatial skip connection, and a sinusoidal clock."""
    def __init__(self, width=32):
        super().__init__()
        self.width = width
        self.register_buffer('frequencies', torch.exp(torch.linspace(0, math.log(1000), 16)))
        self.time_mlp = nn.Sequential(nn.Linear(32, 64), nn.SiLU(), nn.Linear(64, 64))
        self.encoder = Block(1, width)
        self.middle = Block(width, 2*width)
        self.decoder = Block(3*width, width)
        self.output = nn.Conv2d(width, 1, 1)

    def forward(self, x, t):
        phase = t[:, None] * self.frequencies[None, :]
        emb = self.time_mlp(torch.cat([phase.sin(), phase.cos()], dim=1))
        skip = self.encoder(x, emb)                       # [B,w,28,28]
        low = self.middle(F.avg_pool2d(skip, 2), emb)     # [B,2w,14,14]
        up = F.interpolate(low, size=skip.shape[-2:], mode='nearest')
        return self.output(self.decoder(torch.cat([up, skip], dim=1), emb))


def make_schedule(steps=1000, device='cpu'):
    if steps < 2:
        raise ValueError('At least two diffusion steps are required.')
    # The default is the conventional 1000-step linear DDPM schedule.
    # Other lengths are allowed for code checks; they are different processes.
    beta = torch.linspace(1e-4, .02, steps, device=device)
    a = 1-beta
    bar = torch.cumprod(a, dim=0)
    previous = torch.cat([bar.new_ones(1), bar[:-1]])
    posterior_var = beta*(1-previous)/(1-bar)
    return dict(beta=beta, a=a, bar=bar, posterior_var=posterior_var)


def at(values, index):
    return values[index][:, None, None, None]


def noise_loss(model, x0, schedule):
    N = len(schedule['beta'])
    i = torch.randint(N, (len(x0),), device=x0.device)
    eps = torch.randn_like(x0)
    bar = at(schedule['bar'], i)
    xt = bar.sqrt()*x0+(1-bar).sqrt()*eps
    # i=0 represents mathematical n=1; t=(i+1)/N is always positive.
    eps_hat = model(xt, (i.float()+1)/N)
    return F.mse_loss(eps_hat, eps)


@torch.no_grad()
def sample(model, schedule, count=64, method='ddpm', ddim_steps=50, seed=123):
    device = next(model.parameters()).device
    generator = torch.Generator(device=device).manual_seed(seed)
    x = torch.randn(count, 1, 28, 28, device=device, generator=generator)
    model.eval()
    N = len(schedule['beta'])
    if method == 'ddpm':
        for i in range(N-1, -1, -1):
            eps = model(x, x.new_full((count,), (i+1)/N))
            mean = (x-schedule['beta'][i]/(1-schedule['bar'][i]).sqrt()*eps)/schedule['a'][i].sqrt()
            x = mean
            if i > 0:
                x = x+schedule['posterior_var'][i].sqrt()*torch.randn(x.shape, device=device, generator=generator)
    elif method == 'ddim':
        if not 2 <= ddim_steps <= N:
            raise ValueError('DDIM steps must be between 2 and the trained schedule length.')
        indices = torch.linspace(N-1, 0, ddim_steps).round().long().tolist()
        for k, i in enumerate(indices):
            eps = model(x, x.new_full((count,), (i+1)/N))
            bar = schedule['bar'][i]
            x0_hat = (x-(1-bar).sqrt()*eps)/bar.sqrt()
            j = indices[k+1] if k+1 < len(indices) else -1
            next_bar = schedule['bar'][j] if j >= 0 else x.new_tensor(1.)
            x = next_bar.sqrt()*x0_hat+(1-next_bar).sqrt()*eps
    else:
        raise ValueError(method)
    return x


def save_checkpoint(path, model, ema, optimizer, schedule, updates, seed):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(dict(model=model.state_dict(), ema=ema.state_dict(),
                    optimizer=optimizer.state_dict(), schedule={k:v.cpu() for k,v in schedule.items()},
                    updates=updates, seed=seed, width=model.width,
                    prediction='noise', time='t=(index+1)/N; data at 0',
                    normalization='2 * pixel[0,1] - 1', variance='fixed posterior',
                    torch_version=str(torch.__version__)), path)


def load_checkpoint(path, device='cpu'):
    state = torch.load(path, map_location=device, weights_only=True)
    if state['prediction'] != 'noise' or state['variance'] != 'fixed posterior':
        raise ValueError('Incompatible checkpoint conventions.')
    model = TinyUNet(state['width']).to(device)
    model.load_state_dict(state['ema'])
    model.eval()
    return model, state['schedule']


def train(args):
    from torchvision import datasets, transforms
    torch.manual_seed(args.seed)
    device = torch.device(args.device)
    data = datasets.MNIST(args.data, train=True, download=True,
                          transform=transforms.Compose([transforms.ToTensor(), transforms.Normalize((.5,),(.5,))]))
    if args.subset:
        data = torch.utils.data.Subset(data, range(min(args.subset, len(data))))
    loader = torch.utils.data.DataLoader(data, batch_size=args.batch_size, shuffle=True, num_workers=0)
    model = TinyUNet().to(device)
    ema = copy.deepcopy(model).eval().requires_grad_(False)
    optimizer = torch.optim.Adam(model.parameters(), lr=2e-4)
    schedule = make_schedule(args.steps, device)
    started = time.perf_counter()
    updates = 0
    while updates < args.updates:
        for x0, _ in loader:  # Labels are unused: this is unconditional generation.
            loss = noise_loss(model, x0.to(device), schedule)
            optimizer.zero_grad()
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.)
            optimizer.step()
            with torch.no_grad():
                for target, source in zip(ema.parameters(), model.parameters()):
                    target.lerp_(source, .001)
            updates += 1
            if updates % 100 == 0:
                print(json.dumps(dict(update=updates, loss=loss.item(), seconds=round(time.perf_counter()-started,1))), flush=True)
            if updates % 1000 == 0 or updates == args.updates:
                save_checkpoint(args.checkpoint, model, ema, optimizer, schedule, updates, args.seed)
            if updates == args.updates:
                break


def smoke(args):
    """Exercise gradients, schedule, checkpoint round-trip and both samplers."""
    torch.manual_seed(args.seed)
    model = TinyUNet(width=8)
    schedule = make_schedule(20)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    x0 = torch.randn(4,1,28,28).clamp(-1,1)
    loss = noise_loss(model, x0, schedule)
    loss.backward()
    assert torch.isfinite(loss) and all(torch.isfinite(p.grad).all() for p in model.parameters() if p.grad is not None)
    optimizer.step()
    assert schedule['posterior_var'][0] == 0
    assert torch.all(schedule['bar'][1:] < schedule['bar'][:-1])
    # Verify the two algebraic forms of the reverse mean agree.
    i=7; b=schedule['beta'][i]; a=schedule['a'][i]; bar=schedule['bar'][i]; prev=schedule['bar'][i-1]
    eps=torch.randn_like(x0); estimate=(x0-(1-bar).sqrt()*eps)/bar.sqrt()
    mean1=(x0-b/(1-bar).sqrt()*eps)/a.sqrt()
    mean2=prev.sqrt()*b/(1-bar)*estimate+a.sqrt()*(1-prev)/(1-bar)*x0
    assert torch.allclose(mean1,mean2,atol=2e-6)
    save_checkpoint(args.checkpoint,model,model,optimizer,schedule,1,args.seed)
    restored, loaded_schedule = load_checkpoint(args.checkpoint)
    probe=torch.full((4,),.5)
    assert torch.equal(model(x0,probe),restored(x0,probe))
    for method in ['ddpm','ddim']:
        result=sample(restored,loaded_schedule,count=4,method=method,ddim_steps=10)
        assert result.shape==(4,1,28,28) and torch.isfinite(result).all()
        assert torch.equal(result,sample(restored,loaded_schedule,count=4,method=method,ddim_steps=10))
    print(json.dumps(dict(status='passed', loss=loss.item(), checks='gradient, posterior mean, schedule, checkpoint, DDPM, DDIM, repeatability')))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['train','sample','smoke'])
    parser.add_argument('--checkpoint',default='runs/mnist-ddpm.pt')
    parser.add_argument('--data',default='data')
    parser.add_argument('--device',default='cpu',choices=['cpu','cuda'])
    parser.add_argument('--seed',type=int,default=20260930)
    parser.add_argument('--steps',type=int,default=1000)
    parser.add_argument('--updates',type=int,default=10000)
    parser.add_argument('--batch-size',type=int,default=64)
    parser.add_argument('--subset',type=int,default=0)
    parser.add_argument('--method',default='ddpm',choices=['ddpm','ddim'])
    parser.add_argument('--ddim-steps',type=int,default=50)
    parser.add_argument('--count',type=int,default=64)
    parser.add_argument('--output',default='samples.png')
    args=parser.parse_args()
    if args.updates<1 or args.batch_size<1 or args.count<1 or args.subset<0:
        parser.error('updates, batch size and count must be positive; subset must be nonnegative')
    torch.set_num_threads(2)
    if args.command=='train':
        train(args)
    elif args.command=='smoke':
        smoke(args)
    else:
        from torchvision.utils import save_image
        model,schedule=load_checkpoint(args.checkpoint,args.device)
        x=sample(model,schedule,args.count,args.method,args.ddim_steps,args.seed)
        # Save raw samples first. Clamping below is only for the display image.
        output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True)
        torch.save(x.cpu(),output.with_suffix('.pt'))
        save_image(((x+1)/2).clamp(0,1),output,nrow=8)


if __name__=='__main__':
    main()
