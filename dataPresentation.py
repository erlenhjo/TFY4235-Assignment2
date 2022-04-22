# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:15:14 2022

@author: Erlend Johansen
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate

from units import eV, eta, kbT
import units
import potential
import dataGeneration

#plots ratchet potential and corresponding force in reduced units
def plot_ratchet_potential(alpha):
    #set x axis
    x_hat=np.linspace(-2,2,1000)
    #create new plot/window and plot the potential and force
    fig,ax=plt.subplots()
    potential.plot_potential_and_force(x_hat, alpha, ax)
            
def plot_tracks_in_potential(parameters, flashing, desired_particle_count):
    #get relevant parameters
    dt=parameters["dt"]
    N=parameters["N"]
    alpha=parameters["alpha"]
    tau=parameters["tau"]
    
    fig, ax=plt.subplots()
    tracks=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="tracks")
    
    #calculate time axis
    t=np.array(range(N))*dt
    
    #plot all tracks to given ax
    for i in range(desired_particle_count):
        ax.plot(tracks[::100,i],t[::100],color="k", alpha=0.2)
        
    x_hat=np.linspace(tracks.min(),tracks.max(),1000)
    potential.ax_plot_potential(x_hat, alpha, ax)
    
    
def compare_to_Boltzmann_constant(parameters_list, desired_particle_count):
    global kbT
    flashing=False
    
    fig,ax=plt.subplots()
    
    for parameters in parameters_list:
        alpha=parameters["alpha"]
        deltaU=parameters["deltaU"]
        N=parameters["N"]
        potential.ax_plot_probability_density(alpha, deltaU, kbT, ax)    
        tracks=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="tracks")
        visited_potential=potential.constant_ratchet_potential(tracks, alpha).flatten()
        
        ax.hist(visited_potential, bins=100, density=True, alpha=0.5)
        #ax.set_yscale("log")
        
def velocity_stats(endpoints,t_max):
    velocity_average=np.mean(endpoints/t_max)
    velocity_variance=np.var(endpoints/t_max)
    return velocity_average, velocity_variance
    
def plot_velocity_over_tau(parameters_list, flashing, desired_particle_count):
    fig, ax=plt.subplots()
    v_avgs=[]
    v_vars=[]
    taus=[]
    for parameters in parameters_list:
        t_max=parameters["t_max"]
        tau=parameters["tau"]
        endpoints=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="endpoints")
        v_avg, v_var = velocity_stats(endpoints, t_max)
            
        v_avgs.append(v_avg)
        v_vars.append(v_var)
        taus.append(tau)
    
    ax.errorbar(taus,v_avgs,yerr=np.sqrt(v_vars), fmt=".k")
    
    v_of_tau=interpolate.interp1d(taus,v_avgs,kind="cubic")
    
    tau=np.linspace(taus[0], taus[-1],1000)
    v=v_of_tau(tau)
    ax.plot(tau,v)
    
    tau_opt=tau[np.argmax(v)]
    
    ax.scatter(tau_opt,v_of_tau(tau_opt), marker="x", color="r", label="Max τ")
    
    ax.legend()
    return tau_opt
    
        
        
        
        
        