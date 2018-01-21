import numpy as np

print("loading")
npzfile = np.load("clean_dataset.npz")
dat = np.reshape(npzfile['arr_0'], (-1, 21))
data = np.copy(dat)
i = 0
while i < len(data):
    if data[i][0].astype(float) > 0:
        break
    else:
        i += 1
data = data[:i]
data = data.astype(float)
for row in data:
    row[6] = row[6] + row[8] + row[10] + row[12]
    row[7] = row[7] + row[9] + row[11] + row[13]

for _ in range(6):
    data = np.delete(data, 8, 1)

np.savez("small_but_prettier_dataset.npz", data)
