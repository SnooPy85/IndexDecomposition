# Index Decomposition Analysis
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
        
    sector  _2018   _2019 _2020 _2021
    A       1   1.2   1.3   1.3
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
