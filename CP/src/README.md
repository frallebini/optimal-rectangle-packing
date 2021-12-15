# VLSI — CP Model

Tested with Python 3.8.5 and MiniZinc 2.5.3.

## How to run MiniZinc models yourself

1. Open  [`vlsi.mzp`](vlsi.mzp) in the MiniZinc IDE.
2. Go to `MiniZinc > Solver configurations` and select either the [`gecode`](gecode.mpc) or [`chuffed`](chuffed.mpc) custom configuration.
3. To run the fixed-orientation model, run [`fixed.mzn`](fixed.mzn) with one of the `.dzn` files from [`ins/`](ins/) as data.

    To run the rotation model, run [`rotation.mzn`](rotation.mzn) with one of the `.dzn` files from [`ins_rot/`](ins_rot/) as data.

## Where to find solutions of the *best* model–search combinations
Go to [`../out`](../out/): you will find two folders with naming convention `modelName_solver_variableOrdering_valueOrdering/`. Each of those folders contains `.txt` files storing the solutions produced under 5 minutes by the corresponding model–search combination — the best-performing fixed-orientation and rotation one, respectively. The solution of instance [`../../ins/ins-i.txt`](../../ins/) is called `out-i.txt`.

## Where to find raw outputs and statistics of *all* tests run by us
Go to [`stats/`](stats/): you will find text files storing the (copy-pasted) output produced by the MiniZinc IDE when running a specific model–search combination. Such combination is encoded in the file name, which follows the convention `modelName_solver_variableOrdering_valueOrdering.txt`.

## How to generate solution visualizations of the *best* model–search combinations
1. Run [`save_sol.py`](save_sol.py).
2. Go to [`../out_img`](../out_img/): you will find two folders with naming convention `modelName_solver_variableOrdering_valueOrdering/`. Each of those folders contains `.pdf` images showing the solutions produced under 5 minutes by the corresponding model–search combination — the best-performing fixed-orientation and rotation one, respectively. The image showing the solution of instance [`../../ins/ins-i.txt`](../../ins/) is called `out-i.pdf`.

## How to generate solutions and solution visualizations of *other* model–search combinations
1. Open [`save_sol.py`](save_sol.py)
2. At the end of the file, there is a list of `modelName_solver_variableOrdering_valueOrdering` names: uncomment the name(s) corresponding to the model–search combination(s) you are interested in. The two already uncommented names are those of the best-performing fixed-orientation and rotation model–search combinations, respectively.
3. Run [`save_sol.py`](save_sol.py).
4. Go to [`../out`](../out/): you will find three (or more) folders with naming convention `modelName_solver_variableOrdering_valueOrdering/`. Each of those folders contains `.txt` files storing the solutions produced under 5 minutes by the corresponding model–search combinations (the two best-performing ones and the one(s) you selected). The solution of instance [`../../ins/ins-i.txt`](../../ins/) is called `out-i.txt`.
    
    Go to [`../out_img`](../out_img/): you will find one (or more) folders with naming convention `modelName_solver_variableOrdering_valueOrdering/`. Each of those folders contains `.pdf` images showing the solutions produced under 5 minutes by the corresponding model–search combinations (the one(s) you selected). The image showing the solution of instance [`../../ins/ins-i.txt`](../../ins/) is called `out-i.pdf`.
    