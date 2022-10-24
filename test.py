import ast
import inspect
from pathlib import Path

        



        

l = [[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]
#root = Node(l)
#
#
#
#
#
#
#def print_uzel( deep, ind, sep, connect, first, name ):
#    if deep > 0:
#        if deep > 1:
#            print(first, end="")
#            if deep > 2:
#                print(sep, end="")
#            for x in range( (deep-1) * (ind-1) ):
#                print(sep, end="")
#        print(connect, end="")
#        for x in range( ind-2 ):
#            print("─", end="")
#        print(">", end="")
#        print(name)
#    else:
#        print(name)
#def print_lists( neco, deep, ind, sep, last, total, father ):
#    l_lists = []
#    l_names = []
#    first = ""
#    connect = ""
#    for x in neco:
#        if type(x) == list:
#            l_lists.append(x)
#        else:
#            l_names.append(x)
#    for x in l_names:
#        if last:
#            connect = "└"
#            first = sep
#            father = True
#        elif x == neco[-1]:
#            connect = "└"
#        else:
#            connect = "├"
#            first = "│"
#        if father:
#            first = sep
#        print_uzel( deep, ind, sep, connect, first, x)
#        if len(l_lists) != 0:
#            deep += 1
#    for x in l_lists:
#        if x == total[-1]:
#            last = True        
#        else:
#            last = False 
#        print_lists( x, deep, ind, sep, last, total, father )
#l = [[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]
#l = [[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23]], [3, ['x', 'y']], [4, []]], 42]
#l = [6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]
#l = [6, [5, ['dva\nradky']]]
#for x in l:
#    if type(x) == list:
#        total = x
#father = False
#deep = 0
#ind = 2
#sep = " "
#last = False
#print(last)
#print_lists(l, deep, ind, sep, last, total, father )


class TreeNode:
    def __init__(self, data, parent=None):
        self.name = None
        self.parent = parent
        self.children = []
        for x in data:
            if type(x) != list:
                self.name = x
            if type(x) == list:
                self.children = x
        for x in self.children:
            TreeNode(self.children, self) 

    def printTree( self,indent, separator, child=None ):
        if (child == None):
            child = self.parent
        print(self.name)
        if self.children:
            for child in self.children:
                self.printTree( indent, separator, child )


# zachovejte interface metody
def render_tree(tree: list = None, indent: int = 2, separator: str = ' ') -> str:
    binary_tree = TreeNode(tree)
    binary_tree.printTree(indent, separator)
    return ''

l = [[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]
s = render_tree(l, 2, " ")


"""
Version 0.1

Cílem je vykreslit v "UTF16-artu" strom definovaný listem hodnot. Každý uzel stromu obsahuje vždy dvě položky: název uzlu
a seznam potomků (nemusí být nutně v tomto pořadí). Názvem může být jakýkoli objekt kromě typu list (seznam). Příklad
triviálního stromu o 1 uzlu: [1, []]

Strom bude vykreslen podle následujících pravidel:
    - Vykresluje se shora dolů, zleva doprava.
    - Uzel je reprezentován jménem, které je stringovou serializací objektu daného v definici uzlu.
    - Uzel v hloubce N bude odsazen zlava o N×{indent} znaků, přičemž hodnota {indent} bude vždy kladné celé číslo > 1.
    - Má-li uzel K potomků, povede:
        - k 1. až K-1. uzlu šipka začínající znakem ├ (UTF16: 0x251C)
        - ke K. uzlu šipka začínající znakem └ (UTF16: 0x2514)
    - Šipka k potomku uzlu je vždy zakončena znakem > (UTF16: 0x003E; klasické "větší než").
    - Celková délka šipky (včetně úvodního znaku a koncového ">") je vždy {indent}, výplňovým znakem je zopakovaný znak ─ (UTF16: 0x2500).
    - Všichni potomci uzlu jsou spojeni na úrovni počátku šipek svislou čarou │ (UTF16: 0x2502); tedy tam, kde není jako úvodní znak ├ nebo └.
    - Pokud název uzlu obsahuje znak `\n` neodsazujte nijak zbytek názvu po tomto znaku.
    - Každý řádek je ukončen znakem `\n`.

Další požadavky na vypracovní:
    - Pro nevalidní vstup musí implementace vyhodit výjimku `raise Exception('Invalid tree')`.
    - Mít codestyle v souladu s PEP8 (můžete ignorovat požadavek na délku řádků - C0301 a používat v odůvodněných případech i jednopísmenné proměnné - C0103)
        - otestujte si pomocí `pylint --disable=C0301,C0103 trees.py`
    - Vystačit si s buildins metodami, tj. žádné importy dalších modulů.


Příklady vstupu a výstupu:
INPUT:
[[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
42
├──>1
│...└──>True
│.......├──>abc
│.......└──>def
└──>2
....├──>3.14159
....└──>6.023e+23

INPUT:
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23]], [3, ['x', 'y']], [4, []]], 42]

PARAMS:
    indent = 4
    separator = '.'

OUTPUT:
├──>1
│...├──>True
│...│...├──>abc
│...│...└──>def
│...└──>False
│.......├──>1
│.......└──>2
├──>2
│...├──>3.14159
│...└──>6.023e+23
├──>3
│...├──>x
│...└──>y
└──>4

INPUT:
[6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>4
    ├>1
    │ ├>2
    │ └>3
    └>42
      ├>-43
      └>44

INPUT:
[6, [5, ['dva\nradky']]]

PARAMS:
    indent = 2
    separator = ' '

OUTPUT:
6
└>5
  └>dva
radky

Potřebné UTF16-art znaky:
└ ├ ─ │

Odkazy:
https://en.wikipedia.org/wiki/Box_Drawing
"""