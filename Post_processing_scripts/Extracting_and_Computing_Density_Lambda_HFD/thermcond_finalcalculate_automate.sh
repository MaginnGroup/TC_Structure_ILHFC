#!/bin/bash
for k in $(cat labels_make_data.txt)

do

cd  /scratch365/bagbodek/Heat_Flux_Decomposition_et_Structural_analysis/"$k"


cp    ../thermal_sim_extract.py    ../thermal_cond_finalcalc.py    ../TC_finalcalc_job.sh    .



sed -i "s/DIR_INDEX/""$k""/g" thermal_sim_extract.py
sed -i "s/DIR_INDEX/""$k""/g" thermal_cond_finalcalc.py



sed -i "s/DIR_INDEX/""$k""/g" TC_finalcalc_job.sh


qsub TC_finalcalc_job.sh 



done