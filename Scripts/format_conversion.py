import numpy as np

data = np.zeros((0,5))
numfiles = 69

for patient in range(numfiles):
    filename = "../RAW/data-"
    if patient < 9:
        filename += "0"
    filename += str(patient + 1)
    
    inFile = open(filename, "r")

    for line in inFile:
        # read and save in the matrix
        row = np.append(str(patient), line.split('\t'))
        if len(row) != 5:
            continue
        data = np.append(data, row)

    inFile.close()

np.savez("../Processed/complete_database", data)
