from turtle import *
from pprint import pprint
from sys import exit, argv
from random import random

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

def equiturtle(axiome1, angle, taille):
    axiome2=''
    ctaille=str(taille)+")"
    cangle=str(angle)+")"
    dico={
    'a':'pd();fd('+ctaille,
    'b':'pu();fd('+ctaille,
    '+':'right('+cangle,
    '-':'left('+cangle,
    '*':'right(180)',
    '[':'positions.append([heading(), pos()])',
    ']':'h,p = positions.pop(-1)\nseth(h);pu();setpos(p);pd()',
    'F':'fd('+ctaille,
    'R':'if r+dc<256: r+=dc;pencolor(r,g,b)',
    'G':'if g+dc<256: g+=dc;pencolor(r,g,b)',
    'B':'if b+dc<256: b+=dc;pencolor(r,g,b)'
    }
    for carac in axiome1:
        if carac in dico:
            axiome2+=dico[carac]
            axiome2+=";\n"
    return axiome2

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

def afficheprog(axiome, taille, angle, regles, niveau):
    axiome2 = (niv(axiome, regles, niveau))
    print(axiome2)
    print(regles)
    commandes = equiturtle(axiome2, angle, taille)
    print("from turtle import *")
    print("positions=[]")
    print("scr = Screen()")
    print("tracer(False)")
    print(commandes)
    print("scr.update()")
    print("exitonclick()")

def write_program_to_file(axiome, taille, angle, regles, niveau, out_file=None):
    axiome2 = niv(axiome, regles, niveau)
    code = "from turtle import *\npositions=[]\nscr = Screen()\ntracer(False)\nr,g,b=0,0,0\ndc=1\nscr.colormode(255)\n"
    code += equiturtle(axiome2, angle, taille)
    code += "scr.update()\nexitonclick()\n"

    if out_file:
        with open(out_file, "w+") as f:
            f.write(code)
    print(code)
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



