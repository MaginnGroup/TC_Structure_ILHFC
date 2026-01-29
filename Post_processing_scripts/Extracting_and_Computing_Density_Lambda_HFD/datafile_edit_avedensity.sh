#!/bin/bash


a=$(cat ave_Vol_DIR_INDEX.txt)
length_cubic=$(awk -v A="$a" 'BEGIN { print A**0.33333333 ; exit 0}')


file_path="restart_DIR_INDEX_NPT_final.data"
search_pattern_1="xlo xhi"
search_pattern_2="ylo yhi"
search_pattern_3="zlo zhi"

# Use grep to search for the line containing the search pattern
matched_line_1=$(grep "$search_pattern_1" "$file_path")
matched_line_2=$(grep "$search_pattern_2" "$file_path")
matched_line_3=$(grep "$search_pattern_3" "$file_path")



replacement_line_1="0.00 length_cubic_for_update xlo xhi"
replacement_line_2="0.00 length_cubic_for_update ylo yhi"
replacement_line_3="0.00 length_cubic_for_update zlo zhi"



cp "restart_DIR_INDEX_NPT_final.data" "restart_DIR_INDEX_NPT_final_edit.data"



sed -i  "s/""$matched_line_1""/""$replacement_line_1""/" "restart_DIR_INDEX_NPT_final_edit.data"
sed -i  "s/""$matched_line_2""/""$replacement_line_2""/" "restart_DIR_INDEX_NPT_final_edit.data"
sed -i  "s/""$matched_line_3""/""$replacement_line_3""/" "restart_DIR_INDEX_NPT_final_edit.data"


sed -i "s/length_cubic_for_update/""$length_cubic""/g" "restart_DIR_INDEX_NPT_final_edit.data"

