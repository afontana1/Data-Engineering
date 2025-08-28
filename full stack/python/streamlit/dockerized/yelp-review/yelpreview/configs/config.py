"""Model configurations in json format. 
Paths are always relative to the location of the command line,
paths are not relative to any objects in the source codes.
If you are not running scripts from the root folder (e.g., using cd instead), 
then the paths here need to be checked and modified accordingly"""


# "./" = root folder of the project
CFGLog = {
    "data": {
        "path": "./data/yelp.csv",
        "x": "text",
        "y": "stars",
        "test_size": 0.2,
        "random_state": 2022,
        "ngram_range": (1, 2),
        "min_df": 10

    },
    "train": {
            "solver": "liblinear",
            "max_iter": 1000,
            "random_state": 2022,
            "C": 0.01,
            "penalty": "l2",
    },
    "output": {
        "output_path": "./data/exported_models/",
        "model_name": "20230217_152148_LogReg.pickle",
    }
}