import sys
import json
import pdb
from string import Template


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

if __name__ == '__main__':
    filename = sys.argv[1]
    f = open(filename, 'r')
    Compiler.compile(f.read())
    print(Compiler.output)
    archivo = open("cplusplus.cpp", "w")
    archivo.write(Compiler.output)