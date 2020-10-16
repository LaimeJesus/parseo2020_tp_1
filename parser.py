from sly import Lexer, Parser
from sys import argv, stdin
from json import dumps

class AvalanchaLexer(Lexer):

    # literals = {}

    tokens = {
        FUN,
        CHECK,
        LOWERID,
        UPPERID,
        ARROW,
        COMMA,
        LPAREN,
        RPAREN,
        IMP,
        OR,
        AND,
        NOT,
        TRUE,
        FALSE,
        UNDERSCORE,
        COLON,
        QUESTION,
        BANG,
        EQ
    }

    # Tokens
    FUN         = r'fun'
    CHECK       = r'check'
    ARROW       = r'->'
    COMMA       = r','
    LPAREN      = r'\('
    RPAREN      = r'\)'
    IMP         = r'imp'
    OR          = r'or'
    AND         = r'and'
    NOT         = r'not'
    TRUE        = r'true'
    FALSE       = r'false'
    UNDERSCORE  = r'_'
    COLON       = r':'
    QUESTION    = r'\?'
    BANG        = r'!'
    EQ          = '=='
    LOWERID     = r'[a-z][_a-zA-Z0-9]*'
    UPPERID     = r'[A-Z][_a-zA-Z0-9]*'

    # Ignored pattern
    ignore_whitespaces = '\s'
    ignore_tabs = '\t+'
    ignore_newline = r'\n+'
    ignore_carry = r'\r+'
    ignore_comment = r'--.*'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n') # len(t.value)

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class AvalanchaParser(Parser):
    # Get the token list from the lexer (required)
    tokens = AvalanchaLexer.tokens
    # debugfile = 'parser.out'
    start = 'program'

    @_('prevDeclaraciones declaraciones postDeclaraciones chequeos')
    def program(self, p):
        return ['program', p.declaraciones, p.chequeos]

    @_('declaraciones declaracion')
    def declaraciones(self, p):
        return p.declaraciones + [p.declaracion]

    @_('')
    def prevDeclaraciones(self, p):
        self.nombreMetodo = []

    @_('')
    def postDeclaraciones(self,p):
        metodos = set()
        for a in self.nombreMetodo:
            if a not in metodos:
                metodos.add(a)
            else:
                raise Exception("Mismo Nombre")

    @_('empty')
    def declaraciones(self, p):
        return []

    @_('FUN LOWERID prevReglas prevSignatura signatura postSignatura precondicion postcondicion reglas seenReglas')
    def declaracion(self, p):
        self.nombreMetodo.append(p.LOWERID)
        if self.isEmptySignature:
            signatura = p.seenReglas
        else:
            signatura = p.signatura
        return ['fun', p.LOWERID, signatura, p.precondicion, p.postcondicion, p.reglas]

    @_('')
    def prevSignatura(self, p):
        self.signatureVariables = []

    @_('')
    def postSignatura(self, p):
        variables = set()
        for a in self.signatureVariables:
            if a not in variables:
                variables.add(a)
            else:
                raise Exception('Hay variables en signatura repetidas')

    @_('')
    def prevReglas(self, p):
        self.arity = 0
        self.arities = []

    @_('')
    def seenReglas(self, p):
        comodines = ['_'] * self.arity
        for a in self.arities:
            for b in self.arities:
                if a != b:
                    raise Exception("Diferente Aridad")
        return ['sig', comodines, '_']

    @_('empty')
    def signatura(self, p):
        self.isEmptySignature = True
        return ['sig', [], '_']

    @_('COLON listaParametros ARROW parametro')
    def signatura(self, p):
        self.arity = len(p.listaParametros)
        self.arities = [self.arity]
        self.isEmptySignature = False
        return ['sig', p.listaParametros, p.parametro]

    @_('empty')
    def listaParametros(self, p):
        return []

    @_('listaParametrosNoVacia')
    def listaParametros(self, p):
        return p.listaParametrosNoVacia

    @_('parametro')
    def listaParametrosNoVacia(self, p):
        return [p.parametro]

    @_('parametro COMMA listaParametrosNoVacia')
    def listaParametrosNoVacia(self, p):
        return [p.parametro] + p.listaParametrosNoVacia

    @_('UNDERSCORE')
    def parametro(self, p):
        return '_'

    @_('LOWERID')
    def parametro(self, p):
        self.signatureVariables.append(p.LOWERID)
        return p.LOWERID

    @_('empty')
    def reglas(self, p):
        return []

    @_('regla reglas')
    def reglas(self, p):
        return [p.regla] + p.reglas

    @_('prevPatrones listaPatrones postPatrones ARROW expresion')
    def regla(self, p):
        size = len(p.listaPatrones)
        self.arities.append(size)
        self.arity = max(self.arity, size)
        return ['rule', p.listaPatrones,  p.expresion]

    @_('')
    def prevPatrones(self, p):
        self.variables = []

    @_('')
    def postPatrones(self, p):
        variables = set()
        for a in self.variables:
            if a not in variables:
                variables.add(a)
            else:
                raise Exception('Hay variables repetidas')

    @_('empty')
    def listaPatrones(self, p):
        return []

    @_('listaPatronesNoVacia')
    def listaPatrones(self, p):
        return p.listaPatronesNoVacia

    @_('patron')
    def listaPatronesNoVacia(self, p):
        return [p.patron]

    @_('patron COMMA listaPatronesNoVacia')
    def listaPatronesNoVacia(self, p):
        return [p.patron] + p.listaPatronesNoVacia

    @_('UNDERSCORE')
    def patron(self, p):
        return ['pwild']

    @_('LOWERID')
    def patron(self, p):
        self.variables.append(p.LOWERID)
        return ['pvar', p.LOWERID]

    @_('UPPERID')
    def patron(self, p):
        return ['pcons', p.UPPERID, []]

    @_('UPPERID LPAREN listaPatrones RPAREN')
    def patron(self, p):
        return ['pcons', p.UPPERID, p.listaPatrones]

    @_('empty')
    def precondicion(self, p):
        return ['pre', ['true']]

    @_('QUESTION seenChequeo formula')
    def precondicion(self, p):
        return ['pre', p.formula]

    @_('empty')
    def postcondicion(self, p):
        return ['post', ['true']]

    @_('BANG seenChequeo formula')
    def postcondicion(self, p):
        return ['post', p.formula]

    @_('empty')
    def chequeos(self, p):
        return []

    @_('chequeo chequeos')
    def chequeos(self, p):
        return [p.chequeo] + p.chequeos

    @_('CHECK seenChequeo formula')
    def chequeo(self, p):
        return ['check', p.formula]

    @_('')
    def seenChequeo(self, p):
        self.isSingleExpression = True

    @_('formulaImpOrAndNeg')
    def formula(self, p):
        return p.formulaImpOrAndNeg

    @_('formulaOrAndNeg')
    def formulaImpOrAndNeg(self, p):
        return p.formulaOrAndNeg

    @_('formulaOrAndNeg IMP formulaImpOrAndNeg')
    def formulaImpOrAndNeg(self, p):
        return ['imp', p.formulaOrAndNeg, p.formulaImpOrAndNeg]

    @_('formulaAndNeg')
    def formulaOrAndNeg(self, p):
        return p.formulaAndNeg

    @_('formulaAndNeg OR formulaOrAndNeg')
    def formulaOrAndNeg(self, p):
        return ['or', p.formulaAndNeg, p.formulaOrAndNeg]

    @_('formulaNeg')
    def formulaAndNeg(self, p):
        return p.formulaNeg

    @_('formulaNeg AND formulaAndNeg')
    def formulaAndNeg(self, p):
        return ['and', p.formulaNeg, p.formulaAndNeg]

    @_('formulaAtomica')
    def formulaNeg(self, p):
        return p.formulaAtomica

    @_('NOT formulaNeg')
    def formulaNeg(self, p):
        return ['not', p.formulaNeg]

    @_('TRUE')
    def formulaAtomica(self, p):
        self.isSingleExpression = False
        return ["true"]

    @_('FALSE')
    def formulaAtomica(self, p):
        self.isSingleExpression = False
        return ["false"]

    @_('LPAREN formula RPAREN')
    def formulaAtomica(self, p):
        return p.formula

    @_('expresion')
    def formulaAtomica(self, p):
        if self.isSingleExpression:
            return [
                'equal',
                p.expresion,
                ['cons', 'True', []]
            ]
        return p.expresion

    @_('expresion EQ expresion')
    def formulaAtomica(self, p):
        self.isSingleExpression = False
        return ["equal", p[0], p[2]]

    @_('LOWERID')
    def expresion(self, p):
        return ["var", p.LOWERID]

    @_('LOWERID LPAREN listaExpresiones RPAREN')
    def expresion(self, p):
        return ["app", p.LOWERID, p.listaExpresiones]

    @_('UPPERID')
    def expresion(self, p):
        return ["cons", p.UPPERID, []]

    @_('UPPERID LPAREN listaExpresiones RPAREN')
    def expresion(self, p):
        return ["cons", p.UPPERID, p.listaExpresiones]

    @_('empty')
    def listaExpresiones(self, p):
        return []

    @_('listaExpresionesNoVacia')
    def listaExpresiones(self, p):
        return p.listaExpresionesNoVacia

    @_('expresion')
    def listaExpresionesNoVacia(self, p):
        return [p.expresion]

    @_('expresion COMMA listaExpresionesNoVacia')
    def listaExpresionesNoVacia(self, p):
        return [p.expresion] + p.listaExpresionesNoVacia

    @_('')
    def empty(self, p):
        return []

if __name__ == '__main__':

    '''
    python parser.py tests_parser/test02.input > test02-custom-print.output
    '''

    inputFile  = 'no_input.txt'
    if len(argv) >= 2:
        inputFile = argv[1]
    with open(inputFile,'r') as inputContent:
        data = inputContent.read()

    try:
        lexer = AvalanchaLexer()
        parser = AvalanchaParser()
        tokenized = lexer.tokenize(data)
        result = parser.parse(tokenized)
        jsonResult = dumps(result, indent=3)
        print(jsonResult)
    except Exception as e:
        print(e)
