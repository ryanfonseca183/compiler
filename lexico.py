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

class Lexer:
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = None

    def openFile(self):
        if not self.file is None:
            print('ERROR: File is already open')
            quit()
        elif not path.exists(self.fileName):
            print('ERROR: File "%s" does not exists.' % self.fileName)
            quit()
        self.file = open(self.fileName, "r")
        self.buffer = ''
        self.line = 1

    def closeFile(self):
        if self.file is None:
            print('ERROR: File is already close')
            quit()
        self.file.close()

    def getChar(self):
        if self.file is None:
            print('ERROR: There\'s no open file')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            return c
        else:
            c = self.file.read(1)
            return None if len(c) == 0 else c

    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

if __name__== "__main__":
    lex = Lexer('exemplo.toy')
    lex.openFile()
    print(lex.getChar())
    print(lex.getChar())
    c = lex.getChar()
    print(c)
    lex.ungetChar(c)
    print(lex.getChar())
    lex.closeFile()
