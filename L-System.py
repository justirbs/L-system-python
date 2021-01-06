from turtle import *
from pprint import pprint
from sys import exit, argv
from random import random, randrange

from Error_Handling import handle_errors
from File_Handling import open_settings_file 

START_CENTER = True

START_CODE = """
from turtle import *
from random import randrange
positions=[]
scr = Screen()
scr.colormode(255)
tracer(False)
r,g,b=0,0,0
dc=1
thickness={0}
"""
END_CODE = """
scr.update()
exitonclick()
"""

if START_CENTER:
    START_CODE += """
lt(90)
w,h = screensize()
pu()
goto(0, -h+10)
pd()
"""


simple_commands = {
        'a':lambda l,a: 'pd();fd({0})'.format(l),
        'b':lambda l,a: 'pu();fd({0})'.format(l),
        '+':lambda l,a: 'right({0})'.format(a),
        '-':lambda l,a: 'left({0})'.format(a),
        '*':lambda l,a: 'right(180)',
        '[':lambda l,a: 'positions.append([heading(), pos(), thickness])',
        ']':lambda l,a: 'h,p,t = positions.pop(-1)\nseth(h);pu();setpos(p);pd();thickness=t;pensize(thickness)',
        'F':lambda l,a: 'fd({0})'.format(l),
        'f':lambda l,a: 'pu();fd({0});pd()'.format(l),
        'R':lambda l,a: 'if r+dc<256: r+=dc;pencolor(r,g,b)',
        'G':lambda l,a: 'if g+dc<256: g+=dc;pencolor(r,g,b)',
        'B':lambda l,a: 'if b+dc<256: b+=dc;pencolor(r,g,b)',
        'r':lambda l,a: 'if r-dc>=0: r-=dc;pencolor(r,g,b)',
        'g':lambda l,a: 'if g-dc>=0: g-=dc;pencolor(r,g,b)',
        'b':lambda l,a: 'if b-dc>=0: b-=dc;pencolor(r,g,b)',
        '~':lambda l,a: 'right({0})'.format(randrange(-a,a))
        }

def advanced_command_maker(axiom, angle, length):
    commands = ""
    lengths = []
    i = 0
    while i < len(axiom):
        c = axiom[i]
        if c == 'l':
            if axiom[i+1] == '(':
                length *= float(axiom[i+2:i+2+axiom[i+2:].index(')')])
                i += axiom[i+2:].index(')') + 1
        elif c == 't':
            if axiom[i+1] == '(':
                angle *= float(axiom[i+2:i+2+axiom[i+2:].index(')')])
                i += axiom[i+2:].index(')') + 1
        elif c == '!':
            if axiom[i+1] == '(':
                color = axiom[i+2:i+2+axiom[i+2:].index(')')]
                commands += 'thickness += int({0});pensize(thickness)\n'.format(color)
                i += axiom[i+2:].index(')') + 1
        elif c in simple_commands:
            commands += simple_commands[c](length, angle) + '\n'
            if c == '[':
                lengths.append(length)
            elif c == ']':
                length = lengths.pop(-1)
        i += 1

    return commands

def generate_axiom(original_axiom, rules, level):
    if level==0:
        new_axiom=original_axiom
    else:
        
        for i in range(level):
            new_axiom = ''
            for character in original_axiom:
                if character in rules :
                    for p, v in rules[character]:
                        if random() < p:
                            new_axiom += v
                            break

                else:
                    new_axiom += character

            original_axiom = new_axiom
    return new_axiom

def write_program_to_file(axiom, length, angle, rules, level, out_file=None):
    axiom = generate_axiom(axiom, rules, level)
    code = START_CODE.format(1)
    code += advanced_command_maker(axiom, angle, length)
    code += END_CODE
    if out_file:
        with open(out_file, "w+") as f:
            f.write(code)
    exec(code)
    #print(code)

def generate_rules(rules) :
    dico = {}
    for rule in rules :
        key, e, value = rule.partition("=")
        if '(' in key and ')' in key:
            k,v = key[0], float(key[2:-1])
            if k in dico:
                dico[k].append([v, value])
            else:
                dico[k] = [[v, value]]

        else:
            dico[key] = [[1.0, value]]

    return(dico)

if __name__ == '__main__':
    file_input = None
    file_output = None
    if len(argv) > 1:
        for i in range(1, len(argv)-1):
            if argv[i] == '-i':
                try:
                    file_input = argv[i+1]
                except:
                    handle_errors(11)

            if argv[i] == '-o':
                try:
                    file_output = argv[i+1]
                except:
                    handle_errors(12)

    else:
        file_input = input("Fichier d'input: ")

    axiom, angle, length, level, rules = open_settings_file(file_input)
    # pprint(rules)
    # pprint(generate_rules(rules))
    write_program_to_file(axiom, length, angle, generate_rules(rules), level, file_output)



