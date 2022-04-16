# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 22:42:44 2022

@author: Erlend Johansen
"""

import os
import numpy as np

import euler
from units import r_1, eV, L, alpha, eta, kbT
import units

#### Raw data folder structure####
# constant potential
#     radius
#     N
#     deltaU
#     seed
#         x_hat_vals.npy
#         metadata.pickle
# flashing potential
#     radius
#     N
#     tau
#     seed
#         x_hat_vals.npy
#         metadata.npy 
# zero potential
#     radius
#     N
#     seed
#         x_vals.npy
#         metadata.npy

# seed is used as indentifier, so that identical seeds overwrite eachother and are \\
#     not double counted if results from multiple runs are merged
###################################



#Function for creating a folder and all missing previous folders
#If the for instance the folder already exists, the error is printed rather than raised
def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as err: 
        print(err)
        
def folder_path_constant(radius_name,deltaU,N):
    deltaU_per_kbT=deltaU/kbT
    folder_path=os.path.join("raw_data","constant_potential",radius_name,f"N_{N}",f"deltaU_{deltaU_per_kbT:.2f}kbT")
    return folder_path
    
def folder_path_flashing(radius_name,tau,N):
    folder_path=os.path.join("raw_data","flashing_potential",radius_name,f"N_{N}",f"tau_{tau}")
    return folder_path
        
def generate_particle_tracks(radius_name, N, particle_count, deltaU, tau, flashing):
    global r_1, L, alpha, eta, kbT
    
    if radius_name=="r_1":
        r=r_1
    elif radius_name=="r_2":
        r=3*r_1
    
    gamma=units.gamma(eta, r)
    omega=units.omega(deltaU, gamma, L)
    D_hat=units.D_hat(kbT, deltaU)    
    dt=units.dt(gamma, kbT, alpha, L, deltaU)
    dt_hat=units.dt_hat(dt, omega)
    
    #aquiring a suitable seed for the PRNG from computer entropy
    rng_seed=np.random.SeedSequence().entropy  

    #calculating the x positions of the particles through the euler scheme    
    trajectories=euler.execute_euler_scheme(particle_count,dt_hat,tau,alpha,omega,D_hat,N,rng_seed,flashing)

    #create dict for metadata and add values
    metadata={}
    metadata["deltaU"]=deltaU
    metadata["r"]=r
    metadata["gamma"]=gamma
    metadata["omega"]=omega
    metadata["D_hat"]=D_hat
    metadata["dt"]=dt
    metadata["dt_hat"]=dt_hat
    metadata["particle_count"]=particle_count
    metadata["flashing"]=flashing
    metadata["rng_seed"]=rng_seed
    metadata["N"]=N
    metadata["tau"]=tau
    
    #set the path for the outer data folder
    if flashing:
        folder_path=folder_path_flashing(radius_name, tau, N)
    else:
        folder_path=folder_path_constant(radius_name, deltaU, N)
    
    #create the seed folder and all missing intermediate folders
    create_folder(os.path.join(folder_path,str(rng_seed)))
    
    #save x values and metadata to file
    trajectories_path=os.path.join(folder_path, str(rng_seed), "trajectories.npy")
    metadata_path=os.path.join(folder_path, str(rng_seed), "metadata.npy")
    np.save(trajectories_path, trajectories)
    np.save(metadata_path, metadata)


def get_available_seeds(radius_name, N, deltaU, tau, flashing):
    #set outer folder path
    if flashing:
        folder_path=folder_path_flashing(radius_name, tau, N)
    else:
        folder_path=folder_path_constant(radius_name, deltaU, N)
    
    #get seeds from folder names
    seeds=os.listdir(folder_path)
    
    #find particle count for all seeds
    particle_counts=[]
    for seed in seeds:
        #set path to metadata file
        metadata_path=os.path.join(folder_path,seed,"metadata.npy")
        #load metadata dict from file
        metadata=np.load(metadata_path, allow_pickle=True).item()
        #extract particle count
        particle_counts.append(metadata["particle_count"])
        
    return seeds, particle_counts

    
    
