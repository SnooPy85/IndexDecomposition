#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 15:51:39 2021

@author: Sascha Rexhäuser
"""

import numpy as np
import pandas as pd
    

class IndexDecomposition(object):
    
    def __init__(self, df_size, df_indicator, id_column = None, method = "LMD"):
        if id_column:
            self.__df_y = df_size.drop(id_column, axis = 1)
            self.__df_i = df_indicator.drop(id_column, axis = 1)
        else:
            self.__df_y = df_size
            self.__df_i = df_indicator
        self.__method = method


    @classmethod
    def _logMean(cls, x, y):
        if x == y:
            return x
        else:
            try:
                return (y - x)/(np.log(y) - np.log(x))
            except:
                raise ZeroDivisionError("At least on data point is zero or negative. Please use the Laspeyeres or Arithmetic Mean Divisia Method.")
    

    @classmethod
    def _modifiedLog(cls, number):
        if number == 0:
            return np.log(number + 0.0001)
        else:
            try:
                return np.log(number)
            except:
                raise ZeroDivisionError("At least on data point is zero or negative. Please use the Laspeyeres or Arithmetic Mean Divisia Method.")


    @classmethod
    def _get_lmd_indices(cls, list_y, list_y_base, list_i, list_i_base):
                  
        list_int = [x/y for x, y in zip(list_i, list_y)]
        list_int_base = [x/y for x, y in zip(list_i_base, list_y_base)]
        list_int_change = [x/y for x, y in zip(list_int, list_int_base)]
        
        list_struct = [x/np.sum(list_y) for x in list_y]
        list_struct_base = [x/np.sum(list_y_base) for x in list_y_base]
        list_struct_change = [x/y for x, y in zip(list_struct, list_struct_base)]
                
        list_omega = [x/np.sum(list_i) for x in list_i]
        list_omega_base = [x/np.sum(list_i_base) for x in list_i_base]
        list_log_mean_omega = [cls._logMean(x, y) for x, y in zip(list_omega, list_omega_base)]
        sum_log_mean_omega = np.sum(list_log_mean_omega)
        
        if sum_log_mean_omega == 0:
            scale_effect = 0
            tech_effect = 0
            comp_effect = 0
        else:
            scale_effect = np.exp(np.sum([x/sum_log_mean_omega*cls._modifiedLog(np.sum(list_y)/np.sum(list_y_base)) for x in list_log_mean_omega]))
            tech_effect = np.exp(np.sum([x/sum_log_mean_omega*cls._modifiedLog(y) for x, y in zip(list_log_mean_omega, list_int_change)]))
            comp_effect = np.exp(np.sum([x/sum_log_mean_omega*cls._modifiedLog(y) for x, y in zip(list_log_mean_omega, list_struct_change)]))
        
        total_effect = scale_effect*tech_effect*comp_effect
        
        return (total_effect, scale_effect, tech_effect, comp_effect)
        
    
    @classmethod
    def _get_amd_indices(cls, list_y, list_y_base, list_i, list_i_base):
        pass
        
        
    @classmethod
    def _get_lpi_indices(cls, list_y, list_y_base, list_i, list_i_base):
        pass
    
    
    def get_results(self):
        
        states = list(self.__df_y.columns.values)
        total_effect = []
        scale_effect = []
        tech_effect = []
        comp_effect = []
        
        if self.__method == "LMD":
            for s in range(0, len(states)):
                # assuming that first state is base/initial state.
                total_i, scale_i, tech_i, comp_i = self._get_lmd_indices(self.__df_y[states[s]], 
                                                                        self.__df_y[states[0]], 
                                                                        self.__df_i[states[s]], 
                                                                        self.__df_i[states[0]])
                
                total_effect.append(total_i)
                scale_effect.append(scale_i)
                tech_effect.append(tech_i)
                comp_effect.append(comp_i)
                   
        else:
            pass 
        
        return pd.DataFrame({'states': states, 'total effect': total_effect, "scale effect": scale_effect, "technology effect": tech_effect, "composition effect": comp_effect})


#if __name__ == "__main__":
#    
#    output = pd.read_csv("example_output_data.csv", sep = ",").drop('desc', axis = 1)
#    energy = pd.read_csv("example_energy_data.csv", sep = ",").drop('desc', axis = 1)
#    
#    test = IndexDecomposition(df_size = output, df_indicator = energy, id_column = "code")
#    print(test.get_results())
    