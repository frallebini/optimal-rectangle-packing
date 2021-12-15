import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from z3 import *


def save_out_file(
    model_name, id, model, 
    n_circuits, plate_width, plate_length, widths, lengths, xs, ys,
    failed=False):
    
    Path(f'../out/{model_name}').mkdir(parents=True, exist_ok=True)
    if failed:
        Path(f'../out/{model_name}/failed').mkdir(parents=True, exist_ok=True)
    
    with open(f'../out/{model_name + ("/failed" if failed else "")}/out-{id}.txt', 'w') as f:
        f.write(f'{plate_width} {model.evaluate(plate_length)}\n{n_circuits}')
        for wi,li,xi,yi in zip(widths,lengths,xs,ys):
            f.write(f'\n{wi} {li} {model.evaluate(xi)} {model.evaluate(yi)}')


def savefig(model_name, id, failed=False):
    Path(f'../out_img/{model_name}').mkdir(parents=True, exist_ok=True)
    if failed:
        Path(f'../out_img/{model_name}/failed').mkdir(parents=True, exist_ok=True)
    
    lines = []
    with open(f'../../ins/ins-{id}.txt') as f:
        for line in f:
            lines.append(line)
    lines = [line.replace('\n','').split(' ') for line in lines]
    w = int(lines[0][0])
    n = int(lines[1][0])
    ws_ins = [int(line[0]) for line in lines[2:]]
    ls_ins = [int(line[1]) for line in lines[2:]]
    colors = list(range(n))

    lines = []
    with open(f'../out/{model_name + ("/failed" if failed else "")}/out-{id}.txt') as f:
        for line in f:
            lines.append(line)
    lines = [line.replace('\n','').split(' ') for line in lines]
    l = int(lines[0][1])
    ws_out = [int(line[0]) for line in lines[2:]]
    ls_out = [int(line[1]) for line in lines[2:]]
    xs = [int(line[2]) for line in lines[2:]]
    ys = [int(line[3]) for line in lines[2:]]

    ins = np.zeros((max(ls_ins),sum(ws_ins)))
    ins -= 1
    x = 0
    for i,(wi,li) in enumerate(zip(ws_ins,ls_ins)):
        ins[max(ls_ins)-li:max(ls_ins),x:x+wi] = colors[i]
        x += wi
    ins[ins==-1] = None

    out = np.zeros((l,w))
    out -= 1
    for i,(wi,li,xi,yi) in enumerate(zip(ws_out,ls_out,xs,ys)):
        out[l-yi-li:l-yi,xi:xi+wi] = colors[i]
    out[out==-1] = None
        
    fig, ax = plt.subplots(2, 1, figsize=(8,5), gridspec_kw={'height_ratios': [1,2]})
    fig.tight_layout(pad=1.8)

    x_labels = ['0'] + [''] * (sum(ws_ins)-1) + [str(sum(ws_ins))]
    y_labels = [str(max(ls_ins))] + [''] * (max(ls_ins)-1) + ['0']

    ax[0].set_xticks(list(np.arange(-0.5, sum(ws_ins)-0.5+1)))
    ax[0].set_yticks(list(np.arange(-0.5, max(ls_ins)-0.5+1)))
    ax[0].set_xticklabels(x_labels)
    ax[0].set_yticklabels(y_labels)
    ax[0].set_aspect('equal')
    ax[0].set_title('Instance')
    ax[0].imshow(ins, cmap='rainbow')
    ax[0].grid()

    x_labels = ['0'] + [''] * (w-1) + [str(w)]
    y_labels = [str(l)] + [''] * (l-1) + ['0']

    ax[1].set_xticks(list(np.arange(-0.5, w-0.5+1)))
    ax[1].set_yticks(list(np.arange(-0.5, l-0.5+1)))
    ax[1].set_xticklabels(x_labels)
    ax[1].set_yticklabels(y_labels)
    ax[1].set_aspect('equal')
    ax[1].set_title('Output')
    ax[1].imshow(out, cmap='rainbow')
    ax[1].grid()

    plt.savefig(f'../out_img/{model_name + ("/failed" if failed else "")}/out-{id}.pdf')
    plt.close()


def format_time(secs):
    if secs < 1:
        return f'{int(secs*1000)}msec'
    if secs < 60:
        res =  f'{secs:.3f}'.split('.')
        return f'{res[0]}s {int(res[1])}msec'
    res = f'{secs/60:2f}'.split('.')
    s = f'0.{res[1]}'
    return f'{res[0]}m {int(float(s)*60)}s'


def max_z3(vals):
  m = vals[0]
  for v in vals[1:]:
    m = If(v > m, v, m)
  return m


def cumulative(starts, durations, requirements, capacity, max_time=None):
    assert len(starts) == len(durations) == len(requirements)
    n_tasks = len(starts)
    if not max_time:
        max_time = sum(durations)
    timestep_req = [[
            If(And(starts[i] <= t, t < starts[i] + durations[i]), requirements[i], 0) 
        for i in range(n_tasks)] 
    for t in range(max_time)]
    return [sum(timestep_req[t]) <= capacity for t in range(max_time)]
