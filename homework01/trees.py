#!/usr/bin/env python3
# -*- coding: utf-8 -*-
class Node:
    def __init__(self):
        self.name = str()
        self.children = []

    def add_node_name(self, name):
        self.name = name

    def add_node_children(self, children):
        self.children.append(children)

    def isLast(self, indent, parent_children: list) -> str:
        for x in parent_children:
            if self.name == x.name:
                if x == parent_children[-1]:
                    return "└" + ("─" * (indent-2)) + ">"
                else:
                    return "├" + ("─" * (indent-2)) + ">"

    def addFill(self, indent, separator, lvl, pred=[]) -> str:
        res = str()
        if lvl > 1:
            for x in range(lvl):
                if x in pred:
                    res += "│" + (indent-1)*separator
                else:
                    if x != 0:
                        res += (indent)*separator
        return res


def node_name(l: list) -> int:
    if len(l) != 2:
        raise Exception('Invalid tree')
    if type(l[0]) == list:
        return 1
    else:
        return 0


def tree_correctness(l: list):
    if len(l) != 2:
        return False
    return (type(l[0]) != list) != (type(l[1]) != list)


class TreeNode:
    def __init__(self):
        self.root = Node()

    def build_tree(self, l: list, is_first=True):
        node = Node()
        node_index = node_name(l)
        node.name = l[node_index]
        children = l[1-node_index]
        if type(children) != list:
            raise Exception('Invalid tree')
        if is_first:
            is_first = False
            self.root = node
        if len(children) == 1 or len(children) > 2:
            for child in children:
                if type(child) == list:
                    raise Exception('Invalid tree')
                Hodor = Node()
                Hodor.add_node_name(child)
                node.add_node_children(Hodor)
            return node
        if len(children) == 2 and type(children[0]) != list and type(children[1]) != list:
            for child in children:
                Hodor = Node()
                Hodor.add_node_name(child)
                node.add_node_children(Hodor)
            return node
        else:
            if tree_correctness(children):
                children = [children]
            for child in children:
                node.add_node_children(self.build_tree(child, is_first))
        return node
    # └ ├ ─ │

    def print_tree(self, indent, indent2, separator, father=None, node=None, pred=[]) -> str:
        res = str()
        final_str = str()
        lvl = indent2//indent
        pred_counter = []
        if node != None and len(node.children) != 0:
            final_str = node.isLast(indent, father.children)
            if final_str == ("├" + ("─" * (indent-2)) + ">"):
                pred_counter.append(lvl)
                pred = pred_counter
        if node == None:
            node = self.root
            res += str(node.name) + '\n'
        if len(node.children) == 0:
            if node != self.root:
                final_str = node.isLast(indent, father.children)
                before_str = node.addFill(indent, separator, lvl, pred)
            return before_str + final_str + str(node.name) + "\n"
        if node != self.root:
            final_str = node.isLast(indent, father.children)
            before_str = node.addFill(indent, separator, lvl, pred)
            res += before_str + final_str + str(node.name) + "\n"
        for child in node.children:
            res += self.print_tree(indent, indent2 +
                                   indent, separator, node, child, pred)
        return res


# zachovejte interface metody
def render_tree(tree: list = None, indent: int = 2, separator: str = ' ') -> str:
    t = TreeNode()
    t.build_tree(tree)
    res = (t.print_tree(indent, 0, separator, t.root))
    return res


l = [[[1, [True, ['abc', 'def']]], [2, [3.14159, 6.023e23]]], 42]
r = [6, [5, ['dva\nradky']]]
#r = [6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]
#q =  [[[1, [[True, ['abc', 'def']], [False, [1, 2]]]],
#  [2, [3.14159, 6.023e23]], [3, ['x', 'y']], [4, []]], 42]
#z = [6, [[[[1, [2, 3]], [42, [-43, 44]]], 4], 5]]
joffrey_lannister = [1, 2, 3]
render_tree(r, 2, " ")
# s = render_tree(l, 2, " ")
