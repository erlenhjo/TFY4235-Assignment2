# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:29:48 2022

@author: Erlend Johansen
"""
import numpy as np

###### Global constants ######
r_1=12e-9     #m
eV=1.602e-19
L=20e-6     #m   
alpha=0.2   #unitless
eta=1e-3    #Pa*s
kbT=26e-3*eV   #J
########################


def gamma(eta,r):
    return 6*np.pi*eta*r

def omega(deltaU,gamma,L):
    return deltaU/(gamma*L**2)

def t_hat(t,omega):
    return omega*t

def t(t_hat, omega):
    return t_hat/omega

def x_hat(x,L):
    return x/L

def x(x_hat,L):
    return x_hat*L

def D_hat(kbT,deltaU):
    return kbT/deltaU

def dt(gamma,kbT,alpha,L,deltaU):
    a=deltaU/(L*alpha*gamma)
    b=4*np.sqrt(2*kbT/gamma)
    c=-alpha*L
    
    sqrt_dt_max=(-b+np.sqrt(b**2-4*a*c))/(2*a)   #positive solution

    return sqrt_dt_max**2*0.01
    
def dt_hat(dt, omega):
    return dt*omega


def dt_hat_2(alpha,D):
    a=1/alpha
    b=4*np.sqrt(2*D)
    c=-alpha
    
    sqrt_dt_max=(-b+np.sqrt(b**2-4*a*c))/(2*a)   #positive solution

    return sqrt_dt_max**2*0.01