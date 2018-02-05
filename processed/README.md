# Processed data
Folder containing all the processed file. All the files are in format .npz, which can be opened using Numpy (python library)

## Instructions

If you want to use the data in python in tensorflow we reccomend to use this script for both files

    import numpy as np
    
    npzfile = np.load("../processed/cleaned_complete_database.npz")
    data = np.reshape(np.copy(npzfile['arr_0']), (-1, 5))

The matrix data can then be used without any concern in python for reuse and modification.
