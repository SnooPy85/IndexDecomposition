#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  1 15:51:39 2021

@author: Sascha Rexhäuser
"""

import numpy as np
import pandas as pd
    

class IndexDecomposition(object):
    
    """
    This class allows to decompose data into several effects, namely a scale
    (size) effect, a composition (structural change) effect, and a
    technology effect (intensity or model effect). Use cases are for example
    the decomposition of a country's CO2 emissions into its drivers, meaning
    here economic growth (scale), structural change (shift from CO2-intensive
    sectors such as pulp and paper to less intensive ones like services) and
    technical change, meaning the improvement of production technologies 
    so that for the same output produced, less CO2 is produced. Of course,
    there are more various possible use cases. 
    
    The class requires on instancing
    two Pandas dataframes: df_size and df_indicator. df_size includes data
    for activity, in our example output produced by sectors. The structure of
    the dataframes should look as follows: the rows are the different units
    a total unit consists of (in our example the sectors of an economy). 
    The column for those units (if desired) can be included in the dataframe. 
    If so, the name of this column must be provided by the argument id_column. 
    The different states (e.g. years in our example) are the columns of the 
    Pandas dataframe. Here is an example:
        
    sector  _2018 _2019 _2020 _2021
      A       1     1.2   1.3   1.3
      B       3     3.3   2.9   3.5
      
    In this example, id_column must equal sector. Please make sure there is no 
    row for the total in! In a similar fashion, the dataframe df_indicator is
    the data for the indicator that should be decomposed. In our example, this
    would be CO2 emission data by sectors. 
    
    In both dataframes, the first column of
    data (not the id_column) is assumed to be the initial state (e.g. the base)
    year for comparision in our example. Thus, the columns need to be ordered.    
    
    Calling the method get_results() on an instance of IndexDecomposition 
    returns a Pandas dataframe including the results by state (e.g. years).
    
    This class is based on the index decomposition analysis survey by
    Ang and Zhang (2000), see B.W. Ang and F.Q. Zhang (2000), A survey of
    index decomposition analysis in energy and environmental studies, in:
    Energy, Vol. 25, pages 1149 - 1176. 
    """
    
    def __init__(self, df_size, df_indicator, id_column = None, method = "LMDI"):
        if id_column:
            if isinstance(df_size, pd.DataFrame) and isinstance(df_indicator, pd.DataFrame):
                self.__df_y = df_size.drop(id_column, axis = 1)
                self.__df_i = df_indicator.drop(id_column, axis = 1)
            else:
                raise TypeError("The provided data is not of type pandas dataframe. Please check.")
        else:
            if isinstance(df_size, pd.DataFrame) and isinstance(df_indicator, pd.DataFrame):
                self.__df_y = df_size
                self.__df_i = df_indicator
            else:
                raise TypeError("The provided data is not of type pandas dataframe. Please check.")
        if method in ["LMDI"]:         
            self.__method = method
        else:
            raise ValueError("The method " + method + " is not allowed. Please choose LMDI (Log Mean Divisia Index). More will be implemented later.")


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
    def _get_lmdi_indices(cls, list_y, list_y_base, list_i, list_i_base):
                  
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
        
        
    def get_results(self):
        
        states = list(self.__df_y.columns.values)
        total_effect = []
        scale_effect = []
        tech_effect = []
        comp_effect = []
        
        if self.__method == "LMDI":
            for s in range(0, len(states)):
                # assuming that first state is base/initial state.
                total_i, scale_i, tech_i, comp_i = self._get_lmdi_indices(self.__df_y[states[s]], 
                                                                        self.__df_y[states[0]], 
                                                                        self.__df_i[states[s]], 
                                                                        self.__df_i[states[0]])
                
                total_effect.append(total_i)
                scale_effect.append(scale_i)
                tech_effect.append(tech_i)
                comp_effect.append(comp_i)
                   
        else:
            print("Not yet implemented.")
        
        return pd.DataFrame({'states': states, 'total effect': total_effect, "scale effect": scale_effect, "technology effect": tech_effect, "composition effect": comp_effect})


#if __name__ == "__main__":
#    
#    output = pd.read_csv("example_output_data.csv", sep = ",").drop('desc', axis = 1)
#    energy = pd.read_csv("example_energy_data.csv", sep = ",").drop('desc', axis = 1)
#    
#    test = IndexDecomposition(df_size = output, df_indicator = energy, id_column = "code")
#    print(test.get_results())
    