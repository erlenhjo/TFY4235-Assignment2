# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:15:14 2022

@author: Erlend Johansen
"""

import numpy as np
import matplotlib.pyplot as plt


from units import eV, eta, kbT
import units
import potential
import dataGeneration

#plots ratchet potential and corresponding force in reduced units
def plot_ratchet_potential():
    global alpha
    
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
    
    fig, ax=plt.subplots()
    tracks=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="tracks")
    
    #calculate time axis
    t=np.array(range(N))*dt
    
    #plot all tracks to given ax
    for i in range(desired_particle_count):
        ax.plot(tracks[:,i],t)
        
    x_hat=np.linspace(tracks.min(),tracks.max(),1000)
    potential.ax_plot_potential(x_hat, alpha, ax)
    #adds lines to show when the potential switches on/off
    if flashing:
        for i in range(int(np.ceil(N*dt))):
            ax.axhline(y = i+0.75, color = 'r', linestyle = '--')
            ax.axhline(y = i+1, color = 'r', linestyle = '--')
    
    
    
    
    
    
    

        

    
def compare_to_Boltzmann():
    
    fig,ax=plt.subplots()
    deltaU=0.1*kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)    
    
    deltaU=kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)  
    
    deltaU=10*kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)

    
"""
euler.plot_tracks(x_vals,dt_hat,flashing)

fig,ax=plt.subplots()
U_vals=potential.constant_ratchet_potential(x_vals.flatten(), alpha)

p_hist,bin_edges,_=ax.hist(U_vals[N//10:],bins=100,density=True,alpha=0)
bin_centers = 0.5*(bin_edges[1:]+bin_edges[:-1])
ax.plot(bin_centers,p_hist,"x")
potential.plot_probability_density(alpha, deltaU, kbT, ax)
"""


#def plot_velocity_over_tau(taus):
        
        
        
        
        
        
        
        