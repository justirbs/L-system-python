from sys import exit

#  ce fichier gere les erreurs qui peut se
#  produit dans le program.

def handle_errors(id):
    error_0(id)
    error_1(id)
    error_2(id)
    error_3(id)
    error_4(id)
    error_5(id)
    error_6(id)
    error_7(id)
    error_8(id)
    error_9(id)
    error_10(id)
    error_11(id)
    error_12(id)
    error_13(id)
    error_14(id)
    exit()

def error_0(id):
    if id == 0:
        print("Axiome non define")
        
def error_1(id):
    if id == 1:
        print("Regle non define")
        
def error_2(id):
    if id == 2:
        print("Angle non define")
        
def error_3(id):
    if id == 3:    
        print("Egale pas dans regle")
        
def error_4(id):
    if id == 4:
        print("Egale pas dans axiome")
        
def error_5(id):
    if id == 5:
        print("Egale pas dans angle")
        
def error_6(id):
    if id == 6:
        print("Egale pas dans taille")
        
def error_7(id):
    if id == 7:
        print("Egale pas dans niveau")
        
def error_8(id):
    if id == 8:
        print("angle n'est pas nombre")
        
def error_9(id):
    if id == 9:
        print("taille n'est pas nombre")
        
def error_10(id):
    if id == 10:
        print("niveau n'est pas nombre")
        
def error_11(id):
    if id == 11:
        print("le fichier d'entree n'est pas specificie")
        
def error_12(id):
    if id == 12:
        print("le fichier de sorttie n'est pas specificie")

def error_13(id):
    if id == 13:
        print("Erreur sur l'entree du largeur du stylo")

def error_14(id):
    if id == 13:
        print("Erreur sur l'entree du differnce du couleurs")
