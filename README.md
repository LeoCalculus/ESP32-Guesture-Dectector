# ESP32-Guesture-Dectector
Implemented with C++ and Python

## Stage 1: Setup
-[x] Put the sensors together with ESP32 and ensure the I2C communication is OK.  
-[x] Continuously to read data from sensor and format the output.  
-[x] Set up bluetooth for remote reading.  

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