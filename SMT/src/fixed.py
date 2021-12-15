from z3 import *
from time import time
from utils import *
import numpy as np
from math import ceil, floor


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

i_max = np.argmax(areas)  # index of the circuit with the biggest area
max_length = sum(lengths)  # worst-case plate length: circuits are on top of each other
min_length = ceil(sum(areas) / plate_width);  # best-case plate length: no empty space between circuits

#############
# VARIABLES #
#############
xs = [Int(f'x{i}') for i in range(n_circuits)]
ys = [Int(f'y{i}') for i in range(n_circuits)]
plate_length = max_z3([ys[i] + lengths[i] for i in range(n_circuits)])

###############
# CONSTRAINTS #
###############
containment = [
    And(
        xs[i] >= 0, 
        ys[i] >= 0,
        xs[i] + widths[i] <= plate_width
    ) 
    for i in range(n_circuits)
]
no_overlap = [
    Or(
        xs[i] + widths[i]  <= xs[j],  # i is on the left of j
        xs[j] + widths[j]  <= xs[i],  # i is on the right of j
        ys[i] + lengths[i] <= ys[j],  # i is below j
        ys[j] + lengths[j] <= ys[i]   # i is above j
    ) 
    for i in range(n_circuits) for j in range(n_circuits) if i < j
]
cumulative_x = cumulative(xs, widths, lengths, max_length)
cumulative_y = cumulative(ys, lengths, widths, plate_width)

# place the biggest-area circuit in the bottom-left region of the plate
bottom_left_x = [xs[i_max] <= floor((plate_width - widths[i_max]) / 2)]
bottom_left_y = [ys[i_max] <= floor((min_length - lengths[i_max]) / 2)]

main_constraints = containment + no_overlap
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
# store results #
#################
#model_name = 'base'
#model_name = 'implied'
model_name = 'symmetry'

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
