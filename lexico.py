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
    BOOL = (24, 'BOOL')
    CHAR = (25, 'CHAR')
    IF = (26, 'IF')
    ELSE = (27, 'ELSE')
    WHILE = (28, 'WHILE')
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
    reservedWords = {
        'PROGRAM': TypeToken.PROGRAM,
        'VAR': TypeToken.VAR,
        'INT': TypeToken.INT,
        'REAL': TypeToken.REAL,
        'BOOL': TypeToken.BOOL,
        'CHAR': TypeToken.CHAR,
        'IF': TypeToken.IF,
        'ELSE': TypeToken.ELSE,
        'WHILE': TypeToken.WHILE,
        'READ': TypeToken.READ,
        'WRITE': TypeToken.WRITE,
        'FALSE': TypeToken.FALSE,
        'TRUE': TypeToken.TRUE
    }

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

    def getToken(self):
        lexeme = ''
        state = 1
        char = None
        while (True):
            if state == 1:
                char = self.getChar()
                if char is None:
                    return Token(TypeToken.EOF, '<eof>', self.line)
                elif char in {' ', '\t', '\n'}:
                    if char == '\n':
                        self.line = self.line + 1
                elif char.isalpha():
                    state = 2
                elif char.isdigit():
                    state = 3
                elif char == '#':
                    state = 5
                else:
                    return Token(TypeToken.ERROR, '<' + char + '>', self.line)
            elif state == 2:
                lexeme = lexeme + char
                if len(lexeme) > 32:
                    return Token(TypeToken.ERROR, '<' + lexeme + '>', self.line)
                char = self.getChar()
                if char is None or (not char.isalnum()):
                    self.ungetChar(char)
                    if lexeme in Lexer.reservedWords:
                        return Token(Lexer.reservedWords[lexeme], lexeme, self.line)
                    else:
                        return Token(TypeToken.ID, lexeme, self.line)
            elif state == 3:
                lexeme = lexeme + char
                char = self.getChar()
                if char is None or (not char.isdigit()):
                    self.ungetChar(char)
                    return Token(TypeToken.CTE, lexeme, self.line)
            elif state == 5:
                # consumindo comentario
                while (not char is None) and (char != '\n'):
                    char = self.getChar()
                self.ungetChar(char)
                state = 1

if __name__== "__main__":
    lex = Lexer('exemplo.toy')
    lex.openFile()
    while(True):
       token = lex.getToken()
       print("token= %s , lexema= (%s), linha= %d" % (token.label, token.lexeme, token.line))
       if token.const == TypeToken.EOF[0]:
           break
    lex.closeFile()
