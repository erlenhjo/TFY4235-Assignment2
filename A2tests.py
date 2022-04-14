# -*- coding: utf-8 -*-
# """
# Created on Wed Mar  9 13:28:53 2022

# @author: Erlend Johansen
# """
import matplotlib.pyplot as plt
import numpy as np

import potential
import rng as RNG
import euler
import units
import scipy


###### Global constants ######
r_1=12e-9     #m
eV=1.602e-19
L=20e-6     #m   
alpha=0.2   #unitless
eta=1e-3    #Pa*s
kbT=26e-3*eV   #J
########################


def potential_test():
    global alpha   
    x_hat=np.linspace(-2,2,1000)
    
    fig,ax=plt.subplots()
    potential.plot_potential_and_force(x_hat, alpha, ax)
    
    
def probability_test():
    global alpha, kbT
    U_hat=np.linspace(0,1,1000)

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
    RNG.test_generator(seed)


def euler_test():
    global r_1, eV, L, alpha, eta, kbT
    
    r=r_1
    tau=1
    #deltaU=80*eV
    #deltaU=0.1*kbT
    #deltaU=kbT
    deltaU=10*kbT
    
    gamma=units.gamma(eta, r)
    omega=units.omega(deltaU, gamma, L)
    D_hat=units.D_hat(kbT, deltaU)
    
    dt=units.dt(gamma, kbT, alpha, L, deltaU)
    dt_hat=units.dt_hat(dt, omega)
    
    print(gamma)
    print(omega)
    print(D_hat)
    print(dt)
    print(dt_hat)
    
    print(units.dt_hat_2(alpha,D_hat))
    
    flashing=False
    rng_seed=0
    particle_count=100
    N=1000000
    
    x_vals=euler.execute_euler_scheme(particle_count,dt_hat,tau,alpha,omega,D_hat,N,rng_seed,flashing)
    
    
    #euler.plot_trajectories(x_vals,dt_hat,flashing)
    
    x_hat=np.linspace(x_vals.min(),x_vals.max(),1000)
    
    fig,ax=plt.subplots()
    
    potential.plot_potential(x_hat, alpha, ax)
    ax.hist(x_vals[N-1,:],bins=100,density=True)
    
    fig,ax=plt.subplots()
    U_vals=potential.constant_ratchet_potential(x_vals.flatten(), alpha)
    
    p_hist,bin_edges,_=ax.hist(U_vals[N//10:],bins=100,density=True,alpha=0)
    bin_centers = 0.5*(bin_edges[1:]+bin_edges[:-1])
    ax.plot(bin_centers,p_hist,"x")
    potential.plot_probability_density(alpha, deltaU, kbT, ax)
    
    
if __name__=="__main__":
    
    #potential_test()
    #probability_test()
    euler_test()
    
