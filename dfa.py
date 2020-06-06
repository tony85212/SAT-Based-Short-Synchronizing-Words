from pysmt.shortcuts import Symbol, Or, And, Not, Equals, Int, get_model, is_sat, Solver
from pysmt.typing import INT
import string
import random
import sys

class DFA:

    current_state = None;

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):

        self.states = states;
        self.alphabet = alphabet;
        self.transition_function = transition_function;
        self.start_state = start_state;
        self.accept_states = accept_states;
        self.current_state = start_state;

        return;

    def transition_to_state_with_input(self, input_value):

        if ((self.current_state, input_value) not in self.transition_function.keys()):

            self.current_state = None;

            return;

        self.current_state = self.transition_function[(self.current_state, input_value)];

        return;


    def in_accept_state(self):

        return self.current_state;# in accept_states;

    def go_to_initial_state(self):

        self.current_state = self.start_state;

        return;

    def run_with_input_list(self, input_list):

        self.go_to_initial_state();

        for inp in input_list:

            self.transition_to_state_with_input(inp);

            continue;

        return self.in_accept_state();

    pass;

def brute_force(d):
    length = 1
    while (length < (len(d.states)-1)**2 + 1):
        all_possible_input = enumarate_input(d.alphabet, length)

        for input in all_possible_input:
            inp_program = list(input)
            #print("input =", input)
            final_state = []
            for initial_state in d.states:
                d.start_state = initial_state
                final_state.append(d.run_with_input_list(inp_program))
            #print(final_state)
            if(len(set(final_state)) == 1):
                print("congra!!")
                return input
        length += 1
    return None

def DFA_generator(num_states, num_alphabet):
    states = [i for i in range(num_states)]
    alphabet = list(string.ascii_lowercase[0:num_alphabet])

    tf = dict()
    for i in states:
        for j in alphabet:
            tf[(i, j)] = random.choice(states)

    return DFA(states, alphabet, tf, 0, states)


def SAT_Based(d, length):

    alphabet = d.alphabet
    num_alphabet = len(alphabet)
    num_state = len(d.states)


    #length = 9

    #constraint 1

    constraint_1 = []

    X = [[Symbol('X' + str(i) + j) for j in alphabet] for i in range(length)]


    for i in range(length):
        constraint_1.append(Or(X[i]))
        for j in range(num_alphabet):
            for k in range(j+1, num_alphabet):
                p = Or(Not(X[i][j]), Not(X[i][k]))
                constraint_1.append(p)
    c1 = And(constraint_1)

    #constraint 2

    constraint_2 = []

    S = [[[Symbol('S' + str(i) + str(j) + str(k)) for k in range(num_state)] for j in range(length+1)] for i in range(num_state)]
    #print(S)
    for i in range(num_state):
        for j in range(length+1):
            constraint_2.append(Or(S[i][j]))
            for k in range(num_state):
                for l in range(k+1, num_state):
                    p = Or(Not(S[i][j][k]), Not(S[i][j][l]))
                    constraint_2.append(p)
    c2 = And(constraint_2)
    #print(c2)

    constraint_3 = []
    for i in range(num_state):
        constraint_3.append(S[i][0][i])
    c3 = And(constraint_3)

    #constraint 4

    constraint_4 = []

    #print(d.transition_function[(0, 'a')])

    for i in range(num_state):
        for j in range(length):
            for k in range(num_state):
                for l in range(num_alphabet):
                    tran_func = (k, alphabet[l])
                    next_state = d.transition_function[tran_func]
                    #print(S[i][j][k], X[j][l], S[i][j+1][next_state])
                    A = S[i][j][k]
                    B = X[j][l]
                    C = S[i][j+1][next_state]
                    p = Or(Not(A), Not(B), C)
                    constraint_4.append(p)

    c4 = And(constraint_4)

    #constraint 5

    constraint_5 = []
    Y = [Symbol('Y'+ str(i)) for i in range(num_state)]
    constraint_5.append(Or(Y))

    for i in range(num_state):
    	for j in range(i+1, num_state):
    		p = Or(Not(Y[i]), Not(Y[j]))
    		constraint_5.append(p)


    c5 = And(constraint_5)

    #constraint 6
    constraint_6 = []
    for i in range(num_state):
        for j in range(num_state):
            p = Or(Not(Y[i]), S[j][length][i])
            constraint_6.append(p)
    c6 = And(constraint_6)


    CNF = And(c1, c2, c3, c4, c5, c6)

    model = get_model(CNF)
    synchronizing_words = []
    if(not model):
        print("not Satisfied")
    else:
        for i in range(length):
            for j in range(num_alphabet):
                #print(str(model[X[i][j]]))
                if(str(model[X[i][j]]) == 'True'):
                    synchronizing_words.append(alphabet[j])
        return ''.join(synchronizing_words)

'''
states = [0, 1, 2]
alphabet = ['a', 'b']

tf = dict()

tf[(0, 'a')] = 1
tf[(0, 'b')] = 0
tf[(1, 'a')] = 2
tf[(1, 'b')] = 1
tf[(2, 'a')] = 0
tf[(2, 'b')] = 0
'''
l = []
for line in sys.stdin:
    l.append(line.strip().split(' '))

num_state = int(l[0][0])
num_alphabet = int(l[0][1])

states = [i for i in range(num_state)]
alphabet = list(string.ascii_lowercase[0:num_alphabet])

tf = dict();

for i in range(1, len(l)):
    tran_func = (int(l[i][0]), l[i][1])
    tf[tran_func] = int(l[i][2])

#dfa = DFA_generator(10, 2)
#print(dfa.transition_function)


d = DFA(states, alphabet, tf, 0, states)
k = SAT_Based(d, 9)
print(k)
