# -*- coding: utf-8 -*-
"""DL 2 assignment.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qsYpRQEdYMj0tYyJmMupl00zcUD2jo7t

Prarabdha pandey
22070126072
AIML A3

TASK 1

DIFFERENT ACTIVATION FUNCTIONS

**Linear Activation Function-**
A linear activation function is a function used in neural networks that returns the input value directly as the output. In mathematical terms, it can be represented as f(x)=x. This function does not apply any transformation to the input, allowing for linear relationships between the input and output.
"""

import numpy as np
import matplotlib.pyplot as plt

def linear(x):
  return x

x = np.linspace(-20, 10, 300) #(start,stop,num of values)
y = linear(x)
plt.plot(x, y)
plt.title('Linear Activation Function')
plt.xlabel('x')
plt.ylabel('f(x) = x')
plt.grid()
plt.show()

"""**Sigmoid Function-**
A sigmoid function is a type of activation function commonly used in neural networks, which maps any input value to a value between 0 and 1.
y=1/(1+e^(-X))

"""

def sigmoid(x):
  return 1 / (1 + np.exp(-x))

x = np.linspace(-10, 10, 300)
y = sigmoid(x)
plt.plot(x, y)
plt.title('Sigmoid Function')
plt.xlabel('x')
plt.ylabel('sigmoid(x)')
plt.grid()
plt.show()

"""**Hyperbolic Tangent (tanh) Function-**
It outputs values between -1 and 1, making it zero-centered and useful for mapping inputs to a range around zero. y=tan(X)
"""

def tanh(x):
  return np.tanh(x)

x = np.linspace(-10, 10, 300)
y = tanh(x)
plt.plot(x, y)
plt.title('Tanh Function')
plt.xlabel('x')
plt.ylabel('tanh(x)')
plt.grid()
plt.show()

"""**ReLU (Rectified Linear Unit) Function-**
y=max(0,X)
It outputs the input if it is positive; otherwise, it outputs zero, helping to mitigate the vanishing gradient problem.
"""

def relu(x):
  return np.maximum(0, x)

x = np.linspace(-10, 10, 400)
y = relu(x)
plt.plot(x, y)
plt.title('ReLU Function')
plt.xlabel('x')
plt.ylabel('ReLU(x)')
plt.grid()
plt.show()

"""**Leaky ReLU Function-**
The Leaky ReLU function is an attempt to fix the "dying ReLU" problem by allowing a small, non-zero gradient when the input is negative.
"""

def leaky_relu(x, alpha=0.05):
  return np.where(x > 0, x, alpha * x)

x = np.linspace(-10, 10, 400)
y = leaky_relu(x)
plt.plot(x, y)
plt.title('Leaky ReLU Function')
plt.xlabel('x')
plt.ylabel('Leaky ReLU(x)')
plt.grid()
plt.show()

"""**Softmax Function-**
The softmax function is often used in the output layer of a neural network to represent a probability distribution.
y=exp(X)/sum(exp(x))

"""

def softmax(x):
  exp_x = np.exp(x - np.max(x)) # Shift for numerical stability
  return exp_x / exp_x.sum(axis=0)

x = np.linspace(-2, 2, 10)
y = softmax(x)
plt.bar(x, y)
plt.title('Softmax Function')
plt.xlabel('x')
plt.ylabel('Softmax(x)')
plt.grid()
plt.show()

"""TASK 2-

NN from scratch
"""

import numpy as np
#from sklearn.metrics import accuracy_score
class NeuralNetwork:
  def __init__(self, input_size, hidden_size, output_size):
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.output_size = output_size
    # Initialize weights
    self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size)
    self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size)
    # Initialize the biases
    self.bias_hidden = np.zeros((1, self.hidden_size))
    self.bias_output = np.zeros ((1, self.output_size))

  def sigmoid(self,x):
    return 1/(1+ np.exp(-x))

  def sigmoid_derivative(self,x):
    return x*(1-x)

  def feedforward (self, X):
    # Input to hidden
    self.hidden_activation = np.dot(X, self.weights_input_hidden) + self.bias_hidden
    self.hidden_output = self.sigmoid(self.hidden_activation)

    # Hidden to output
    self.output_activation = np.dot (self.hidden_output, self.weights_hidden_output) + self.bias_output
    self.predicted_output = self.sigmoid(self.output_activation)

    return self.predicted_output

  def backward(self, X, y, learning_rate):
    # Compute the output layer error
    output_error = y - self.predicted_output
    output_delta = output_error * self.sigmoid_derivative(self.predicted_output)

    # Compute the hidden layer error
    hidden_error = np.dot (output_delta, self.weights_hidden_output.T)
    hidden_delta = hidden_error * self.sigmoid_derivative (self.hidden_output)

    # Update weights and biases
    self.weights_hidden_output += np.dot(self.hidden_output. T, output_delta) * learning_rate
    self.bias_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate
    self.weights_input_hidden += np.dot (X.T, hidden_delta) * learning_rate
    self.bias_hidden += np.sum (hidden_delta, axis=0, keepdims=True) * learning_rate

  def train(self, X, y, epochs, learning_rate):
    for epoch in range(epochs):
      output = self.feedforward(X)
      self.backward(X, y, learning_rate)
      if epoch % 5000 == 0:
        loss = np.mean (np.square (y - output))
        print("Epoch:", {epoch}," Loss:", {loss})

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y= np.array([[1], [1], [0], [1]])

nn = NeuralNetwork(input_size=2, hidden_size=4, output_size=1)
nn.train (X, y, epochs=70000, learning_rate=0.1)

# Test the trained model
output = nn.feedforward(X)
print("Predictions after training:")
print (output)

"""TASK 3-

Applying NN on a dataset
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

data = pd.read_csv('/content/data.csv')
data.head()

data.drop(['id'], axis=1)

# Encode the target variable (M = 1, B = 0)
data['diagnosis'] = data['diagnosis'].map({'M': 1, 'B': 0})

# Split the data into features and target
X = data.drop('diagnosis', axis=1)
y = data['diagnosis']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Standardize the feature data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

class NeuralNetwork:
  def __init__(self, input_size, hidden_size, output_size,learning_rate=0.01):
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.output_size = output_size
    self.learning_rate = learning_rate

# Initialize weights and biases
    self.W1 = np.random.randn(self.input_size, self.hidden_size)
    self.b1 = np.zeros((1, self.hidden_size))
    self.W2 = np.random.randn(self.hidden_size, self.output_size)
    self.b2 = np.zeros((1, self.output_size))

  def sigmoid(self, z):
    return 1 / (1 + np.exp(-z))
  def sigmoid_derivative(self, z):
    return z * (1 - z)
  def forward(self, X):
    self.z1 = np.dot(X, self.W1) + self.b1
    self.a1 = self.sigmoid(self.z1)
    self.z2 = np.dot(self.a1, self.W2) + self.b2
    self.a2 = self.sigmoid(self.z2)
    return self.a2
  def backward(self, X, y, output):
    m = X.shape[0]
  # Calculate the error
    d_output = (output - y) / m
    d_hidden = np.dot(d_output, self.W2.T) * self.sigmoid_derivative(self.a1)

  # Update weights and biases
    self.W2 -= self.learning_rate * np.dot(self.a1.T, d_output)
    self.b2 -= self.learning_rate * np.sum(d_output, axis=0, keepdims=True)
    self.W1 -= self.learning_rate * np.dot(X.T, d_hidden)
    self.b1 -= self.learning_rate * np.sum(d_hidden,axis=0, keepdims=True)
  def train(self, X, y, iterations=10000):
    for i in range(iterations):
      output = self.forward(X)
      self.backward(X, y, output)
  def predict(self, X):
    output = self.forward(X)
    return [1 if i > 0.5 else 0 for i in output]

# Convert target variable to numpy array and reshape
y_train = y_train.values.reshape(-1, 1)
y_test = y_test.values.reshape(-1, 1)

# Initialize the neural network
nn = NeuralNetwork(input_size=X_train.shape[1], hidden_size=10, output_size=1, learning_rate=0.01)
# Train the neural network
nn.train(X_train, y_train, iterations=10000)
# Make predictions
y_pred = nn.predict(X_test)
# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

"""Conclusion - The implementation of a simple neural network from scratch using the Breast Cancer Wisconsin (Diagnostic) dataset shows that basic neural networks can perform binary classification tasks but may require further tuning and complexity to achieve higher accuracy, as demonstrated by the current 62% accuracy."""