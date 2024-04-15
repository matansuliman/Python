def arithmetic_arranger(problems, show_answers=False):
    n = len(problems)
    if(n > 5): return "Error: Too many problems."
    tops = []
    operators = []
    bottoms = []
    problems_len = []
    results = []
    for problem in problems:
        n_problem = len(problem)

        #search for + and - in string
        plus_index = problem.find('+',0,n_problem-1)
        minus_index = problem.find('-',0,n_problem-1)

        #didnt found +/- operators
        if(plus_index == -1 and minus_index == -1): return "Error: Operator must be '+' or '-'."

        #found both + and - operators
        if(plus_index != -1 and minus_index != -1): return "Error: Single operator only."

        #only one of + or - found
        operator_index = plus_index if plus_index > minus_index else minus_index

        #slice the top and bottom strings
        top_str = problem[:operator_index].strip()
        bottom_str = problem[operator_index+1:].strip()

        #top or bottom are not numbers
        if(not top_str.isdigit() or not bottom_str.isdigit()): return "Error: Numbers must only contain digits."

        #top and bottom are numbers
        top, bottom = int(top_str), int(bottom_str)

        #top or bottom has more then 4 digits
        if(top > 9999 or bottom > 9999): return "Error: Numbers cannot be more than four digits."

        #appending the values
        tops.append(top)
        bottoms.append(bottom)

        problems_len.append(max(len(top_str), len(bottom_str)) + 2)

        #append valeus for + and - cases
        if(plus_index != -1):
            operators.append('+')
            results.append(top + bottom)
        elif(minus_index != -1): 
            operators.append('-')
            results.append(top - bottom)

    #construct problems as needed
    problems = ""
    #top
    for i in range(n):
        problems += f'{tops[i]:{problems_len[i]}}'
        if(i != n-1): problems += ' ' * 4
    problems += '\n'
    #operator and bottom
    for i in range(n):
        problems += operators[i]
        problems += f'{bottoms[i]:{problems_len[i]-1}}'
        if(i != n-1): problems += ' ' * 4
    problems += '\n'
    #dashes
    for i in range(n):
        problems += '-' * problems_len[i]
        if(i != n-1): problems += ' ' * 4
    #results
    if(show_answers):
        problems += '\n'
        for i in range(n):
            problems += f'{results[i]:{problems_len[i]}}'
            if(i != n-1): problems += ' ' * 4

    return problems


# Example usage:

print(f'\n{repr(arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"]))}')
print(f'\n{repr(arithmetic_arranger(["3 + 855", "988 + 40"], True))}')