import numpy as np
import time

npzfile = np.load("../processed/complete_database.npz")
data = np.reshape(np.copy(npzfile['arr_0']), (-1, 5))

def isTimeFormat(time):
    if int(time.split(':')[0]) < 23:
        True
    else:
        False

def valid_code(code):
    if code < 33:
        False
    elif code > 35 and code < 48:
        False
    elif code > 49 and code < 57:
        False
    elif code > 71:
        False
    else:
        True

i = 0
while True:
    i += 1;
    if i == len(data):
        break
    row = data[i]
    time = row[2]
    if isTimeFormat(time) == False:
        data = np.delete(data, i, 0)
        
        i -= 1
        continue

    code = int(row[3])
    
    if valid_code(code) == False:
        data = np.delete(data, i, 0)
        i -= 1
        continue

    value = row[4]
    value = value.rstrip()
    if any(c.isalpha() for c in value):
        data = np.delete(data, i, 0)
        i -= 1
        continue
    
    if i + 1 == len(data):
        break

np.savez("../processed/cleaned_complete_database.npz",data)
    
