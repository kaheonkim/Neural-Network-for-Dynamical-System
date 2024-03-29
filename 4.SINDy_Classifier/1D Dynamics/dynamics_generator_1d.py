# -*- coding: utf-8 -*-
"""Dynamics_generator_1D.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SLfBHGvXMe2tBYHgpvHVPIgQnsqM1NHB
"""

import numpy as np
import pandas as pd
import random
from scipy.integrate import odeint
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import pysindy as ps
from sklearn.preprocessing import StandardScaler

class saddle_bif(): 
  def __init__(self, lamb, time, init, noise=None):
    self.time = time
    def saddle_node_eq(x, t):
      dx = lamb + x**2
      return dx
    self.label = 0
    self.value = odeint(saddle_node_eq, init, t = time)
    if noise == 'Gaussian':
      self.value = odeint(saddle_node_eq, init, t = time) + np.random.normal(0, 1e-5,np.shape(self.value))
    elif noise == None:
      self.value = self.value
  
  def describe(self):

    plt.plot(self.time, *self.value.T)
    plt.xlabel("t Axis")
    plt.ylabel("X Axis")
    plt.title("Saddle-Node Bifurcation")

    plt.show()

class trans_bif(): #transcritical Bifurcation
  def __init__(self, lamb, time, init, noise=None):
    self.time = time
    def trans_bif_eq(x, t):
      dx = lamb*x + x**2
      return dx
    self.label = 1
    self.value = odeint(trans_bif_eq, init, t = time)
    if noise == 'Gaussian':
      self.value = odeint(trans_bif_eq, init, t = time) + np.random.normal(0, 1e-5,np.shape(self.value))
    elif noise == None:
      self.value = self.value
  
  def describe(self):

    plt.plot(self.time, *self.value.T)
    plt.xlabel("t Axis")
    plt.ylabel("X Axis")
    plt.title("Transcritical Bifurcation")

    plt.show()

class super_pitchfork(): #Supercritical Pitchfork Bifurcation
  def __init__(self, lamb, time, init, noise=None):
    self.time = time
    def super_pitchfork_eq(x, t):
      dx = lamb*x - x**3
      return dx
    self.label = 2
    self.value = odeint(super_pitchfork_eq, init, t = time)
    if noise == 'Gaussian':
      self.value = odeint(super_pitchfork_eq, init, t = time) + np.random.normal(0, 1e-5,np.shape(self.value))
    elif noise == None:
      self.value = self.value
  
  def describe(self):

    plt.plot(self.time, *self.value.T)
    plt.xlabel("t Axis")
    plt.ylabel("X Axis")
    plt.title("Supercritical Pitchfork Bifurcation")

    plt.show()

class sub_pitchfork(): #Subcritical Pitchfork Bifurcation
  def __init__(self, lamb, time, init, noise=None):
    self.time = time
    def sub_pitchfork_eq(x, t):
      dx = lamb*x + x**3
      return dx
    self.label = 3
    self.value = odeint(sub_pitchfork_eq, init, t = time)
    if noise == 'Gaussian':
      self.value = odeint(sub_pitchfork_eq, init, t = time) + np.random.normal(0, 1e-5,np.shape(self.value))
    elif noise == None:
      self.value = self.value
  
  def describe(self):

    plt.plot(self.time, *self.value.T)
    plt.xlabel("t Axis")
    plt.ylabel("X Axis")
    plt.title("Subcritical Pitchfork Bifurcation")

    plt.show()

class Hysteresis(): #System with Hysteresis
  def __init__(self, lamb, time, init, noise=None):
    self.time = time
    def hysteresis_eq(x, t):
      dx = lamb + x - x**3
      return dx

    self.label = 4
    self.value = odeint(hysteresis_eq, init, t = time)
    if noise == 'Gaussian':
      self.value = odeint(hysteresis_eq, init, t = time) + np.random.normal(0, 1e-5,np.shape(self.value))
    elif noise == None:
      self.value = self.value
  
  def describe(self):

    plt.plot(self.time, *self.value.T)
    plt.xlabel("t Axis")
    plt.ylabel("X Axis")
    plt.title("System with Hysteresis")

    plt.show()

def gen_BIF (N= 100, func = saddle_bif, noise = 'Gaussian', sign = 'pos'):
  param = []
  for i in range(N):
    param_set = {}
    if sign == 'pos':
        gen_lamb = random.uniform(1,10)
    else:
        gen_lamb = random.uniform(-10,-1)
    gen_init = random.uniform(-1,1)
    gen_t = np.linspace(0,random.uniform(1,10), 1001)
    gen_t = random.sample(list(gen_t), random.randint(250,1000))
    gen_t = np.sort(gen_t)
    param_set['lamb'], param_set['init'], param_set['t'] = gen_lamb, gen_init, gen_t
    param.append(param_set)

  gen_series_set = []
  for param in param:
    gen_series = func(lamb = param['lamb'], init = param['init'], 
                      time = param['t'], noise = noise)
    label = gen_series.label
    gen_series_set.append([gen_series.value, param['t'], label])

  return gen_series_set

def coef_processing(Data):
  X_data, y_data = [], []
  for series, time, label in Data:
    try:
      model_sindy = ps.SINDy()
      model_sindy.fit(series, t = time)
      coef = model_sindy.coefficients().reshape(-1)
      X_data.append(coef)
      y_data.append(label)
    except:
      pass
  return X_data, y_data