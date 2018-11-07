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


#  create random index not including first element
def random_index_greater_zero(lst):
    index_rand = rnd.randint(1, (len(lst) - 1))
    return index_rand


# Create random solutions
def random_solution(lst):
    rnd_solution = []
    for ind in range(len(lst)):
       rnd_solution = swap_colours(lst)

    return rnd_solution


# Swap two colours at random indexes
def swap_colours(lst):
    new_solution = lst
    not_swapped = True

    while not_swapped:
        # Generate two random indexes
        random_index_one = random_index_greater_zero(new_solution)
        random_index_two = random_index_greater_zero(new_solution)

        # Make sure they are not the same index
        if random_index_one != random_index_two:
            # Extract the corresponding information from each index
            colour_one = new_solution[random_index_one]
            colour_two = new_solution[random_index_two]
            # Swap the colours to make the new random solution
            new_solution[random_index_one] = colour_two
            new_solution[random_index_two] = colour_one
            not_swapped = False
    return new_solution


# Func author: James Simpson
# This is an implementation of a greedy heuristic to sort the colours into
# colour order
def greedy_heuristics(colour_list):
    rnd_colour_list = random_solution(colour_list)
    sorted_colours = []
    dis = 0
    distances = []  # Keeping a record of all the distances from the initial colour to then compare new distances

    start_colour = rnd_colour_list[0]
    sorted_colours.append(start_colour)
    distances.append(dis)

    # Calculating all the distances from the start colour
    for test_colour in rnd_colour_list:
        dis = evaluate(start_colour, test_colour)
        distances.append(dis)

    colour = 1
    # Sorting the colours using the list of distances
    # Sorted in ascending order
    while colour < (len(distances) - 1):
        lowest = min(distances)
        colour_lowest_distance = distances.index(lowest)
        next_colour = rnd_colour_list[colour_lowest_distance]
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
        # Create a new random solution
        random_sol = random_solution(sol)
        # Calculate the total of the new solution
        total_two = cal_total(random_sol)
        # Compare the two totals
        # If less than, there is a better solution present
        if total_two < total_one:
            total_one = total_two
            optima = True
        # If greater than, there are no better solutions
        else:
            optima = False
        ind += 1
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
        competitor_solution = random_solution(best_solution)
        competitor_total = cal_total(competitor_solution)  # This is the total distance between the colours in
        # the new random solution
        if best_solution != random_solution:

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
    return best_solution, best_total


def mhc(tries):
    best_solution = random_solution(test_colours)
    iterations = 0
    total = cal_total(best_solution)

    while iterations < tries:
        competitor_sol, competitor_tot = hill_climbing()
        if competitor_tot < total:
            best_solution = competitor_sol
            total = competitor_tot
        iterations += 1

    return best_solution

def tabu():
    current_solution = random_solution(test_colours)  # get a initial solution

    tabu_list = [(current_solution, current_solution, current_solution, current_solution, current_solution,
                  current_solution, current_solution, current_solution, current_solution, current_solution)]  # generate a tabu list of moves we cant do

    for i in range(9):  # loop till a condition is met

        current_solution.append(tabu_list)  # add the starting value to the tabu list

        random_neighbour1 = swap_colours(current_solution)  # get a random neighbour of our current solution
        total1 = cal_total(random_neighbour1)  # find its total

        lowest = total1  # set this total as the lowest
        current_best = random_neighbour1[:]  # set this new solution to the current best solution

        for a in range(9):
            if current_best in tabu_list:  # check to see if the current best is in the tabu list
                current_best = current_solution[:]  # if it is then reverse the change

        random_neighbour2 = swap_colours(current_solution)  # do this for multiple neighbours always checking to see if a new one is lower
        total2 = cal_total(random_neighbour2)

        if total2 < lowest:
            lowest = total2
            current_best = random_neighbour2[:]
            for a in range(9):
                if current_best in tabu_list:
                    current_best = current_solution[:]

        random_neighbour3 = swap_colours(current_solution)
        total3 = cal_total(random_neighbour3)

        if total3 < lowest:
            lowest = total3
            current_best = random_neighbour3[:]
            for a in range(9):
                if current_best in tabu_list:
                    current_best = current_solution[:]

        random_neighbour4 = swap_colours(current_solution)
        total4 = cal_total(random_neighbour4)

        if total4 < lowest:
            lowest = total4
            current_best = random_neighbour4[:]
            for a in range(9):
                if current_best in tabu_list:
                    current_best = current_solution[:]

        random_neighbour5 = swap_colours(current_solution)
        total5 = cal_total(random_neighbour5)

        if total5 < lowest:
            lowest = total5
            current_best = random_neighbour5[:]
            for a in range(9):
                if current_best in tabu_list:
                    current_best = current_solution[:]

    return current_solution  # return the best solution


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

    ratio = 4  # ratio of line height/width, e.g. colour lines will have height 10 and width 1
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

test_size = 500  # Size of the subset of colours for testing
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
plot_colours(sorted_col, permutation, "Greedy")

sorted_col, tot = hill_climbing()
permutation = rnd.sample(range(len(sorted_col)),
                         test_size)
plot_colours(sorted_col, permutation, "Hill-Climbing")


sorted_col = mhc(10)
permutation = rnd.sample(range(len(sorted_col)),
                         test_size)
plot_colours(sorted_col, permutation, "Multi-run Hill Climb")
