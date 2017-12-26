'''
Created on Nov 11, 2017
@author: ishank

'''
from time import time

PrintTrace = False

class AtomicSentence(object):
    
    def __init__(self, atomicSentence = "", varCount = 0):
        
        self.negation = False            # Negation: Boolean. True: Negative
        self.predicate = "_UnAssigned"   # Name of the predicate: String
        self.arguments = []              # Arguments: List
                
        if isinstance(atomicSentence, str) and len(atomicSentence) > 0:                              
            self.buildAtomicSentence(atomicSentence, varCount)       
        
        # Create a copy
        elif isinstance(atomicSentence, AtomicSentence):            
            self.negation = atomicSentence.negation
            self.predicate = atomicSentence.predicate                   
            self.arguments = [ v for v in atomicSentence.arguments ]  
    
    # Build Atomic Sentence from a valid string                    
    def buildAtomicSentence(self, strAtomicSentence, varCount = 0):
        
        strAtomicSentence.strip()
        # Removing closing Bracket and split on Opening Bracket
        strParts = strAtomicSentence[:-1].split("(", 1)
        
        self.predicate = strParts[0].strip()
        if strParts[0][0] == '~':
            self.negation = True
            self.predicate = self.predicate[1:]
            
        for s in strParts[1].split(","):
            arg = s.strip()
            if isVariable(arg):
                arg = arg + "_" + str(varCount)
                self.arguments.append(arg)
            else:
                self.arguments.append(arg)
     
    # Stringify this Object
    def toString(self):        
        strAtomicSentence = ""
        if self.negation: 
            strAtomicSentence += "~"
        strAtomicSentence = strAtomicSentence + self.predicate + "("
        for arg in self.arguments:
            strAtomicSentence = strAtomicSentence + arg.split('_')[0] + ", "
        strAtomicSentence = strAtomicSentence[:-2] +  ")"
        return strAtomicSentence
    
    # Is this object equivalent to the Object passed in the argument?
    def equals(self, atomicSentence):
        
        if self.negation != atomicSentence.negation:
            return False
        
        if self.predicate != atomicSentence.predicate:
            return False
        
        for i in range(len(self.arguments)):
            if atomicSentence.arguments[i] != self.arguments[i]:
                return False
        
        return True

class KB(object):
    
    def __init__(self):
        # List of sentences containing this atomicSentence/predicate
        self.atomicSentences = {}    
        # List of sentences in KB      
        self.sentences = []
        self.constantSentences = set([]) 
        self.varCount = 0  
        self.proof = ""
        
    def toString(self, sentence):
        sentStr = ""
        for strS in sentence:
            sentStr = sentStr + strS.toString() + " | "
        return sentStr[:-2]
        
    
    def tell(self, strSentence):
        
        self.varCount += 1
        #  Each complex sentence is stored as a list of atomic sentence
        atomicSentences = [AtomicSentence(s.strip(), self.varCount) for s in strSentence.split("|")]
        self.sentences.append(atomicSentences)
        
        # To find out which sentences in the KB contain this predicate, 
        # append the index of current sentence to self.atomicSentences
        position = len(self.sentences) - 1        
        for atSen in atomicSentences:
            if self.atomicSentences.has_key(atSen.predicate):
                self.atomicSentences[atSen.predicate].add(position)
            else:
                self.atomicSentences[atSen.predicate] = set([position])
        
        if self.isConstantSentence(position):
            self.constantSentences.add(position)            
    
    def remove(self, strQuery):  
        position = len(self.sentences) - 1       
         
        if self.isConstantSentence(position):
            self.constantSentences.remove(position)
            
        atSen = self.sentences.pop()
        
        assert atSen[0].toString() == strQuery
        
        locations = self.atomicSentences[atSen[0].predicate]
        locations.remove(position)
                
    def isConstantSentence(self, location):
        
        sentence = self.sentences[location]
        
        for atSen in sentence:
            for arg in atSen.arguments:
                if isVariable(arg):
                    return False
        
        return True
    
    # strQuery: takes a single Query in string format  
    def ask(self, strQuery):
        # Sanity check
        if len(strQuery) == 0: 
            return False
          
        # Atomic Sentence that needs to be resolved
        query = AtomicSentence(strQuery.strip())
        # Negate the query and try to find a contradiction   
        query.negation = not query.negation        
        queryGoals = [query]
        
        self.tell(query.toString())

        # sentSet: Set of all sentences in KB, initialized with all sentences in KB
        def resolve(queryGoals, sentSet):
            for queryGoal in queryGoals:
                # If this predicate is not in KB, it can not be resolved
                if not self.atomicSentences.has_key(queryGoal.predicate):
                    return False            
                        
                for loc in self.atomicSentences[queryGoal.predicate]:
                    
                    if loc not in sentSet: continue
                    
                    # Substitution for the individual goal Query 
                    subst = {}
                    sentence = self.sentences[loc]
                    
                    for atSen in sentence:
                        if atSen.predicate == queryGoal.predicate and atSen.negation != queryGoal.negation:
                            try:
                                unify(atSen, queryGoal, subst)
                            except UnifyException:                            
                                continue
                            else:
                                
                                if PrintTrace:
                                    print self.toString(queryGoals)
                                    print self.toString(sentence)
                                    print "------------------------------------------" , subst
    
                                # Need a new array to allow backtracking
                                newQueryGoals = []
                                #Remove the current goal query and duplicates
                                for i in range(len(queryGoals)):
                                    if not queryGoals[i].equals(queryGoal):
                                        newQueryGoals.append(AtomicSentence(queryGoals[i]))      
                                # Add all unresolved Atomic Sentences to goal, and remove duplicates
                                for s in sentence:
                                    if not s.equals(atSen):
                                        newQueryGoals.append(AtomicSentence(s))
                                
                                # Reached a Contradiction
                                if len(newQueryGoals) == 0:
                                    
                                    self.proof += self.toString(queryGoals) + '\n'
                                    self.proof += self.toString(sentence) + '\n'
                                    substStr = [ssk.split('_')[0] + ' = ' + ssv.split('_')[0] for ssk, ssv in subst.items() ]
                                    self.proof +=  "------------------------------------------ {" + ', '.join(substStr) + '}\n'
                                    self.proof +="{}\n***"
                                    return True
                                
                                # Apply Substitution
                                for i, g in enumerate(newQueryGoals):
                                    for j, arg in enumerate(g.arguments):
                                        if isVariable(arg):
                                            if subst.has_key(arg):                          
                                                newQueryGoals[i].arguments[j] = subst[arg]          
                                
                                # Need new array to allow backtracking
                                newSentSet = list(sentSet) 
                                # Each sentence should be used only once, except one with Constants only
                                if not loc in self.constantSentences:
                                    newSentSet.remove(loc)
                                    
                                if PrintTrace: print self.toString(newQueryGoals) + "\n"
                                
                                # Resolve all unresolved queries using unused sentences
                                if resolve(list(newQueryGoals), newSentSet):
                                    
                                    self.proof += self.toString(queryGoals) + '\n'
                                    self.proof += self.toString(sentence) + '\n'
                                    substStr = [ssk.split('_')[0] + ' = ' + ssv.split('_')[0] for ssk, ssv in subst.items() ]
                                    self.proof +=  "------------------------------------------ {" + ', '.join(substStr) + '}\n'
                                    self.proof += self.toString(newQueryGoals) + "\n***"
                                    return True
                                
            if PrintTrace: print "***BackTracking..\n"  
            return False
#         result = resolution(queryGoals)
        result = resolve(queryGoals, [i for i in range(len(self.sentences))])
        
        self.remove(query.toString())            
        return result
    
class UnifyException(Exception):
    pass
# A Variable is a string with first character Lower case    
def isVariable(v):
    if isinstance(v, str):    
        if len(v) > 0:
            return v[0].islower()    
    return False
# A Constant is a string with first character Upper case
def isConstant(c):
    if isinstance(c, str):
        if len(c) > 0:
            return c[0].isupper()
    return False
# Unify two arguments
def unify(x, y, subst):
        
    if x == y: return subst
    if isConstant(x) and isConstant(y) and x == y:
        return subst
    elif isVariable(x):
        return unifyVar(x, y, subst)
    elif isVariable(y):
        return unify(y, x, subst)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) == len(y):
            for i in range(len(x)):
                unify(x[i], y[i], subst)
    elif isinstance(x, AtomicSentence) and isinstance(y, AtomicSentence):
        if x.predicate == y.predicate:
            unify(x.arguments, y.arguments, subst)    
    else:
        raise UnifyException
    return subst

def unifyVar(var, x, subst):
    
    if subst.has_key(var):
        return unify(subst[var], x, subst)
    elif subst.has_key(x):
        return unify(var, subst[x], subst)
    
    subst[var] = x   
    
    return subst

def main():
    
    ipFile = open("input.txt")
    opFile = open("output.txt","w")
    
    kb = KB()
    
    numQueries = int(ipFile.readline())
    strQueries = []
    
    for _ in range(numQueries):
        strQueries.append(ipFile.readline().strip())
        
    numSentences = int(ipFile.readline())
    
    for _ in range(numSentences):  
        kb.tell(ipFile.readline().strip())   
    
    t0 = time()
    for query in strQueries:
        if kb.ask(query):
            t1 = time()
            print "TRUE: ", t1 - t0 
            opFile.write("TRUE\n")
            print "\nResolution: Proof by Contradiction\n*********************************************"
            for p in kb.proof.split('***')[::-1]:
                print p
        else:
            t1 = time()
            print "FALSE: ", t1 - t0
            opFile.write("FALSE\n")
        
    ipFile.close()
    opFile.close()

if __name__ == "__main__":
    main()
