#!/bin/bash

#$ -q *long                                             # Specify queue
#$ -pe smp 16                                           # Specify number of cores to use.
#$ -N DIR_INDEX_Cluster_Analysis                                # Specify job name




export OMP_NUM_THREADS=${NSLOTS}

python extract_frames_run.py

cp NVTComplete_02_DIR_INDEX_averaged_clust_df.csv "/scratch365/bagbodek/Heat_Flux_Decomposition_et_Structural_analysis/Collated_Clust_df_all/"




