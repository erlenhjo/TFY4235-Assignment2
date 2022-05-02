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
    t_max=parameters["t_max"]
    
    fig, ax=plt.subplots()
    tracks=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="tracks")
    
    #calculate time axis
    t=np.array(range(N))*dt
    
    #plot all tracks to given ax
    for i in range(desired_particle_count):
        if i==1:
            ax.plot(tracks[::100,i],t[::100],color="k", alpha=0.2, label="Particle tracks")
        else:
            ax.plot(tracks[::100,i],t[::100],color="k", alpha=0.2)
        
    ax.set_xlabel("Reduced position [unitless]")
    ax.set_ylabel("Time [s]")
    ax.set(ylim=(0,t_max))
    
    if flashing:
        xmin=-1
        xmax=3
        ax.set(xlim=(xmin,xmax))
    else:
        xmin=-1
        xmax=1
        ax.set(xlim=(xmin,xmax))
    
    twin_axis=ax.twinx()
    x_hat=np.linspace(tracks.min(),tracks.max(),1000)
    potential.ax_plot_potential(np.linspace(xmin,xmax,1000), alpha, twin_axis)
    twin_axis.set(ylim=(0, 4))

    twin_axis.set_ylabel("Reduced potential [unitless]")
    
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax.transAxes)

    
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
        
        ax.hist(visited_potential, bins=100, density=True, alpha=0.5,label=f"Visited potential distribution {deltaU/kbT:.1f}kbT")
        ax.set_ylabel("Probability density [unitless]")
        ax.set_xlabel("Reduced potential [unitless]")
        ax.legend()
        #ax.set_yscale("log")
        
def velocity_stats(endpoints,t_max,L):
    velocity_average=np.mean(endpoints*L/t_max)
    velocity_variance=np.var(endpoints*L/t_max)
    return velocity_average, velocity_variance
    
def plot_velocity_over_tau(parameters_list_1,parameters_list_2, flashing, desired_particle_count):
    fig, ax=plt.subplots()
    v_avgs=[]
    v_vars=[]
    taus=[]
    for parameters in parameters_list_1:
        t_max=parameters["t_max"]
        tau=parameters["tau"]
        L=parameters["L"]
        endpoints=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="endpoints")
        v_avg, v_var = velocity_stats(endpoints, t_max, L*1e6)
        v_avgs.append(v_avg)
        v_vars.append(v_var)
        taus.append(tau)
    
    ax.errorbar(taus,v_avgs,yerr=np.sqrt(v_vars), fmt=".k")
    
    v_of_tau=interpolate.interp1d(taus,v_avgs,kind="cubic")
    
    tau=np.linspace(taus[0], taus[-1],1000)
    v=v_of_tau(tau)
    ax.plot(tau,v,label="Radius 1")
    
    tau_opt_1=tau[np.argmax(v)]
    
    ax.scatter(tau_opt_1,v_of_tau(tau_opt_1), marker="x", color="r", label="Optimal τ radius 1",zorder=1000)
    
    v_avgs=[]
    v_vars=[]
    taus=[]
    for parameters in parameters_list_2:
        t_max=parameters["t_max"]
        tau=parameters["tau"]
        L=parameters["L"]
        endpoints=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="endpoints")
        v_avg, v_var = velocity_stats(endpoints, t_max, L*1e6)
            
        v_avgs.append(v_avg)
        v_vars.append(v_var)
        taus.append(tau)
    
    ax.errorbar(taus,v_avgs,yerr=np.sqrt(v_vars), fmt=".k")
    
    v_of_tau=interpolate.interp1d(taus,v_avgs,kind="cubic")
    
    tau=np.linspace(taus[0], taus[-1],1000)
    v=v_of_tau(tau)
    ax.plot(tau,v,label="Radius 2")
    
    tau_opt_2=tau[np.argmax(v)]
    print(tau_opt_2)
    
    ax.scatter(tau_opt_2,v_of_tau(tau_opt_2), marker="x", color="b", label="Optimal τ radius 2",zorder=1001)
    
    ax.set_xlabel("Temporal period τ [s]")
    ax.set_ylabel("Drift velocity [μm/s]")
    
    ax.legend(loc="upper right")
    
    return tau_opt_1
    
        
def diffusion(D,t,x,N):
    return 1/(np.sqrt(4*np.pi*D*t))*np.exp(-x**2/(4*D*t))
        
def plot_diffusion(parameters_list, flashing, desired_particle_count):
        
    for i,parameters in enumerate(parameters_list):
        L=parameters["L"]
        t=parameters["t_max"]
        r=parameters["r"]
        alpha=parameters["alpha"]
        
        D=kbT/(6*np.pi*eta*r)
        
        endpoints=dataGeneration.get_data(parameters, flashing, desired_particle_count, data_type="endpoints")
        
        
        fig,ax=plt.subplots()

        x_hat=np.linspace(-1,1)*L
        
        print(np.sum(np.where(endpoints>alpha,1,0))/desired_particle_count)
        
        ax.plot(x_hat,diffusion(D,t,x_hat, desired_particle_count),label="Diffusion equation")
        ax.hist(endpoints*L,bins=1000, density=True,label="Meassured distribution")
        ax.set_xlabel("x [μm]")
        ax.set_ylabel("Particle denisty")
        ax.plot([0.2*L,0.2*L],[0,np.max(diffusion(D,t,x_hat, desired_particle_count))],label="First potential peak")
    
        ax.legend()
        fig.tight_layout()
        fig.savefig(f"dist{i}")
        
        
def motion_ensemble(parameters_1,parameters_2,flashing,desired_particle_count):
    N_1=parameters_1["N"]
    N_2=parameters_2["N"]
    dt_1=parameters_1["dt"]
    dt_2=parameters_2["dt"]
    t_1=np.arange(N_1)*dt_1
    t_2=np.arange(N_2)*dt_2
    tau=parameters_1["tau"]
    
    tracks_1=endpoints=dataGeneration.get_data(parameters_1, flashing, desired_particle_count, data_type="tracks")
    tracks_2=endpoints=dataGeneration.get_data(parameters_2, flashing, desired_particle_count, data_type="tracks")
    
    plt.figure()
    ind_1=np.searchsorted(t_1, 10*tau)
    _ , bins,_=plt.hist(tracks_1[ind_1],bins=100, alpha=0.4)
    
    fig_1,ax_1=plt.subplots(nrows=3,sharex=True)
    fig_2,ax_2=plt.subplots(nrows=3,sharex=True)
    for i,num_tau in enumerate([0,10,20]):
        ind_1=np.searchsorted(t_1, num_tau*tau)
        ax_1[i].hist(tracks_1[ind_1],bins=bins, alpha=0.4)
        ax_1[i].set_ylabel("Particles")
        ind_2=np.searchsorted(t_2, num_tau*tau)
        ax_2[i].hist(tracks_2[ind_2],bins=bins, alpha=0.4)
        ax_2[i].set_ylabel("Particles")
    
    ax_1[2].set_xlabel("x_hat")
    ax_2[2].set_xlabel("x_hat")
    
    