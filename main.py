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
        print("made it to vars")
        # Looping thru file
        v = []
        with args.variables.open() as f:
            for line in f:
                domain = line.split()
                domain.pop(0)
                v.append(domain)
    else:
        print("Please provide a .var file that exists. Make sure you are not just providing a directory.")

    # Getting constraint data from .var file if path exists
    if args.constraints.exists() and args.constraints.is_file():
        print("made it to cons")
    else:
        print("Please provide a .con file that exists. Make sure you are not just providing a directory.")

    # Getting enforcement setting from command line
    if args.consistency_enforcing == "none" or args.consistency_enforcing == "fc":
        print("made it to none/fc")
    else:
        print("Please provide an option for the consistency enforcement. The choices are none and fc.")


if __name__ == '__main__':
    main()
