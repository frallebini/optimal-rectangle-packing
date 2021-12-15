include "globals.mzn";
%include "gecode.mzn";

%%%%%%%%
% DATA %
%%%%%%%%
int: plate_width;
int: n_circuits;

set of int: CIRCUITS = 1..n_circuits;

array[CIRCUITS] of int: widths;
array[CIRCUITS] of int: lengths;

array[CIRCUITS] of int: areas            = [widths[i] * lengths[i] | i in CIRCUITS];
array[CIRCUITS] of int: ORDERED_CIRCUITS = reverse(arg_sort(areas)); % circuit indexes ordered by decreasing areas

int: i_max      = ORDERED_CIRCUITS[1];            % index of the circuit with the biggest area
int: max_length = sum(lengths);                   % worst-case plate length: circuits are on top of each other
int: min_length = ceil(sum(areas) / plate_width); % best-case plate length: no empty space between circuits

%%%%%%%%%%%%%
% VARIABLES %
%%%%%%%%%%%%%
array[CIRCUITS] of var 0..plate_width - min(widths): xs;
array[CIRCUITS] of var 0..max_length - min(lengths): ys;

var int: plate_length = max(i in CIRCUITS)(ys[i] + lengths[i]);

%%%%%%%%%%%%%%%%%%%%
% MAIN CONSTRAINTS %
%%%%%%%%%%%%%%%%%%%%
constraint max(i in CIRCUITS)(xs[i] + widths[i]) <= plate_width; % circuits do not exceed the plate width
constraint diffn(xs, ys, widths, lengths);                       % circuits do not overlap

%%%%%%%%%%%%%%%%%%%%%%%
% IMPLIED CONSTRAINTS %
%%%%%%%%%%%%%%%%%%%%%%%
constraint cumulative(xs, widths, lengths, max_length);  % implied cumulative constraint along x...
constraint cumulative(ys, lengths, widths, plate_width); % ...and y axes

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SYMMETRY-BREAKING CONSTRAINTS %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
constraint xs[i_max] <= floor((plate_width - widths[i_max]) / 2); % symmetry-breaking constraints: the biggest circuit...
constraint ys[i_max] <= floor((min_length - lengths[i_max]) / 2); % ...is placed in the bottom-left region of the plate

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
%:: relax_and_reconstruct(xs, 80)

:: int_search([xs[i] | i in ORDERED_CIRCUITS], input_order, indomain_min)
:: int_search([ys[i] | i in ORDERED_CIRCUITS], input_order, indomain_min)
      
%:: int_search([xs[i] | i in ORDERED_CIRCUITS], input_order, indomain_random)
%:: int_search([ys[i] | i in ORDERED_CIRCUITS], input_order, indomain_min)
%:: restart_luby(1000)
%:: relax_and_reconstruct(xs, 80)
minimize plate_length;

output ["\(plate_width) \(plate_length)\n\(n_circuits)\n"] ++ 
       ["\(widths[i]) \(lengths[i]) \(xs[i]) \(ys[i])\n" | i in CIRCUITS];