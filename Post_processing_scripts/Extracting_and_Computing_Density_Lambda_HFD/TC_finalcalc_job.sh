#!/bin/bash


#$ -q  long                                       # Specify queue
#$ -pe smp 8                                      # Specify number of cores to use.
#$ -N  DIR_INDEX_NPT_TC_finalcalc                 # Specify job name


export OMP_NUM_THREADS=${NSLOTS}
python thermal_sim_extract.py
python thermal_cond_finalcalc.py


output_dir="/scratch365/bagbodek/Heat_Flux_Decomposition_et_Structural_analysis/TC_corr_HFD_final_outputs/"


cp  kappa_value_DIR_INDEX.txt  kappa_value_abserror_DIR_INDEX.txt      avefluxes_one_left.DIR_INDEX_reshape_HFD.0.0035.profile $output_dir
cp  avefluxes_one_right.DIR_INDEX_reshape_HFD.0.0035.profile           avefluxes_one_ce_left.DIR_INDEX_reshape_HFD.0.0035.profile $output_dir
cp  avefluxes_one_ce_right.DIR_INDEX_reshape_HFD.0.0035.profile  $output_dir
