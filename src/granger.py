#################################################################################################################
# Author: Alexander Diedrich
# Date: 05.05.2022
# Description: File to perform Granger Causality analysis
#################################################################################################################

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests, adfuller
from statsmodels.tsa.api import VAR
from statsmodels.tools.eval_measures import rmse, aic

#Run an ADF test to check for stationarity
def adf_test(data):
    ''' ADF für stationary '''


    tolerance = 1e-5  # Define a tolerance level for considering values as constant

    columns_to_remove = []  # List to store indices of columns to be removed
    length = data.shape[1]
    pvalue = []
    adf_lag = []

    for n in range(0, length):
        array = data.iloc[:, n]
        if np.allclose(array, array.iloc[0], atol=tolerance):
            columns_to_remove.append(n)
        else:
            print(n)
            print(array)
            stationary = adfuller(array)
            pvalue.append(stationary[1])
            adf_lag.append(stationary[2])

    # Remove constant columns from the data
    data = data.drop(data.columns[columns_to_remove], axis=1)

    return pvalue, adf_lag



'''
    length = data.shape[1]
    pvalue = []
    adf_lag = []
    
    for n in range(0, length):
        print(n)
        array = data.iloc[:,n]
        print(array)
        stationary = adfuller(array)
        pvalue.append(stationary[1])
        adf_lag.append(stationary[2])'''
    
    

    
# Create the matrix with the result from granger causality. Maxlag is dertermined with AIC. 
def create_matrix(data, variables, test = 'ssr_chi2test', maxlag=1, verbose=False):
    ''' Granger causality, results as matrix '''
    dataset = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)

    for c in dataset.columns:
        for r in dataset.index:
            try:
                test_result = grangercausalitytests(data[[r,c]], maxlag=maxlag)
            
                p_values = [round(test_result[i+1][0][test][1],4) for i in range(maxlag)]
                if verbose: print(f'Y = {r}, X = {c}, P Values = {p_values}')

                min_p_value = np.min(p_values)
                dataset.loc[r,c] = min_p_value
            except Exception as inst:
                print(inst)  
                pass

    dataset.columns = [var + '_x' for var in variables]
    dataset.index = [var + '_y' for var in variables]
    print('GC done!')
    return dataset

# Function to perform the adf tests. P-value of 5%. If data is stationary, try to take the derivative.
def perform_adf_tests(data, repetitions=10, pvalueTau=0.05):
    for _ in range (0, repetitions):
        weiter = False
        pvalues, lag = adf_test(data)

        # stationary durch diff oder log
        for i in range(0,len(pvalues)):
            if pvalues[i] > pvalueTau:
                data.iloc[:,i] = data.iloc[:,i].diff() #Differentiate to get stationarity
                data.drop(data.index[0], inplace=True)
                weiter = True
                #print (i)
        if weiter == False:
            break
    return data

#Calculate AIC to determine the optimal lag.
def calculateAIC(data, repetitions=7):
    model = VAR(data) #recall that rawData is w/o difference operation
    for i in range(1,repetitions):
        result = model.fit(i)
        try:
            print('Lag Order =', i)
            print('AIC : ', result.aic)
            print('BIC : ', result.bic)
            print('FPE : ', result.fpe)
            print('HQIC: ', result.hqic, '\n')
        except Exception as e:
            print("AIC exception: ", e)
            continue
