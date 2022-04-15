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



#Simple function for creating a folder and all missing previous folders
#If the folder already exists, the error is printed rather than raised
def create_folder(path):
    try:
        os.makedirs(path)
    except OSError as err: 
        print(err)


def generate_particle_tracks_flashing(radius_name, tau, N, particle_count):
    global r_1, eV, L, alpha, eta, kbT
    
    #setting and calculating experiment variables
    deltaU=80*eV
    if radius_name=="r_1":
        r=r_1
    elif radius_name=="r_2":
        r=3*r_1
    gamma=units.gamma(eta, r)
    omega=units.omega(deltaU, gamma, L)
    D_hat=units.D_hat(kbT, deltaU)    
    dt=units.dt(gamma, kbT, alpha, L, deltaU)
    dt_hat=units.dt_hat(dt, omega)
    flashing=True   #flashing potential
    
    #aquiring a suitable seed for the PRNG from computer entropy
    rng_seed=np.random.SeedSequence().entropy  
    
    #calculating the x positions of the particles through the euler scheme
    x_hat_vals=euler.execute_euler_scheme(particle_count,dt_hat,tau,alpha,omega,D_hat,N,rng_seed,flashing)

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
    
    #create the path for the data folder
    folder_path=os.path.join("raw_data","flashing_potential",radius_name,f"N_{N}",f"tau_{tau}",str(rng_seed))
    #create said folder and all missing intermediate folders
    create_folder(folder_path)
    
    #save x values and metadata to file
    x_path=os.path.join(folder_path, "x_hat_vals.npy")
    metadata_path=os.path.join(folder_path, "metadata.npy")
    np.save(x_path,x_hat_vals)
    np.save(metadata_path,metadata)
    
def generate_particle_tracks_constant(radius_name, deltaU_per_kbT, N, particle_count):
    global r_1, L, alpha, eta, kbT
    
    tau=1   #irrelevant as there is no flashing, but necessary as a function input
    deltaU=deltaU_per_kbT*kbT
    if radius_name=="r_1":
        r=r_1
    elif radius_name=="r_2":
        r=3*r_1
    gamma=units.gamma(eta, r)
    omega=units.omega(deltaU, gamma, L)
    D_hat=units.D_hat(kbT, deltaU)    
    dt=units.dt(gamma, kbT, alpha, L, deltaU)
    dt_hat=units.dt_hat(dt, omega)
    flashing=False  #constant potential
    
    #aquiring a suitable seed for the PRNG from computer entropy
    rng_seed=np.random.SeedSequence().entropy  

    #calculating the x positions of the particles through the euler scheme    
    x_hat_vals=euler.execute_euler_scheme(particle_count,dt_hat,tau,alpha,omega,D_hat,N,rng_seed,flashing)

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
    
    #create the path for the data folder
    folder_path=os.path.join("raw_data","constant_potential",radius_name,f"N_{N}",f"deltaU_{deltaU_per_kbT}kbT",str(rng_seed))
    #create said folder and all missing intermediate folders
    create_folder(folder_path)
    
    #save x values and metadata to file
    x_path=os.path.join(folder_path, "x_hat_vals.npy")
    metadata_path=os.path.join(folder_path, "metadata.npy")
    np.save(x_path,x_hat_vals)
    np.save(metadata_path,metadata)
    
if __name__=="__main__":
    generate_particle_tracks_flashing("r_1", 1, 1000, 10)
    generate_particle_tracks_constant("r_1", 1, 1000, 10)
