from sly import Lexer, Parser
from sys import argv, stdin
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

class CalcLexer(Lexer):

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
    ignore = ' \t'

    # Tokens
    FUN         = r'fun'
    CHECK       = r'check'
    ARROW       = r'->'
    COMMA       = r','
    LPAREN      = r'\('
    RPAREN      = r'\)'
    IMP         = r'->'
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
    ignore_newline = r'\n+'
    ignore_comment = r'--.*'
    # ignore_tab     = r'\s*'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n') # len(t.value)

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

'''
Estructura para modelar las restricciones

curr_context = i

info_checks = {
    i: {
        parametros: 1,
        signatura: [variables],
        patrones: [
            patron: {
                varX: True,
                varX
            }
        ]
    }
}


'''


class CalcParser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens
    #debugfile = 'parser.out'
    start = 'program'

    def __init__(self):
        self.current_context = None
        self.state = {}

    def addFunction(self, fun, params):
        pass
    
    def addSignature(self, fun):
        pass

    def addPattern(self, rule, patron):
        pass

    @_('declaraciones chequeos')
    def program(self, p):
        return ['program', p.declaraciones, p.chequeos]

    @_('declaraciones declaracion')
    def declaraciones(self, p):
        return p.declaraciones + [p.declaracion]

    @_('empty')
    def declaraciones(self, p):
        return []

    @_('FUN LOWERID signatura precondicion postcondicion reglas')
    def declaracion(self, p):
        return ['fun', p.LOWERID, p.signatura, p.precondicion, p.postcondicion, p.reglas]

    @_('empty')
    def signatura(self, p):
        return []

    @_('COLON listaParametros ARROW parametro')
    def signatura(self, p):
        return [':', p.listaParametros, '->', p.parametro]

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
        return [p.parametro, ',', p.listaParametrosNoVacia]

    @_('UNDERSCORE')
    def parametro(self, p):
        return ['_', p.UNDERSCORE]

    @_('LOWERID')
    def parametro(self, p):
        return ['LOWERID', p.LOWERID]

    @_('empty')
    def reglas(self, p):
        return []

    @_('regla reglas')
    def reglas(self, p):
        return [p.regla] + p.reglas

    @_('listaPatrones ARROW expresion')
    def regla(self, p):
        return [p.listaPatrones, '->', p.expresion]

    @_('empty')
    def listaPatrones(self, p):
        return []

    @_('listaPatronesNoVacia')
    def listaPatrones(self, p):
        return [p.listaPatronesNoVacia]

    @_('patron')
    def listaPatronesNoVacia(self, p):
        return [p.patron]

    @_('patron COMMA listaPatronesNoVacia')
    def listaPatronesNoVacia(self, p):
        return [p.patron, ',', p.listaParametrosNoVacia]

    @_('UNDERSCORE')
    def patron(self, p):
        return ['_', p.UNDERSCORE]

    @_('LOWERID')
    def patron(self, p):
        return ['LOWERID', p.LOWERID]

    @_('UPPERID')
    def patron(self, p):
        return ['UPPERID', p.UPPERID]

    @_('UPPERID LPAREN listaPatrones RPAREN')
    def patron(self, p):
        return ['UPPERID', p.UPPERID, '(', p.listaPatrones, ')']

    @_('empty')
    def precondicion(self, p):
        return []

    @_('QUESTION formula')
    def precondicion(self, p):
        return ['?', p.formula]

    @_('empty')
    def postcondicion(self, p):
        return []

    @_('BANG formula')
    def postcondicion(self, p):
        return ['?', p.formula]

    @_('empty')
    def chequeos(self, p):
        return []

    @_('chequeo chequeos')
    def chequeos(self, p):
        return p.chequeo + p.chequeos

    @_('CHECK formula')
    def chequeo(self, p):
        return ['check', p.formula]

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
        return ["true"]

    @_('FALSE')
    def formulaAtomica(self, p):
        return ["false"]

    @_('LPAREN formula RPAREN')
    def formulaAtomica(self, p):
        return ['(', p.formula, ')']

    @_('expresion')
    def formulaAtomica(self, p):
        return p.expresion

    @_('expresion EQ expresion')
    def formulaAtomica(self, p):
        return ["equal", p[0], p[2]]

    @_('LOWERID')
    def expresion(self, p):
        return ["var", p.LOWERID]

    @_('LOWERID LPAREN listaExpresiones RPAREN')
    def expresion(self, p):
        return [p.LOWERID, '(', p.listaExpresiones, ')']

    @_('UPPERID')
    def expresion(self, p):
        return [p.UPPERID]

    @_('UPPERID LPAREN listaExpresiones RPAREN')
    def expresion(self, p):
        return [p.UPPERID, '(', p.listaExpresiones, ')']

    @_('empty')
    def listaExpresiones(self, p):
        return []

    @_('listaExpresionesNoVacia')
    def listaExpresiones(self, p):
        return [p.listaExpresionesNoVacia]

    @_('expresion')
    def listaExpresionesNoVacia(self, p):
        return [p.expresion]

    @_('expresion COMMA listaExpresionesNoVacia')
    def listaExpresionesNoVacia(self, p):
        return [p.expresion, ',', p.listaExpresionesNoVacia]

    @_('')
    def empty(self, p):
        return []

if __name__ == '__main__':

    inputFile  = 'no_input.txt'
    outputFile = 'no_output.txt'
    if len(argv) >= 2:
        inputFile = argv[1]
    if len(argv) >= 3:
        outputFile = argv[2]
    print(inputFile)
    print(outputFile)
    with open(inputFile,'r') as inputContent:
        data = inputContent.read()
    lexer = CalcLexer()
    parser = CalcParser()
    result = parser.parse(lexer.tokenize(data))
    with open(outputFile,'w') as outputContent:
        # outputContent.write(result)
        pp.pprint(result)
