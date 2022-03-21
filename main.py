import argparse
from pathlib import Path

'''
Each variable read in from *.var will be put into a list. So that list will be a 2d array. A=0, B=1 etc. To access the third value of A's domain it would be list[0][2] 
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
        domains = [] # Holds domain of each variable
        letters = [] # Holds letter for each, to be used with constraints
        with args.variables.open() as f:
            for line in f:
                v = line.split()
                l = v.pop(0).split(":").pop(0) # Removing first element, then getting the letter
                letters.append(l)
                v = [int(x) for x in v] # Converting all ints from string to int TODO optimize
                domains.append(v)
    else:
        print("Please provide a .var file that exists. Make sure you are not just providing a directory.")
        exit()

    # Getting constraint data from .var file if path exists
    if args.constraints.exists() and args.constraints.is_file():
        # Looping thru file
        constraints = [] # Holds constraint relationships
        for l in letters:
            t = []
            for i in letters:
                t.append(0)
            constraints.append(t)    # Creating a 2d list, first dim is left of the OP, second is right of the OP. The value will be the OP. TODO optimize
        with args.constraints.open() as f:
            for line in f:
                cons = line.split()
                if cons[0] in letters and cons[2] in letters: # TODO optimize
                    left = letters.index(cons[0])
                    right = letters.index(cons[2])
                    constraints[left][right] = cons[1]
                    if cons[1] == "<":
                        constraints[right][left] = ">"
                    elif cons[1] == ">":
                        constraints[right][left] = "<"
                    else:
                        constraints[right][left] = cons[1]
                else:
                    print("Constraint file contains variable names that are not in the variable file. Please make sure you are inputing the correct and matching paths.")
                    exit()
    else:
        print("Please provide a .con file that exists. Make sure you are not just providing a directory.")
        exit()

    # Getting enforcement setting from command line
    con_enf = "" 
    if args.consistency_enforcing == "none": con_enf = "none"
    elif args.consistency_enforcing == "fc": con_enf = "fc"
    else:
        print("Please provide an option for the consistency enforcement. The choices are none and fc.")
        exit()

    print(letters)
    print(domains)
    print(constraints)

    # Counting number of constraints for each letter
    num_con = []
    for list in constraints:
        num_con.append(len(list) - list.count(0))
    print(num_con)
    
        

if __name__ == '__main__':
    main()
