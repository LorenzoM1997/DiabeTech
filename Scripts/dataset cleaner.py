import numpy as np

input_file = open("complete_database","r")
outfile = "clean_dataset.npz"

prev_line = None

def can_merge(code, prev_code):
    if min(code,prev_code) >= 6 and min(code,prev_code) <= 12:
        if max(code,prev_code) >= 13 and max(code,prev_code) <19:
            return True
        else:
            return False
    else:
        return False

data = np.zeros((0,21), dtype=int)

for line in input_file:
    moved = False
    if prev_line != None:
        prev_time = prev_line.split(',')[2]
        time = line.split(',')[2]
        prev_value = prev_line.split(',')[20].rstrip()
        for i in range(3,19):
            if int(line.split(',')[i]) == 1:
                code = i
        for i in range(3,19):
            if int(prev_line.split(',')[i]) == 1:
                prev_code = i
        
        if can_merge(code, prev_code):
            if abs(int(prev_time) - int(time)) <10:
                row = np.zeros(21)
                row[code] = 1
                row[prev_code] = 1
                row[0] = line.split(',')[0]
                row[1] = line.split(',')[1]
                row[2] = int(time)
                if prev_code < code:
                    row[20] = prev_value
                else:
                    row[20] = value
                data = np.append(data, row)
            prev_line = False
        else:           
            if time == prev_time:
                value = line.split(',')[20].rstrip()
                prev_value = str(np.floor((int(prev_value) + int(value)) / 2))
                moved = True
            if not moved:
                row = prev_line.split(',')
                row[20] = row[20].rstrip()
                data = np.append(data, row)
        
    prev_line = line
    
np.savez(outfile, data)
input_file.close()
