import numpy as np

def score_mape(y_pred, y_true, as_days=False):
    """Returns the Mean Absolute Error Percentage 
    for the 10 weeks to predict

    input:
    @y_pred: prediction of the next 10 week
    @y_true: true values of the next 10 week
    @as_days: True if y's are days, False if y's are weeks
    """
    if as_days:
    	# convert array from days to week by taking average every 5 days
    	y_pred = np.array([np.mean(y_pred[i:i+5]) 
    		for i in range(0, len(y_pred), 5)])
    	y_true = np.array([np.mean(y_true[i:i+5]) 
    		for i in range(0, len(y_true), 5)])
    	print(y_pred)
    	print(y_true)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return mape

y_true = np.array([1,2,3,4,5,1,2,3,4,5])
y_pred = np.array([2,2,3,4,5,1,2,3,4,5])
print(score_mape(y_pred, y_true, as_days=True))
