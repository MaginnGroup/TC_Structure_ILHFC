# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import io

import networkx as nx
from collections import Counter



def read_extracted_frame(frame_file):
    df = pd.read_csv(frame_file, sep=r"\s+")
    return df




def get_mass_map(filename):
    mass_map = {}
    found_masses_header = False
    
    with open(filename, 'r') as f:
        for line in f:
            clean = line.strip()
            
            # 1. Look for the Masses header
            if "Masses" in clean:
                found_masses_header = True
                continue
            
            if found_masses_header:
                # 2. Split by single space as requested
                parts = line.strip('\n').split(" ")
                # Remove empty strings from list
                data = [p for p in parts if p.strip() != ""]
                
                # 3. Handling logic
                if not data:
                    # If we hit a blank line AFTER collecting masses, STOP.
                    if mass_map: 
                        break
                    continue
                
                # 4. Only record if it's a mass line (starts with digit)
                if data[0].isdigit():
                    try:
                        m_type = int(data[0])
                        m_value = float(data[1])
                        mass_map[m_type] = m_value
                    except (ValueError, IndexError):
                        # If the line structure changes, we've likely left the section
                        if mass_map: break
                else:
                    # If we hit a word (like "Pair" or "Bond"), STOP.
                    if mass_map: 
                        break
    mass_map_out = mass_map
    
    return mass_map_out
    


def extract_topology_from_lammps_data(nvt_data_file):
    name_wo_ext = nvt_data_file.split('.')[0]
    name_parts = name_wo_ext.split('_')
    hfc_name = name_parts[3]
    num_hfc = int(name_parts[5])
    num_il = int(name_parts[6])

    hfc_mol_ids = np.arange(1, num_hfc + 1)
    cation_ids = np.arange(num_hfc + 1, num_hfc + num_il + 1)
    anion_ids = np.arange(num_hfc + num_il + 1, num_hfc + 2 * num_il + 1)

    atoms_data = []
    current_section = None

    with open(nvt_data_file, 'r') as f:
        for line in f:
            clean = line.strip()
            if not clean:
                continue

            if clean.startswith("Atoms"):
                current_section = "atoms"
                continue
            elif any(h in clean for h in ["Velocities", "Bonds", "Angles"]):
                current_section = None
                continue

            if current_section == "atoms":
                atoms_data.append(line)

    cols = ['id', 'mol', 'type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz']
    df = pd.read_csv(io.StringIO("".join(atoms_data)),
                     sep=r'\s+', header=None, names=cols)

    # Drop coordinates — they will come from trajectory
    df = df[['id', 'mol', 'type']]

    mass_map = get_mass_map(nvt_data_file)
    df['mass'] = df['type'].map(mass_map)

    conditions = [
        df['mol'].isin(hfc_mol_ids),
        df['mol'].isin(cation_ids),
        df['mol'].isin(anion_ids)
    ]

    df['specie_id'] = np.select(conditions, [0, 1, 2], default=-1)

    return df




def merge_topology_with_frame(topology_df, frame_df):
    """
    Merge static topology with dynamic frame coordinates
    """
    df = topology_df.merge(
        frame_df[['id', 'xu', 'yu', 'zu']],
        on='id',
        how='inner'
    )

    return df



def extract_data_4cluster_analysis(nvt_data_file):
    name_wo_ext = nvt_data_file.split('.')[0]
    name_parts = name_wo_ext.split('_')
    hfc_name = name_parts[3]
    num_hfc = int(name_parts[5])
    num_il = int(name_parts[6])
    hfc_mol_ids = np.linspace(1, num_hfc, num_hfc)
    hfc_mol_ids = (hfc_mol_ids).astype(int)
    cation_ids = np.linspace(int(num_hfc + 1), int(num_hfc+num_il), num_il)
    cation_ids = (cation_ids).astype(int)
    anion_ids = np.linspace(int(num_hfc + num_il + 1), int(num_hfc+2*num_il), num_il)
    anion_ids = (anion_ids).astype(int)

    with open(nvt_data_file, 'r') as f:
        lines = f.readlines()
        
    atoms_data = []
    
    current_section = None
    
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
            
        # Detect Section
        if clean == "Atoms" or "Atoms" in clean:
            current_section = "atoms"
            continue
        elif any(header in clean for header in ["Velocities", "Bonds", "Angles"]):
            current_section = None
            continue
        
        # Parse Atoms
        elif current_section == "atoms":
            atoms_data.append(line)

    # 2. Create DataFrame
    cols = ['id', 'mol', 'type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz']
    df = pd.read_csv(io.StringIO("".join(atoms_data)), sep=r'\s+', header=None, names=cols)

    mass_map = get_mass_map(nvt_data_file)
    
    # 3. Map the extracted Masses to the 'type' column
    df['mass'] = df['type'].map(mass_map)

    conditions = [
    df['mol'].isin(hfc_mol_ids),
    df['mol'].isin(cation_ids),
    df['mol'].isin(anion_ids)
    ]

    # 3. Define the corresponding values for the new column
    choices = [0, 1, 2]
    
    # 4. Create the new column at the end
    # 'default=-1' helps you spot if any molecule ID wasn't in your lists
    df['specie_id'] = np.select(conditions, choices, default=-1)

    return df
        
def extract_box_from_lammps_data(filepath):
    box = {}

    with open(filepath, "r") as f:
        for line in f:
            parts = line.strip().split()

            if len(parts) >= 4:
                if parts[2] == "xlo" and parts[3] == "xhi":
                    box["Lx"] = float(parts[1]) - float(parts[0])
                elif parts[2] == "ylo" and parts[3] == "yhi":
                    box["Ly"] = float(parts[1]) - float(parts[0])
                elif parts[2] == "zlo" and parts[3] == "zhi":
                    box["Lz"] = float(parts[1]) - float(parts[0])

    return np.array([box["Lx"], box["Ly"], box["Lz"]])



def compute_specie_com(df_atoms, box):
    Lx, Ly, Lz = box

    df = df_atoms.copy()

    # weighted sums
    df["mx"] = df["mass"] * df["xu"]
    df["my"] = df["mass"] * df["yu"]
    df["mz"] = df["mass"] * df["zu"]

    grouped = df.groupby("mol")

    com_df = grouped.agg(
        x=("mx", "sum"),
        y=("my", "sum"),
        z=("mz", "sum"),
        m_tot=("mass", "sum"),
        specie_id=("specie_id", "first")
    ).reset_index()

    # divide by total mass
    com_df["x"] /= com_df["m_tot"]
    com_df["y"] /= com_df["m_tot"]
    com_df["z"] /= com_df["m_tot"]

    # wrap back into box
    com_df["x"] %= Lx
    com_df["y"] %= Ly
    com_df["z"] %= Lz

    return com_df[["mol", "x", "y", "z", "specie_id"]]



def build_adjacency(coords, box, cutoff):
    """
    Build adjacency matrix using MIC distances.
    """
    N = len(coords)
    adjacency = np.zeros((N, N), dtype=bool)

    for i in range(N):
        dr = coords[i+1:] - coords[i]
        dr -= box * np.round(dr / box)  # MIC
        d = np.linalg.norm(dr, axis=1)

        neighbors = np.where(d <= cutoff)[0] + i + 1
        adjacency[i, neighbors] = True
        adjacency[neighbors, i] = True

    return adjacency


def cluster_analysis_from_com(com_df, box, cutoff):
    """
    Performs cluster analysis on ion CoMs.

    Returns:
        cluster_df : dataframe with columns cluster_size | count
        singlet_mol_ids : list of mol IDs that are singlets
    """

    coords = com_df[["x", "y", "z"]].values

    # Build adjacency (neighbors within cutoff using MIC)
    adjacency = build_adjacency(coords, box, cutoff)

    # Graph ? connected components
    G = nx.from_numpy_array(adjacency)
    clusters = list(nx.connected_components(G))

    # Cluster sizes
    sizes = [len(c) for c in clusters]

    # Count how many clusters of each size
    size_counts = Counter(sizes)

    # Build dataframe from size 1 to max size
    max_size = max(size_counts.keys())

    cluster_df = pd.DataFrame({
        "cluster_size": range(1, max_size + 1),
        "count": [size_counts.get(k, 0) for k in range(1, max_size + 1)]
    })

    singlet_indices = [next(iter(c)) for c in clusters if len(c) == 1]
    singlet_mol_ids = com_df.iloc[singlet_indices]["mol"].tolist()

    return cluster_df, singlet_mol_ids



def clustering_analysis_ions(nvt_data_file, cutoff):
    atoms_df = extract_data_4cluster_analysis(nvt_data_file)
    ions_df = atoms_df[atoms_df["specie_id"].isin([1, 2])].copy()
    box_ = extract_box_from_lammps_data(nvt_data_file)
    com_ions_df = compute_specie_com(ions_df, box_)
    
    clust_df, singlets = cluster_analysis_from_com(com_ions_df, box_, cutoff)

    return clust_df, singlets, com_ions_df, atoms_df
    



def clustering_analysis_single_frame(nvt_data_file, extracted_frame_file, cutoff):
    topology_df = extract_topology_from_lammps_data(nvt_data_file)
    box = extract_box_from_lammps_data(nvt_data_file)

    frame_df = read_extracted_frame(extracted_frame_file)
    atoms_df = merge_topology_with_frame(topology_df, frame_df)
    ions_df = atoms_df[atoms_df["specie_id"].isin([1, 2])].copy()
    com_ions_df = compute_specie_com(ions_df, box)

    cluster_df, singlets = cluster_analysis_from_com(com_ions_df, box, cutoff)

    return cluster_df, singlets, com_ions_df, atoms_df





