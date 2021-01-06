# L-SYSTEM

## Usage
The file is run with
```
python L-System.py
```
then addition flags are available:
```
-i "input file"
-o "output file"
-c centered at bottom
-s <pen size>
```
the input file must contain: 
```
axiome = ""
regle = ""
angle = <int>
```
to be valid
with angle being an integer

Additional settings can be added:
```
taille = <int>
niveau = <int>
```
You can find more examples in Tests/


In axiome and regles these characters are special:
key characters:
```
a : pen down and move forward 'taille' steps
b : pen up and move forward 'taille' steps
+ : turn right 'angle' degrees
- : turn left 'angle' degrees
F : move forward 'taille' steps
r : change red value by -dc
g : change green value by -dc
b : change blue value by -dc
R : change red value by dc
G : change green value by dc
B : change blue value by dc
l : change line length : l(.5) = half line length : l(2) = double line length
t : change pen size  : l(.5) = half pen size  : l(2) = double pen size 
! : change angle  : l(.5) = half angle  : l(2) = double angle 
```

thanks
