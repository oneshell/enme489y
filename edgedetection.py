# ENME 489Y: Remote Sensing
# Edge detection

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Define slice of an arbitrary original image
f = np.empty((0))
index = np.empty((0))

# Create intensity data, including noise
for i in range(2000):
    index = np.append(index, i)
    if i <= 950:
        f = np.append(f, 50 + np.random.normal(0,1))
    elif i > 950 and i < 1000:
        f = np.append(f, 50 + (i - 950)/2 + np.random.normal(0,1))
    elif i >= 1000 and i < 1050:
        f = np.append(f, 75 + (i - 1000)/2 + np.random.normal(0,1))
    else:
        f = np.append(f, 100 + np.random.normal(0,1))

print f.shape
print index.shape

plt.figure(2)
plt.plot(index, f, 'r-')
plt.title('Slice of Original Image: f(x)')
plt.xlabel('Pixel x')
plt.ylabel('Pixel intensity f(x)')
plt.grid()
plt.show()

# Plot the gradient (first derivative) of the original signal
messy = np.gradient(f)

plt.figure(3)
plt.plot(messy, 'r-')
plt.title('Derivative of Original Image Slice: df/dx')
plt.xlabel('Pixel x')
plt.ylabel('Derivative df/dx')
plt.grid()
plt.show()

# Define Gaussian filter
mean = 0
std = 5
var = np.square(std)

x = np.arange(-20, 20, 0.1)
kernel = (1/(std*np.sqrt(2*np.pi)))*np.exp(-np.square((x-mean)/std)/2)
print kernel.shape

plt.figure(4)
plt.plot(x, kernel, 'b-')
plt.title('Kernel: Gaussian Filter h(x)')
plt.xlabel('Pixel x')
plt.ylabel('Kernel h(x)')
plt.grid()
plt.show()

# Convolve original image signal with Gaussian filter
smoothed = np.convolve(kernel, f, 'same')
print smoothed.shape

plt.figure(5)
plt.plot(smoothed, 'r-')
plt.title('Apply Gaussian Filter: Convolve h(x) * f(x)')
plt.xlabel('Pixel x')
plt.ylabel('Convolution')
plt.grid()
plt.show()

# Plot the gradient (first derivative) of the filtered signal
edges = np.gradient(smoothed)

plt.figure(6)
plt.plot(edges, 'r-')
plt.title('Derivative of Convolved Image: d/dx[ h(x) * f(x) ] ')
plt.xlabel('Pixel x')
plt.ylabel('Derivative')
plt.grid()
plt.show()

# Plot the gradient (first derivative) of the Gaussian kernel
first_diff = np.gradient(kernel)

plt.figure(7)
plt.plot(first_diff, 'b-')
plt.title('1st Derivative of Gaussian: d/dx[ h(x) ]')
plt.xlabel('Pixel x')
plt.ylabel('Derivative')
plt.grid()
plt.show()

# Convolve original image signal with Gaussian filter
smoothed = np.convolve(first_diff, f, 'same')
print smoothed.shape

plt.figure(8)
plt.plot(smoothed, 'r-')
plt.title('Apply Gaussian Filter: Convolve d/dx[ h(x) ] * f(x)')
plt.xlabel('Pixel x')
plt.ylabel('Convolution')
plt.grid()
plt.show()

# Plot the second derivative of the Gaussian kernel: the Laplacian operator
laplacian = np.gradient(first_diff)

plt.figure(9)
plt.plot(laplacian, 'b-')
plt.title('2nd Derivative of Gaussian: Laplacian Operator d^2/dx^2[ h(x) ]')
plt.xlabel('Pixel x')
plt.ylabel('Derivative')
plt.grid()
plt.show()

# Convolve original image signal with Gaussian filter
smoothed = np.convolve(laplacian, f, 'same')
print smoothed.shape

plt.figure(10)
plt.plot(smoothed, 'r-')
plt.title('Apply Laplacian Operator: Convolve d^2/dx^2[ h(x) ] * f(x)')
plt.xlabel('Pixel x')
plt.ylabel('Convolution')
plt.grid()
plt.show()

