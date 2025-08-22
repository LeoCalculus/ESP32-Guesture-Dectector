# Work Flow for Gesture Prediction Project

Note: This project aims to detect 3 gestures: line, arc and circle, with dense neural network.

## Stage 1: Setup
-[ ] Put the sensors together with ESP32 and ensure the I2C communication is OK.
-[ ] Continuously to read data from sensor and format the output.

## Stage 2: Data 
-[ ] Format the data in either .csv format or .txt format, the data should include 
both X,Y,Z acceleration data and Gyro acceleration data.
-[ ] Label each group of data to match certain gesture.
-[ ] Format the data into batches used for training.
-[ ] Format batches into two training sets, one used for training the network and the other
used for test and prediction.

## Stage 3: Training the neural network
-[ ] Use Python to deploy a dense neural network with multiple hidden layers.
-[ ] Train the data and attempt to get the success rate 70%-80%, if cannot, go back to Stage 2
to get more data.
-[ ] If prediction is OK, extract weight, bias and other important data from neural network.

## Stage 4: Deploy on ESP32 
-[ ] Make the forward propagation model in esp32 used for prediction.
-[ ] Connect the esp32 GPIO pins to three different LEDs for prediction output.
-[ ] Test and try for multiple cases. 

---

# Other Notes:

To update the pio default python environment, we should use command:
```bash 
& "$HOME\.platformio\penv\Scripts\python.exe" -m pip install <packageName>
```

The prediction data will be composed into both X,Y,Z acceleration and Gyro acceleration data,
using both of them since user movements are random, having both acceleration data will be useful
in predicting the user movement vectors.

The data will have a similar style like training the images, the images we used to train each 
pixel which each one has three dimension Red, Green and Blue. Similarly, for each sample
took by the microcontroller we have total six dimensions: X,Y,Z acceleration and Gyro acceleration.

And for entire motion of one gesture will be composed into one big column matrix starting from 
all x samples and then y samples ..., end with Gyro z samples, we arrange group of column matrix 
to compose a bigger batch matrix which enable us for vectorization work.