import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

def indicator(x,bucket):
    if(bucket%2==0): #number of buckets have to be strictly odd
        return 0,0
    else:    
        dif=np.array(np.diff(x))     
        output=np.zeros(len(x))
        ratio=np.zeros(len(x))
    
    #used to calculate the ratio of change in value from yesterday's value     
        for i in range(1,len(x)): 
            ratio[i]=(100*dif[i-1]/x[i])
            
    #values have the percentile boundary values of the buckets.
    #eg: if bucket=3, values = [33 percentile , 66 percentile] value

        values=np.array(range(bucket-1))    
        for i in range(len(values)):
            values[i]=np.sort(ratio)[int(len(x)/bucket)*(i+1)-1]

    #buckets have the categorical value that needs to be filled.
    #eg: if bucket=3, buckets= [-1,0,1]

        start=-int((bucket-1)/2)
        buckets=np.array(range(bucket))        
        for i in range(len(buckets)):
            buckets[i]=start
            start+=1
            
    #This loop is used to assign the custom bucket values.
    #eg: if bucket =3, value -1 is assigned if the value is below 33 pecentile
    # value 0 for between 33 to 66 percentile
    #value 1 for above 66 percentile. 

        for i in range(len(ratio)): #used to assign values for 
            for j in range(len(values)):
                if (j==0):
                    if(ratio[i]<=values[j]):
                        output[i]=buckets[j]
                    else:
                        pass
                elif j==(len(values)-1):
                    if(ratio[i]>values[j]):
                        output[i]=buckets[j+1]
                    else:
                        pass
                elif (ratio[i]>values[j-1]) and (ratio[i]<values[j]):
                    output[i]=buckets[j]  
        return output

#taked pandas as the input and returns the indicator pandas, 
#with indicator values split into as many buckets as specified.

def indicator_panda(p,bucket):
    out=pd.DataFrame()
    for i in p.columns:
        out[i]=indicator(p[i].values,bucket)
    return out