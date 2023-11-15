from os import path

class TypeToken:
    ID = (1, 'ID')
    READ = (2, 'READ')
    WRITE = (3, 'WRITE')
    CTE = (4, 'CONSTANTE')
    CADEIA = (5, 'CADEIA')
    ATRIB = (6, '=')
    OPREL = (7, 'RELACIONAL')
    OPAD = (8, 'ADIÇÃO')
    OPMULT = (9, '*')
    OPNEG = (10, '!')
    PVIRG = (11, ';')
    DPONTOS = (12, ':')
    VIRG = (13, ',')
    ABREPAR = (14, '(')
    FECHAPAR = (15, ')')
    ABRECH = (16, '{')
    FECHACH = (17, '}')
    ERROR = (18, 'ERROR')
    EOF = (19, 'END OF FILE')
    PROGRAM = (20, 'PROGRAM')
    VAR = (21, 'VAR')
    INT = (22, 'INT')
    REAL = (23, 'REAL')
    CHAR = (24, 'CHAR')
    IF = (25, 'IF')
    ELSE = (26, 'ELSE')
    WHILE = (27, 'WHILE')
    READ = (28, 'READ')
    FALSE = (29, 'FALSE')
    TRUE = (30, 'TRUE')

class Token:
    def __init__(self, typeToken, lexeme, line):
        (const, label) = typeToken
        self.type = typeToken
        self.lexeme = lexeme
        self.const = const
        self.label = label
        self.line = line

if __name__== "__main__":
    print(token.const, token.label, token.lexeme)
