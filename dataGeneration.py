# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 22:42:44 2022

@author: Erlend Johansen
"""

import os
import numpy as np

import euler
from units import kbT

#### Raw data folder structure####
# constant potential
#     radius
#     t_max
#     deltaU
#     seed
#         tracks.npy
#         metadata.pickle
# flashing potential
#     radius
#     t_max
#     tau
#     seed
#         tracks.npy
#         metadata.npy 
# zero potential
#     radius
#     t_max
#     seed
#         tracks.npy
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



####### Flashing and non-zero constant potential #######

#returns relative path to data storage folder for constant potential \\
    #at a given r, N and deltaU
def folder_path_constant(radius_name, t_max, deltaU):
    global kbT
    deltaU_per_kbT=deltaU/kbT
    folder_path=os.path.join("raw_data","constant_potential",radius_name,f"t_max_{t_max:.2e}",f"deltaU_{deltaU_per_kbT:.2f}kbT")
    return folder_path

#returns relative path to data storage folder for flashing potential \\
    #at a given r, N and tau   
def folder_path_flashing(radius_name, t_max, tau):
    folder_path=os.path.join("raw_data","flashing_potential",radius_name,f"t_max_{t_max:.2e}",f"tau_{tau:.2e}")
    return folder_path


#runs a single experiment in a flashing or constant potential and saves the data to file \\
    #given the parameters r, N, number of particles in parallel, deltaU and tau
def generate_particle_tracks(parameters, particle_count, flashing):    
    #get relevant parameters for euler scheme
    dt_hat=parameters["dt_hat"]
    tau=parameters["tau"]
    alpha=parameters["alpha"]
    omega=parameters["omega"]
    D_hat=parameters["D_hat"]
    N=parameters["N"]
    
    #get additional parameters for data storage
    radius_name=parameters["radius_name"] 
    deltaU=parameters["deltaU"]
    t_max=parameters["t_max"]
    
    
    #aquiring a suitable seed for the PRNG from computer entropy
    rng_seed=np.random.SeedSequence().entropy  

    #calculating the x positions of the particles through the euler scheme    
    tracks=euler.execute_euler_scheme(particle_count,dt_hat,tau,alpha,omega,D_hat,N,rng_seed,flashing)

    #extract endpoints
    endpoints=tracks[-1]
    
    #set the path for the outer data folder
    if flashing:
        folder_path=folder_path_flashing(radius_name, t_max, tau)
    else:
        folder_path=folder_path_constant(radius_name, t_max, deltaU)
    
    #create the seed folder and all missing intermediate folders
    create_folder(os.path.join(folder_path,str(rng_seed)))
    
    #save tracks, endpoints and particle_count to file
    tracks_path=os.path.join(folder_path, str(rng_seed), "tracks.npy")
    particle_count_path=os.path.join(folder_path, str(rng_seed), "particle_count.npy")
    endpoints_path=os.path.join(folder_path, str(rng_seed), "endpoints.npy")
    np.save(tracks_path, tracks)
    np.save(particle_count_path, particle_count)
    np.save(endpoints_path, endpoints)


#gets a list of seeds and their particle counts for \\
    #track data sets given r, N, deltaU, tau and potential type
def get_available_seeds(parameters, flashing):
    #get relevant parameters
    radius_name=parameters["radius_name"] 
    t_max=parameters["t_max"]
    deltaU=parameters["deltaU"]
    tau=parameters["tau"]
    
    #set outer folder path
    if flashing:
        folder_path=folder_path_flashing(radius_name, t_max, tau)
    else:
        folder_path=folder_path_constant(radius_name, t_max, deltaU)
    
    #get seeds from folder names
    try:
        seeds=os.listdir(folder_path)
    except:
        seeds=[]
    
    #find particle count for all seeds
    particle_counts=[]
    for seed in seeds:
        #set path to file
        particle_count_path=os.path.join(folder_path,seed,"particle_count.npy")
        #load particle count from file, as a 1x1 array
        particle_count=np.load(particle_count_path)
        #append particle count
        particle_counts.append(particle_count)
        
    return seeds, particle_counts
    
#function to get the tracks or endpoints from a spesific experiment    
def get_data(parameters, flashing, desired_particle_count, data_type):
    #get relevant parameters
    radius_name=parameters["radius_name"] 
    t_max=parameters["t_max"]
    deltaU=parameters["deltaU"]
    tau=parameters["tau"]
    
    #set outer folder path
    if flashing:
        folder_path=folder_path_flashing(radius_name, t_max, tau)
    else:
        folder_path=folder_path_constant(radius_name, t_max, deltaU)
    
    seeds, particle_counts=get_available_seeds(parameters, flashing)
    
    if data_type=="tracks" or data_type=="endpoints":
        missing_particles=desired_particle_count
        for i,(seed, particle_count) in enumerate(zip(seeds, particle_counts)):
            desired_indices=min(particle_count,missing_particles)
            #set path to file
            data_path=os.path.join(folder_path,seed,f"{data_type}.npy")
            #load from file and return data from as many particles as desired
            if data_type=="tracks":
                if i==0:
                    desired_data=np.load(data_path)[:,:desired_indices]
                else:
                    desired_data.append(np.load(data_path)[:,:desired_indices], axis=1)
            elif data_type=="endpoints":
                if i==0:
                    desired_data=np.load(data_path)[:desired_indices]
                else:
                    desired_data.append(np.load(data_path)[:desired_indices])
            missing_particles-=desired_indices
            #break when data from enough particles is aquired
            if not missing_particles:
                break
    else:
        raise("Error: Not valid datatype")
        
    return desired_data





########################################################

###### Zero potential ######







############################
    
