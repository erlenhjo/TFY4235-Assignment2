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

def build_statistics_in_potential(parameters, desired_particle_count, flashing):
    seeds, particle_counts=dataGeneration.get_available_seeds(parameters, flashing)
    
    missing_particles=desired_particle_count-sum(particle_counts)
    while missing_particles:
        particle_count=1000 ##int(1e9/parameters["N"])
        dataGeneration.generate_particle_tracks(parameters, particle_count, flashing)
        missing_particles-=particle_count

def run_experiment_constant(desired_particle_count):
    global kBT, alpha, L
    
    radius_name="r_1"
    deltaU_values=np.array([0.1,1,10])*kbT
    tau=1
    t_max=1

    flashing=False
    
    for deltaU in deltaU_values:
        parameters=set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L)
        build_statistics_in_potential(parameters, desired_particle_count, flashing)
        print(dataGeneration.get_available_seeds(parameters, flashing))

def run_experiment_flashing(desired_particle_count):
    global eV, L, alpha, kbT, eta
    
    radius_name="r_1"
    t_max=1
    deltaU=80*eV
    dt=units.calculate_dt(units.gamma(eta, radius(radius_name), kbT, alpha, L, deltaU))
    taus=[dt*8*2**i for i in range(20)]
    flashing=True
    
    for tau in taus:
        parameters=set_experiment_parameters(radius_name, deltaU, tau, t_max, alpha, L)
        build_statistics_in_potential(parameters, desired_particle_count, flashing)
        print(dataGeneration.get_available_seeds(parameters))
    
    
if __name__=="__main__":
    
    run_experiment_constant(desired_particle_count=100)
    run_experiment_flashing(desired_particle_count=100, radius_name="r_1")
    
    #run_experiment_no_potential
    


    
    
    
    
    
    
    