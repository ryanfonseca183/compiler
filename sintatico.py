from lexico import TypeToken, Token, Lexer

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
        self.consume(TypeToken.EOF)
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


if __name__== "__main__":
   #nome = input("Entre com o nome do arquivo: ")
   fileName = 'exemplo.toy'
   parser = Syntactic()
   parser.analyze(fileName)
