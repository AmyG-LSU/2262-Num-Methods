import numpy as np
import matplotlib.pyplot as plt

# Define the coefficients matrix manually (example)
coefficients_matrix = np.array([
    [1, -2, 1],
    [2, -3, 0],
    [1, 0, 0],
    [2, 1, 1]
])

# Sample data points
x_data = np.array([0, 1, 2, 3, 4])  # x values of data points
y_data = np.array([0, 2, 1, 3, 2])  # y values of data points

# Function to compute the spline value at a given x
def compute_spline(x):
    # Determine which interval x belongs to
    interval = np.searchsorted(x_data[1:], x)
    interval = min(interval, len(coefficients_matrix) - 1)  # Ensure not out of range

    # Get coefficients of the polynomial for the interval
    a, b, c, d = coefficients_matrix[:, interval]

    # Compute the y value using the cubic polynomial
    y = a * (x - x_data[interval]) ** 3 + b * (x - x_data[interval]) ** 2 + c * (x - x_data[interval]) + d
    return y

# Plot data points and spline curve
plt.figure(figsize=(8, 6))
plt.plot(x_data, y_data, 'o', label='Data Points')

# Generate points for the spline curve
x_spline = np.linspace(min(x_data), max(x_data), 100)
y_spline = np.array([compute_spline(x) for x in x_spline])

plt.plot(x_spline, y_spline, label='Cubic Spline')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Cubic Spline Interpolation')
plt.legend()
plt.grid(True)
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# Given data
x = np.array([0, 3, 6, 8])
y = np.array([3, 4, 1, 4])

# Calculate differences
h = np.diff(x)
delta_y = np.diff(y)

# Construct the tridiagonal matrix A
A = np.zeros((len(x), len(x)))
np.fill_diagonal(A, 2*(h[:-1] + h[1:]))
np.fill_diagonal(A[1:], h)
np.fill_diagonal(A[:, 1:], h)

# Construct the vector B
B = np.zeros(len(x))
B[1:-1] = 6 * (delta_y[1:] / h[1:] - delta_y[:-1] / h[:-1])

# Solve for the coefficients vector b
b = np.linalg.solve(A, B)

# Calculate the other coefficients
a = np.diff(b) / (6 * h)
c = (y[1:] - y[:-1]) / h - (2 * h * b[:-1] + h * b[1:]) / 6
d = y[:-1]

# Define the cubic spline function
def S(x_val, i):
    return a[i] * (x_val - x[i])**3 + b[i] * (x_val - x[i])**2 + c[i] * (x_val - x[i]) + d[i]

# Plot the spline
x_range = np.linspace(0, 10, 100)
y_range = np.piecewise(x_range, [x_range <= xi for xi in x], [lambda x_val: S(x_val, i) for i in range(len(x)-1)])
plt.plot(x_range, y_range)
plt.scatter(x, y, color='red', label='Data Points')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Cubic Spline')
plt.legend()
plt.grid(True)
plt.show()
