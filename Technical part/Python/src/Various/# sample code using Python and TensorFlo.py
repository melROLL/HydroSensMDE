# sample code using Python and TensorFlow library to train a CNN to detect if the paper is wet or not 
# thisi=s from chat gpt 
# rthis file is not compiling yet 

import tensorflow as tf
from tensorflow.keras import layers

# load dataset and prepare data

# define the model
model = tf.keras.Sequential([
  layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
  layers.MaxPooling2D(),
  layers.Conv2D(64, (3,3), activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(1, activation='sigmoid')
])

# compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# train the model
model.fit(train_data, epochs=10, validation_data=val_data)

# evaluate the model
test_loss, test_acc = model.evaluate(test_data)
print('Test accuracy:', test_acc)
