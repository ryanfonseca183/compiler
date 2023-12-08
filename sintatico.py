# Nome Discente: Ryan William Fonseca
# Matrícula: 0035165
# Data: 16/11/2023

# Declaro que sou o único autor e responsável por este programa. Todas as partes do programa, exceto as que foram fornecidas
# pelo professor ou copiadas do livro ou das bibliotecas de Aho et al., foram desenvolvidas por mim. Declaro também que
# sou responsável por todas  as eventuais cópias deste programa e que não distribui nem facilitei a distribuição de cópias. 

# A classe Syntactic tem por responsabilidade realizar a análise sintática do arquivo-fonte fornecido através da entrada,
# para a gramática da Linguagem Z. Para esse objetivo, foi definida a função analyze, que inicia o processo de análise
# abrindo o arquivo e chamando a regra de partida da gramática. Em seguida, o analisador sintático faz chamadas ao analisador
# léxico que irá retornar Tokens classificando cada lexema encontrado no código-fonte. Com base nos tokens, o analisador sintático
# irá comparar se o que o léxico retornou está de acordo com as regras de produção da gramática Z. Em caso positivo, a análise
# prossegue até que o fim do arquivo seja encontrado. Em caso negativo, o programa gera uma mensagem de erro de sintaxe e finaliza
# a execução. As regras de derivação, por sua vez, tomaram forma de funções que irão consumir os tokens e chamar umas as outras.

# Para implementação dos analisadores léxicos e sintáticos, foi consultado o material da Geovane Griesang, do
# departamento de informática da Universidade de Santa Cruz do Sul - UNISC, O link pode ser encontrado em:
# https://geovanegriesang.files.wordpress.com/2015/04/compiladores_01_introduc3a7c3a3o.pdf 
# Além disso, foi consultado o material disponibilizado no ambiente Google Classroom, no decorrer da disciplina. 

from lexico import TypeToken as Type, Token, Lexer

class Syntactic:

    def __init__(self, table):
        self.debug = True
        self.lexer = None
        self.currentToken = None
        self.error = False
        self.panic = False
        self.table = table
        self.sincronismToken = [Type.PVIRG, Type.EOF, Type.ABRECH, Type.FECHACH, Type.ABREPAR, Type.FECHAPAR, Type.IF, Type.ELSE, Type.DPONTOS, Type.WHILE, Type.INT, Type.REAL, Type.BOOL, Type.CHAR, Type.WRITE, Type.READ]

    # Inicia o processo de análise, com a regra de partida da gramática
    def analyze(self, fileName):
        if self.lexer is not None:
            print('ERROR: File is already being processed')
            quit()
        self.lexer = Lexer(fileName, self.table)
        self.lexer.openFile()
        self.currentToken = self.lexer.getToken()
        self.PROG()
        self.consume(Type.EOF)
        self.lexer.closeFile()
        return self.error

    # Verifica se o token atual, é igual ao token esperado
    def currentEqualTo(self, token):
        return self.currentToken.const == token[0]
    
    # Verifica se o token atual está entre os tokens esperados
    def currentIn(self, *tokens):
        for token in tokens:
            if self.currentToken.const == token[0]:
                return 1
        return 0

    # Obtem o próximo token, caso o token atual seja igual ao esperado
    def consume(self, token = None):
        if token and self.currentEqualTo(token):
            self.currentToken = self.lexer.getToken()
        else:
            self.panic = True
            self.error = True
            if token: 
                print('[Line %d] Syntax Error: "%s" was expected but received "%s"' % (
                    self.currentToken.line, token[1], self.currentToken.lexeme
                ))
            else: 
                print('[Line %d] Syntax Error: Unexpected "%s" ' % (self.currentToken.line, self.currentToken.lexeme))
                self.currentToken = self.lexer.getToken()

            while self.panic:
                if self.currentIn(*self.sincronismToken):
                    self.panic = False
                    break
                self.currentToken = self.lexer.getToken()

    # As funções a seguir definem cada uma das regras de derivação da linguagem
    def PROG(self):
        self.debug and print('PROG')
        self.consume(Type.PROGRAM)
        self.consume(Type.ID)
        self.consume(Type.PVIRG)
        self.DECLS()
        self.C_COMP()
    
    def DECLS(self):
        self.debug and print('DECLS')
        if self.currentEqualTo(Type.VAR):
            self.consume(Type.VAR)
            self.LIST_DECLS()
    
    def LIST_DECLS(self):
        self.debug and print('LIST_DECLS')
        self.DECL_TIPO()
        self.D()

    def DECL_TIPO(self):
        self.debug and print('DECL_TIPO')
        self.LIST_ID()
        self.consume(Type.DPONTOS)
        self.TIPO()
        self.consume(Type.PVIRG)

    def D(self):
        self.debug and print('D')
        if self.currentEqualTo(Type.ID):
            self.LIST_DECLS()

    def LIST_ID(self):
        self.debug and print('LIST_ID')
        self.consume(Type.ID)
        self.E()

    def TIPO(self):
        self.debug and print('TIPO')
        if self.currentEqualTo(Type.INT): 
            self.consume(Type.INT)
        elif self.currentEqualTo(Type.REAL): 
            self.consume(Type.REAL)
        elif self.currentEqualTo(Type.BOOL): 
            self.consume(Type.BOOL)
        elif self.currentEqualTo(Type.CHAR):
            self.consume(Type.CHAR)
        else:
            self.consume(Type.TIPO)

    def E(self):
        self.debug and print('E')
        if self.currentEqualTo(Type.VIRG):
            self.consume(Type.VIRG)
            self.LIST_ID()
        
    def C_COMP(self):
        self.debug and print('C_COMP')
        self.consume(Type.ABRECH)
        self.LISTA_COMANDOS()
        self.consume(Type.FECHACH)

    def LISTA_COMANDOS(self):
        self.debug and print('LISTA_COMANDOS')
        self.COMANDOS()
        self.G()
    
    def COMANDOS(self):
        self.debug and print('COMANDOS')
        if (self.currentEqualTo(Type.ID)): 
            self.ATRIBUICAO()
        elif (self.currentEqualTo(Type.IF)):
            self.SE()
        elif (self.currentEqualTo(Type.WHILE)):
            self.ENQUANTO()
        elif (self.currentEqualTo(Type.READ)):
            self.LEIA()
        elif (self.currentEqualTo(Type.WRITE)):
            self.ESCREVA()

    def ATRIBUICAO(self):
        self.debug and print('ATRIBUICAO')
        self.consume(Type.ID)
        self.consume(Type.ATRIB)
        #Se não reconheceu o operador de atribuição e o proximo for PVIRG, então consome
        if(self.currentEqualTo(Type.PVIRG)):
            self.consume(Type.PVIRG)
            return
        self.EXPR()
        if self.currentEqualTo(Type.PVIRG):
            self.consume(Type.PVIRG)
        else:
            print('[Line %d] Syntax Error: "%s" was expected but received "%s"' % (
                self.currentToken.line, ';', self.currentToken.lexeme
            ))

    def EXPR(self):
        self.debug and print('EXPR')
        self.SIMPLES()
        self.P()

    def SIMPLES(self):
        self.debug and print('SIMPLES')
        self.TERMO()
        self.R()
    
    def P(self):
        self.debug and print('P')
        if(self.currentEqualTo(Type.OPREL)):
            self.consume(Type.OPREL)
            self.SIMPLES()

    def TERMO(self):
        self.debug and print('TERMO')
        self.FAT()
        self.S()
    
    def R(self):
        self.debug and print('R')
        if(self.currentEqualTo(Type.OPAD)):
            self.consume(Type.OPAD)
            self.SIMPLES()

    def FAT(self):
        self.debug and print('FAT')
        if(self.currentEqualTo(Type.ID)):
            self.consume(Type.ID)
        elif (self.currentEqualTo(Type.CTE)):
            self.consume(Type.CTE)
        elif (self.currentEqualTo(Type.ABREPAR)):
            self.consume(Type.ABREPAR)
            self.EXPR()
            self.consume(Type.FECHAPAR)
        elif (self.currentEqualTo(Type.TRUE)):
            self.consume(Type.TRUE)
        elif (self.currentEqualTo(Type.FALSE)):
            self.consume(Type.FALSE)
        elif (self.currentEqualTo(Type.OPNEG)):
            self.consume(Type.OPNEG)
            self.FAT()
        else:
            self.consume()

    def S(self):
        self.debug and print('S')
        if(self.currentEqualTo(Type.OPMUL)):
            self.consume(Type.OPMUL)
            self.TERMO()

    def SE(self):
        self.debug and print('SE')
        self.consume(Type.IF)
        self.consume(Type.ABREPAR)
        self.EXPR()
        self.consume(Type.FECHAPAR)
        self.C_COMP()
        self.H()

    def H(self):
        self.debug and print('H')
        if self.currentEqualTo(Type.ELSE):
            self.consume(Type.ELSE)
            self.C_COMP()

    def ENQUANTO(self):
        self.debug and print('ENQUANTO')
        self.consume(Type.WHILE)
        self.consume(Type.ABREPAR)
        self.EXPR()
        self.consume(Type.FECHAPAR)
        self.C_COMP()

    def LEIA(self):
        self.debug and print('LEIA')
        self.consume(Type.READ)
        self.consume(Type.ABREPAR)
        self.LIST_ID()
        self.consume(Type.FECHAPAR)
        self.consume(Type.PVIRG)

    def ESCREVA(self):
        self.debug and print('ESCREVA')
        self.consume(Type.WRITE)
        self.consume(Type.ABREPAR)
        self.LIST_W()
        self.consume(Type.FECHAPAR)
        self.consume(Type.PVIRG)

    def LIST_W(self):
        self.debug and print('LIST_W')
        self.ELEM_W()
        self.L()

    def ELEM_W(self):
        self.debug and print('ELEM_W')
        if (self.currentEqualTo(Type.CADEIA)):
            self.consume(Type.CADEIA)
        elif (self.currentIn(Type.ID, Type.ABREPAR, Type.CTE, Type.TRUE, Type.FALSE, Type.OPNEG)):
            self.EXPR()
        else:
            self.consume()
        
    def L(self):
        self.debug and print('L')
        if self.currentEqualTo(Type.VIRG):
            self.consume(Type.VIRG)
            self.LIST_W()

    def G(self):
        self.debug and print('G')
        if(self.currentIn(Type.ID, Type.IF, Type.WHILE, Type.READ, Type.WRITE)):
            self.LISTA_COMANDOS()

if __name__== "__main__":
   fileName = input("Informe o caminho do arquivo: ")
   parser = Syntactic()
   parser.analyze(fileName)
