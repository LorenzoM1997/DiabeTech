import numpy as np

output_file = open("complete_database","w")
numfiles = 69

def normalize_code(code):
    code_array = np.zeros(18, dtype=int)
    if code == 33:
        i = 0
    elif code == 34:
        i = 0
    elif code == 35:
        i = 1
    elif code == 48:
        i = 2
    elif code == 57:
        i = 2
    elif code == 58 :
        i = 3
    elif code == 59:
        i = 4
    elif code == 60:
        i = 5
    elif code == 61:
        i = 6
    elif code == 62:
        i = 7
    elif code == 63:
        i = 8
    elif code == 64:
        i = 9
    elif code == 65:
        i = 10
    elif code == 66:
        i = 11
    elif code == 67:
        i = 12
    elif code == 68:
        i = 13
    elif code == 69:
        i = 14
    elif code == 70:
        i = 15
    elif code == 71:
        i = 16
    else:
        return "error"

    code_array[i] = 1
    string_code = ""

    for j in range(17):
        string_code = string_code + str(code_array[j]) + ","
    
    return string_code

def normalize_time(time,code):
    hours = int(time.split(':')[0])
    minutes = int(time.split(':')[1])

    num_time = hours * 60 + minutes
    if code >= 33 and code <= 35:
        num_time += 1
    return str(num_time)

def convert(date):
    value = int(date.split('-')[2]) * 365 + int(date.split('-')[0]) * 31 + int(date.split('-')[1])
    return value

for patient in range(numfiles):
    filename = "data-"
    if patient < 9:
        filename = filename + "0"
    filename = filename + str(patient + 1)
    input_file = open(filename, "r")

    first_day = None
    for line in input_file:
        #read and normalize
        
        date = line.split('\t')[0]
        if first_day == None:
            first_day = convert(date)
        n_date = str(convert(date) - first_day)                                                    
        time = line.split('\t')[1]
        code = int(line.split('\t')[2])
        value = line.split('\t')[3]
        if any(c.isalpha() for c in value):
           break
        if any(c == '\'' for c in value):
            break
        if any(c == '.' for c in value):
            break
        n_code = normalize_code(code)
        if n_code == "error":
            break
        n_time = normalize_time(time, code)
        if int(n_time) > 1440:
            break
        output = str(patient)+ ',' + n_date + ',' + n_time + ',' + n_code + value
        output_file.write(output)
    input_file.close()

output_file.close()

    
