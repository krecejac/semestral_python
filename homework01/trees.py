"""
Module trees
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Node:
    """node"""
    # zachovejte interface metody
    def __init__(self):
        self.name = str()
        self.children = []
        self.pred = []

Cílem je vykreslit v "UTF16-artu" strom definovaný listem hodnot. Každý vnitřní uzel stromu obsahuje vždy dvě položky: název uzlu a seznam potomků (nemusí být nutně v tomto pořadí). Názvem může být jakýkoli objekt kromě typu list (seznam). Příklad triviálního stromu o 1 uzlu: [1, []]

    # zachovejte interface metody
    def add_node_children(self, children):
        """blabla"""
        self.children.append(children)

    # zachovejte interface metody
    def add_node_pred(self, predecessor):
        """blabla"""
        self.pred += predecessor

    # zachovejte interface metody
    def isLast(self, indent, parent_children: list) -> str:
        """blabla"""
        res = ""
        for x in parent_children:
            if self.name == x.name:
                if x == parent_children[-1]:
                    res = "└" + ("─" * (indent-2)) + ">"
                    return res
                res = "├" + ("─" * (indent-2)) + ">"
                return res
        return res


# zachovejte interface metody
def addFill(indent, separator, lvl, pred) -> str:
    """blabla"""
    res = str()
    if lvl > 1:
        for x in range(lvl):
            if x in pred:
                res += "│" + (indent-1)*separator
            else:
                if x != 0:
                    res += (indent)*separator
    return res

# zachovejte interface metody
def node_name(l: list) -> int:
    """blabla"""
    if len(l) != 2:
        raise Exception('Invalid tree')
    if isinstance(l[0], list):
        return 1
    return 0

# zachovejte interface metody
def tree_correctness(l: list):
    """blabla"""
    if len(l) != 2:
        return False
    return ( not isinstance(l[0], list) ) != ( not isinstance(l[1], list) )

INPUT:
[[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23, 2.718281828]], [3, ['x', 'y']], [4, []]], 42]

def allchildNotList(children: list):
    """blabla"""
    return isinstance(children[0], list) and all(isinstance(child, list) for child in children)

OUTPUT:
42
├──>1
│...├──>True
│...│...├──>abc
│...│...└──>def
│...└──>False
│.......├──>1
│.......└──>2
├──>2
│...├──>3.14159
│...├──>6.023e+23
│...└──>2.718281828
├──>3
│...├──>x
│...└──>y
└──>4

class TreeNode:
    """blabla"""
    # zachovejte interface metody
    def __init__(self, def_indent, def_separator):
        """blabla"""
        self.root = Node()
        self.indent = def_indent
        self.separator = def_separator

    # zachovejte interface metody
    def build_tree(self, l: list, is_first=True):
        """blabla"""
        node = Node()
        node_index = node_name(l)
        node.name = l[node_index]
        children = l[1-node_index]
        if not isinstance(children, list):
            raise Exception('Invalid tree')
        if is_first:
            is_first = False
            self.root = node
        if childNum(node, children):
            return node
        if len(children) > 2:
            if allchildNotList(children):
                for child in children:
                    node.add_node_children(self.build_tree(child, is_first))
                return node
            if all(isinstance(child, int) for child in children):
                for child in children:
                    Hodor = Node()
                    Hodor.add_node_name(child)
                    node.add_node_children(Hodor)
                return node
            raise Exception('Invalid tree')
        if tree_correctness(children):
            children = [children]
        for child in children:
            node.add_node_children(self.build_tree(child, is_first))
        return node
    # └ ├ ─ │

    # zachovejte interface metody
    def print_tree(self, indent2, father=None, node=None) -> str:
        """blabla"""
        res = str()
        final_str = str()
        lvl = indent2//self.indent
        pred_counter = []
        if node is not None:
            node.pred += father.pred
        if node is not None and len(node.children) != 0:
            final_str = node.isLast(self.indent, father.children)
            if final_str == ("├" + ("─" * (self.indent-2)) + ">"):
                pred_counter.append(lvl)
                node.pred += pred_counter
        if node is None:
            node = self.root
            res += str(node.name) + '\n'
        if len(node.children) == 0:
            if node != self.root:
                final_str = node.isLast(self.indent, father.children)
                before_str = addFill(self.indent, self.separator, lvl, node.pred)
            return before_str + final_str + str(node.name) + "\n"
        if node != self.root:
            final_str = node.isLast(self.indent, father.children)
            before_str = addFill(self.indent, self.separator, lvl, node.pred)
            res += before_str + final_str + str(node.name) + "\n"
        for child in node.children:
            res += self.print_tree( indent2 + self.indent, node, child )
        return res


# zachovejte interface metody
def render_tree(tree: list = None, indent: int = 2, separator: str = ' ') -> str:
    """blabla"""
    t = TreeNode(indent, separator)
    t.build_tree(tree)
    res = (t.print_tree( 0, t.root))
    print(res)
    return res


my_l = [[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]
#q = [[[1, [[True, ['abc', 'def']], [False, [1, 2]]]], [2, [3.14159, 6.023e23]], [3, ['x', 'y']], [4, []]], 42]
#r = [6, [5, ['dva\nradky']]]
#s = [6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]
#joffrey_lannister = [1, 2, 3]
#p = [4, [5, 6, 7, 8, 9]]
#ll = [1, [2]]
render_tree(my_l, 2, " ")
# s = render_tree(l, 2, " ")
