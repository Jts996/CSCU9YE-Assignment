import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import os

test_colours = []


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

    return distance


# Create a new random index
def random_index(lis):
    index_rand = rnd.randint(0, (len(lis) - 1))
    return index_rand


# Create random solutions
def random_solution(lst):
    rnd_solution = []
    for ind in range(len(lst)):
        random_colour = lst[random_index(lst)]
        rnd_solution.append(random_colour)

    return rnd_solution


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

    # Calculating all the distances from the start colour
    for test_colour in orig_colour_list:
        dis = evaluate(start_colour, test_colour)
        distances.append(dis)

    colour = 0
    # Sorting the colours using the list of distances
    # Sorted in ascending order
    while colour < (len(distances) - 1):
        lowest = min(distances)
        colour_lowest_distance = distances.index(lowest)
        next_colour = orig_colour_list[colour_lowest_distance]
        sorted_colours.append(next_colour)
        colour += 1

    return sorted_colours


# Method to calculate the total distance of a solution
def cal_total(sol):
    s = sol
    total = 0
    for ind in range(len(s) - 1):
        dis = evaluate(s[ind], s[ind + 1])
        total = total + dis
    return total


#  Method which receives a solution and uses 1-bit flp to find whether or not it  can find a better solution
def local_optima(sol):
    s = sol
    total_one = cal_total(sol)

    optima = False
    ind = 0
    while ind < len(s):
        random_sol = random_solution(sol)
        total_two = cal_total(random_sol)
        print("I'm here")
        if total_two < total_one:
            total_one = total_two
            optima = True
        else:
            optima = False
        ind += 1
    print("Optima is: " + str(optima))
    return optima


# Finding the next valid Solution
def random_better_solution(sol):
    not_better = True
    current_best_total = cal_total(sol)
    while not_better:
        temp_sol = sol
        temp_sol = random_solution(temp_sol)
        competitor_total = cal_total(temp_sol)

        if competitor_total < current_best_total:
            sol = temp_sol
            not_better = False
    return sol


# Func author: Chris Hayes & James Simpson
# This is an implementation of th Hill Climbing algorithm
def hill_climbing():
    initial_solution = random_solution(test_colours)  # This is the original random list
    best_solution = initial_solution  # This is the best solution found within the specified number of iterations
    not_best = True  # Flag for the while loop
    totals = []
    best_total = cal_total(best_solution)  # The total between the colours in the current best solution
    totals.append(best_total)
    while not_best:
        if best_solution != random_solution:
            competitor_solution = random_solution(best_solution)
            competitor_total = cal_total(competitor_solution)  # This is the total distance between the colours in
            # the new random solution

            # If the total distance of the new solution is less than the old solution
            # this is the new best solution
            if competitor_total < best_total:
                best_solution = competitor_solution
                # print("The best solution is: " + str(best_solution))
                best_total = competitor_total
                totals.append(competitor_total)
            else:
                not_best = local_optima(best_solution)
        else:
            not_best = local_optima(best_solution)
    print("Length of best solution at end of function is: " + str(len(best_solution)))
    print(totals)
    return best_solution, best_total


def mhc(tries):
    best_solution = random_solution(test_colours)
    iterations = 0
    total = cal_total(best_solution)

    while iterations < tries:
        competitor_sol, competitior_tot = hill_climbing()
        if competitior_tot < total:
            best_solution = competitor_sol
            total = competitior_tot
        iterations += 1

    return best_solution

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
# Added name so that each plot can be identified

def plot_colours(col, perm, name):
    assert len(col) == len(perm)

    ratio = 100  # ratio of line height/width, e.g. colour lines will have height 10 and width 1
    img = np.zeros((ratio, len(col), 3))
    for i in range(0, len(col)):
        img[:, i, :] = colours[perm[i]]

    fig, axes = plt.subplots(1, figsize=(8, 4))  # figsize=(width,height) handles window dimensions
    axes.imshow(img, interpolation='nearest')
    axes.axis('off')
    plt.title(name)
    plt.show()


#####_______main_____######

# Get the directory where the file is located
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)  # Change the working directory so we can read the file

ncolors, colours = read_file('colours.txt')  # Total number of colours and list of colours

test_size = 10  # Size of the subset of colours for testing
test_colours = colours[0:test_size]  # list of colours for testing

permutation = rnd.sample(range(test_size),
                         test_size)  # produces random permutation of length test_size, from the numbers 0 to
# test_size -1
plot_colours(test_colours, permutation, "Original")

# d1 = evaluate(colours[1], colours[6])
# d2 = evaluate(colours[10], colours[6])
# print(str(d1))
# print(str(d2))

sorted_col = greedy_heuristics(test_colours)
permutation = rnd.sample(range(len(sorted_col)),
                         test_size)
print(str(permutation))
plot_colours(sorted_col, permutation, "Greedy")

sorted_col, tot = hill_climbing()
permutation = rnd.sample(range(len(sorted_col)),
                         len(sorted_col))
print("Length of sample: " + str(len(permutation)))
print("length of the colours: " + str(len(sorted_col)))
plot_colours(sorted_col, permutation, "Hill-Climbing")


sorted_col = mhc(10)
permutation = rnd.sample(range(len(sorted_col)),
                         len(sorted_col))
plot_colours(sorted_col, permutation, "Multi run Hill Climb")
