variables = dict()
while True:
    line = input()
    if line.strip():
        if line == '/exit':
            print('Bye!')
            break
        elif line == '/help':
            print("The program calculates the sum of numbers")
        elif line.startswith('/'):
            print('Unknown command')
            continue
        else:
            for k in line:
                if k not in '=-+ ' and not k.isalnum():
                    print("Invalid expression")
                    break
            else:
                if line.endswith('+') or line.endswith('-'):
                    print("Invalid expression")
                elif line.count('=') > 1:
                    print("Invalid assignment")
                else:
                    if line.strip().isalpha():
                        if line.strip() in variables.keys():
                            print(variables[line.strip()])
                        else:
                            print("Unknown variable")
                    elif '=' in line:
                        expression = [x.strip() for x in line.split('=')]
                        if len(expression) != 2:
                            print("Invalid assignment")
                        elif not expression[0].isalpha():
                            print("Invalid assignment")
                        elif expression[1].isalpha() and expression[1] not in variables.keys():
                            print("Unknown variable")
                        elif expression[1].isalpha():
                            variables[expression[0]] = variables[expression[1]]
                        else:
                            for k in expression[1]:
                                if k not in ' -0123456789':
                                    print("Invalid assignment")
                                    break
                            else:
                                variables[expression[0]] = expression[1]
                    else:
                        expression = line.replace('+', '').split()
                        my_sum = 0
                        multiplier = 1
                        error = False
                        for e in expression:
                            if e.isdigit() or e.isalpha() or (e.startswith('-') and len(e) > 1 and e[1] != '-'):
                                num = 0
                                if e.isalpha():
                                    if e in variables.keys():
                                        num = variables[e]
                                    else:
                                        print("Unknown variable")
                                        error = True
                                        break
                                else:
                                    num = e
                                my_sum += multiplier * int(num)
                                multiplier = 1
                            elif e.startswith('-'):
                                multiplier = pow(-1, len(e))
                            else:
                                print("Unknown variable")
                                error = True
                                break
                        if not error:
                            print(my_sum)