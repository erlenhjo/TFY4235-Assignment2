# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 15:31:03 2022

@author: Erlend Johansen
"""
import numpy as np
import matplotlib.pyplot as plt
import time

import dataGeneration
import dataPresentation
import units

from units import eV, eta, kbT

###### Experiment constants ######
r_1=12e-9     #m
L=20e-6     #m   
alpha=0.2   #unitless
##################################

def radius(radius_name):
    if radius_name=="r_1":
        r=r_1
    elif radius_name=="r_2":
        r=3*r_1
    return r

def set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L):
    global eta, kBT
    parameters={}
    parameters["radius_name"]=radius_name
    parameters["deltaU"]=deltaU
    parameters["tau"]=tau
    parameters["t_max"]=t_max
    parameters["alpha"]=alpha
    parameters["L"]=L
    
    parameters["r"]=radius(radius_name)
    parameters["gamma"]=units.gamma(eta, parameters["r"])
    parameters["omega"]=units.omega(deltaU, parameters["gamma"], L)
    parameters["dt"]=units.calculate_dt(parameters["gamma"], kbT, alpha, L, deltaU)
    parameters["dt_hat"]=units.dt_hat(parameters["dt"], parameters["omega"])
    parameters["N"]=units.N(parameters["t_max"], parameters["dt"])
    parameters["D_hat"]=units.D_hat(kbT, deltaU)
    
    return parameters

def build_statistics_in_potential(parameters, flashing, desired_particle_count, save_tracks):
    
    if save_tracks:
        data_type="tracks"
    else: 
        data_type="endpoints"
    
    seeds, particle_counts=dataGeneration.get_available_seeds(parameters, flashing, data_type)
    
    missing_particles=desired_particle_count-sum(particle_counts)
    while missing_particles>0:
        print(f"Missing {missing_particles} particles.")
        particle_count=min(missing_particles,int(1e8/parameters["N"]))
        dataGeneration.generate_particle_tracks(parameters, particle_count, flashing, save_tracks)
        print("Tracks calculated.")
        missing_particles-=particle_count

def run_experiment_constant(desired_particle_count):
    global kBT, alpha, L, eV
    
    radius_name="r_1"
    deltaU_values=np.append(np.array([0.1,10])*kbT,80*eV)
    tau=1
    
    flashing=False
    
    for deltaU in deltaU_values:
        t_max=4
        parameters=set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L)
        build_statistics_in_potential(parameters, flashing, desired_particle_count, save_tracks=True)
        dataPresentation.plot_tracks_in_potential(parameters, flashing, desired_particle_count=20)
    
    parameters_list=[]
    for deltaU in deltaU_values:
        t_max=100
        parameters=set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L)
        #print(parameters)
        parameters_list.append(parameters)
        build_statistics_in_potential(parameters, flashing, desired_particle_count, save_tracks=True)

        
    dataPresentation.compare_to_Boltzmann_constant(parameters_list[:2], desired_particle_count)
    

def run_experiment_flashing(desired_particle_count):
    global eV, L, alpha, kbT, eta
    
    radius_name="r_1"
    deltaU=80*eV
    t_max=100
    flashing=True
    
    taus=np.arange(1,31)/15
    parameters_list_1=[]
    parameters_list_2=[]
    for tau in taus:
        print(f"Radius=r_1, Tau={tau}")
        parameters=set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L)
        #print(parameters)
        parameters_list_1.append(parameters)
        build_statistics_in_potential(parameters, flashing, desired_particle_count, save_tracks=False)
    for tau in taus:
        print(f"Radius=r_2, Tau={tau}")
        parameters=set_experiment_parameters("r_2", deltaU, tau, t_max, alpha, L)
        parameters_list_2.append(parameters)
        build_statistics_in_potential(parameters, flashing, desired_particle_count, save_tracks=False)
        
    tau_opt=dataPresentation.plot_velocity_over_tau(parameters_list_1,parameters_list_2, flashing, desired_particle_count)
    
    tau_opt=0.44791458124791456
    t_max=10
    print(f"Radius=r_1, Tau={tau_opt}")
    parameters_1=set_experiment_parameters(radius_name, deltaU, tau_opt, t_max, alpha, L)
    build_statistics_in_potential(parameters_1, flashing, desired_particle_count=200, save_tracks=True)
    print(f"Radius=r_2, Tau={tau_opt}")
    parameters_2=set_experiment_parameters("r_2", deltaU, tau_opt, t_max, alpha, L)
    build_statistics_in_potential(parameters_2, flashing, desired_particle_count=200, save_tracks=True)
        
    dataPresentation.motion_ensemble(parameters_1,parameters_2,flashing,desired_particle_count=200)
        
    
    plot_taus=[0.1,tau_opt,1]
    for tau in plot_taus:
        t_max=1
        parameters=set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L)
        build_statistics_in_potential(parameters, flashing, desired_particle_count=100, save_tracks=True)
        dataPresentation.plot_tracks_in_potential(parameters, flashing, desired_particle_count=100)
      
    parameters_list=[]
    for t_max in np.array([0.1,0.4479,1.0])*0.75:
        tau=1000
        parameters=set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L)
        parameters_list.append(parameters)
        build_statistics_in_potential(parameters, flashing, desired_particle_count=100000, save_tracks=False)
    
    dataPresentation.plot_diffusion(parameters_list, flashing, desired_particle_count=100000)
    
    


if __name__=="__main__":
    
    #run_experiment_constant(desired_particle_count=1000)
    run_experiment_flashing(desired_particle_count=10000)
    
    



    
    
    