"""
made by Lorenzo Mambretti
2/4/2018
Visualize the measurements of glucose for patient 0
"""
import numpy as np
import matplotlib.pyplot as plt

# load the data from file
npzfile = np.load("../processed/cleaned_complete_database.npz")
data = np.reshape(np.copy(npzfile['arr_0']), (-1, 5))

# create the matrices to store the measurements for patient 0
measure = np.zeros(0)
time_axis = np.zeros(0)

def convert(time):
    hour = int(time.split(':')[0])
    minutes = int(time.split(':')[1])
    return (hour * 60) + minutes

# select the right rows and columns
for row in data:
    if row[0] == '1':
        break
    else:
        code = int(row[3])
        if code >= 33 and code  <= 35:
            measure = np.append(measure, int(row[4]))
            time = convert(row[2])
            time_axis = np.append(time_axis, time)

plt.scatter(measure, time_axis)
plt.show()

