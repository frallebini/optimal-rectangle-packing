import matplotlib.pyplot as plt
from math import log10
from pathlib import Path


def collect_stats(model_name):
    with open(f'stats/{model_name}.txt') as f:
        model_time = {}
        model_conflicts = {}
        skip = False
        for line in f:
            if line.startswith('Type'):
                id = int(line.split()[-1])
                skip = False
            elif line.startswith('Finished'):
                time_str = line.split('in')[-1].strip()
                l = len(time_str.split())
                if l == 1:  # time expressed in msec
                    time = int(time_str.strip('msec'))
                elif l == 2:  # (sec + msec) or (min + sec)
                    t1, t2 = time_str.split()
                    if t1.endswith('s'):  # sec + msec
                        t1 = int(t1.strip('s')) * 1000
                        t2 = int(t2.strip('msec'))
                    elif t1.endswith('m'):  # min + sec
                        t1 = int(t1.strip('m')) * 60 * 1000
                        t2 = int(t2.strip('s')) * 1000
                    time = t1 + t2  # in msec
            elif ':conflicts' in line:
                conflicts = int(line.split()[-1])
            elif 'canceled' in line or 'unknown' in line:
                skip = True
            elif line == '\n' and not skip:
                model_time[id] = time
                model_conflicts[id] = conflicts
        return model_time, model_conflicts


def plot_stats(ids, ylabel, figname, **stats):
    xs = [str(i) for i in ids]
    plt.figure(figsize=(10, 5))
    for name, stat in stats.items():
        plt.plot(xs, [log10(stat[i]) for i in ids], '.-', label=name)
    plt.legend()
    plt.xlabel('Instance')
    plt.ylabel(ylabel)
    plt.tight_layout()
    Path(f'../plots').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'../plots/{figname}.pdf')
    plt.close()


base_time, base_conflicts = collect_stats('base')
implied_time, implied_conflicts = collect_stats('implied')
symmetry_time, symmetry_conflicts = collect_stats('symmetry')

ylabels = ['log10(Time) (ms)', 'log10(Conflicts)']
fignames = [
    'base_vs_impl_vs_sym_time', 
    'base_vs_impl_vs_sym_conflicts', 
    'impl_vs_sym_time', 
    'impl_vs_sym_conflicts'
]

common_ids = list(set(base_time.keys())
    .intersection(set(implied_time.keys()))
    .intersection(set(symmetry_time.keys())))
plot_stats(
    common_ids, ylabels[0], fignames[0], 
    base=base_time, implied=implied_time, symmetry=symmetry_time)
plot_stats(
    common_ids, ylabels[1], fignames[1], 
    base=base_conflicts, implied=implied_conflicts, symmetry=symmetry_conflicts)

common_ids = list(set(implied_time.keys())
    .intersection(set(symmetry_time.keys())))
plot_stats(
    common_ids, ylabels[0], fignames[2], 
    implied=implied_time, symmetry=symmetry_time)
plot_stats(
    common_ids, ylabels[1], fignames[3], 
    implied=implied_conflicts, symmetry=symmetry_conflicts)

baseRot_time, baseRot_conflicts = collect_stats('baseRot')
impliedRot_time, impliedRot_conflicts = collect_stats('impliedRot')
symmetryRot_time, symmetryRot_conflicts = collect_stats('symmetryRot')

fignames = [
    'baseRot_vs_implRot_vs_symRot_time', 
    'baseRot_vs_implRot_vs_symRot_conflicts', 
]

common_ids = list(set(baseRot_time.keys())
    .intersection(set(impliedRot_time.keys()))
    .intersection(set(symmetryRot_time.keys())))
plot_stats(
    common_ids, ylabels[0], fignames[0], 
    base_rot=baseRot_time, implied_rot=impliedRot_time, symmetry_rot=symmetryRot_time)
plot_stats(
    common_ids, ylabels[1], fignames[1], 
    base_rot=baseRot_conflicts, implied_rot=impliedRot_conflicts, symmetry_rot=symmetryRot_conflicts)
