#!/bin/bash
for k in $(cat labels_HFD_ILHFC.txt)

do


cd    "$k"


mol=$(echo "$k" | awk -F'[_]' '{print $1;}')


cp kappa_value_"$k".txt kappa_value_abserror_"$k".txt "/scratch365/bagbodek/Heat_Flux_Decomposition_et_Structural_analysis/TC_corr_HFD_final_outputs/"

cp avefluxes_one_left."$k"_reshape_HFD.0.0035.profile avefluxes_one_right."$k"_reshape_HFD.0.0035.profile avefluxes_one_ce_left."$k"_reshape_HFD.0.0035.profile  avefluxes_one_ce_right."$k"_reshape_HFD.0.0035.profile  "/scratch365/bagbodek/Heat_Flux_Decomposition_et_Structural_analysis/TC_corr_HFD_final_outputs/"

cp avefluxes_one_ce_imp_left."$k"_reshape_HFD.0.0035.profile avefluxes_one_ce_imp_right."$k"_reshape_HFD.0.0035.profile  "/scratch365/bagbodek/Heat_Flux_Decomposition_et_Structural_analysis/TC_corr_HFD_final_outputs/"
 

cd ..


done



