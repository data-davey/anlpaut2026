"""
Basic Perceptron Example for Beginners
========================================
This example teaches a perceptron to classify objects as either:
- Vehicle (output: 1)
- Living Being (output: 0)

Features:
1. Is Round (0 = No, 1 = Yes)
2. Has Wheels (0 = No, 1 = Yes)
3. Can Breathe (0 = No, 1 = Yes)
"""

import random

# Step 1: Initialize weights and bias randomly
weights = [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
bias = random.uniform(-1, 1)
learning_rate = 0.1

print("Starting weights:", [round(w, 3) for w in weights])
print("Starting bias:", round(bias, 3))
print()

# Step 2: Prepare training data
# Format: [is_round, has_wheels, can_breathe], label
# Label: 0 = Living Being, 1 = Vehicle

training_data = [
    # Vehicles (label = 1)
    ([1, 1, 0], 1),  # Car: round wheels, has wheels, can't breathe
    ([0, 1, 0], 1),  # Truck: not round, has wheels, can't breathe
    ([1, 1, 0], 1),  # Bicycle: round wheels, has wheels, can't breathe
    ([0, 1, 0], 1),  # Bus: not round, has wheels, can't breathe

    # Living Beings (label = 0)
    ([1, 0, 1], 0),  # Human: round head, no wheels, can breathe
    ([0, 0, 1], 0),  # Dog: not round, no wheels, can breathe
    ([0, 0, 1], 0),  # Cat: not round, no wheels, can breathe
    ([1, 0, 1], 0),  # Bird: round body, no wheels, can breathe
]

# Step 3: Train the perceptron
print("Training the Perceptron...")
print("-" * 50)

epochs = 100
for epoch in range(epochs):
    errors = 0

    for features, target in training_data:
        # Make a prediction
        # Calculate: weight1*feature1 + weight2*feature2 + weight3*feature3 + bias
        total = weights[0] * features[0] + weights[1] * features[1] + weights[2] * features[2] + bias

        # Activation: if total >= 0, predict 1 (vehicle), else predict 0 (living being)
        prediction = 1 if total >= 0 else 0

        # Calculate error
        error = target - prediction
        print(f"Epoch {epoch + 1}, Features: {features}, Target: {target}, Prediction: {prediction}, Error: {error}")

        # If we made a mistake, update weights
        if error != 0:
            errors += 1
            print(f"Updating weights and bias..."
                  f"\nOld Weights: [{weights[0]:.3f}, {weights[1]:.3f}, {weights[2]:.3f}], Old Bias: {bias:.3f}")
            # Update each weight: new_weight = old_weight + learning_rate * error * feature
            weights[0] = weights[0] + learning_rate * error * features[0]
            weights[1] = weights[1] + learning_rate * error * features[1]
            weights[2] = weights[2] + learning_rate * error * features[2]

            # Update bias
            bias = bias + learning_rate * error
            print(f"New Weights: [{weights[0]:.3f}, {weights[1]:.3f}, {weights[2]:.3f}], New Bias: {bias:.3f}")

    # Print weights after each epoch
    print(f"Epoch {epoch + 1}: {errors} errors | Weights: [{weights[0]:.3f}, {weights[1]:.3f}, {weights[2]:.3f}] Bias: {bias:.3f}")

    # Stop if no errors
    if errors == 0:
        print(f"\nPerfect! No errors - Training complete!")
        break

# Step 4: Test the trained perceptron
print("\n" + "=" * 40)
print("Testing the Perceptron")
print("=" * 40)

test_cases = [
    ([1, 1, 0], "Mystery Object 1 (round, wheels, no breath)"),
    ([0, 0, 1], "Mystery Object 2 (not round, no wheels, breathes)"),
    ([1, 0, 1], "Mystery Object 3 (round, no wheels, breathes)"),
    ([0, 1, 0], "Mystery Object 4 (not round, wheels, no breath)"),
]

for features, description in test_cases:
    # Make prediction
    total = weights[0] * features[0] + weights[1] * features[1] + weights[2] * features[2] + bias
    prediction = 1 if total >= 0 else 0

    result = "VEHICLE" if prediction == 1 else "LIVING BEING"
    print(f"\n{description}")
    print(f"Features: Is Round={features[0]}, Has Wheels={features[1]}, Can Breathe={features[2]}")
    print(f"Prediction: {result}")

# Show final weights
print("\n" + "=" * 40)
print("Final Perceptron Weights")
print("=" * 40)
print(f"Weight for 'Is Round': {weights[0]:.3f}")
print(f"Weight for 'Has Wheels': {weights[1]:.3f}")
print(f"Weight for 'Can Breathe': {weights[2]:.3f}")
print(f"Bias: {bias:.3f}")
