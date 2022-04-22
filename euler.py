# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 16:03:36 2022

@author: Erlend Johansen
"""
import numpy as np
from numba import njit

import potential

@njit(cache=True)
def euler_increment_flashing(x_hat,t_hat,dt_hat,tau,alpha,omega,D_hat,epsilon):
    force=potential.flashing_ratchet_force(x_hat, t_hat, tau, alpha, omega)
    return x_hat+force*dt_hat+np.sqrt(2*D_hat*dt_hat)*epsilon

@njit(cache=True)
def euler_increment_constant(x_hat,dt_hat,alpha,D_hat,epsilon):
    force=potential.constant_ratchet_force(x_hat,alpha)
    return x_hat+force*dt_hat+np.sqrt(2*D_hat*dt_hat)*epsilon

@njit(cache=True)
def iterate_euler(particle_count,dt_hat,tau,alpha,omega,D_hat,N,flashing,epsilons):
    x_vals=np.empty((N,particle_count))
    x_vals[0]=0
    t_hat_n=0
    if flashing:
        for n in range(N-1):
            x_vals[n+1]=euler_increment_flashing(x_vals[n], t_hat_n, dt_hat, tau, alpha, omega, D_hat, epsilons[n])
            t_hat_n=t_hat_n+dt_hat
    else:
        for n in range(N-1):
            x_vals[n+1]=euler_increment_constant(x_vals[n], dt_hat, alpha, D_hat, epsilons[n])            
    return x_vals

def execute_euler_scheme(particle_count,dt_hat,tau,alpha,omega,D_hat,N,rng_seed,flashing):
    rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence(rng_seed)))
    epsilons=rng.normal(size=(N,particle_count))
    x_vals=iterate_euler(particle_count, dt_hat, tau, alpha, omega, D_hat, N, flashing, epsilons) 
    return x_vals  #returns x_vals in reduced units


             
    

    
    