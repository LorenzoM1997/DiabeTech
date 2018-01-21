import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score

# visulaize the important characteristics of the dataset
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
"""
# step 1: download the data
dataframe_all = pd.DataFrame(columns=list('ABCDEFGHILMNOPQRSTUVWZ'))
input_file = open("clean_dataset","r")
for line in input_file:
    row = np.zeros(22, dtype=int)
    for i in range(2,22):
        row[i] = int(line.split(',')[i])
    df2 = pd.DataFrame([row], columns=list('ABCDEFGHILMNOPQRSTUVWZ'))
    dataframe_all = dataframe_all.append(df2)
num_rows = dataframe_all.shape[0]


# step 3: get features (x) and scale the features
# get x and convert it to numpy array
x = dataframe_all.ix[:,:-1].values
standard_scaler = StandardScaler()
x_std = standard_scaler.fit_transform(x)

# step 4: get class labels y and then encode it into number 
# get class label data
y = dataframe_all.ix[:,-1].values
# encode the class label
class_labels = np.unique(y)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# step 5: split the data into training set and test set
test_percentage = 0.1
x_train, x_test, y_train, y_test = train_test_split(x_std, y, test_size = test_percentage, random_state = 0)

# t-distributed Stochastic Neighbor Embedding (t-SNE) visualization
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=0)
x_test_2d = tsne.fit_transform(x_test)

# scatter plot the sample points among 5 classes
markers=('s', 'd', 'o', '^', 'v')
color_map = {0:'red', 1:'blue', 2:'lightgreen', 3:'purple', 4:'cyan'}
plt.figure()
for idx, cl in enumerate(np.unique(y_test)):
    plt.scatter(x=x_test_2d[y_test==cl,0], y=x_test_2d[y_test==cl,1], c=color_map[idx], marker=markers[idx], label=cl)
plt.xlabel('X in t-SNE')
plt.ylabel('Y in t-SNE')
plt.legend(loc='upper left')
plt.title('t-SNE visualization of test data')
plt.show()
"""

input_file = open("clean_dataset","r")
xs = np.zeros(0, dtype=int)
ys = np.zeros(0, dtype=int)
zs = np.zeros(0, dtype=int)
for line in input_file:
    value = int(line.split(',')[20])
    third = int(line.split(',')[3])
    time = int(line.split(',')[2])
    if time < 1500:
        xs = np.append(xs, value)
        ys = np.append(ys, third)
        zs = np.append(zs, time)
    
    
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(xs,ys,zs)
plt.show()

