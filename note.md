# Work Flow for Gesture Prediction Project

Note: This project aims to detect 3 gestures: line, arc and circle, with dense neural network.


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