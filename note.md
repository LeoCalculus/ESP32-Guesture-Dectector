# Work Flow for Gesture Prediction Project

This project aims to detect 3 gestures: line, arc and circle, with dense neural network, meanwhile there
will be an "other" option to filter some gestures that does not belong to any of them.

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

---

# Stages of deep neural network
1. In each csv file, I have around 50 examples and for each examples I have sampled 50 times of its acceleration data; meanwhile, get a batch we should have mixed examples, therefore, I plan to have a 
batch with size (16, 50, 6) the first 16 means it contain 16 examples from all four gestures and 50
means each example has 50 sampled data and 6 means 6 dimension of acceleration, the data will be flatterned
to feed into model training. After flatting the batch matrix, I should expect a (16, 300) size matrix.
2. For a gesture detection NN, the hidden layer should be large, at least 3+ layers, so first layer I plane to have layers like: first layer 256 neurons, second layer 128 neurons, third layer 64 neuron, fourth layer 16 neurons, and last layer 4 neurons which correspond to 4 outputs, and for first four layers after the linear transformation, I will apply the ReLU activation function and for the last layer I will use softmax activation function so I can get a probability of four gestures map the expect output will be (16, 4) for 16 examples each example has four column which corresponds to arc, circle, line and others.
3. The result will compare with actual result which will be coded into one hot code, for example arc the matrix will be like: [1, 0, 0, 0], the loss will be calculated with cross entropy loss function and the backward propagation's required for gradient descent will be proceeded by autograd in PyTorch

---

# Exception records
When I was training my model using Coursera technic, I found my model suck at 1.386 and the output for probability is 0.25 for all, the cost did not change may be due to learning rate problem and weight problem, I improved the learning rate by 10 times but things did not change, then I went to see the weight, I found if I initialize all weights with 10 times large the loss become normal and converges quickly, this may due to small weights lead to weak signal in NN. 

---

# Final performance
The model is good at detecting arc and circle, but it has difficulty in detecing linear guestures.
