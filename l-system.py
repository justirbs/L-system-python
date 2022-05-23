from turtle import *
from pprint import pprint
from sys import exit, argv
from random import random, randrange

def error_out(id):
    if id == 0:
        print("Axiome non define")
        exit()
    if id == 1:
        print("Regle non define")
        exit()
    if id == 2:
        print("Angle non define")
        exit()
    if id == 3:
        print("Egale pas dans regle")
        exit()
    if id == 4:
        print("Egale pas dans axiome")
        exit()
    if id == 5:
        print("Egale pas dans angle")
        exit()
    if id == 6:
        print("Egale pas dans taille")
        exit()
    if id == 7:
        print("Egale pas dans niveau")
        exit()
    if id == 8:
        print("angle n'est pas nombre")
        exit()
    if id == 9:
        print("taille n'est pas nombre")
        exit()
    if id == 10:
        print("niveau n'est pas nombre")
        exit()
    if id == 11:
        print("le fichier d'entree n'est pas specificie")
        exit()
    if id == 12:
        print("le fichier de sorttie n'est pas specificie")
        exit()

def verifie(axiome, angle, taille, niveau, regles):
    if not axiome:
        error_out(0)
    if not regles:
        error_out(1)
    else:
        for r in regles:
            if "=" not in r:
                error_out(3)
    if not angle:
        error_out(2)
    if not taille:
        taille = 4
    if not niveau:
        niveau = 1

    return axiome, angle, taille, niveau, regles

def ouvrirFichier(fichier) :
    with open(fichier, "r") as f :
        lines = f.readlines()
    axiome, angle, taille, niveau, regles = None,None,None,None,None
    for i, line in enumerate(lines):
        if "axiome" in line :
            if '=' not in line: error_out(4)
            else: axiome = line.split("=")[1].replace('"', "").replace(" ", "").strip()
        if "angle" in line :
            if '=' not in line: error_out(5)
            else:
                try: angle = int(line.split("=")[1].replace(" ", ""))
                except ValueError: error_out(8)
        if "taille" in line :
            if '=' not in line: error_out(6)
            else:
                try: taille = int(line.split("=")[1].replace(" ", ""))
                except ValueError: error_out(9)
        if "niveau" in line :
            if '=' not in line: error_out(7)
            else:
                try: niveau = int(line.split("=")[1].replace(" ", ""))
                except ValueError: error_out(10)
        if "regle" in line and '"' in line :
            regles = [line.partition("=")[2].replace('"', "").replace(" ", "").strip()]
        if "regles" in line :
            j = i+1
            regles = []
            while '"' in lines[j] :
                regles.append(lines[j].replace('"', "").replace(" ", "").strip())
                j += 1

    axiome, angle, taille, niveau, regles = verifie(axiome, angle, taille, niveau, regles)
    return(axiome, angle, taille, niveau, regles)

def hex_to_rgb(h):
    s = '0123456789abcdef'
    return [s.index(h[1]) * 16 + s.index(h[2]), s.index(h[3]) * 16 + s.index(h[4]), s.index(h[5]) * 16 + s.index(h[6])]

def get_colors():
    colors = []
    with open("color.conf", "r") as f:
        for line in f:
            if line[0] == "#":
                colors.append(hex_to_rgb(line.strip()))

    return colors

def create_blended_colors(blend_factor, args):
    colors = args + [args[0]]
    all_colors = []
    for i in range(len(colors)-1):
        c1, c2 = colors[i], colors[i+1]
        d_red   = (c2[0] - c1[0]) / blend_factor
        d_green = (c2[1] - c1[1]) / blend_factor
        d_blue  = (c2[2] - c1[2]) / blend_factor
        for s in range(blend_factor):
            all_colors.append([int(c1[0] + d_red * s), int(c1[1] + d_green * s), int(c1[2] + d_blue * s)])


    return all_colors


def get_indexed_color(index, colors):
    total_colors = len(colors)
    color_index = index % total_colors

    return colors[color_index]



def advanced_command_maker(axiom, angle, length):
    color_mode = 1                                      # 0 == change with index 1 == change with dist
    colors = create_blended_colors(50, get_colors())
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
            '~':lambda l,a: 'right({0})'.format(randrange(-a,a))
            }
    commands = ""
    
    lengths = []
    i = 0
    depth = 0
    depths = []
    while i < len(axiom):
        c = axiom[i]
        if c in ['F', 'a', 'b']:
            depth += 1
        elif c == '[':
            depths.append(depth)
        elif c == ']':
            depth = depths.pop(-1)
        
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
                commands += 'thickness += int({0});pensize(thickness)\n'.format(axiom[i+2:i+2+axiom[i+2:].index(')')])
                i += axiom[i+2:].index(')') + 1
        elif c == 'i':
            if color_mode == 0:
                commands += 'pencolor({0})\n'.format(str(get_indexed_color(depth, colors)))
            elif color_mode == 1:
                commands += 'pencolor({0})\n'.format()
        elif c in simple_commands:
            commands += simple_commands[c](length, angle) + '\n'
            if c == '[':
                lengths.append(length)
            elif c == ']':
                length = lengths.pop(-1)

        i += 1

    return commands


def niv(axiome1, regles, niveau):
    if niveau==0:
        axiomeniv=axiome1
    else:
        for i in range(niveau):
            axiomeniv = ''
            for carac in axiome1:
                if carac in regles :
                    for p, v in regles[carac]:
                        if random() < p:
                            axiomeniv += v
                            break

                else:
                    axiomeniv += carac

            axiome1 = axiomeniv
    return axiomeniv

def write_program_to_file(axiome, taille, angle, regles, niveau, out_file=None):
    axiome2 = niv(axiome, regles, niveau)
    code = "from turtle import *\nfrom random import randrange\npositions=[]\nscr = Screen()\ntracer(False)\nr,g,b=0,0,0\ndc=1\nscr.colormode(255)\nthickness={0}\nht()\nscr.bgcolor(51,51,51)\n".format(niveau)
    code +=advanced_command_maker(axiome2, angle, taille)
    code += "scr.update()\nexitonclick()\n"

    if out_file:
        with open(out_file, "w+") as f:
            f.write(code)
    #print(code)
    exec(code)

def nvRegles(regles) :
    dico = {}
    for regle in regles :
        cle, e, valeur = regle.partition("=")
        if '(' in cle and ')' in cle:
            k,v = cle[0], float(cle[2:-1])
            if k in dico:
                dico[k].append([v, valeur])
            else:
                dico[k] = [[v, valeur]]

        else:
            dico[cle] = [[1.0, valeur]]

    return(dico)

if __name__ == '__main__':
    fichier_entree = None
    fichier_sortie = None
    if len(argv) > 1:
        for i in range(1, len(argv)-1):
            if argv[i] == '-i':
                try:
                    fichier_entree = argv[i+1]
                except:
                    print("here")
                    error_out(11)

            if argv[i] == '-o':
                try:
                    fichier_sortie = argv[i+1]
                except:
                    error_out(12)

    else:
        fichier_entree = input("Fichier d'entree: ")

    axiome, angle, taille, niveau, regles = ouvrirFichier(fichier_entree)
    # pprint(regles)
    # pprint(nvRegles(regles))
    write_program_to_file(axiome, taille, angle, nvRegles(regles), niveau, fichier_sortie)



