from pulp import *

#OPTIMIZATION MODEL
model = LpProblem("Cubewise Problem", LpMaximize)

#PARAMETERS
objective_weights = {'R': 100, 'O': 10, 'I': 1}

#DECISION VARIABLES
letters = ['C', 'U', 'B', 'E', 'W', 'I', 'S', 'M', 'O', 'R']
letter_numbers = LpVariable.dicts("Letter", letters, 0, 9, LpInteger) #xi  
letter_pairs = LpVariable.dicts("Pair", (letters, letters), 0, 1, LpBinary) #bij
print(letter_numbers)

#OBJECTIVE FUNCTION
objective_letters = ['R', 'O', 'I']
objective_function = lpSum(objective_weights[i]*letter_numbers[i] for i in objective_letters)
print(objective_function)

model += objective_function

#CONSTRAINTS
model += (lpSum([(letter_numbers['C'] + letter_numbers['W'] - letter_numbers['M'])*1000, 
                (letter_numbers['U'] + letter_numbers['I'] - letter_numbers['O'])*100,
                (letter_numbers['B'] + letter_numbers['S'] - letter_numbers['R'])*10, 
                letter_numbers['E']]) == 0)

for i in letter_pairs:
    for j in letter_pairs[i]:
        if i != j:
            model += letter_numbers[i] >= letter_numbers[j] + (1 - letter_pairs[i][j]) - 9*letter_pairs[i][j]
            model += letter_numbers[j] >= letter_numbers[i] + letter_pairs[i][j] - 9*(1 - letter_pairs[i][j])

model.solve()
print("Status: ", LpStatus[model.status])

for v in model.variables():
    if v.name.startswith('Letter'):
        print(v.name, "=", v.varValue)
 
print("ROI = ", value(model.objective))
