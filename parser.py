from sly import Lexer, Parser

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
    LOWERID     = r'[a-z][_a-zA-Z0-9]*'
    UPPERID     = r'[A-Z][_a-zA-Z0-9]*'
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

class CalcParser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens
    #debugfile = 'parser.out'
    start = 'program'

    @_('declaraciones')
    def program(self, p):
        return ('program', p.declaraciones)

    @_('declaraciones declaracion')
    def declaraciones(self, p):
        return p.declaraciones + [p.declaracion]

    @_('empty')
    def declaraciones(self, p):
        return []

    @_('FUN LOWERID signatura precondicion postcondicion reglas')
    def declaracion(self, p):
        return ('fun', p.LOWERID, p.signatura, p.precondicion, p.postcondicion, p.reglas)

    @_('empty')
    def signatura(self, p):
        pass

    @_('COLON listaParametros ARROW parametro')
    def signatura(self, p):
        return (':', p.listaParametros, '->', p.parametro)

    @_('empty')
    def listaParametros(self, p):
        return []

    @_('listaParametrosNoVacia')
    def listaParametros(self, p):
        return p.listaParametrosNoVacia

    @_('parametro')
    def listaParametrosNoVacia(self, p):
        return p.parametro

    @_('parametro COMMA listaParametrosNoVacia')
    def listaParametrosNoVacia(self, p):
        return (p.parametro, ',', p.listaParametrosNoVacia)

    @_('UNDERSCORE')
    def parametro(self, p):
        return ('_', p.UNDERSCORE)

    @_('LOWERID')
    def parametro(self, p):
        return ('LOWERID', p.LOWERID)

    @_('empty')
    def reglas(self, p):
        return []

    @_('regla reglas')
    def reglas(self, p):
        return [p.regla] + p.reglas

    @_('listaPatrones ARROW expresion')
    def regla(self, p):
        return (p.listaPatrones, '->', p.expresion)

    @_('empty')
    def listaPatrones(self, p):
        pass

    @_('listaPatronesNoVacia')
    def listaPatrones(self, p):
        return (p.listaPatronesNoVacia)

    @_('patron')
    def listaPatronesNoVacia(self, p):
        return (p.patron)

    @_('patron COMMA listaPatronesNoVacia')
    def listaPatronesNoVacia(self, p):
        return (p.patron, ',', p.listaParametrosNoVacia)

    @_('UNDERSCORE')
    def patron(self, p):
        return ('_', p.UNDERSCORE)

    @_('LOWERID')
    def patron(self, p):
        return ('LOWERID', p.LOWERID)

    @_('UPPERID')
    def patron(self, p):
        return ('UPPERID', p.UPPERID)

    @_('UPPERID LPAREN listaPatrones RPAREN')
    def patron(self, p):
        return ('UPPERID', p.UPPERID, '(', p.listaPatrones, ')')

    @_('empty')
    def precondicion(self, p):
        pass

    @_('QUESTION formula')
    def precondicion(self, p):
        return ('?', p.formula)

    @_('empty')
    def postcondicion(self, p):
        pass

    @_('BANG formula')
    def postcondicion(self, p):
        return ('?', p.formula)

    @_('empty')
    def chequeos(self, p):
        return []

    @_('chequeo chequeos')
    def chequeos(self, p):
        return [p.chequeo] + p.chequeos

    @_('CHECK formula')
    def chequeo(self, p):
        return ('CHECK', p.formula)

    @_('formulaImpOrAndNeg')
    def formula(self, p):
        return p.formulaImpOrAndNeg

    @_('formulaOrAndNeg')
    def formulaImpOrAndNeg(self, p):
        return p.formulaOrAndNeg

    @_('formulaOrAndNeg IMP formulaImpOrAndNeg')
    def formulaImpOrAndNeg(self, p):
        return (p.formulaOrAndNeg, 'IMP', p.formulaImpOrAndNeg)

    @_('formulaAndNeg')
    def formulaOrAndNeg(self, p):
        return p.formulaAndNeg

    @_('formulaAndNeg OR formulaOrAndNeg')
    def formulaOrAndNeg(self, p):
        return (p.formulaAndNeg, 'OR', p.formulaOrAndNeg)

    @_('formulaNeg')
    def formulaAndNeg(self, p):
        return p.formulaNeg

    @_('formulaNeg AND formulaAndNeg')
    def formulaAndNeg(self, p):
        return (p.formulaNeg, 'AND', p.formulaAndNeg)

    @_('formulaAtomica')
    def formulaNeg(self, p):
        return p.formulaAtomica

    @_('NOT formulaNeg')
    def formulaNeg(self, p):
        return ('NOT', p.formulaNeg)

    @_('TRUE')
    def formulaAtomica(self, p):
        return 'True'

    @_('FALSE')
    def formulaAtomica(self, p):
        return 'False'

    @_('LPAREN formula RPAREN')
    def formulaAtomica(self, p):
        return ('(', p.formula, ')')

    @_('expresion')
    def formulaAtomica(self, p):
        return p.expresion

    @_('expresion EQ expresion')
    def formulaAtomica(self, p):
        return (p[0], '==', p[1])

    @_('LOWERID')
    def expresion(self, p):
        return p.LOWERID

    @_('LOWERID LPAREN listaExpresiones RPAREN')
    def expresion(self, p):
        return (p.LOWERID, '(', p.listaExpresiones, ')')

    @_('UPPERID')
    def expresion(self, p):
        return p.UPPERID

    @_('UPPERID LPAREN listaExpresiones RPAREN')
    def expresion(self, p):
        return (p.UPPERID, '(', p.listaExpresiones, ')')

    @_('empty')
    def listaExpresiones(self, p):
        pass

    @_('listaExpresionesNoVacia')
    def listaExpresiones(self, p):
        return p.listaExpresionesNoVacia

    @_('expresion')
    def listaExpresionesNoVacia(self, p):
        return p.expresion

    @_('expresion COMMA listaExpresionesNoVacia')
    def listaExpresionesNoVacia(self, p):
        return (p.expresion, ',', p.listaExpresionesNoVacia)

    @_('')
    def empty(self, p):
        return []

if __name__ == '__main__':
    data = '''
    fun f
    fun g : x -> y
    fun h
        A -> B
    fun i : x -> y
        A -> B
    '''
    lexer = CalcLexer()
    parser = CalcParser()
    print(parser.parse(lexer.tokenize(data)))
