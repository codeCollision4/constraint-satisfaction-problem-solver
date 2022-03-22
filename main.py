import argparse
from pathlib import Path
from algorithms import Search_Algorithms as sa

'''
Each variable read in from *.var will be put into a dictionary. 
The domain, constraint relationships, and number of constraints can be accessed by provided the letter as the key in any dict.
'''


def main():
    # Command Line Parser
    parser = argparse.ArgumentParser()
    # Positional Arguments
    parser.add_argument("variables",
                        help="Path to a .var file that holds variable info",
                        type=Path
                        )
    parser.add_argument("constraints",
                        help="Path to a .con file that holds constraint info",
                        type=Path
                        )
    parser.add_argument("consistency_enforcing",
                        help="none|fc are the choices. none is for backtracking. fc is for forward checking."
                        )
    # Parse input
    args = parser.parse_args()

    # Getting variable data from .var file if path exists
    if args.variables.exists() and args.variables.is_file():
        # Looping thru file
        domains = {} # Holds domain of each variable
        letters = {} # Holds letter for each, to be used with constraints. Value is a number to be used like an index
        with args.variables.open() as f:
            for idx, line in enumerate(f):
                v = line.split()
                l = v.pop(0).split(":").pop(0) # Removing first element, then getting the letter
                letters[l] = idx
                v = [int(x) for x in v] # Converting all ints from string to int TODO optimize
                domains[l] = v
    else:
        print("Please provide a .var file that exists. Make sure you are not just providing a directory.")
        exit()

    # Getting constraint data from .var file if path exists
    if args.constraints.exists() and args.constraints.is_file():
        # Looping thru file
        constraints = {} # Holds constraint relationships
        for l in letters:
            t = []
            for i in letters:
                t.append(0)
            constraints[l] = t # put in a list with len equal to amount of letters into dict value
        with args.constraints.open() as f:
            for line in f:
                cons = line.split()
                if cons[0] in letters and cons[2] in letters: 
                    left_key = cons[0] # Key for dict
                    right_key = cons[2]
                    left_index = letters[cons[0]]
                    right_index = letters[cons[2]]
                    op = cons[1]
                    constraints[left_key][right_index] = op
                    if op == "<":
                        constraints[right_key][left_index] = ">"
                    elif op == ">":
                        constraints[right_key][left_index] = "<"
                    else:
                        constraints[right_key][left_index] = op
                else:   
                    print("Constraint file contains variable names that are not in the variable file. Please make sure you are inputing the correct and matching paths.")
                    exit()
    else:
        print("Please provide a .con file that exists. Make sure you are not just providing a directory.")
        exit()

    # Counting number of constraints for each letter
    num_con = {}
    for key, list in constraints.items():
        num_con[key] = len(list) - list.count(0)
    
    # Creating dictionaries for domains, constraints and num of constraints. Letters array will hold the keys for each.

    # Init Search Algorithms
    solver = sa(domains, constraints, num_con)

    # Getting enforcement setting from command line
    if args.consistency_enforcing == "none": solver.backtracking() # Call backtracking solver
    elif args.consistency_enforcing == "fc": solver.forward_checking() # Call forward checking solver
    else:
        print("Please provide an option for the consistency enforcement. The choices are none and fc.")
        exit()

    print(letters)
    print(domains)
    print(constraints)
    print(num_con)

    
    
        

if __name__ == '__main__':
    main()
