#pragma once
#include <vector>
#include <cmath>
#include <algorithm>

class NeuralNetwork {
private:
    // Helper functions
    void relu(const float* input, float* output, int size);
    void softmax(const float* input, float* output, int size);
    void matrix_multiply(const float* input, const float weights[][256], const float* biases, float* output, int input_size, int output_size);
    void matrix_multiply_128(const float* input, const float weights[][128], const float* biases, float* output, int input_size, int output_size);
    void matrix_multiply_64(const float* input, const float weights[][64], const float* biases, float* output, int input_size, int output_size);
    void matrix_multiply_32(const float* input, const float weights[][32], const float* biases, float* output, int input_size, int output_size);
    void matrix_multiply_4(const float* input, const float weights[][4], const float* biases, float* output, int input_size, int output_size);
    void normalize_input(const float* input, float* output);

public:
    NeuralNetwork();
    void predict(const float* input, float* output);
    int get_prediction_class(const float* input);
    const char* get_class_name(int class_idx);
};