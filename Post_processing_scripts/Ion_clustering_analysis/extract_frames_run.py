# -*- coding: utf-8 -*-
"""

"""

from extract_frames_4rm_traj import *
from compute_ion_clusters_perframe import *
import time
import glob
import pandas as pd
import os


traj_file = "DIR_INDEX_reshape_HFD.lammpstrj_1"
cutoff = CUTOFF_INDEX
nvt_data_file = "restart_NVTComplete_02_DIR_INDEX_reshape_HFD.data"



start_time = time.perf_counter()

output_dir_name = make_output_dir(traj_file, prefix="Ext_frms_")
n_extract_ = 100

extract_frames(
    traj_file=traj_file,
    n_extract=n_extract_,
    output_dir=output_dir_name
)

end_time = time.perf_counter()

elapsed = end_time - start_time

print("\nTiming information")
print("------------------")
print(f"Total wall time : {elapsed:.2f} s")
print(f"Frames extracted: {n_extract_}")
print(f"Time per frame  : {elapsed/n_extract_:.4f} s")





# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

clust_dfs = []

frame_files = sorted(
    glob.glob(os.path.join(output_dir_name, "frame_*.dat"))
)

print(f"\nFound {len(frame_files)} extracted frames for clustering")

for frame_file in frame_files:
    print(f"Processing {os.path.basename(frame_file)}")

    clust_df, singlets, com_df, atoms_df = clustering_analysis_single_frame(
        nvt_data_file,
        frame_file,
        cutoff
    )

    # Save per-frame cluster distribution
    frame_tag = os.path.splitext(os.path.basename(frame_file))[0]
    out_csv = os.path.join(
        output_dir_name,
        f"{frame_tag}_cluster_df.csv"
    )
    clust_df.to_csv(out_csv, index=False)

    # Keep for averaging
    clust_dfs.append(clust_df)


def average_cluster_dfs(cluster_dfs):
    aligned = [
        df.set_index("cluster_size")["count"]
        for df in cluster_dfs
    ]

    combined = pd.concat(aligned, axis=1).fillna(0)
    combined["avg_count"] = combined.mean(axis=1)

    return combined[["avg_count"]].reset_index()

def make_averaged_output_name(data_file):
    base = os.path.basename(data_file)

    # Remove prefix and suffix
    base = base.replace("restart_", "")
    base = base.replace("_reshape_HFD.data", "")

    return f"{base}_averaged_clust_df.csv"


averaged_clust_df = average_cluster_dfs(clust_dfs)


avg_outfile = make_averaged_output_name(nvt_data_file)

avg_outpath = os.path.join(
    output_dir_name,
    avg_outfile
)

averaged_clust_df.to_csv(avg_outpath, index=False)
averaged_clust_df.to_csv(avg_outfile, index=False)

print(f"\nAveraged cluster distribution written to:")
print(avg_outpath)


