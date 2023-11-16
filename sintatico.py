from lexico import TypeToken as Type, Token, Lexer

class Syntactic:

    def __init__(self):
        self.lexer = None
        self.currentToken = None

    def analyze(self, fileName):
        if self.lexer is not None:
            print('ERROR: File is already being processed')
            quit()
        self.lexer = Lexer(fileName)
        self.lexer.openFile()
        self.currentToken = self.lexer.getToken()
        self.PROG()
        self.C_COMP()
        self.consume(Type.EOF)
        self.lexer.closeFile()

    def currentEqualTo(self, token):
        return self.currentToken.const == token[0]

    def consume(self, token):
        if not self.currentEqualTo(token):
            print('[Line %d] Syntax Error: "%s" was expected but received "%s"' % (
                self.currentToken.line, token[1], self.currentToken.lexeme
            ))
            quit()
        self.currentToken = self.lexer.getToken()

    def PROG(self):
        self.consume(Type.PROGRAM)
        self.consume(Type.ID)
        self.consume(Type.PVIRG)
        self.DECLS()

    def C_COMP(self):
        print('ccomp')

    def DECLS(self):
        if self.currentEqualTo(Type.VAR):
            self.consume(Type.VAR)
            self.LIST_DECLS()
    
    def LIST_DECLS(self):
        self.DECL_TIPO()
        self.D()

    def DECL_TIPO(self):
        self.LIST_ID()
        self.consume(Type.DPONTOS)
        self.TIPO()
        self.consume(Type.PVIRG)

    def D(self):
        if self.currentEqualTo(Type.ID):
            self.LIST_DECLS()

    def LIST_ID(self):
        self.consume(Type.ID)
        self.E()

    def TIPO(self):
        if self.currentEqualTo(Type.INT): 
            self.consume(Type.INT)
        elif self.currentEqualTo(Type.REAL): 
            self.consume(Type.REAL)
        elif self.currentEqualTo(Type.BOOL): 
            self.consume(Type.BOOL)
        else:
            self.consume(Type.CHAR)

    def E(self):
        if self.currentEqualTo(Type.VIRG):
            self.consume(Type.VIRG)
            self.LIST_ID()



if __name__== "__main__":
   #nome = input("Entre com o nome do arquivo: ")
   fileName = 'exemplos/exemplo1.txt'
   parser = Syntactic()
   parser.analyze(fileName)
