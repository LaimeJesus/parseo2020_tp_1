# Repositorio del TP 1 de la materia Parseo y Generación de Código, Universidad Nacional de Quilmes 2020

Utilizamos el programa [SLY](https://github.com/dabeaz/sly) para implementar el parser y lexer de la gramática pedida.

## Instrucciones

Este repositorio contiene los siguientes archivos

- `parser.py`: ejecutable python que contiene el lexer **AvalanchaLexer** y el parser **AvalanchaParser**
- los scripts:
    - `test_all.sh`, ejecuta el parser con todos los archivos de prueba compartidos
    - `test_all_rules.sh`, ejecuta el parser con casos de prueba sobre las restricciones
    - `test_parser.sh`, ejecuta el parser sobre un archivo en particular

## Instalación

Se necesita instalar **SLY** y **Python 3.6 >=**, para esto vamos a instalar dos dependencias [**pyenv**](https://github.com/pyenv/pyenv) y [**pipenv**](https://pypi.org/project/pipenv/).
Una vez instalados, instalamos la versión python 3.7 de Python con pyenv
- `pyenv install 3.7`
Luego, en la raíz del repositorio generamos un entorno virtual utilizando la versión 3.7 de Python
- `pipenv --python 3.7`
Inicializamos el entorno virtual
- `pipenv shell`
Finalmente instalamos las dependencias
- `pipenv install`

## Pruebas

Se pueden utilizar los scripts generados para realizar las pruebas del parser, por ejemplo:
Probar todos los casos de prueba.
- `./test_all.sh`
También, se puede probar el parser con un input en particular
- `python parser.py tests_parser/test00.input`

## Referencias
- Trabajo Práctico: https://unqpgc.github.io/files/2020s2/tp1.pdf
- Pyenv installer: https://github.com/pyenv/pyenv-installer
