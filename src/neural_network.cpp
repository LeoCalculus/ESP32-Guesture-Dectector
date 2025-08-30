#include "neural_network.h"
#include "model_parameters.h"
#include <iostream>

NeuralNetwork::NeuralNetwork() {

}

void NeuralNetwork::normalize_input(const float* input, float* output) {
    // Calculate mean
    float mean = 0.0f;
    for (int i = 0; i < 300; i++) {
        mean += input[i];
    }
    mean /= 300.0f;
    
    // Calculate standard deviation
    float variance = 0.0f;
    for (int i = 0; i < 300; i++) {
        float diff = input[i] - mean;
        variance += diff * diff;
    }
    variance /= 300.0f;
    float std_dev = sqrt(variance) + 1e-8f;
    
    // Z-score normalization
    for (int i = 0; i < 300; i++) {
        output[i] = (input[i] - mean) / std_dev;
    }
}

void NeuralNetwork::relu(const float* input, float* output, int size) {
    for (int i = 0; i < size; i++) {
        output[i] = input[i] > 0.0f ? input[i] : 0.0f;
    }
}

void NeuralNetwork::softmax(const float* input, float* output, int size) {
    float max_val = input[0];
    for (int i = 1; i < size; i++) {
        if (input[i] > max_val) max_val = input[i];
    }
    
    float sum = 0.0f;
    for (int i = 0; i < size; i++) {
        output[i] = exp(input[i] - max_val);
        sum += output[i];
    }
    
    for (int i = 0; i < size; i++) {
        output[i] /= sum;
    }
}

void NeuralNetwork::matrix_multiply(const float* input, const float weights[][256], const float* biases, float* output, int input_size, int output_size) {
    for (int i = 0; i < output_size; i++) {
        output[i] = biases[i];
        for (int j = 0; j < input_size; j++) {
            output[i] += input[j] * weights[j][i];
        }
    }
}

void NeuralNetwork::matrix_multiply_128(const float* input, const float weights[][128], const float* biases, float* output, int input_size, int output_size) {
    for (int i = 0; i < output_size; i++) {
        output[i] = biases[i];
        for (int j = 0; j < input_size; j++) {
            output[i] += input[j] * weights[j][i];
        }
    }
}

void NeuralNetwork::matrix_multiply_64(const float* input, const float weights[][64], const float* biases, float* output, int input_size, int output_size) {
    for (int i = 0; i < output_size; i++) {
        output[i] = biases[i];
        for (int j = 0; j < input_size; j++) {
            output[i] += input[j] * weights[j][i];
        }
    }
}

void NeuralNetwork::matrix_multiply_32(const float* input, const float weights[][32], const float* biases, float* output, int input_size, int output_size) {
    for (int i = 0; i < output_size; i++) {
        output[i] = biases[i];
        for (int j = 0; j < input_size; j++) {
            output[i] += input[j] * weights[j][i];
        }
    }
}

void NeuralNetwork::matrix_multiply_4(const float* input, const float weights[][4], const float* biases, float* output, int input_size, int output_size) {
    for (int i = 0; i < output_size; i++) {
        output[i] = biases[i];
        for (int j = 0; j < input_size; j++) {
            output[i] += input[j] * weights[j][i];
        }
    }
}

void NeuralNetwork::predict(const float* input, float* output) {
    // buffers for intermediate calculations
    static float normalized[300];
    static float layer1_out[256];
    static float layer2_out[128];
    static float layer3_out[64];
    static float layer4_out[32];
    static float layer5_out[4];
    
    // Normalize input
    normalize_input(input, normalized);
    
    // Layer 1: 300 -> 256
    matrix_multiply(normalized, LAYER_1_WEIGHTS, LAYER_1_BIASES, layer1_out, 300, 256);
    relu(layer1_out, layer1_out, 256);
    
    // Layer 2: 256 -> 128
    matrix_multiply_128(layer1_out, LAYER_2_WEIGHTS, LAYER_2_BIASES, layer2_out, 256, 128);
    relu(layer2_out, layer2_out, 128);
    
    // Layer 3: 128 -> 64
    matrix_multiply_64(layer2_out, LAYER_3_WEIGHTS, LAYER_3_BIASES, layer3_out, 128, 64);
    relu(layer3_out, layer3_out, 64);
    
    // Layer 4: 64 -> 32
    matrix_multiply_32(layer3_out, LAYER_4_WEIGHTS, LAYER_4_BIASES, layer4_out, 64, 32);
    relu(layer4_out, layer4_out, 32);
    
    // Layer 5: 32 -> 4 (output)
    matrix_multiply_4(layer4_out, LAYER_5_WEIGHTS, LAYER_5_BIASES, layer5_out, 32, 4);
    softmax(layer5_out, output, 4);
}

int NeuralNetwork::get_prediction_class(const float* input) {
    static float predictions[4];
    predict(input, predictions);
    
    // Debug output
    std::cout << "Raw predictions: ";
    for (int i = 0; i < 4; i++) {
        std::cout << predictions[i] << " ";
    }
    std::cout << std::endl;
    
    int max_idx = 0;
    float max_val = predictions[0];
    
    for (int i = 1; i < 4; i++) {
        if (predictions[i] > max_val) {
            max_val = predictions[i];
            max_idx = i;
        }
    }
    
    return max_idx;
}

const char* NeuralNetwork::get_class_name(int class_idx) {
    const char* class_names[] = {"Arc", "Circle", "Line", "Others"};
    if (class_idx >= 0 && class_idx < 4) {
        return class_names[class_idx];
    }
    return "Unknown";
}