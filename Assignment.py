import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import os


def evaluate(colour1, colour2):
    print("Colour 1: " + str(colour1))
    print("Colour 2: " + str(colour2))

    # This is the break down of colour one
    red1 = float(colour1[0])
    green1 = float(colour1[1])
    blue1 = float(colour1[2])
    # This is the break down of colour two
    red2 = float(colour2[0])
    green2 = float(colour2[1])
    blue2 = float(colour2[2])

    red_diff = red2 - red1
    green_diff = green2 - green1
    blue_diff = blue2 - blue1

    distance = np.sqrt((red_diff * red_diff) + (green_diff * green_diff) + (blue_diff * blue_diff))

    return distance

    
def greedy_heuristics(colour_list):
    sorted_colours = []
    col = 0

    start_colour_index = rnd.randint(0, len(colour_list))
    sorted_colours.append(colour_list[start_colour_index])
    del colour_list[start_colour_index]

    while col in colour_list:
        start_colour_index = rnd.randint(0, len(colour_list))


# Reads the file  of colours
# Returns the number of colours in the file and a list with the colours (RGB) values

def read_file(fname):
    with open(fname, 'r') as afile:
        lines = afile.readlines()
    n = int(lines[3])  # number of colours  in the file
    col = []
    lines = lines[4:]  # colors as rgb values
    for l in lines:
        rgb = l.split()
        col.append(rgb)
    return n, col


# Display the colours in the order of the permutation in a pyplot window
# Input, list of colours, and ordering  of colours.
# They need to be of the same length

def plot_colours(col, perm):
    assert len(col) == len(perm)

    ratio = 10  # ratio of line height/width, e.g. colour lines will have height 10 and width 1
    img = np.zeros((ratio, len(col), 3))
    for i in range(0, len(col)):
        img[:, i, :] = colours[perm[i]]

    fig, axes = plt.subplots(1, figsize=(8, 4))  # figsize=(width,height) handles window dimensions
    axes.imshow(img, interpolation='nearest')
    axes.axis('off')
    plt.show()


#####_______main_____######

# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = read_file('colours.txt')  # Total number of colours and list of colours

test_size = 100  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

permutation = rnd.sample(range(test_size),
                         test_size)  # produces random pemutation of lenght test_size, from the numbers 0 to
                                     # test_size -1
plot_colours(test_colours, permutation)

d = evaluate(colours[1], colours[6])
print(str(d))

