from os import path
import re

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
        'program': TypeToken.PROGRAM,
        'VAR': TypeToken.VAR,
        'int': TypeToken.INT,
        'real': TypeToken.REAL,
        'bool': TypeToken.BOOL,
        'char': TypeToken.CHAR,
        'if': TypeToken.IF,
        'else': TypeToken.ELSE,
        'while': TypeToken.WHILE,
        'read': TypeToken.READ,
        'write': TypeToken.WRITE,
        'false': TypeToken.FALSE,
        'true': TypeToken.TRUE
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
                        self.line += 1
                elif re.match('^[A-Za-z]+$', char):
                    state = 2
                elif char.isdigit():
                    state = 3
                elif char == '"':
                    state = 4
                elif char in {'=', ';', ',', ':', '+', '-', '*', '!', '(', ')', '{', '}', '=', '<', '>'}:
                    state = 5
                elif char == '/':
                    state = 6
                else:
                    return Token(TypeToken.ERROR, '<' + char + '>', self.line)
            elif state == 2:
                #IDENTIFICADORES
                lexeme = lexeme + char
                if len(lexeme) > 32:
                    return Token(TypeToken.ERROR, '<' + lexeme + '>', self.line)
                char = self.getChar()
                if char is None or (not re.match('^[A-Za-z0-9]+$', char)):
                    self.ungetChar(char)
                    if lexeme in Lexer.reservedWords:
                        return Token(Lexer.reservedWords[lexeme], lexeme, self.line)
                    else:
                        return Token(TypeToken.ID, lexeme, self.line)
            elif state == 3:
                #CONSTANTES NUMÉRICAS REAIS/INTEIRAS
                lexeme = lexeme + char
                char = self.getChar()
                if char == ".":
                    if "." in lexeme:
                        return Token(TypeToken.ERROR, '<' + lexeme + '>', self.line)
                    continue
                if char is None or (not char.isdigit()):
                    self.ungetChar(char)
                    return Token(TypeToken.CTE, lexeme, self.line)
            elif state == 4:
                #CADEIAS DE CARACTERES
                if char != '"':
                    lexeme = lexeme + char
                char = self.getChar()
                if char == '\n':
                    self.ungetChar(char)
                    state = 1
                    return Token(TypeToken.ERROR, '<' + lexeme + '>', self.line)
                if char == '"':
                    if len(lexeme) > 0:
                        return Token(TypeToken.CADEIA, lexeme, self.line)
                    else:
                        state = 1
            elif state == 5:
                #DEMAIS CLASSES DE TOKENS
                lexeme = lexeme + char
                if char in {'=', '<', '>'}:
                    nextChar = self.getChar()
                    if nextChar == '=' or (char == '<' and nextChar == '>'):
                        lexeme = lexeme + nextChar
                    else:
                        self.ungetChar(nextChar)
                        if char == '=':
                            return Token(TypeToken.ATRIB, lexeme, self.line)
                    return Token(TypeToken.OPREL, lexeme, self.line)
                elif char == ';':
                    return Token(TypeToken.PVIRG, lexeme, self.line)
                elif char == ':':
                    return Token(TypeToken.DPONTOS, lexeme, self.line)
                elif char == ',':
                    return Token(TypeToken.VIRG, lexeme, self.line)
                elif char in {'+', '-'}:
                    return Token(TypeToken.OPAD, lexeme, self.line)
                elif char == '*':
                    return Token(TypeToken.OPMULT, lexeme, self.line)
                elif char == '!':
                    return Token(TypeToken.OPNEG, lexeme, self.line)
                elif char == '(':
                    return Token(TypeToken.ABREPAR, lexeme, self.line)
                elif char == ')':
                    return Token(TypeToken.FECHAPAR, lexeme, self.line)
                elif char == '{':
                    return Token(TypeToken.ABRECH, lexeme, self.line)
                elif char == '}':
                    return Token(TypeToken.FECHACH, lexeme, self.line)
            elif state == 6:
                # COMENTÁRIOS
                nextChar = self.getChar()
                if nextChar == '\n':
                    return Token(TypeToken.ERROR, '<' + char + '>', self.line)
                # REMOVE COMENTÁRIOS DE LINHA
                if nextChar == '/':
                    while (char is not None) and (char != '\n'):
                        char = self.getChar()
                    self.ungetChar(char)
                # REMOVE COMENTÁRIOS DE MULTIPLAS LINHAS
                if nextChar == '*':
                    while (char is not None):
                        char = self.getChar()
                        if char == '\n':
                            self.line += 1
                        if char == '*':
                            nextChar = self.getChar()
                            if nextChar == '/':
                                break
                state = 1

if __name__== "__main__":
    lex = Lexer('exemplos/exemplo5.txt')
    lex.openFile()
    while(True):
       token = lex.getToken()
       print("token= %s , lexeme= (%s), line= %d" % (token.label, token.lexeme, token.line))
       if token.const == TypeToken.EOF[0]:
           break
    lex.closeFile()
