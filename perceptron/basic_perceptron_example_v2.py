"""
Basic Perceptron Example V2 - Using Matrix Operations
=======================================================
This version uses NumPy and dot products for efficient calculations.
This is how neural networks are typically implemented in practice!

The perceptron classifies objects as either:
- Vehicle (output: 1)
- Living Being (output: 0)

Features:
1. Is Round (0 = No, 1 = Yes)
2. Has Wheels (0 = No, 1 = Yes)
3. Can Breathe (0 = No, 1 = Yes)
"""

import numpy as np

# Step 1: Initialize weights and bias randomly
weights = np.random.uniform(-1, 1, 3)  # 3 random weights as a NumPy array
bias = np.random.uniform(-1, 1)
learning_rate = 0.1

print("Starting weights:", np.round(weights, 3))
print("Starting bias:", round(bias, 3))
print()

# Step 2: Prepare training data
# Format: [is_round, has_wheels, can_breathe], label
# Label: 0 = Living Being, 1 = Vehicle

training_data = [
    # Vehicles (label = 1)
    (np.array([1, 1, 0]), 1),  # Car: round wheels, has wheels, can't breathe
    (np.array([0, 1, 0]), 1),  # Truck: not round, has wheels, can't breathe
    (np.array([1, 1, 0]), 1),  # Bicycle: round wheels, has wheels, can't breathe
    (np.array([0, 1, 0]), 1),  # Bus: not round, has wheels, can't breathe

    # Living Beings (label = 0)
    (np.array([1, 0, 1]), 0),  # Human: round head, no wheels, can breathe
    (np.array([0, 0, 1]), 0),  # Dog: not round, no wheels, can breathe
    (np.array([0, 0, 1]), 0),  # Cat: not round, no wheels, can breathe
    (np.array([1, 0, 1]), 0),  # Bird: round body, no wheels, can breathe
]

# Step 3: Train the perceptron using dot products
print("Training the Perceptron...")
print("-" * 50)

epochs = 100
for epoch in range(epochs):
    errors = 0

    for features, target in training_data:
        # Make a prediction using DOT PRODUCT
        # np.dot(weights, features) = weight1*feature1 + weight2*feature2 + weight3*feature3
        total = np.dot(weights, features) + bias

        # Activation: if total >= 0, predict 1 (vehicle), else predict 0 (living being)
        prediction = 1 if total >= 0 else 0

        # Calculate error
        error = target - prediction
        print(f"Epoch {epoch + 1}, Features: {features}, Target: {target}, Prediction: {prediction}, Error: {error}")

        # If we made a mistake, update weights
        if error != 0:
            errors += 1
            print(f"Updating weights and bias..."
                  f"\nOld Weights: {np.round(weights, 3)}, Old Bias: {bias:.3f}")

            # Update weights using vector operations: weights = weights + learning_rate * error * features
            weights = weights + learning_rate * error * features

            # Update bias
            bias = bias + learning_rate * error
            print(f"New Weights: {np.round(weights, 3)}, New Bias: {bias:.3f}")

    # Print weights after each epoch
    print(f"Epoch {epoch + 1}: {errors} errors | Weights: {np.round(weights, 3)} Bias: {bias:.3f}")

    # Stop if no errors
    if errors == 0:
        print(f"\nPerfect! No errors - Training complete!")
        break

# Step 4: Test the trained perceptron
print("\n" + "=" * 40)
print("Testing the Perceptron")
print("=" * 40)

test_cases = [
    (np.array([1, 1, 0]), "Mystery Object 1 (round, wheels, no breath)"),
    (np.array([0, 0, 1]), "Mystery Object 2 (not round, no wheels, breathes)"),
    (np.array([1, 0, 1]), "Mystery Object 3 (round, no wheels, breathes)"),
    (np.array([0, 1, 0]), "Mystery Object 4 (not round, wheels, no breath)"),
]

for features, description in test_cases:
    # Make prediction using DOT PRODUCT
    total = np.dot(weights, features) + bias
    prediction = 1 if total >= 0 else 0

    result = "VEHICLE" if prediction == 1 else "LIVING BEING"
    print(f"\n{description}")
    print(f"Features: Is Round={features[0]}, Has Wheels={features[1]}, Can Breathe={features[2]}")
    print(f"Dot Product: {np.dot(weights, features):.3f}, Total (with bias): {total:.3f}")
    print(f"Prediction: {result}")

# Show final weights
print("\n" + "=" * 40)
print("Final Perceptron Weights")
print("=" * 40)
print(f"Weights: {np.round(weights, 3)}")
print(f"Weight for 'Is Round': {weights[0]:.3f}")
print(f"Weight for 'Has Wheels': {weights[1]:.3f}")
print(f"Weight for 'Can Breathe': {weights[2]:.3f}")
print(f"Bias: {bias:.3f}")

# Bonus: Show the mathematical equivalence
print("\n" + "=" * 40)
print("Understanding Dot Product")
print("=" * 40)
print("The dot product is just a shorthand for:")
print(f"weights · features = {weights[0]:.3f}*f1 + {weights[1]:.3f}*f2 + {weights[2]:.3f}*f3")
print("\nFor example, with features [1, 1, 0]:")
print(f"Dot product: {np.dot(weights, np.array([1, 1, 0])):.3f}")
print(f"Manual calc: {weights[0]:.3f}*1 + {weights[1]:.3f}*1 + {weights[2]:.3f}*0 = {weights[0]*1 + weights[1]*1 + weights[2]*0:.3f}")
