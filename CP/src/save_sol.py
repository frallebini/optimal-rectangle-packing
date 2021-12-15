import numpy as np
import matplotlib.pyplot as plt
from glob import iglob
import re
from pathlib import Path
from itertools import chain


def save_out(fname):
    with open(f'stats/{fname}.txt') as f:
        out = ''
        dir_name = fname.split("/")[-1]
        Path(f'../out/{dir_name}').mkdir(parents=True, exist_ok=True)
        found_sol = False
        
        for line in f:
            if line.startswith('Running'):
                out = ''
                id = re.findall(r'\d+', line.split(' ')[-1])[0]
            elif line[0].isdigit():
                out += line
            elif line.startswith('-'):
                found_sol = True
            elif 'Finished' in line:
                if found_sol:
                    if '4m 59s' in line or ('5m' in line and 'msec' not in line):
                        Path(f'../out/{dir_name}/failed').mkdir(parents=True, exist_ok=True)
                        fpath = f'../out/{dir_name}/failed/out-{id}.txt'
                    else: 
                        fpath = f'../out/{dir_name}/out-{id}.txt'
                    with open(fpath, 'w') as ff:
                        ff.write(out)
                    found_sol = False


def save_fig(dir_name):
    Path(f'../out_img/{dir_name}').mkdir(parents=True, exist_ok=True)
    if Path(f'../out/{dir_name}/failed').exists():
        Path(f'../out_img/{dir_name}/failed').mkdir(parents=True, exist_ok=True)
    
    for fpath in chain(iglob(f'../out/{dir_name}/*.txt'), iglob(f'../out/{dir_name}/failed/*.txt')):
        if 'failed' in fpath and 'failed' not in dir_name:
            dir_name += '/failed' 

        lines = []
        id = ''.join([char for char in fpath if char.isdigit()])
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
        with open(fpath) as f:
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

        plt.savefig(f'../out_img/{dir_name}/out-{id}.pdf')
        plt.close()


names = [
#    'base_gecode_inputOrder_indomainMin',
#    'implied_gecode_inputOrder_indomainMin',
#    'symmetry_gecode_inputOrder_indomainMin',
#    'symmetry_gecode_domWdeg_indomainMin',
#    'symmetry_gecode_inputOrder_indomainRandom',
#    'symmetry_gecode_domWdeg_indomainRandom',
#    'symmetry_gecode_domWdeg_randX_minY_luby',
#    'symmetry_gecode_domWdeg_randX_minY_luby_lns',
    'symmetry_gecode_orderedByArea_indomainMin',
#    'symmetry_gecode_orderedByArea_randX_minY_luby',
#    'symmetry_gecode_orderedByArea_randX_minY_luby_lns',
#    'symmetry_chuffed_default',
#    'symmetry_chuffed_orderedByArea_indomainMin',
#    'baseRot_gecode_inputOrder_indomainMin',
#    'impliedRot_gecode_inputOrder_indomainMin',
#    'symmetryRot_gecode_inputOrder_indomainMin',
#    'symmetryRot_gecode_domWdeg_indomainMin',
#    'symmetryRot_gecode_inputOrder_indomainRandom',
#    'symmetryRot_gecode_domWdeg_indomainRandom',
#    'symmetryRot_gecode_domWdeg_randX_minY_luby',
#    'symmetryRot_gecode_domWdeg_randX_minY_luby_lns',
#    'symmetryRot_gecode_orderedByArea_indomainMin',
#    'symmetryRot_gecode_orderedByArea_randX_minY_luby',
#    'symmetryRot_gecode_orderedByArea_randX_minY_luby_lns',
    'symmetryRot_chuffed_default',
#    'symmetryRot_chuffed_orderedByArea_indomainMin',
]
for name in names:
    save_out(name)
    save_fig(name)
