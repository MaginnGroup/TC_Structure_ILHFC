# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import os


def make_output_dir(traj_file, prefix="Ext_frms_"):
    base = os.path.basename(traj_file)

    # Remove known suffix
    base = base.replace("_reshape_HFD", "")

    # Convert extension to underscore form
    if ".lammpstrj_" in base:
        name, idx = base.split(".lammpstrj_")
        base = f"{name}_lammpstrj_{idx}"

    return prefix + base




def count_lammps_frames(traj_file):
    """Count number of frames in a LAMMPS dump file"""
    nframes = 0
    with open(traj_file, 'r') as f:
        for line in f:
            if line.startswith("ITEM: TIMESTEP"):
                nframes += 1
    return nframes


def extract_frames(
    traj_file,
    n_extract=100,
    output_dir="extracted_frames"
):
    os.makedirs(output_dir, exist_ok=True)

    total_frames = count_lammps_frames(traj_file)
    frame_indices = np.linspace(
        0, total_frames - 1, n_extract, dtype=int
    )
    frame_indices = set(frame_indices)

    print(f"Total frames: {total_frames}")
    print(f"Extracting {len(frame_indices)} frames")

    current_frame = -1
    atom_lines_expected = 0
    atom_data = []

    with open(traj_file, 'r') as f:
        for line in f:

            if line.startswith("ITEM: TIMESTEP"):
                current_frame += 1
                atom_data = []

            elif line.startswith("ITEM: NUMBER OF ATOMS"):
                natoms = int(next(f))
                atom_lines_expected = natoms

            elif line.startswith("ITEM: BOX BOUNDS"):
                # skip box bounds lines
                next(f); next(f); next(f)

            elif line.startswith("ITEM: ATOMS"):
                # Parse column positions
                cols = line.strip().split()[2:]
                col_idx = {c: i for i, c in enumerate(cols)}

                # Required columns (wrapped + unwrapped)
                required = ['id', 'mol', 'type', 'x', 'y', 'z', 'xu', 'yu', 'zu']
                idx = [col_idx[c] for c in required]

                for _ in range(atom_lines_expected):
                    parts = next(f).split()
                    atom_data.append([parts[i] for i in idx])

                if current_frame in frame_indices:
                    out_file = os.path.join(
                        output_dir,
                        f"frame_{current_frame:05d}.dat"
                    )
                    with open(out_file, 'w') as out:
                        out.write("id mol type x y z xu yu zu\n")
                        for row in atom_data:
                            out.write(" ".join(row) + "\n")

    print("Extraction complete.")



