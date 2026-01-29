#!/bin/bash

parent_dir=/scratch365/bagbodek/Heat_Flux_Decomposition_et_Structural_analysis/

for k in $(cat labels_HFD_ILHFC_mixonly.txt)
do

cd    $parent_dir/$k

[ -d ""$k"_PyLAT_Diff_Gr" ] || mkdir ""$k"_PyLAT_Diff_Gr"
#mkdir ""$k"_PyLAT_Diff_Gr"

cp -r ../src ../compile.sh ../compile.py ../PyLAT.py ../PyLAT_Diff_gr_jobsubmit.sh  $parent_dir/$k/"$k"_PyLAT_Diff_Gr

cp "$k"_reshape_HFD.lammpstrj_1 "$k"_reshape_HFD.lammpstrj_2 "$k"_reshape_HFD.lammpstrj_3 $parent_dir/$k/"$k"_PyLAT_Diff_Gr
cp  "$k"_reshape_HFD.log "$k".data $parent_dir/$k/"$k"_PyLAT_Diff_Gr

cd   $parent_dir/$k/"$k"_PyLAT_Diff_Gr


#sed -i "s/INDEX/""$k""/g" PyLAT_Diff_gr_jobsubmit.sh
#sed -i '50 s/.*/timestep        1.0/' "$k"_NVT_Cv_statepoint.log


HFC_mol_name=$(echo "$k" | awk -F'[_]' '{print $1;}')
HFC_mol_number=$(echo "$k" | awk -F'[_]' '{print $3;}')
IL_mol_number=$(echo "$k" | awk -F'[_]' '{print $4;}')


sed -i "s/DIR_INDEX/""$k""/g" PyLAT_Diff_gr_jobsubmit.sh
sed -i "s/HFC_NAME_INDEX/""$HFC_mol_name""/g" PyLAT_Diff_gr_jobsubmit.sh
sed -i "s/HFC_NUM_INDEX/""$HFC_mol_number""/g" PyLAT_Diff_gr_jobsubmit.sh
sed -i "s/IL_NUM_INDEX/""$IL_mol_number""/g" PyLAT_Diff_gr_jobsubmit.sh

sed -i 's/${simulationtimestep}/1/g' "${k}_reshape_HFD.log"



qsub PyLAT_Diff_gr_jobsubmit.sh


done