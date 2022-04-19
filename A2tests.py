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
    seed=np.random.SeedSequence()
    gen=np.random.Generator(np.random.PCG64(seed))
    vals=gen.normal(size=1000000)
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
    
