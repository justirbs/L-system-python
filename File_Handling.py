from Error_Handling import handle_errors

def verify(axiom, angle, length, level, rules):
    if not axiom:
        handle_errors(0)
    if not rules:
        handle_errors(1)
    else:
        for r in rules:
            if "=" not in r:
                handle_errors(3)
    if not angle:
        handle_errors(2)
    if not length:
        length = 4
    if not level:
        level = 1
    return axiom, angle, length, level, rules

def open_settings_file(file) :
    with open(file, "r") as f :
        lines = f.readlines()
    axiom, angle, length, level, rules = None,None,None,None,None
    for i, line in enumerate(lines):
        if axiom == None:  axiom = get_axiom(line)
        if angle == None:  angle = get_angle(line)
        if length == None: length = get_length(line)
        if level == None:  level = get_level(line)
        if rules == None:  rules = get_rule(line)
        if rules == None:  rules = get_rules(lines, line, i)
    axiom, angle, length, level, rules = verify(axiom, angle, length, level, rules)
    return(axiom, angle, length, level, rules)

def get_axiom(line):
    if "axiom" in line :
        if '=' not in line: 
            handle_errors(4)
        else: 
            axiom = line.split("=")[1].replace('"', "").replace(" ", "").strip()
            return axiom

def get_angle(line):
    if "angle" in line :
        if '=' not in line: 
            handle_errors(5)
        else:
            try: 
                angle = int(line.split("=")[1].replace(" ", ""))
                return angle
            except ValueError: 
                handle_errors(8)

def get_length(line):
    if "taille" in line :
        if '=' not in line: 
            handle_errors(6)
        else:
            try: 
                length = int(line.split("=")[1].replace(" ", ""))
                return length
            except ValueError: 
                handle_errors(9)

def get_level(line):
    if "niveau" in line :
        if '=' not in line: 
            handle_errors(7)
        else:
            try: 
                level = int(line.split("=")[1].replace(" ", ""))
                return level
            except ValueError: 
                handle_errors(10)

def get_rule(line):
    if "regle" in line and '"' in line :
        rules = [line.partition("=")[2].replace('"', "").replace(" ", "").strip()]
        return rules

def get_rules(lines, line, i):
    if "regles" in line :
        j = i+1
        rules = []
        while '"' in lines[j] :
            rules.append(lines[j].replace('"', "").replace(" ", "").strip())
            j += 1

        return rules

