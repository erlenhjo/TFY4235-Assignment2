# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 23:15:14 2022

@author: Erlend Johansen
"""

import numpy as np
import matplotlib.pyplot as plt


from units import r_1, eV, L, alpha, eta, kbT
import units
import potential


def ax_plot_trajectories(trajectories,dt,flashing, ax):
    #find N and number of particles in parallel from the dimensions of the \\
        #the trajectories array
    N=np.shape(trajectories)[0]
    particle_count=np.shape(trajectories)[1]
    
    #calculate time axis
    t=np.array(range(N))*dt
    
    #plot all trajectories to given ax
    for i in range(particle_count):
        ax.plot(trajectories[:,i],t)
    
    
    #adds lines to show when the potential switches on/off
    if flashing:
        for i in range(int(np.ceil(N*dt))):
            ax.axhline(y = i+0.75, color = 'r', linestyle = '--')
            ax.axhline(y = i+1, color = 'r', linestyle = '--')
            
            
    
#plots ratchet potential and corresponding force in reduced units
def plot_ratchet_potential():
    global alpha
    
    #set x axis
    x_hat=np.linspace(-2,2,1000)
    
    #create new plot/window and plot the potential and force
    fig,ax=plt.subplots()
    potential.plot_potential_and_force(x_hat, alpha, ax)
        
        
        
        
        
        
        
        
        