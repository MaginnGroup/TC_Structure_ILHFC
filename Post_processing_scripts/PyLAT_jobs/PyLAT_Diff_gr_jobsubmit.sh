#!/bin/bash

#$ -q *long                                             # Specify queue
#$ -pe smp 4                                            # Specify number of cores to use.
#$ -N DIR_INDEX_Diff_RDF                                # Specify job name




# --- DO NOT load system python ---
module purge

# --- Load conda module ---
module load conda



PYTHON="$HOME/.conda/envs/pylat310/bin/python"

echo "==== FORCED PYTHON ===="
$PYTHON --version
$PYTHON -c "import sys; print(sys.executable)"


echo "==== DEBUG: python resolution ===="
which $PYTHON || true
$PYTHON --version || true
$PYTHON -c "import sys; print('sys.executable =', sys.executable)" || true



$PYTHON compile.py


export OMP_NUM_THREADS=${NSLOTS}
module load python
$PYTHON PyLAT.py -c -d -g --mol HFC_NAME_INDEX --mol EMIM --mol TFSI --nummol HFC_NUM_INDEX --nummol IL_NUM_INDEX  --nummol IL_NUM_INDEX -f DIR_INDEX_Diff_RDF_1.json -v 2 DIR_INDEX_reshape_HFD.log DIR_INDEX.data DIR_INDEX_reshape_HFD.lammpstrj_1

$PYTHON PyLAT.py -c -d -g --mol HFC_NAME_INDEX --mol EMIM --mol TFSI --nummol HFC_NUM_INDEX --nummol IL_NUM_INDEX  --nummol IL_NUM_INDEX -f DIR_INDEX_Diff_RDF_2.json -v 2 DIR_INDEX_reshape_HFD.log DIR_INDEX.data DIR_INDEX_reshape_HFD.lammpstrj_2

$PYTHON PyLAT.py -c -d -g --mol HFC_NAME_INDEX --mol EMIM --mol TFSI --nummol HFC_NUM_INDEX --nummol IL_NUM_INDEX  --nummol IL_NUM_INDEX -f DIR_INDEX_Diff_RDF_3.json -v 2 DIR_INDEX_reshape_HFD.log DIR_INDEX.data DIR_INDEX_reshape_HFD.lammpstrj_3




