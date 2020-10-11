from sly import Lexer, Parser
from sys import argv, stdin
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=3)

def custom_tab(s, size):
    tab_str = ['   '] * size
    tab_str = ''.join(tab_str)
    return tab_str + s

def custom_print(ls, tabs=0):
    if not isinstance(ls, list):
        # print('not list: ' + ls)
        print(custom_tab(ls, tabs))
    elif len(ls) == 0:
        # print('empty list')
        print(custom_tab("[]", tabs))
    else:
        curr_tab = tabs + 1
        print(custom_tab("[", tabs))
        # print('recursive list')
        for elem in ls:
            custom_print(elem, curr_tab)
        print(custom_tab("]", tabs))

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
        self.chequeos = []
        self.currentCheck = -1
        # self.resetCheckVariables()

    def addFunction(self, fun, params):
        pass
    
    def addSignature(self, fun):
        pass

    def addPattern(self, rule, patron):
        pass

    def getCheckVariables(self):
        return ['hasAnd', 'hasOr', 'hasImp', 'hasEq']

    def getCurrentCheck(self):
        if self.currentCheck >= 0 and len(self.chequeos) > self.currentCheck:
            return self.chequeos[self.currentCheck]
        return None

    def resetCheckVariables(self):
        variables = self.getCheckVariables()
        for var in variables:
            self.addCheckVariable(var, False)

    def addCheckVariable(self, var, val=True):
        currentCheck = self.getCurrentCheck()
        if currentCheck:
            # print('------addCheckVariable--------')
            # print(currentCheck)
            currentCheck[var] = val
            # print(currentCheck)

    # recordar que chequeos es una lista de diccionarios
    def isSingleExpression(self):
        variables = self.getCheckVariables()
        check = self.getCurrentCheck()
        if check is not None:
            return not any(
                map(
                    lambda x: x in check and check[x],
                    variables
                )
            )
        return True

    def addChequeo(self):
        check_info = {
            'hasAnd': False,
            'hasOr': False,
            'hasImp': False,
            'hasEq': False
        }
        self.chequeos.append(check_info)
        self.currentCheck = len(self.chequeos) - 1
    
    def addFormula(self, key):
        check = self.getCurrentCheck()
        check[key] = True

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
        return ['pwild', p.UNDERSCORE]

    @_('LOWERID')
    def patron(self, p):
        return ['pvar', p.LOWERID]

    @_('UPPERID')
    def patron(self, p):
        return ['pcons', p.UPPERID]

    @_('UPPERID LPAREN listaPatrones RPAREN')
    def patron(self, p):
        return ['pcons', p.UPPERID, p.listaPatrones]

    @_('empty')
    def precondicion(self, p):
        return []

    @_('QUESTION formula')
    def precondicion(self, p):
        return ['pre', p.formula]

    @_('empty')
    def postcondicion(self, p):
        return []

    @_('BANG formula')
    def postcondicion(self, p):
        return ['post', p.formula]

    @_('empty')
    def chequeos(self, p):
        return []

    @_('chequeo chequeos')
    def chequeos(self, p):
        # self.addChequeo()
        return [p.chequeo] + p.chequeos

    @_('CHECK seenChequeo formula')
    def chequeo(self, p):
        return ['check', p.formula]

    @_('')
    def seenChequeo(self, p):
        # print('seenChequeo')
        self.addChequeo()

    @_('formulaImpOrAndNeg')
    def formula(self, p):
        return p.formulaImpOrAndNeg

    @_('formulaOrAndNeg')
    def formulaImpOrAndNeg(self, p):
        return p.formulaOrAndNeg

    @_('formulaOrAndNeg seenIMP IMP formulaImpOrAndNeg')
    def formulaImpOrAndNeg(self, p):
        return ['imp', p.formulaOrAndNeg, p.formulaImpOrAndNeg]
    
    @_('')
    def seenIMP(self, p):
        self.addCheckVariable('hasImp')
        return True

    @_('formulaAndNeg')
    def formulaOrAndNeg(self, p):
        return p.formulaAndNeg

    @_('formulaAndNeg seenOR OR formulaOrAndNeg')
    def formulaOrAndNeg(self, p):
        return ['or', p.formulaAndNeg, p.formulaOrAndNeg]

    @_('')
    def seenOR(self, p):
        self.addCheckVariable('hasOr')
        return True

    @_('formulaNeg')
    def formulaAndNeg(self, p):
        return p.formulaNeg

    @_('formulaNeg seenAND AND formulaAndNeg')
    def formulaAndNeg(self, p):
        return ['and', p.formulaNeg, p.formulaAndNeg]

    @_('')
    def seenAND(self, p):
        self.addCheckVariable('hasAnd')
        return True

    @_('formulaAtomica')
    def formulaNeg(self, p):
        return p.formulaAtomica

    @_('NOT formulaNeg')
    def formulaNeg(self, p):
        return ['not', p.formulaNeg]

    @_('TRUE')
    def formulaAtomica(self, p):
        if self.isSingleExpression():
            print("is single expr - true")
        return ["true"]

    @_('FALSE')
    def formulaAtomica(self, p):
        if self.isSingleExpression():
            print("is single expr - false")
        return ["false"]

    @_('LPAREN formula RPAREN')
    def formulaAtomica(self, p):
        if self.isSingleExpression():
            print("is single expr p.form")
        return [p.formula]

    @_('expresion')
    def formulaAtomica(self, p):
        if self.isSingleExpression():
            # print('is single exp p.expresion')
            return [
                'equal',
                p.expresion,
                ['cons', 'True', []]
            ]
        return p.expresion

    @_('expresion seenEQ EQ expresion')
    def formulaAtomica(self, p):
        return ["equal", p[0], p[3]]

    @_('')
    def seenEQ(self, p):
        self.addCheckVariable('hasEq')
        return True

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
    outputFile = 'no_output.txt'
    if len(argv) >= 2:
        inputFile = argv[1]
    if len(argv) >= 3:
        outputFile = argv[2]
    with open(inputFile,'r') as inputContent:
        data = inputContent.read()
    lexer = CalcLexer()
    parser = CalcParser()
    tokenized = lexer.tokenize(data)
    # print('----tokenized---')
    # for token in tokenized:
    #     print(token)
    result = parser.parse(tokenized)
    with open(outputFile,'w') as outputContent:
        # outputContent.write(result)
        custom_print(result)
        # pp.pprint(result)
