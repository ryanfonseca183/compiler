# Nome Discente: Ryan William Fonseca
# Matrícula: 0035165
# Data: 16/11/2023

# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias. 

# A classe Lexer tem por responsabilidade realizar a análise léxica do arquivo-fonte fornecido através da entrada,
# para a gramática da Linguagem Z. Para esse objetivo, foi definida a função getToken, que fará a leitura de um caractere por vez
# até formar os lexemas, e então atribuir uma classe definida em TypeToken. Caso nenhuma correspondência seja verificada,
# o analisador léxico retorna o Token de ERROR padrão

# Para implementação dos analisadores léxicos e sintáticos, foi consultado o material da Geovane Griesang, do
# departamento de informática da Universidade de Santa Cruz do Sul - UNISC, O link pode ser encontrado em:
# https://geovanegriesang.files.wordpress.com/2015/04/compiladores_01_introduc3a7c3a3o.pdf 
# Além disso, foi consultado o material disponibilizado no ambiente Google Classroom, no decorrer da disciplina. 

from os import path
import re

# Classe que define todos as classes de tokens possíveis para a linguagem Z
class TypeToken:
    ID = (1, 'ID')
    READ = (2, 'READ')
    WRITE = (3, 'WRITE')
    CTE = (4, 'CONSTANTE')
    CADEIA = (5, 'CADEIA')
    ATRIB = (6, '=')
    OPREL = (7, 'RELACIONAL')
    OPAD = (8, 'ADIÇÃO')
    OPMUL = (9, '*')
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

# Classe modelo para Tokens
class Token:
    def __init__(self, typeToken, lexeme, line):
        (const, label) = typeToken
        self.type = typeToken
        self.lexeme = lexeme
        self.const = const
        self.label = label
        self.line = line

class Lexer:
    # Enumerador de palavras reservadas
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

    def __init__(self, fileName, table):
        self.fileName = fileName
        self.file = None
        self.table = table
        self.identifiersWithMissingType = []
        self.functionKeywordWasRead = False

    # Abre o arquivo, se existir e não estiver fechado
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

    # Fecha o arquivo, se aberto
    def closeFile(self):
        if self.file is None:
            print('ERROR: File is already close')
            quit()
        self.file.close()

    # Obtem o próximo caractere do arquivo-fonte, caso o buffer esteja vazio
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

    # Devolve o caractere lido para o buffer, para que seja novamente lido na próxima chamada de getChar()
    def ungetChar(self, c):
        if not c is None:
            self.buffer = self.buffer + c

    # Maquina de estados responsável por classificar os tokens, conforme os aspectos léxicos da linguagem
    def getToken(self):
        lexeme = ''
        state = 1
        char = None
        while (True):
            # Estado 1 elimina os espaços, quebras de linha e tabulação e realiza a mudança para outros estados 
            if state == 1:
                char = self.getChar()
                if char is None:
                    return Token(TypeToken.EOF, 'EOF', self.line)
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
                    return Token(TypeToken.ERROR, char, self.line)
            # Estado 2 classifica os lexemas em identificadores
            elif state == 2:
                lexeme = lexeme + char
                # Verifica se o identificador não atingiu o limite de 32 caracteres definidos
                if len(lexeme) > 32:
                    return Token(TypeToken.ERROR, lexeme, self.line)
                char = self.getChar()
                # Verifica se o caractere lido está na forma de letra do alfabeto ou número decimal
                if char is None or (not re.match('^[A-Za-z0-9]+$', char)):
                    self.ungetChar(char)
                    # Verifica se o identificador formado não corresponde a uma palavra reservada
                    if lexeme in Lexer.reservedWords:
                        self.functionKeywordWasRead = lexeme == 'program'
                        if(lexeme in ('real', 'bool', 'char', 'int')):
                            for identifier in self.identifiersWithMissingType:
                                self.table.setType(identifier, lexeme)
                            self.identifiersWithMissingType = []
                        return Token(Lexer.reservedWords[lexeme], lexeme, self.line)
                    else:
                        if not self.table.getType(lexeme):
                            if not self.functionKeywordWasRead:
                                self.identifiersWithMissingType.append(lexeme)
                            self.functionKeywordWasRead = False
                            self.table.setSymbol(lexeme)
                        return Token(TypeToken.ID, lexeme, self.line)
            # Estado 3 classifica os lexemas que podem estar na forma de números inteiros e reais, em constantes
            elif state == 3:
                lexeme = lexeme + char
                char = self.getChar()
                # Realiza a validação específica para números reais do ponto flutuante
                if char == ".":
                    if "." in lexeme:
                        return Token(TypeToken.ERROR, lexeme, self.line)
                    continue
                if char is None or (not char.isdigit()):
                    self.ungetChar(char)
                    return Token(TypeToken.CTE, lexeme, self.line)
            # Estado 4 classifica os lexemas que estejam entre aspas duplas em cadeias de caracteres
            elif state == 4:
                if char != '"':
                    lexeme = lexeme + char
                char = self.getChar()
                if char == '\n':
                    self.ungetChar(char)
                    state = 1
                    return Token(TypeToken.ERROR, lexeme, self.line)
                if char == '"':
                    if len(lexeme) > 0:
                        return Token(TypeToken.CADEIA, lexeme, self.line)
                    else:
                        state = 1
            # Estado 5 classifica os demais tokens de estrutura simples, como operadores, parenteses e outros
            elif state == 5:
                lexeme = lexeme + char
                # Identifica os operadores relacionais, bem como o operador de atribuição
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
                    return Token(TypeToken.OPMUL, lexeme, self.line)
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
            # Estado 6 é responsável por realizar ignorar os comentários em linha ou bloco
            elif state == 6:
                nextChar = self.getChar()
                if nextChar == '\n':
                    return Token(TypeToken.ERROR, char, self.line)
                # Remove comentários em linha
                if nextChar == '/':
                    while (char is not None) and (char != '\n'):
                        char = self.getChar()
                    self.ungetChar(char)
                # Remove comentários em bloco
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
    fileName = input("Informe o caminho do arquivo: ")
    lexer = Lexer(fileName)
    lexer.openFile()
    while(True):
       token = lexer.getToken()
       print("token = %s \nlexeme = %s \nline = %d \n" % (token.label, token.lexeme, token.line))
       if token.const == TypeToken.EOF[0]:
           break
    lexer.closeFile()
