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

    def __init__(self):
        self.lexer = None
        self.currentToken = None

    # Inicia o processo de análise, com a regra de partida da gramática
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

    # Verifica se o token atual, é igual ao token esperado
    def currentEqualTo(self, token):
        return self.currentToken.const == token[0]
    
    # Verifica se o token atual está entre os tokens esperados
    def currentIn(self, *tokens):
        for token in tokens:
            if self.currentToken.const == token[0]:
                return 1
        return 0

    # Exibe um erro de sintaxe padrão e encerra a execução do programa
    def syntaxError(self):
        print('[Line %d] Syntax Error: Unexpected "%s"' % (
            self.currentToken.line, self.currentToken.lexeme
        ))
        quit()

    # Obtem o próximo token, caso o token atual seja igual ao esperado
    def consume(self, token):
        if not self.currentEqualTo(token):
            print('[Line %d] Syntax Error: "%s" was expected but received "%s"' % (
                self.currentToken.line, token[1], self.currentToken.lexeme
            ))
            quit()
        self.currentToken = self.lexer.getToken()

    # As funções a seguir definem cada uma das regras de derivação da linguagem
    def PROG(self):
        self.consume(Type.PROGRAM)
        self.consume(Type.ID)
        self.consume(Type.PVIRG)
        self.DECLS()
    
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
        elif self.currentEqualTo(Type.CHAR):
            self.consume(Type.CHAR)
        else:
            self.syntaxError()

    def E(self):
        if self.currentEqualTo(Type.VIRG):
            self.consume(Type.VIRG)
            self.LIST_ID()
        
    def C_COMP(self):
        self.consume(Type.ABRECH)
        self.LISTA_COMANDOS()
        self.consume(Type.FECHACH)

    def LISTA_COMANDOS(self):
        self.COMANDOS()
        self.G()
    
    def COMANDOS(self):
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
        else:
            self.syntaxError()

    def ATRIBUICAO(self):
        self.consume(Type.ID)
        self.consume(Type.ATRIB)
        self.EXPR()
        self.consume(Type.PVIRG)

    def EXPR(self):
        self.SIMPLES()
        self.P()

    def SIMPLES(self):
        self.TERMO()
        self.R()
    
    def P(self):
        if(self.currentEqualTo(Type.OPREL)):
            self.consume(Type.OPREL)
            self.SIMPLES()

    def TERMO(self):
        self.FAT()
        self.S()
    
    def R(self):
        if(self.currentEqualTo(Type.OPAD)):
            self.consume(Type.OPAD)
            self.SIMPLES()

    def FAT(self):
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
            self.syntaxError()

    def S(self):
        if(self.currentEqualTo(Type.OPMUL)):
            self.consume(Type.OPMUL)
            self.TERMO()

    def SE(self):
        self.consume(Type.IF)
        self.consume(Type.ABREPAR)
        self.EXPR()
        self.consume(Type.FECHAPAR)
        self.C_COMP()
        self.H()

    def H(self):
        if self.currentEqualTo(Type.ELSE):
            self.consume(Type.ELSE)
            self.C_COMP()

    def ENQUANTO(self):
        self.consume(Type.WHILE)
        self.consume(Type.ABREPAR)
        self.EXPR()
        self.consume(Type.FECHAPAR)
        self.C_COMP()

    def LEIA(self):
        self.consume(Type.READ)
        self.consume(Type.ABREPAR)
        self.LIST_ID()
        self.consume(Type.FECHAPAR)
        self.consume(Type.PVIRG)

    def ESCREVA(self):
        self.consume(Type.WRITE)
        self.consume(Type.ABREPAR)
        self.LIST_W()
        self.consume(Type.FECHAPAR)
        self.consume(Type.PVIRG)

    def LIST_W(self):
        self.ELEM_W()
        self.L()

    def ELEM_W(self):
        if (self.currentEqualTo(Type.CADEIA)):
            self.consume(Type.CADEIA)
        elif (self.currentIn(Type.ID, Type.ABREPAR, Type.CTE, Type.TRUE, Type.FALSE, Type.OPNEG)):
            self.EXPR()
        else:
            self.syntaxError()

    def L(self):
        if self.currentEqualTo(Type.VIRG):
            self.consume(Type.VIRG)
            self.LIST_W()

    def G(self):
        if(self.currentIn(Type.ID, Type.IF, Type.WHILE, Type.READ, Type.WRITE)):
            self.LISTA_COMANDOS()

if __name__== "__main__":
   fileName = input("Informe o caminho do arquivo: ")
   parser = Syntactic()
   parser.analyze(fileName)
