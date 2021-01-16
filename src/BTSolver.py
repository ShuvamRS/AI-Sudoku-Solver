import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you assign them
        Return: a tuple of a dictionary and a bool. The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
                The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):
        assignedVars_queue = [v for v in self.network.getVariables() if v.isAssigned()]
        modified = {}

        while len(assignedVars_queue) != 0:
            var = assignedVars_queue.pop(0) 
            val = var.getAssignment()
            neighbors = self.network.getNeighborsOfVariable(var)

            for neighbor in neighbors:
                domain = neighbor.getDomain()
                if neighbor.isChangeable and not neighbor.isAssigned() and domain.contains(val):
                    self.trail.push(neighbor)
                    neighbor.removeValueFromDomain(val)
                    modified[neighbor] = domain

        return (modified, self.assignmentsCheck())


    # =================================================================
    # Arc Consistency
    # =================================================================
    def arcConsistency( self ):
        assignedVars = []
        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)
        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)

    
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you assign them
        Return: a pair of a dictionary and a bool. The dictionary contains all variables 
                that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
                The bool is true if assignment is consistent, false otherwise.
    """
    def norvigCheck ( self ):
        return_dict = {}
        var_list = self.network.getVariables()

        ###################   Norvig’s first Sudoku strategy  #########################
        if not self.forwardChecking()[1]: return ({}, False)

        ###################   Norvig’s second Sudoku strategy  ########################
        Counter = [0]*(self.gameboard.N)
        rows = []
        N = self.gameboard.N

        for i in range(self.gameboard.N):
            row = var_list[i * N : (i + 1) * N]
            rows.append(row)


        for unit in rows:
            for i in range(len(Counter)): Counter[i] = 0

            for i in range(N):
                if unit[i].isAssigned(): pass
                D_Unit_i = unit[i].getDomain().values
                
                for value in D_Unit_i:
                    Counter[value-1] += 1

            for i in range(N):
                if Counter[i] == 1:
                    for square in unit:
                        if square.getDomain().contains(i+1) and not square.isAssigned():
                            self.trail.push(square)
                            square.assignValue(i+1)
                            return_dict[square] = i+1

        return (return_dict, self.assignmentsCheck())


    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return False

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        variables = self.network.getVariables()

        smallest_domain_variable = None
        smallest_domain_size = None

        index = 0
        for variable in variables:
            index += 1
            if variable.isAssigned(): continue
            smallest_domain_variable = variable
            smallest_domain_size = variable.size()
            break

        for variable in variables[index:]:
            if not variable.isAssigned() and variable.size() < smallest_domain_size:
                smallest_domain_size = variable.size()
                smallest_domain_variable = variable

        return smallest_domain_variable

    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with the smallest domain and affecting the  most unassigned neighbors.
                If there are multiple variables that have the same smallest domain with the same number of unassigned neighbors, add them to the list of Variables.
                If there is only one variable, return the list of size 1 containing that variable.
    """
    def MRVwithTieBreaker ( self ):
        variables = self.network.getVariables()
        domainDict = {}
        degreeDict = {}
        getDegree = lambda v: len([neighbor for neighbor in self.network.getNeighborsOfVariable(v)])


        for variable in variables:
            if variable.isAssigned(): continue
            domain_size = variable.getDomain().size()
            try: domainDict[domain_size].append(variable)
            except KeyError: domainDict[domain_size] = [variable]

        for _, variables in sorted(domainDict.items(), key=lambda x: x[0]):
            for variable in variables:
                degree = getDegree(variable)
                try: degreeDict[degree].append(variable)
                except: degreeDict[degree] = variable
            break

        for _,v in sorted(degreeDict.items(), key=lambda x: x[0]):
            if type(v) == list: return v
            return [v]
        return [None]

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # =================================================================
    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        domain_dict = {k:0 for k in v.getDomain().values}
        candidate_values = v.getDomain().values
        neighbors = self.network.getNeighborsOfVariable(v)
        tie_breaker_dict = {}
        return_list = []
        
        for cval in candidate_values:
            self.trail.placeTrailMarker()
            self.trail.push(v)
            v.assignValue(cval)
            self.forwardChecking()

            domain_size_neighbors = 0
            for neighbor in neighbors:
                domain_size_neighbors += neighbor.getDomain().size()

            domain_dict[cval] = domain_size_neighbors
            self.trail.undo()


        for k,v in domain_dict.items():
            try: tie_breaker_dict[v].append(k)
            except KeyError: tie_breaker_dict[v] = [k]

        for _,v in sorted(tie_breaker_dict.items(), key=lambda x: x[0], reverse=True):
            for elem in sorted(v):
                return_list.append(elem)
                
        return return_list


    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self, time_left=600):
        if time_left <= 60:
            return -1

        start_time = time.time()
        if self.hassolution:
            return 0

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            # Success
            self.hassolution = True
            return 0

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recur
            if self.checkConsistency():
                elapsed_time = time.time() - start_time 
                new_start_time = time_left - elapsed_time
                if self.solve(time_left=new_start_time) == -1:
                    return -1
                
            # If this assignment succeeded, return
            if self.hassolution:
                return 0

            # Otherwise backtrack
            self.trail.undo()
        
        return 0

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()[1]

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()[1]

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
