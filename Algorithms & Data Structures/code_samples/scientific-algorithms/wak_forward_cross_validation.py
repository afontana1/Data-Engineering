import random
import math
import matplotlib.pyplot as plt

#time series cross validation

def walk_forward_procedure(
        series: list, training_size:float, backtest_size:float, subset_size: int
) -> dict[str,dict[str,list]]:
    """Create train test split for time series data.

    Given an array of length N, create a window function that partitions data
    into training set and testing sets

    Args:
        series (list): time series array
        training size (float): percentage of training set for each CV split
        backtest size (int): percantage, window size you want to predict
        subset size (int): the length of the subset
    return:
        {
            "split_1": {
                "train": [...],
                "test": [...]
            }
        }
    """
    params = [("training_size",training_size),("backtest_size",backtest_size),("subset_size",subset_size)]
    if any((not isinstance(y,(float,int))) for x,y in params):
        raise Exception(
            f"Type Error, make sure inputs are int {[(x,type(y)) for x,y in params]}"
        )
    if any(y<0 for x,y in params):
        raise Exception("Requires non negative inputs")
    if subset_size > len(series)//2:
        raise Exception("Split size must be less than half of the series length")
    if training_size <= backtest_size:
        raise Exception("backtest size should be less than training size")
    if training_size + backtest_size != 1:
        raise Exception("Proportions must add to 1")
    
    output = {}
    prev = 0
    current_split = 1
    while prev + 1 < len(series) - 1:
        upper_limit = prev + subset_size
        if upper_limit >= len(series):
            new_subset_size = len(series) - prev
            upper_limit = prev + new_subset_size
        
        subset = series[prev:upper_limit]
        train_split_point = math.floor(len(subset)*training_size)
        test_split_point = math.ceil(len(subset)*backtest_size)
        if train_split_point + test_split_point > len(subset):
            raise Exception("some sort of internal error calculating proportions")
        train = subset[:train_split_point]
        test = subset[-test_split_point:]
        output[f"split_{current_split}"] = {
            "train":train,
            "test":test
        }
        current_split+=1
        prev = prev + train_split_point
    
    return output

if __name__ == "__main__":
    series = [random.gauss(0,1) for i in range(130)]
    results = walk_forward_procedure(
        series = series,
        training_size = .8,
        backtest_size = .2,
        subset_size = 15
    )
    print(results)
    plt.plot(range(130),series,"k")
    plt.show()