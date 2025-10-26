print('Setting up')

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from utilis import *
from sklearn.model_selection import train_test_split

### Step 1 -> Importing and Renaming Data (import Excel sheet and allow connection from python)
path = 'myData'
data = importDataInfo(path)

### Step 2 -> Visualization and Distribution of Data (clean and plot data to ensure accurate steering angles)
data = balanceData(data, display = False)

### Step 3 -> Prepare for Process (put all images/steering values in lists and convert to numpy arrays)
imagesPath, steerings = loadData(path, data)
#print(imagesPath[0], steering[0])

### Step 4 -> Split Data (splits data into training and validation. Training data is used to create the model
# the validation data is used to test performance after each epoch)
xTrain, xVal, yTrain, yVal = train_test_split(imagesPath, steerings, test_size=0.2, random_state=5)
print("Total Training Images: ", len(xTrain))
print("Total Validation Images: ", len(xVal))

### Step 5 -> Augmentation of data (add variety to data, zoom, left, right, to have different data to get more images)

### Step 6 -> Preprocessing, (pre-process image to crop only road region)

### Step 7 -> Creating the Neural Network model
print('Generating Model')
model = createModel()
model.summary()

### Step 8 -> Train model
history = model.fit(batchGen(xTrain,yTrain,100,1), steps_per_epoch= 300, epochs = 10,
                    validation_data=batchGen(xVal, yVal, 100,0), validation_steps = 200)

### Step 9 -> Output Model and Graph
model.save('model.h5')
print('Model Saved')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training', 'Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()