

class Search_Algorithms():
    '''
    ### Holds search algorithms
    There isn't a node class but the data held within the greater class holds all the nodes and graph data
    Domains hold the node data
    Constraints holds the edges of the graph with a value attached
    Num_con holds the degree of each node
    A node is the letter which acts as a key for each dict
    Nodes are held in letters dict
    '''
    def __init__(self, letters, domains, constraints, num_con):
        # Original data
        self.og_nodes = letters
        self.og_domains = domains
        self.og_constraints = constraints
        self.og_num_con = num_con
        self.assignment = {} # Holds the value assigned to a node/letter

        # Modifiable data, initialized to original data
        self.nodes = letters
        self.domains = domains
        self.constraints = constraints
        self.num_con = num_con
        

    # Backtracking Search Algorithm

    def backtracking(self):
        # Assignments Complete?
        if len(self.assignment) == len(self.nodes):
            # TODO print branch
            return self.assignment # Solution

        # Getting variable to assign value to
        var = self.most_constrained_var() # Holds a letter which is a key to all dicts

        # Getting value to assign to variable chosen prior
        

        

    '''
    Helper Functions for Backtracking Search
    '''


    # Forward Checking Search Algorithm

    def forward_checking(self):
        pass

    '''
    Helper Functions for Forward Checking Search
    '''


    '''
    Helper functions for both
    '''

    def most_constrained_var(self):
        min_value = min([len(self.domains[letters]) for letters in self.domains]) # Loops thru dict and finds smallest lenght list
        min_key_list = [key for key, val in self.domains.items() if len(val) == min_value] # Creates a list of keys that contain smallest domains

        if len(min_key_list) == 1:
            return min(min_key_list) # Return list if its only one domain ie no ties
        elif len(min_key_list) > 1:
            return self.most_constraining_var(min_key_list) # Break ties with most constraining var func
    
    def most_constraining_var(self, min_key_list):
        value_list = [self.num_con[letters] for letters in min_key_list]
        max_value = max(value_list) # Creating a list of values from min key list, then getting max
        max_key_list = [letters for letters in min_key_list if self.num_con[letters] == max_value] # Creating list of all keys that have max value

        if len(max_key_list) == 1:
            return max_key_list # No ties
        elif len(max_key_list) > 1:
            return min(max_key_list) # Break ties alphabetically
