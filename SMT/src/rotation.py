from z3 import *
from time import time
from utils import *
from pathlib import Path
import numpy as np
from math import ceil


########
# DATA #
########
id = input('Type instance number (1–40): ')
lines = []
with open(f'../../ins/ins-{id}.txt') as f:
    for line in f:
        lines.append(line)
lines = [line.replace('\n','').split(' ') for line in lines]

plate_width = int(lines[0][0])
n_circuits = int(lines[1][0])
widths = [int(line[0]) for line in lines[2:]]
lengths = [int(line[1]) for line in lines[2:]]
areas = np.array(widths) * np.array(lengths)

# index of the circuit with the biggest area
i_max = np.argmax(areas)
# worst-case plate lengths: circuits are all vertically oriented and on top of each other
max_length = sum([max(lengths[i], widths[i]) for i in range(n_circuits)])
# best-case plate length: no empty space between circuits
min_length = ceil(sum(areas) / plate_width)

#############
# VARIABLES #
#############
xs = [Int(f'x{i}') for i in range(n_circuits)]
ys = [Int(f'y{i}') for i in range(n_circuits)]
rot = [Bool(f'r{i}') for i in range(n_circuits)]
widths_rot = [Int(f'w{i}') for i in range(n_circuits)]
lengths_rot = [Int(f'l{i}') for i in range(n_circuits)]
plate_length = max_z3([ys[i] + lengths_rot[i] for i in range(n_circuits)])

###############
# CONSTRAINTS #
###############
square_rot = [
    Implies(widths[i] == lengths[i], Not(rot[i])) for i in range(n_circuits)
]
rect_rot = [
    And(
        Implies(rot[i], widths_rot[i] == lengths[i]),
        Implies(rot[i], lengths_rot[i] == widths[i]),
        Implies(Not(rot[i]), widths_rot[i] == widths[i]),
        Implies(Not(rot[i]), lengths_rot[i] == lengths[i])
    )
    for i in range(n_circuits)
]
containment = [
    And(
        xs[i] >= 0, 
        ys[i] >= 0,
        xs[i] + widths_rot[i] <= plate_width,
    ) 
    for i in range(n_circuits)
]
no_overlap = [
    Or(
        xs[i] + widths_rot[i]  <= xs[j],  # i is on the left of j
        xs[j] + widths_rot[j]  <= xs[i],  # i is on the right of j
        ys[i] + lengths_rot[i] <= ys[j],  # i is below j
        ys[j] + lengths_rot[j] <= ys[i]   # i is above j
    ) 
    for i in range(n_circuits) for j in range(n_circuits) if i < j
]
cumulative_x = cumulative(xs, widths_rot, lengths_rot, max_length, max_length)
cumulative_y = cumulative(ys, lengths_rot, widths_rot, plate_width, max_length)

# place the biggest-area circuit in the bottom-left region of the plate
bottom_left_x = [xs[i_max] <= (plate_width - widths_rot[i_max]) / 2]
bottom_left_y = [ys[i_max] <= (min_length - lengths_rot[i_max]) / 2]

main_constraints = square_rot + rect_rot + containment + no_overlap
implied_constraints = cumulative_x + cumulative_y
symmetry_breaking_constraints = bottom_left_x + bottom_left_y

#########
# SOLVE #
#########
opt = Optimize()
opt.set(timeout=300000)
opt.add(
    main_constraints
    + implied_constraints
    + symmetry_breaking_constraints
)
opt.minimize(plate_length) 
start_time = time()
res = opt.check()

print(f'Finished in {format_time(time() - start_time)}')
print(opt.statistics())

#################
# STORE RESULTS #
#################
#model_name = 'baseRot'
#model_name = 'impliedRot'
model_name = 'symmetryRot'

if res == sat:
    save_out_file(
        model_name, id, opt.model(), 
        n_circuits, plate_width, plate_length, widths, lengths, xs, ys)
    savefig(model_name, id)
elif res == unsat:
    print(res)
else:
    print(opt.reason_unknown())
    save_out_file(
        model_name, id, opt.model(), 
        n_circuits, plate_width, plate_length, widths, lengths, xs, ys,
        failed=True)
    savefig(model_name, id, failed=True)
