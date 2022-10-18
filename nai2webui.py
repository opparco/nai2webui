from io import StringIO
import argparse


class Node:

    def __init__(self, pow):
        self.parent = None
        self.elements = []
        self.pow = pow

    def push_node(self, node):
        node.parent = self
        self.elements.append(node)

    def push_string(self, string):
        self.elements.append(string)

    def improve(self):
        while len(self.elements) == 3 and self.elements[0] == [] and self.elements[2] == []:
            node = self.elements[1]
            self.pow += node.pow
            self.elements = node.elements

        for element in self.elements:
            if type(element) is Node:
                element.improve()

    def write(self, o):
        if self.pow != 0:
            o.write('(')

        for element in self.elements:
            if type(element) is Node:
                element.write(o)
            else:
                for c in element:
                    if c == '(' or c == ')':
                        o.write('\\')
                    o.write(c)

        if self.pow != 0:
            o.write(':{0:.2f})'.format(1.05 ** self.pow))


class Nai2webui:

    def __init__(self, prompt):
        self.root = Node(0)
        node = self.root

        string = []
        node.push_string(string)

        for c in prompt:
            if c == '{' or c == '[':
                nd = Node(1 if c == '{' else -1)
                node.push_node(nd)
                node = nd
                string = []
                node.push_string(string)
            elif c == '}' or c == ']':
                node = node.parent
                string = []
                node.push_string(string)
            else:
                string.append(c)

        self.root.improve()

    def read(self):
        f = StringIO()
        self.root.write(f)
        prompt = f.getvalue()
        f.close()
        return prompt


def nai2webui(prompt):
    n2w = Nai2webui(prompt)
    return n2w.read()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--from-file",
        type=str,
        default="prompt.txt",
        help="path to prompt of NovelAI",
    )
    parser.add_argument(
        "--outpath",
        type=str,
        default="prompt-webui.txt",
        help="path to prompt of WebUI",
    )
    opt = parser.parse_args()

    with open(opt.from_file, "r") as f:
        prompt = f.read()

    with open(opt.outpath, "w") as f:
        f.write(nai2webui(prompt))


if __name__ == "__main__":
    main()
