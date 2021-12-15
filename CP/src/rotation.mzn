include "globals.mzn";
%include "gecode.mzn";

%%%%%%%%
% DATA %
%%%%%%%%
int: plate_width;
int: n_circuits;
int: n_shapes;

set of int: CIRCUITS   = 1..n_circuits;
set of int: SHAPES     = 1..n_shapes;
set of int: DIMENSIONS = 1..2;

array[CIRCUITS] of int:          widths;
array[CIRCUITS] of int:          lengths;
array[SHAPES,DIMENSIONS] of int: sizes;
array[SHAPES,DIMENSIONS] of int: offsets;
array[SHAPES] of set of int:     shapes;
array[CIRCUITS] of set of int:   valid_shapes;

array[CIRCUITS] of int: areas            = [widths[i] * lengths[i] | i in CIRCUITS];
array[CIRCUITS] of int: ORDERED_CIRCUITS = reverse(arg_sort(areas)); % circuit indexes ordered by decreasing areass

int: i_max      = ORDERED_CIRCUITS[1]; % index of the circuit with the biggest area
int: max_length = sum(i in CIRCUITS)(max([widths[i], lengths[i]])); % worst-case plate length: circuits are all vertically oriented and on top of each other
int: min_length = ceil(sum(areas) / plate_width); % best-case plate length: no empty space between circuits

%%%%%%%%%%%%%
% VARIABLES %
%%%%%%%%%%%%%
set of int: POSITIONS = 0..max(plate_width - min(widths++lengths), max_length - min(widths++lengths));

array[CIRCUITS,DIMENSIONS] of var POSITIONS: positions;
array[CIRCUITS] of var SHAPES:               actual_shapes;

array[CIRCUITS] of var int: ws = [sizes[actual_shapes[i],1] | i in CIRCUITS]; % widths of the chosen oriented circuits
array[CIRCUITS] of var int: ls = [sizes[actual_shapes[i],2] | i in CIRCUITS]; % lengths of the chosen oriented circuits
array[CIRCUITS] of var int: xs = [positions[i,1] | i in CIRCUITS];
array[CIRCUITS] of var int: ys = [positions[i,2] | i in CIRCUITS];

var int: plate_length = max(i in CIRCUITS)(ys[i] + ls[i]);

%%%%%%%%%%%%%%%%%%%%
% MAIN CONSTRAINTS %
%%%%%%%%%%%%%%%%%%%%
constraint max(i in CIRCUITS)(xs[i] + ws[i]) <= plate_width;           % circuits do not exceed the plate widths
constraint geost(2, sizes, offsets, shapes, positions, actual_shapes); % circuits do not overlap
constraint forall(i in CIRCUITS)(actual_shapes[i] in valid_shapes[i]); % each circuit is assigned to one of its two shapes

%%%%%%%%%%%%%%%%%%%%%%%
% IMPLIED CONSTRAINTS %
%%%%%%%%%%%%%%%%%%%%%%%
constraint cumulative(xs, ws, ls, max_length);  % implied cumulative constraint along x...
constraint cumulative(ys, ls, ws, plate_width); % ...and  y axes

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SYMMETRY-BREAKING CONSTRAINTS %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
constraint xs[i_max] <= (plate_width - ws[i_max]) div 2; % symmetry-breaking constraints: the biggest circuit...
constraint ys[i_max] <= (min_length - ls[i_max]) div 2;  % ...is placed in the bottom-left region of the plate

solve
%:: int_search(xs, input_order, indomain_min)
%:: int_search(ys, input_order, indomain_min)

%:: int_search(xs, dom_w_deg, indomain_min)
%:: int_search(ys, dom_w_deg, indomain_min)

%:: int_search(xs, input_order, indomain_random)
%:: int_search(ys, input_order, indomain_random)

%:: int_search(xs, dom_w_deg, indomain_random)
%:: int_search(ys, dom_w_deg, indomain_random)

%:: int_search(xs, dom_w_deg, indomain_random)
%:: int_search(ys, dom_w_deg, indomain_min)
%:: restart_luby(1000)
%:: relax_and_reconstruct(x, 80)

%:: int_search([xs[i] | i in ORDERED_CIRCUITS], input_order, indomain_min)
%:: int_search([ys[i] | i in ORDERED_CIRCUITS], input_order, indomain_min)

%:: int_search([xs[i] | i in ORDERED_CIRCUITS], input_order, indomain_random)
%:: int_search([ys[i] | i in ORDERED_CIRCUITS], input_order, indomain_min)
%:: restart_luby(1000)
%:: relax_and_reconstruct(xs, 80)
minimize plate_length;

output ["\(plate_width) \(plate_length)\n\(n_circuits)\n"] ++ 
       ["\(ws[i]) \(ls[i]) \(xs[i]) \(ys[i])\n" | i in CIRCUITS];