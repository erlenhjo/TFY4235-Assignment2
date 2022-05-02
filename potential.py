# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:32:48 2022

@author: Erlend Johansen
"""
import numpy as np
from numba import vectorize
from scipy import integrate

@vectorize(cache=True)
def flashing_ratchet_potential(x_hat,t_hat,tau,alpha,omega):
    t_phase=t_hat/(omega*tau)-np.floor(t_hat/(omega*tau))
    x_phase=x_hat-np.floor(x_hat)
    
    if t_phase>0.75:
        if x_phase<alpha:
            return x_phase/alpha
        else:
            return (1-x_phase)/(1-alpha)
    else:
        return 0
    
@vectorize(cache=True)
def flashing_ratchet_force(x_hat,t_hat,tau,alpha,omega):
    t_phase=t_hat/(omega*tau)-np.floor(t_hat/(omega*tau))
    x_phase=x_hat-np.floor(x_hat)
    
    if t_phase>0.75:
        if x_phase<alpha:
            return -1/alpha
        else:
            return 1/(1-alpha)
    else:
        return 0
    
@vectorize(cache=True)
def constant_ratchet_potential(x_hat,alpha):
    x_phase=x_hat-np.floor(x_hat)
    
    if x_phase<alpha:
        return x_phase/alpha
    else:
        return (1-x_phase)/(1-alpha)

    
@vectorize(cache=True)
def constant_ratchet_force(x_hat,alpha):
    x_phase=x_hat-np.floor(x_hat)

    if x_phase<alpha:
        return -1/alpha
    else:
        return 1/(1-alpha)

    

def ax_plot_potential_and_force(x_hat, alpha, ax):
    U=constant_ratchet_potential(x_hat,alpha)
    F=constant_ratchet_force(x_hat, alpha)

    ax.plot(x_hat,U,label="Potential")
    ax.plot(x_hat,F,label="Force")
    
def ax_plot_potential(x_hat, alpha, ax):
    U=constant_ratchet_potential(x_hat,alpha)
    
    ax.plot(x_hat,U,label="Potential")
    

@vectorize(cache=True)    
def probability_density(U, alpha, deltaU, kbT):
    a=np.exp(-U/kbT)
    b=(1-np.exp(-deltaU/kbT))
    return a/(kbT*b)
    
def ax_plot_probability_density(alpha, deltaU, kbT, ax):
    U=np.linspace(0,deltaU,10000)
    ax.plot(U/deltaU,probability_density(U,alpha,deltaU,kbT)*deltaU,label=f"Probability density {deltaU/kbT:.1f}kbT")
    
def validate_probability_density(alpha, deltaU, kbT):
    p=lambda U : probability_density(U, alpha, deltaU, kbT)
    total_probability,_=integrate.quad(p,0,deltaU)
    print(f"The total probability at deltaU={deltaU/kbT}kbT differs from 1 by {abs(total_probability-1):.1e}")
    
    