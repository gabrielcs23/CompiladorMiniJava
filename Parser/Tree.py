class Tree:
    def __init__(self, rule):
        self.rule = rule
        self.children = []

    def __str__(self, level=0):
        ret = "|\t"*level+repr(self.rule)+"\n"
        if len(self.children) > 0:
            for child in self.children:
                ret += child.__str__(level+1)
        return ret

    def append_child(self, tree):
        self.children.append(tree)
