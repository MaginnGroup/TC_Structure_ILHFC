#!/bin/bash
for j in $(cat labels_HFD_ILHFC_mixonly.txt)


do

k=$(echo "$j" | awk -F'[*]' '{print $1;}')

cd    "$k"


cp  ../compute_ion_clusters_perframe.py    ../extract_frames_4rm_traj.py     ../extract_frames_run.py  ../Cluster_analysis_job.sh  .



cut_off_var=$(echo "$j" | awk -F'[*]' '{print $2;}')


sed -i "s/DIR_INDEX/""$k""/g" Cluster_analysis_job.sh 


sed -i "s/CUTOFF_INDEX/""$cut_off_var""/g" extract_frames_run.py 
sed -i "s/DIR_INDEX/""$k""/g" extract_frames_run.py


qsub Cluster_analysis_job.sh 


cd ..


done



