import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import os


# Func author: James Simpson
# This function is to calculate the difference in two colours
def evaluate(colour1, colour2):
    # This is the break down of colour one
    red1, green1, blue1 = float(colour1[0]), float(colour1[1]), float(colour1[2])
    # This is the break down of colour two
    red2, green2, blue2 = float(colour2[0]), float(colour2[1]), float(colour2[2])
    # Calculating the differences between the different colour RGB values
    red_diff, green_diff, blue_diff = (red2 - red1), (green2 - green1), (blue2 - blue1)

    # Finally conducting Pythagoras to find the Euclidean distance
    distance = np.sqrt((red_diff * red_diff) + (green_diff * green_diff) + (blue_diff * blue_diff))

    distance = distance.euclidean(colour1, colour2)

    return distance


# Create a new random index
def random_index(lis):

    index_rand = rnd.randint(0, (len(lis) - 1))
    return index_rand


# Func author: James Simpson
# This is an implementation of a greedy heuristic to sort the colours into
# colour order
def greedy_heuristics(colour_list):
    orig_colour_list = colour_list
    sorted_colours = []
    dis = 0
    distances = []  # Keeping a record of all the distances from the initial colour to then compare new distances

    random_start_index = random_index(orig_colour_list)
    start_colour = colour_list[random_start_index]
    sorted_colours.append(start_colour)
    distances.append(dis)
    del orig_colour_list[random_start_index]

    for test_colour in orig_colour_list:
        dis = evaluate(start_colour, test_colour)
        distances.append(dis)

    colour = 0
    while colour < (len(distances) - 1):
        lowest = min(distances)
        colour_lowest_distance = distances.index(lowest)
        next_colour = orig_colour_list[colour_lowest_distance]
        sorted_colours.append(next_colour)
        colour += 1

    distances = sorted(distances)
    print("The sorted colours are: " + str(sorted_colours))
    print("The list of ordered distances is: " + str(distances))
    return sorted_colours

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
# plot_colours(test_colours, permutation)

# d1 = evaluate(colours[1], colours[6])
# d2 = evaluate(colours[10], colours[6])
# print(str(d1))
# print(str(d2))

sorted_col = greedy_heuristics(test_colours)
print(str(permutation))
print(str(len(sorted_col)))
plot_colours(sorted_col, permutation)
