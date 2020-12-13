import sys
import json
import pdb
from string import Template
import fun
import cons
import rule
from json import load, loads


class Compiler:

    def __init__(self, ast=[], template_path='template.cpp'):
        self.output = ''
        self.template_path = template_path
        self.template = ''
        self.ast = ast
        self.tags = {}

    def template(self):
        with open(self.template_path, 'r') as content:
            self.template = content.read()
            print(self.template)

    @staticmethod
    def compilePrint():
        c = ['case %d: c = "%s"; break;' % (i, c) for i, c in enumerate(cons.cons)]
        return '''
    switch (t->tag) {{
        {0}
        default: c = "";
    }}
    cout << c;
    for(int i = 0; i < t->children.size(); i++) {{
        cout << "(";
        printTerm(t->children[i]);
        cout << ")";
    }}
    '''.format('\n\t'.join(c))

    def generate_tags_rec(self, ast, tags):
        if isinstance(ast, list) and len(ast) > 0:
            head = ast[0]
        else:
            return tags
        if head in ['program', 'imp', 'or', 'and', 'not', 'equal', 'rule']:
            for elem in ast[1]:
                left_tags = self.generate_tags_rec(elem, tags)
                tags = {**tags, **left_tags}
            if head == 'rule':
                right_tags = self.generate_tags_rec(ast[2], tags)
                tags = {**tags, **right_tags}
            else:
                for elem in ast[2]:
                    right_tags = self.generate_tags_rec(elem, tags)
                    tags = {**tags, **right_tags}
        elif head == 'fun': # fun id sig prec postc rules
            prec_tags = self.generate_tags_rec(ast[3], tags)
            post_tags = self.generate_tags_rec(ast[4], tags)
            for elem in ast[5]:
                rules_tags = self.generate_tags_rec(elem, tags)
                tags = {**tags, **rules_tags}
            tags = {**tags, **prec_tags, **post_tags}
        elif head in ['cons', 'pcons', 'app']:
            constructor = ast[1]
            if head != 'app' and constructor not in tags:
                const_id = len(tags)
                tags[constructor] = const_id
            for elem in ast[2]:
                new_tags = self.generate_tags_rec(elem, tags)
                tags = {**tags, **new_tags}
        elif head in ['pre', 'post', 'check']: # pre formula
            new_tags = self.generate_tags_rec(ast[1], tags)
            tags = {**tags, **new_tags}
        elif head in ['var', 'pvar', 'true', 'false', 'pwild']:
            return tags
        else:
            print('something wrong')
            print(head)
        return tags


    def generate_tags(self, ast):
        tags = self.generate_tags_rec(ast, {})
        return tags

    def compile(self):
        self.tags = self.generate_tags(self.ast)
        print('tags')
        print(self.tags)
        # mapping = {}
        # for element in ast:

        # tpl.substitute()

if __name__ == '__main__':
    filename = sys.argv[1]
    ast = {}
    with open(filename, 'r') as content:
        ast = loads(content.read())
        # print('---')
        # print(ast)
        c = Compiler(ast)
        c.compile()
