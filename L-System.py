from turtle import *
from pprint import pprint
from sys import exit, argv
from random import random, randrange

from Error_Handling import handle_errors
from File_Handling import open_settings_file 


START_CODE = """
from turtle import *
from random import randrange
positions=[]
scr = Screen()
scr.colormode(255)
tracer(False)
r,g,b=220,200,200
dc=10
thickness={0}
pensize(thickness)
w,h = screensize()
if w<0: w=400
if h<0: h=400
screensize(w,h,'#090909')
pencolor(r,g,b)
"""
END_CODE = """
scr.update()
exitonclick()
"""
START_CENTER = """
lt(90)
pu()
goto(0, -h+10)
pd()
"""

#  les commands simple ( 1 caracter )
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

#  fonction qui cree les commandes turtle 
def advanced_command_maker(axiom, angle, length):
    commands = ""                                                                                   #
    lengths = []
    i = 0
    while i < len(axiom):                                                                           # pour chaque caractere dans l'axiom
        c = axiom[i]
        if c == 'l':                                                                                # changer le taille
            if axiom[i+1] == '(':
                length *= float(axiom[i+2:i+2+axiom[i+2:].index(')')])                              # recupere le nombre entre les parentheses
                i += axiom[i+2:].index(')') + 1
        elif c == 't':                                                                              # changer l'angle  
            if axiom[i+1] == '(':
                angle *= float(axiom[i+2:i+2+axiom[i+2:].index(')')])                               # recupere le nombre entre les parentheses
                i += axiom[i+2:].index(')') + 1
        elif c == '!':                                                                              # changer le largeur du stylo
            if axiom[i+1] == '(':
                something = axiom[i+2:i+2+axiom[i+2:].index(')')]                                   # recupere le nombre entre les parentheses
                commands += 'thickness += int({0});pensize(thickness)\n'.format(something)
                i += axiom[i+2:].index(')') + 1
        elif c in simple_commands:                                                                  # le command est simple ( 1 caracter )
            commands += simple_commands[c](length, angle) + '\n'
            if c == '[':
                lengths.append(length)
            elif c == ']':
                length = lengths.pop(-1)
        i += 1
    return commands



#  fonction main 'secondaire' 
def generate_commands(axiom, length, angle, rules, level, width, centered):
    if not width:                                                                                   # 
        width = 1                                                                                   # si l'argument -s n'est pas definer mettre la largeur du style a 1
    elif width < 0:
        width = 1
    axiom = generate_axiom(axiom, rules, level)                                                     # genere l'axiom
    code = START_CODE.format(width)                                                                 # | cree les commands turtle
    if centered: code += START_CENTER                                                               # | 
    code += advanced_command_maker(axiom, angle, length)                                            # |
    code += END_CODE                                                                                # |
    return code



#  fonction recursive qui parse l'axiom pour les parties fondemental
#  could be optimised a bit
def partition_axiom(string, patterns):
    res = []                                                                                        # 
    for p, i in patterns:                                                                           # ermm.. ill come back to this
        if p in string:
            b,f,a = string.partition(p)
            if b:
                res += partition_axiom(b, patterns)
            res += [f]
            if a:
                res += partition_axiom(a, patterns)
            break
    else:
        res = [string]
    return res



#  partion l'axiom dans ces parties fondemental
def create_partitioned_axiom(rules, axiom):
    patterns = []                                                                                   #
    for key in rules.keys():                                                                        # | pour chaque regle
        searching = True
        while searching == True:
            ind = axiom.find(key)                                                                   # | trouver tout les correspondances de ce regle dans l'axiom
            if ind != -1:
                for s,index in patterns:                                                            # | si on a deja trouver ce correspondance
                    if ind == index:
                        searching = False
                        break
                else:
                    patterns.append([axiom[ind:ind+len(key)],ind])                                  # | si non ajouter ce correspondances a le liste ['match', index]
            else:
                searching = False
        
    patterns.sort(key=lambda x: len(x[0]), reverse=True)                                            # trier tout les correspondances en function de son index dans l'axiom
    return partition_axiom(axiom, patterns)                                                         # ╰─> remettre l'axiom dans l'ordre  



#  genere le prochain axiom
def create_next_axiom(splitted_axiom, rules):
    axiom = ''                                                                                      #
    for string in splitted_axiom:                                                                   # | pour chaque partie dans l'axiom : 'abc','bc','cbbba'
        if string in rules:                                                                         # || si le partie est un des regles ( normalement plusier caracters )
            for p, v in rules[string]:                                                              # || recuperer son replacant et le probabilite
                if random() < p:                                                                    # || ajouter avec proba
                    axiom += v
                    break
        else:                                                                                       # || si le partie n'est pas dans regles alors il est compose des singletons 
            for character in string:                                                                # ||| pour tout les caracteres dans ce partie
                if character in rules :                                                             # |||| si il fait partie des regles
                    for p, v in rules[character]:                                                   # |||| ajouter avec proba 
                        if random() < p:
                            axiom += v
                            break
                else:
                    axiom += character                                                              # |||| si non ajouter le caractere
    return axiom



#  genere le generation du axiome
def generate_axiom(original_axiom, rules, level):
    if level==0:                                                                                    # 
        new_axiom=original_axiom                                                                    # case where level == 0
    else:
        for i in range(level):                                                                      # pour chaque niveau cree le prochain
            new_axiom = ''
            splitted_axiom = create_partitioned_axiom(rules, original_axiom)
            new_axiom = create_next_axiom(splitted_axiom, rules)

            original_axiom = new_axiom
    return new_axiom



#  genere le dictionnaire des regles
def generate_rules(rules) :
    dico = {}                                                                                       # 
    for rule in rules :                                                                             # pour chaque regle ( regles separe par \n ) EX: "a<b(.5)=aabb"
        key, e, value = rule.partition("=")                                                         # separe par l'egale: 'a<b(.5)' '=' 'aabb'
        key = key.replace('<','').replace('>','')                                                   # enlever le '<' '>': 'ab(.5)
        if '(' in key and ')' in key:                                                               # | si stockastic
            i = key.index('(')                                                                      # |
            k,v = key[:i], float(key[i+1:key.index(')')])                                           # | separe les lettres et la probabilite
            if k in dico:                                                                           # | ajouter {'ab':[[.5,'aabb']]} au dictionaire
                dico[k].append([v, value])                                                          # |
            else:                                                                                   # |
                dico[k] = [[v, value]]                                                              # |
        else:                                                                                       # | si pas stockastic
            dico[key] = [[1.0, value]]                                                              # | ajouter {'ab':[[1, 'aabb']]} au dictionaire

    return(dico)



#  gere le fichier d'entree
def get_input_file(argv, i):
    if argv[i] == '-i':
        try:
            file_input = argv[i+1]
            return file_input
        except:
            handle_errors(11)



#  gere le fichier de sortie
def get_output_file(argv, i):
    if argv[i] == '-o':
        try:
            file_output = argv[i+1]
            return file_output
        except:
            handle_errors(12)



#  gere la largeur initial du stylo
def get_inital_width(argv, i):
    if argv[i] == '-s':
        try:
            width = int(argv[i+1])
            return width
        except:
            handle_errors(13)



#  main 
if __name__ == '__main__':
    file_input = None                                                                               #
    file_output = None
    width = None
    centered = False
    if len(argv) > 1:                                                                               # | gere les argument du command ligne
        for i in range(1, len(argv)):                                                               # |
            if argv[i] == '-c': centered = True                                                     # |
            if not file_input : file_input  = get_input_file(argv, i)                               # |
            if not file_output: file_output = get_output_file(argv, i)                              # |
            if not width      : width       = get_inital_width(argv, i)                             # |
    else:                                                                                           # |
        file_input = input("Fichier d'input: ")                                                     # |

    axiom, angle, length, level, rules = open_settings_file(file_input)                             # recupere les parametres dans le fichier
    code = generate_commands(axiom, length, angle, generate_rules(rules), level, width, centered)   # cree les commandes turtle
    if file_output:                                                                                 # | si fichier de sortie
        with open(file_output, "w+") as f:                                                          # | ecrit les commandes dans le fichier
            f.write(code)                                                                           # | 

    pprint(code)                                                                                    # afficher les commands turtle 
    exec(code)                                                                                      # executer les commands turtle




