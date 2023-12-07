from sintatico import Syntactic
from tabela import Table
import argparse

if __name__ == '__main__':
    print('Tradutor Toy \n')

    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=str, help='Informe o nome do arquivo para ser exportado')
    args = parser.parse_args()

    filename = input("Entre com o nome do arquivo: ")
    tableFileName = args.t
    table = Table()
    parser = Syntactic(table)
    response = parser.analyze(filename)
    if tableFileName is not None:
        table.export(tableFileName)
    if response:
        print("Arquivo sintaticamente correto.")
