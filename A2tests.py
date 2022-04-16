# -*- coding: utf-8 -*-
# """
# Created on Wed Mar  9 13:28:53 2022

# @author: Erlend Johansen
# """
import matplotlib.pyplot as plt
import numpy as np
import scipy

import potential
import euler
import units
from units import r_1, eV, L, alpha, eta, kbT
import dataGeneration
import dataPresentation

###### Global constants ######
# r_1=12e-9     #m
# eV=1.602e-19
# L=20e-6     #m   
# alpha=0.2   #unitless
# eta=1e-3    #Pa*s
# kbT=26e-3*eV   #J
########################

#plots potential and force for visual confirmation that the implementation is
#correct
def potential_test():
    global alpha   
    x_hat=np.linspace(-2,2,1000)
    
    fig,ax=plt.subplots()
    potential.plot_potential_and_force(x_hat, alpha, ax)
    
    
def probability_test():
    global alpha, kbT

    fig,ax=plt.subplots()
    deltaU=0.1*kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)    
    
    fig,ax=plt.subplots()
    deltaU=kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)  
    
    fig,ax=plt.subplots()
    deltaU=10*kbT
    potential.plot_probability_density(alpha, deltaU, kbT, ax)  

def rng_test():
    seed=0
    gen=np.random.Generator(np.random.MT19937(seed))
    vals=gen.normal(size=100000)
    plt.hist(vals, bins=1000)
    print(f"Mean: {np.mean(vals)}")
    print(f"Std: {np.std(vals)}")

def data_generation_test():
    global r_1, eV, L, alpha, eta, kbT
    
    radius_name="r_1"
    N=int(1e6)
    particle_count=int(1e1)
    
    dataGeneration.generate_particle_tracks(radius_name, N, particle_count, deltaU=kbT, tau=1, flashing=False)
    dataGeneration.generate_particle_tracks(radius_name, N, particle_count, deltaU=80*eV, tau=1, flashing=True)
    
    print(dataGeneration.get_available_seeds(radius_name, N, deltaU=kbT, tau=1, flashing=False))
    print(dataGeneration.get_available_seeds(radius_name, N, deltaU=80*eV, tau=1, flashing=True))
    
    """
    euler.plot_trajectories(x_vals,dt_hat,flashing)
    
    fig,ax=plt.subplots()
    U_vals=potential.constant_ratchet_potential(x_vals.flatten(), alpha)
    
    p_hist,bin_edges,_=ax.hist(U_vals[N//10:],bins=100,density=True,alpha=0)
    bin_centers = 0.5*(bin_edges[1:]+bin_edges[:-1])
    ax.plot(bin_centers,p_hist,"x")
    potential.plot_probability_density(alpha, deltaU, kbT, ax)
    """
    
if __name__=="__main__":
    
    data_generation_test()
    
