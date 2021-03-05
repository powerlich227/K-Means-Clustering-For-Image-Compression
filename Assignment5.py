from matplotlib import pyplot as io
import sys
import numpy as np
from PIL import Image


def initialize(data, k):
    center = [0] * k
    for i in range(k):
        x = np.random.randint(data.shape[0])
        y = np.random.randint(data.shape[1])
        center[i] = [x, y]
    # print center
    return center


def label(data, means):
    x, y, z = data.shape
    labels = [[0 for j in range(y)] for i in range(x)]

    for i in range(x):
        for j in range(y):
            rgb = data[i][j]
            rgb = np.array(rgb)
            min_distance = sys.maxint
            label = 0
            for k in range(len(means)):
                x1, y1 = means[k]
                rgb_mean = data[x1][y1]
                rgb_mean = np.array(rgb_mean)
                distance = np.linalg.norm(rgb - rgb_mean)
                if distance < min_distance:
                    min_distance = distance
                    label = k
            labels[i][j] = label
    # print labels
    return labels


def centralize(labels, k):
    center = [0] * k
    for m in range(k):
        x = 0
        y = 0
        count = 0
        for i in range(len(labels)):
            for j in range(len(labels[i])):
                if labels[i][j] == m:
                    x += i
                    y += j
                    count += 1
        if count == 0:
            center[m] = [0, 0]
        else:
            x_mean = x / count
            y_mean = y / count
            center[m] = [x_mean, y_mean]
    # print center
    return center


def converge(pre_mean, cur_mean, iteration):
    # no_converge = False
    max_iteration = 5
    if iteration > max_iteration:
        return False

    for i in range(len(pre_mean)):
        for j in range(len(pre_mean[i])):
            if pre_mean[i][j] != cur_mean[i][j]:
                return True


if __name__ == "__main__":
    # Image to array
    filename = sys.argv[1]
    img1 = io.imread(filename)  # image is saved as rows * columns * 3 array
    x, y, z = img1.shape
    # print (img1.shape)

    k = int(sys.argv[2])
    iteration = 0
    pre_center = [[0 for j in range(2)] for i in range(k)]
    cur_center = initialize(img1, k)
    labels = [[0 for j in range(y)] for i in range(x)]

    while converge(pre_center, cur_center, iteration):
        iteration += 1
        pre_center = cur_center
        labels = label(img1, cur_center)
        cur_center = centralize(labels, k)

    # Array to image file
    colors = [0] * k
    for m in range(k):
        r = np.random.randint(256)
        g = np.random.randint(256)
        b = np.random.randint(256)
        colors[m] = [r, g, b]
    # print colors

    array = np.zeros([x, y, 3], dtype=np.uint8)
    for color in colors:
        for i in range(len(labels)):
            for j in range(len(labels[i])):
                if labels[i][j] == colors.index(color):
                    array[i][j] = color
    img2 = Image.fromarray(array)
    img2.save('compressed_image.png')
