# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:29:48 2022

@author: Erlend Johansen
"""
import numpy as np


###### Physical constants ######
eV=1.602e-19 #J
eta=1e-3    #Pa*s
kbT=26e-3*eV   #J
################################

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

def calculate_dt(gamma,kbT,alpha,L,deltaU):
    a=deltaU/(L*alpha*gamma)
    b=4*np.sqrt(2*kbT/gamma)
    c=-alpha*L
    
    sqrt_dt_max=(-b+np.sqrt(b**2-4*a*c))/(2*a)   #positive solution

    return sqrt_dt_max**2*0.1
    
def dt_hat(dt, omega):
    return dt*omega

def dt(dt_hat, omega):
    return dt_hat/omega

def calculate_dt_hat(alpha,D_hat):
    a=1/alpha
    b=4*np.sqrt(2*D_hat)
    c=-alpha
    
    sqrt_dt_max=(-b+np.sqrt(b**2-4*a*c))/(2*a)   #positive solution

    return sqrt_dt_max**2*0.1

def N(t_max, omega):
    return int(np.ceil(t_max/omega))