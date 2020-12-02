import sys
import json
import pdb
from string import Template
import fun
import cons
import rule


class Compiler():
    output = ''
    ast = []
    funs = []
    template = Template('''
#include <vector>
#include <string>
#include <iostream>
using namespace std;

typedef int Tag;
struct Term {
    Tag tag;
    vector<Term*> children;
    int refcnt;
};

void incref(Term* t) {
    t->refcnt = t->refcnt++;
}

void decref(Term* t) {
    if (t->refcnt == 0) {
        for(int i = 0; i < t->children.size(); i++) {
            decref(t->children[i]);
        }
        delete t;
    }
}

$prototypes
$functions
$checks

void printTerm(Term* t) {
    string c;
    $print
}

int main() {
    $main
    return 0;
}
''')

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

if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, 'r')
    Compiler.compile(f.read())
    print(Compiler.output)
    archivo = open("cplusplus.cpp", "w")
    archivo.write(Compiler.output)