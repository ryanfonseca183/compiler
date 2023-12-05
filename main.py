from sintatico import Syntactic

if __name__ == '__main__':
    print('Tradutor Toy \n')

    # nome = input("Entre com o nome do arquivo: ")
    nome = 'parte2/testes/exemplo1.txt'
    parser = Syntactic()
    ok = parser.analyze(nome)
    if ok:
        print("Arquivo sintaticamente correto.")
