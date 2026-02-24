# Perceptron Learning Examples

A beginner-friendly educational project demonstrating how a perceptron (the simplest artificial neural network) learns to classify objects through supervised learning.

## Overview

This project contains two implementations of a perceptron that learns to distinguish between **Vehicles** and **Living Beings** based on three simple features. It's designed to help students understand the fundamental concepts of machine learning and neural networks.

## Features

The perceptron uses three binary features to classify objects:

1. **Is Round** - Does it have round parts? (0 = No, 1 = Yes)
2. **Has Wheels** - Does it have wheels? (0 = No, 1 = Yes)
3. **Can Breathe** - Can it breathe? (0 = No, 1 = Yes)

### Classification Examples

**Vehicles (Output: 1)**
- Car: [1, 1, 0] - round wheels, has wheels, can't breathe
- Truck: [0, 1, 0] - not round, has wheels, can't breathe
- Bicycle: [1, 1, 0] - round wheels, has wheels, can't breathe
- Bus: [0, 1, 0] - not round, has wheels, can't breathe

**Living Beings (Output: 0)**
- Human: [1, 0, 1] - round head, no wheels, can breathe
- Dog: [0, 0, 1] - not round, no wheels, can breathe
- Cat: [0, 0, 1] - not round, no wheels, can breathe
- Bird: [1, 0, 1] - round body, no wheels, can breathe

## Files

### Notebooks (Recommended for Learning)

Work through these in order for the best learning experience:

| Notebook | Description |
|----------|-------------|
| [`01_perceptron_from_scratch.ipynb`](01_perceptron_from_scratch.ipynb) | Build a perceptron using pure Python — understand every line of the algorithm |
| [`02_perceptron_with_numpy.ipynb`](02_perceptron_with_numpy.ipynb) | Re-implement with NumPy — learn dot products and vectorised operations |
| [`03_visualising_the_perceptron.ipynb`](03_visualising_the_perceptron.ipynb) | Visualise decision boundaries, training dynamics, XOR failure, and 3-D planes |

### Python Scripts

Standalone scripts that can be run directly from the command line:

### `basic_perceptron_example.py`
Basic implementation using pure Python with explicit mathematical operations. Best for understanding the underlying mathematics step-by-step.

**Pros:**
- No external dependencies (except standard library)
- Shows explicit calculations
- Easy to understand for beginners

### `basic_perceptron_example_v2.py`
Optimized implementation using NumPy with vectorized operations. Shows how neural networks are implemented in practice.

**Pros:**
- Uses dot products and vector operations
- More efficient computation
- Industry-standard approach
- Includes educational explanation of dot products

**Requires:** NumPy

## Requirements

**For basic version / Notebook 1:**
- Python 3.6+

**For NumPy version / Notebook 2:**
- Python 3.6+
- NumPy (`pip install numpy`)

**For visualisation / Notebook 3:**
- Python 3.6+
- NumPy
- Matplotlib (`pip install matplotlib`)

## Installation

1. Clone or download this repository
2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install NumPy (for version 2 only):
   ```bash
   pip install numpy
   ```

## Usage

Run either version of the perceptron:

```bash
# Basic version (pure Python)
python basic_perceptron_example.py

# NumPy version (recommended)
python basic_perceptron_example_v2.py
```

## How It Works

### 1. Initialization
The perceptron starts with random weights and bias:
- 3 weights (one for each feature)
- 1 bias term
- Learning rate: 0.1

### 2. Training Process
For each training example:
1. **Forward Pass**: Calculate weighted sum
   - Basic: `total = w1*f1 + w2*f2 + w3*f3 + bias`
   - NumPy: `total = np.dot(weights, features) + bias`

2. **Activation**: Apply step function
   - If `total >= 0`: predict 1 (Vehicle)
   - If `total < 0`: predict 0 (Living Being)

3. **Error Calculation**: `error = target - prediction`

4. **Weight Update**: If error != 0, adjust weights
   ```python
   new_weight = old_weight + learning_rate * error * feature
   new_bias = old_bias + learning_rate * error
   ```

5. **Repeat**: Train for up to 100 epochs or until perfect accuracy

### 3. Testing
After training, test the perceptron on mystery objects to verify it learned the pattern.

## Learning Objectives

This project teaches:
- **Perceptron Algorithm**: The foundation of neural networks
- **Supervised Learning**: Learning from labeled examples
- **Weight Updates**: How neural networks adjust parameters
- **Linear Classification**: Separating data with a decision boundary
- **Vectorization**: Efficient matrix operations (Version 2)
- **Activation Functions**: Step function for binary classification

## Example Output

```
Starting weights: [-0.234, 0.567, -0.123]
Starting bias: 0.456

Training the Perceptron...
--------------------------------------------------
Epoch 1, Features: [1 1 0], Target: 1, Prediction: 1, Error: 0
Epoch 1, Features: [0 1 0], Target: 1, Prediction: 0, Error: 1
Updating weights and bias...
...
Perfect! No errors - Training complete!

========================================
Testing the Perceptron
========================================

Mystery Object 1 (round, wheels, no breath)
Features: Is Round=1, Has Wheels=1, Can Breathe=0
Prediction: VEHICLE
```

## Understanding the Math

The perceptron implements a linear decision boundary:

```
prediction = activate(w1*x1 + w2*x2 + w3*x3 + b)
```

Where:
- `w1, w2, w3` are weights (learned during training)
- `x1, x2, x3` are input features
- `b` is the bias
- `activate()` is the step function

The learning rule (Perceptron Learning Algorithm):
```
Δw = η * error * input
```
Where `η` (eta) is the learning rate (0.1 in this project)

## Next Steps

After understanding this project, you can explore:
1. **Multi-layer Perceptrons (MLPs)**: Stack multiple perceptrons
2. **Different Activation Functions**: Sigmoid, ReLU, tanh
3. **Gradient Descent**: More sophisticated optimization
4. **Backpropagation**: Training deep networks
5. **Neural Network Frameworks**: TensorFlow, PyTorch, Keras

## Limitations

This perceptron can only learn **linearly separable** patterns. For non-linear problems, you need:
- Multiple layers (MLPs)
- Non-linear activation functions
- More sophisticated architectures

## License

This is an educational project. Feel free to use and modify for learning purposes.

## Contributing

This is a learning project. If you find bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

## References

- Rosenblatt, F. (1958). "The Perceptron: A Probabilistic Model for Information Storage and Organization in the Brain" - The original paper introducing the perceptron algorithm
- [But what is a Neural Network? - 3Blue1Brown](https://www.youtube.com/watch?v=aircAruvnKk) - Excellent visual explanation of how neural networks (including perceptrons) work, with beautiful animations
