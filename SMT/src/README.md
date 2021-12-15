# VLSI — SMT Model

Tested with Python 3.8.5 and Z3 4.8.10.0.

## How to run Z3 models yourself
1. To run the fixed-orientation model, run [`fixed.py`](fixed.py).

    To run the rotation model, run [`rotation.py`](rotation.py).
3. You will be asked to type the instance number among those in [`../../ins/`](../../ins/) to use as data for the model (from 1 to 40).
4. If a solution is successfully computed before the timeout (5 min), then it is stored — assuming you just ran model `modelName` on instance [`ins-i.txt`](../../ins/):
    *  In [`../out/modelName/out-i.txt`](../out/) as a text file.
    * In [`../out_img/modelName/out-i.pdf`](../out_img/) as a `.pdf` image.

## Where to find solutions of the *best* models
Go to [`../out`](../out/): you will find two folders named [`symmetry/`](../out/symmetry/) and [`symmetryRot/`](../out/symmetryRot/). Each of those folders contains `.txt` files storing the solutions produced under 5 minutes by the corresponding model — the best-performing fixed-orientation and rotation one, respectively. The solution of instance [`../../ins/ins-i.txt`](../../ins/) is called `out-i.txt`.

## Where to find statistics of *all* tests run by us
Go to [`stats/`](stats/): you will find text files storing the (copy-pasted) output produced by either [`fixed.py`](fixed.py) or [`rotation.py`](rotation.py)  when running a specific model. Each text file is named after the corresponding model.

## How to plot statistics
Run [`plot_stats.py`](plot_stats.py) and go to [`../plots/`](../plots/): you will find `.pdf` images showing comparisons between solving statistics of different models.