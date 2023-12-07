class Table:
    def __init__(self):
        self.symbols = []

    def getSymbol(self, identifier):
        for symbol in self.symbols:
            if symbol[0] == identifier:
                return symbol
        return False

    def setSymbol(self, identifier):
        symbol = self.getSymbol(identifier)
        #Se o simbolo não existir na tabela, então insere
        if symbol == False:
            self.symbols.append([identifier])

    def getType(self, identifier):
        symbol = self.getSymbol(identifier)
        #Se o símbolo existe e possui o tipo, então retorna o tipo
        if symbol and len(symbol) > 1:
            return symbol[1]
        return False

    def setType(self, identifier, primitiveType):
        symbol = self.getSymbol(identifier)
        #Se o tipo para o símbolo não foi definido, então atualiza
        if len(symbol) == 1:
            symbol.append(primitiveType)

    def export(self, filename):
        with open(filename, 'w') as archive:
            archive.write("Tabela de Simbolos\n")
            archive.write("{:<32} {:<10} \n".format("Nome", "Tipo"))
            archive.write("-" * 42 + "\n")
            for symbol in self.symbols:
                archive.write("{:<32} {:<10} \n".format(symbol[0], symbol[1]))
            print(f"Tabela de Símbolos exportada para '{filename}' com sucesso.")
        