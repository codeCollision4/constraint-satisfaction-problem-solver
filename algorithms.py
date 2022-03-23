import operator
from typing import List

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
        self.nodes = letters
        self.rev_nodes = {v: k for k, v in self.nodes.items()}
        self.og_domains = domains
        self.constraints = constraints
        self.og_num_con = num_con
        self.assignment = {} # Holds the value assigned to a node/letter
        self.a_set = set()
        self.not_a_set = set(node for node in self.nodes)
        

        # Modifiable data, initialized to original data
        self.domains = domains
        self.num_con = num_con
        self.branch_num = 0
        

    # Backtracking Search Algorithm

    def backtracking(self):
        # Assignments Complete?
        if len(self.assignment) == len(self.nodes):
            self.print_branch("solution")
            exit()

        # Getting variable to assign value to
        letter = self.most_constrained_var() # Holds a letter which is a key to all dicts
        # Getting value to assign to variable chosen prior
        value_list = self.least_constraining_value(letter)
        # Checking consistency of value
        for left_val in value_list:
            if self.consistency(letter, left_val): # If value is consistent
                self.a_set.add(letter)  # Set to hold var and check quickly if assigned, assignment dict is for return and to hold data
                self.not_a_set.remove(letter)
                self.assignment[letter] = left_val # adding to dict
                result = self.backtracking()
                if result != "failure":
                    return result
                # Removing from assignment due to failure
                self.a_set.remove(letter)
                self.not_a_set.add(letter)
                del self.assignment[letter]
            else:
                self.print_branch("failure", l=letter, v=left_val)
        return "failure"


        

            

        

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
        updated_domain = self._update_domain()
        min_value = min([len(updated_domain[letters]) for letters in updated_domain]) # Loops thru dict and finds smallest lenght list
        min_key_list = [key for key, val in updated_domain.items() if len(val) == min_value] # Creates a list of keys that contain smallest domains

        if len(min_key_list) == 1:
            return min(min_key_list) # Return list if its only one domain ie no ties
        elif len(min_key_list) > 1:
            return self.most_constraining_var(min_key_list) # Break ties with most constraining var func

    def _update_domain(self):
        return {letters:self.domains[letters] for letters in self.not_a_set}
    
    def most_constraining_var(self, min_key_list):
        updated_numcon = self._update_numcon()
        value_list = [updated_numcon[letters] for letters in min_key_list]
        max_value = max(value_list) # Creating a list of values from min key list, then getting max
        max_key_list = [letters for letters in min_key_list if updated_numcon[letters]  == max_value] # Creating list of all keys that have max value

        if len(max_key_list) == 1:
            return max(max_key_list) # No ties
        elif len(max_key_list) > 1:
            return min(max_key_list) # Break ties with earliest alphabetically
    
    def _update_numcon(self):
        buffer = 0
        new = {}
        for key, list in self.constraints.items():
            for idx, constrain in enumerate(list):
                if self.rev_nodes[idx] in self.a_set and constrain != 0:
                    buffer += 1
            new[key] = len(list) - list.count(0) - buffer
            buffer = 0
        return new

    def least_constraining_value(self, letter):
        '''
        Find the amount of options each value gives for other variables. Then sort in descending order.
        '''
        val_list = self.domains[letter]
        options_list = {}
        for left_val in val_list:
            sum = 0
            for idx, constraint in enumerate(self.constraints[letter]):
                right = self.rev_nodes[idx]
                if right not in self.a_set and constraint != 0 and letter != right: # Not assigned and an constraint
                    temp = self.domains[right] # Hold domain of other variable in constraint
                    count = 0
                    for right_val in temp: # Check if value is allowed based on constraint
                        satisfied = self.satisfied(left_val, right_val, constraint)
                        if satisfied: # If constraint satified include in sum
                            count += 1
                    sum = sum + count
                if right not in self.a_set and constraint == 0 and letter != right: # Not assigned and no constraint
                    # adding full domain as available
                    sum = sum + len(self.domains[right])
            options_list[left_val] = sum # adding amount of options for each domain value to dict
        
        # Sorting keys based on value
        temp = sorted(options_list.values())
        sorted_values = [ele for ele in reversed(temp)]
        sorted_keys = []
        for val in sorted_values:
            for key in options_list.keys():
                if options_list[key] == val and key not in sorted_keys:
                    sorted_keys.append(key)
                    break
        
        
        return sorted_keys # TODO may need to break ties
        

    def satisfied(self, left, right, constraint):
        '''
        Checks if a constraint is satisfied by a value given.
        '''

        if constraint == '<': return left < right 
            
        elif constraint == '>': return left > right
            
        elif constraint == '=': return left == right
            
        elif constraint == '!': return left != right
    
    def consistency(self, letter, left_val):
        # Checking consistency for value
        for idx, constraint in enumerate(self.constraints[letter]):
            right = self.rev_nodes[idx]
            if right in self.a_set and constraint != 0: # assigned and an constraint
                right_val = self.assignment[right] # Hold domain of other variable in constraint
                satisfied = self.satisfied(left_val, right_val, constraint)
                if not satisfied: # If constraint not satified return false
                    return False
        return True # Return true if all constraints met
    
    def print_branch(self, pf, l="", v=None):
        self.branch_num += 1 # New branch
        branch = "{}.  ".format(self.branch_num)
        if pf == 'failure':
            for letter, value in self.assignment.items():
                branch += "{l}={v}, ".format(l=letter, v=value)
            branch += "{l}={v}  {pf}".format(l=l, v=v, pf=pf)
        elif pf == 'solution':
            for idx, tuple in enumerate(self.assignment.items()):
                if idx == len(self.assignment) - 1:
                    branch += "{l}={v}  {pf}".format(l=tuple[0], v=tuple[1], pf=pf)
                else:
                    branch += "{l}={v}, ".format(l=tuple[0], v=tuple[1])
                
        
        print(branch)
