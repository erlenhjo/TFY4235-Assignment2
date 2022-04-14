# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:44:03 2022

@author: Erlend Johansen
"""

import numpy as np
import matplotlib.pyplot as plt

def create_MT_generator(seed):
    return np.random.Generator(np.random.MT19937(seed))

def test_generator(seed):
    Gen=create_MT_generator(seed)
    vals=Gen.normal(size=100000)
    plt.hist(vals, bins=1000)
    print(f"Mean: {np.mean(vals)}")
    print(f"Std: {np.std(vals)}")