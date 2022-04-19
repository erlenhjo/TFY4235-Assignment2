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

#plots ratchet potential and corresponding force in reduced units
def plot_ratchet_potential():
    global alpha
    
    #set x axis
    x_hat=np.linspace(-2,2,1000)
    
    #create new plot/window and plot the potential and force
    fig,ax=plt.subplots()
    potential.plot_potential_and_force(x_hat, alpha, ax)


def plot_tracks(tracks, dt, flashing, ax):
    #find N and number of particles in parallel from the dimensions of the \\
        #the tracks array
    N=np.shape(tracks)[0]
    particle_count=np.shape(tracks)[1]
    
    #calculate time axis
    t=np.array(range(N))*dt
    
    #plot all tracks to given ax
    for i in range(particle_count):
        ax.plot(tracks[:,i],t)
        
    #adds lines to show when the potential switches on/off
    if flashing:
        for i in range(int(np.ceil(N*dt))):
            ax.axhline(y = i+0.75, color = 'r', linestyle = '--')
            ax.axhline(y = i+1, color = 'r', linestyle = '--')
            
def plot_tracks_in_potential(radius_name, N, number_of_tracks, deltaU, tau, flashing):
    global eV, L, alpha, eta, kbT
    
    r=units.radius(radius_name)
    dt=units.calculate_dt(units.gamma(eta, r), kbT, alpha, L, deltaU)
    
    
    
    
    fig, ax=plt.subplots()
    #ax.plot_tracks(tracks,dt,flashing, ax)
    
    
    
    
    
    
    
    
    

        


"""    
def compare_to_Boltzmann():
    global alpha, kbT
    
    fig,ax=plt.subplots()
    deltaU=0.1*kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)    
    
    
    deltaU=kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)  
    
    
    deltaU=10*kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)
      
"""

    
"""
euler.plot_tracks(x_vals,dt_hat,flashing)

fig,ax=plt.subplots()
U_vals=potential.constant_ratchet_potential(x_vals.flatten(), alpha)

p_hist,bin_edges,_=ax.hist(U_vals[N//10:],bins=100,density=True,alpha=0)
bin_centers = 0.5*(bin_edges[1:]+bin_edges[:-1])
ax.plot(bin_centers,p_hist,"x")
potential.plot_probability_density(alpha, deltaU, kbT, ax)
"""


        
        
        
        
        
        
        
        