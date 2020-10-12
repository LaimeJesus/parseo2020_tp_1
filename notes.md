

## Notas

Existen los siguientes generadores de parsers usando definiciones yacc(yet another compiler compiler)

- Java: 
    - [ANTLR4](https://github.com/antlr/antlr4)
- Python:
    - [PLY](https://github.com/dabeaz/ply)
    - [SLY](https://github.com/dabeaz/sly)
    - [Lark](https://github.com/lark-parser/lark)
- C++:
    - [flex/bison](https://www.geeksforgeeks.org/flex-fast-lexical-analyzer-generator/)

Links

- https://tomassetti.me/parsing-in-python/
    - herramientas de parseo y generadores de parsers
- https://tomassetti.me/guide-parsing-algorithms-terminology/
    - repaso general de parseo

### Símbolos del Lenguaje Avalancha

Declaraciones:
    fun     FUN
    check   CHECK

Operadores Lógicos
    imp     IMP
    and     AND
    or      OR
    not     NOT
    true    TRUE
    false   FALSE

Símbolos reservados
    Delimitadores
        Paréntesis Izquierdo    (    LPAREN
        Paréntesis Derecho      )    RPAREN
        Coma                    ,    COMMA
        Flecha                  ->   ARROW
    Expresiones
        Comodín                 _    UNDERSCORE
    Lenguaje de Verificación
        Dos puntos              :    COLON
        Signo de Interrogación  ?    QUESTION
        Signo de Exclamación    !    BANG
    Fórmulas
        Igualdad                ==   EQ

### Gramática del Lenguaje Avalancha

programa                -> declaraciones chequeos
declaraciones           -> _e 
                        | declaracion declaraciones
declaracion             -> FUN LOWERID signatura precondicion postcondicion reglas
signatura               -> _e 
                        | COLON listaParametros ARROW parametro
listaParametros         -> _e 
                        | listaParametrosNoVacia
listaParametrosNoVacia  -> parametro 
                        | parametro COMMA listaParametrosNoVacia
parametro               -> UNDERSCORE 
                        | LOWERID
reglas                  -> _e 
                        | regla reglas
regla                   -> listaPatrones ARROW expresion

listaPatrones           -> _e 
                        | listaPatronesNoVacia
listaPatronesNoVacia    -> patron 
                        | patron COMMA listaPatronesNoVacia

patron                  -> UNDERSCORE 
                        | LOWERID 
                        | UPPERID 
                        | UPPERID LPAREN listaPatrones RPAREN

precondicion            -> _e 
                        | QUESTION formula
postcondicion           -> _e 
                        | BANG formula

chequeos                -> _e 
                        | chequeo chequeos
chequeo                 -> CHECK formula

formula                 -> formulaImpOrAndNeg
formulaImpOrAndNeg     -> formulaOrAndNeg 
                        | formulaOrAndNeg IMP formulaImpOrAndNeg
formulaOrAndNeg        -> formulaAndNeg 
                        | formulaAndNeg OR formulaOrAndNeg
formulaAndNeg           -> formulaNeg 
                        | formulaNeg AND formulaAndNeg
formulaNeg             -> formulaAtomica 
                        | NOT formulaNeg
formulaAtomica          -> TRUE 
                        | FALSE 
                        | LPAREN formula RPAREN 
                        | expresion 
                        | expresion EQ expresion

expresion               -> LOWERID 
                        | LOWERID LPAREN listaExpresiones RPAREN 
                        | UPPERID 
                        | UPPERID LPAREN listaExpresiones RPAREN
listaExpresiones        -> _e 
                        | listaExpresionesNoVacia
listaExpresionesNoVacia -> expresion 
                        | expresion COMMA listaExpresionesNoVacia

