import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data preparation

np.set_printoptions(suppress=True, precision=3)

arc_path = 'src/arc.csv'
circle_path = 'src/circle.csv'
line_path = 'src/line.csv'
others_path = 'src/others.csv'

# each batch will have 16 example: 1 arc, 1 circle, 1 line, 1 others in order and repeat for 4 times 
# I will have 25 batches in total
# use 400 to load all examples so the batch size is flexible 
result = np.empty((400, 50, 6))  # one big batch used for training
label_result = np.empty((400, 4))  

test_set = np.empty((40, 50, 6))  
test_label = np.empty((40, 4))

# 0-109， 0-99 for training, 100-109 for testing
for i in range(110):  # each time we load 4 examples (1 arc, 1 circle, 1 line, 1 others) so we can create mixed batches in a factor of 4
    skip_rows = i * 51 + 1 if i > 0 else 0  # Skip header + previous chunks + empty lines
    arc_data = pd.read_csv(arc_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    circle_data = pd.read_csv(circle_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    line_data = pd.read_csv(line_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    others_data = pd.read_csv(others_path, nrows=50, skiprows=skip_rows, header=None).to_numpy()
    if (i < 100):
        result[i*4] = arc_data
        label_result[i*4] = [1, 0, 0, 0]  # one-hot encoding for arc
        result[i*4+1] = circle_data
        label_result[i*4+1] = [0, 1, 0, 0]  # one-hot encoding for circle
        result[i*4+2] = line_data
        label_result[i*4+2] = [0, 0, 1, 0]  # one-hot encoding for line 
        result[i*4+3] = others_data
        label_result[i*4+3] = [0, 0, 0, 1]  # one-hot encoding for others
    else: # complete the test set
        test_set[(i-100)*4] = arc_data
        test_label[(i-100)*4] = [1, 0, 0, 0]
        test_set[(i-100)*4+1] = circle_data
        test_label[(i-100)*4+1] = [0, 1, 0, 0]
        test_set[(i-100)*4+2] = line_data
        test_label[(i-100)*4+2] = [0, 0, 1, 0]
        test_set[(i-100)*4+3] = others_data
        test_label[(i-100)*4+3] = [0, 0, 0, 1]
    
# one-hot label for them: [1, 0, 0, 0] first column is arc, second is circle, third is line, fourth is others
# sample check 
print(result[8]) # it will be 0-3, 4-7, 8-11, so 8 is arc
print(label_result[8] == [1, 0, 0, 0]) # if True ok

# Flatten the matrix:
X = result.reshape(400, -1).T  # Shape: (300, 400)
y = label_result.T  # Shape: (4, 400)  

test_X = test_set.reshape(40, -1).T  
test_y = test_label.T
test_X_mean = np.mean(test_X, axis=1, keepdims=True)
test_X_std = np.std(test_X, axis=1, keepdims=True) + 1e-8
test_X_normalized = (test_X - test_X_mean) / test_X_std 

X_mean = np.mean(X, axis=1, keepdims=True)
X_std = np.std(X, axis=1, keepdims=True) + 1e-8
X_normalized = (X - X_mean) / X_std

# Model Setup

def initialize_NN_parameters(layer_dims): # layer_dims expect things like [300, 256, 128, 64, 32, 4]
    parameters = {}
    L = len(layer_dims)  # number of layers in the network

    for l in range(1, L):
        # *0.01 does not do anything in my case : loss did not change at all
        parameters['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * 0.1
        parameters['b' + str(l)] = np.zeros((layer_dims[l], 1))

    return parameters

# Activaton functions: Z is linear output, A is activation output
def ReLU(Z): # used for hidden layers
    A = np.maximum(0, Z)
    cache = Z
    return A, cache

def ReLU_derivative(dA, cache):
    Z = cache
    dZ = np.array(dA, copy=True) # recall ReLU derivative is 1 for Z > 0
    dZ[Z <= 0] = 0  
    return dZ

def stable_softmax(Z): # used for output layer
    exp_Z = np.exp(Z - np.max(Z, axis=0, keepdims=True)) # improve numerical stability https://eli.thegreenplace.net/2016/the-softmax-function-and-its-derivative/
    A = exp_Z / exp_Z.sum(axis=0, keepdims=True)
    cache = Z
    return A, cache

def stable_softmax_derivative(dA, cache): # dZ = AL - Y = dA
    return dA

def linear_forward(A, W, b): # only the linear part
    Z = np.dot(W, A) + b
    cache = (A, W, b)
    return Z, cache

def linear_activation_forward(A_prev, W, b, activation):
    if activation == "relu":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = ReLU(Z)
    elif activation == "softmax":
        Z, linear_cache = linear_forward(A_prev, W, b)
        A, activation_cache = stable_softmax(Z)
    cache = (linear_cache, activation_cache)
    return A, cache

def model_foward_porpagation(X, parameters):
    caches = []
    A = X
    L = len(parameters) // 2 

    for l in range(1, L):
        A_prev = A 
        A, cache = linear_activation_forward(A_prev, parameters['W' + str(l)], parameters['b' + str(l)], activation="relu")
        caches.append(cache)

    AL, cache = linear_activation_forward(A, parameters['W' + str(L)], parameters['b' + str(L)], activation="softmax")
    caches.append(cache)

    return AL, caches

# Compute cost -1/m * sum(y * log(AL))
def cross_entropy_loss(AL, Y): # recall AL stands for output of last layer, Y is true label
    m = Y.shape[1]
    loss = -np.sum(Y * np.log(AL)) / m 
    return loss

# Backward propagation
def linear_backward(dZ, cache): # Z^[l] = W^[l] * A^[l-1] + b^[l]
    A_prev, W, b = cache
    m = A_prev.shape[1]

    dW = np.dot(dZ, A_prev.T) / m
    db = np.sum(dZ, axis=1, keepdims=True) / m
    dA_prev = np.dot(W.T, dZ)

    return dA_prev, dW, db

def linear_activation_backward(dA, cache, activation):
    linear_cache, activation_cache = cache

    if activation == "relu":
        dZ = ReLU_derivative(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)
    elif activation == "softmax":
        dZ = stable_softmax_derivative(dA, activation_cache)
        dA_prev, dW, db = linear_backward(dZ, linear_cache)

    return dA_prev, dW, db

def model_backward_propagation(AL, Y, caches):
    grads = {}
    L = len(caches) 
    m = AL.shape[1]
    Y = Y.reshape(AL.shape) 

    dAL = AL - Y 

    current_cache = caches[L-1]
    grads["dA" + str(L-1)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL, current_cache, activation="softmax")

    for l in reversed(range(L-1)):
        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA" + str(l + 1)], current_cache, activation="relu")
        grads["dA" + str(l)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp

    return grads

def update_parameters(parameters, grads, learning_rate):
    L = len(parameters) // 2 

    for l in range(1, L + 1):
        parameters["W" + str(l)] -= learning_rate * grads["dW" + str(l)]
        parameters["b" + str(l)] -= learning_rate * grads["db" + str(l)]

    return parameters

def NN(X_norm, Y, layer_dims, learning_rate=0.001, num_iterations=5000, print_cost=False):
    np.random.seed(1)
    costs = [] 

    parameters = initialize_NN_parameters(layer_dims)

    for i in range(num_iterations):
        AL, caches = model_foward_porpagation(X_norm, parameters)

        cost = cross_entropy_loss(AL, Y)

        grads = model_backward_propagation(AL, Y, caches)

        parameters = update_parameters(parameters, grads, learning_rate)

        if print_cost and i % 100 == 0:
            print(f"Cost after iteration {i}: {cost}")
            costs.append(cost)
            
        if i % 100 == 0:
            costs.append(cost)

    if print_cost:
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per hundreds)')
        plt.title(f'Learning rate = {learning_rate}')
        plt.show()

    return parameters, costs

parameters, costs = NN(X_normalized, y, layer_dims=[300, 256, 128, 64, 32, 4], learning_rate=0.015, num_iterations=5000, print_cost=True)

# Evaluate the model
def predict(X_test, parameters):
    AL, _ = model_foward_porpagation(X_test, parameters)
    predictions = np.argmax(AL, axis=0)
    return predictions

predictions = predict(test_X_normalized, parameters)
true_labels = np.argmax(test_y, axis=0)
accuracy = np.mean(predictions == true_labels)
print(f"Test set accuracy: {accuracy:.4f}")

# Export trained model parameters 
def export_model_parameters(parameters, filename):
    L = len(parameters) // 2  # number of layers
    
    with open(filename, 'w') as f:
        for i in range(1, L + 1):
            # Get weight and bias matrices
            W = parameters[f'W{i}']
            b = parameters[f'b{i}']
            
            # Write layer info and weights
            f.write(f"# Layer {i}: {W.shape[1]} -> {W.shape[0]}\n")
            f.write(f"LAYER_{i}_WEIGHTS:\n")
            np.savetxt(f, W.T, fmt='%.8f', delimiter=',')  # Transpose to match C++ format
            f.write(f"\nLAYER_{i}_BIASES:\n")
            np.savetxt(f, b.flatten(), fmt='%.8f', delimiter=',')
            f.write("\n")

export_model_parameters(parameters, 'src/trained_model_parameters.txt')
print("Model parameters exported to src/trained_model_parameters.txt")