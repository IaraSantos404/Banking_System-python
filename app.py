from abc import ABC, abstractmethod
from datetime import datetime


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass
        
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    def registrar(self, conta):
        if self._valor > 0:
            conta._saldo += self._valor
            conta._historico.adicionar_transacao(f"Depósito de R${self._valor:.2f}\n")
            print("Valor depositado com sucesso!")
        else:
            print("Valor inválido!")

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    def registrar(self, conta):
        if conta.quant_saque < conta.max_saque:
            if self._valor <= 0:
                print("Valor inválido!")
            elif self._valor > conta.limite_saque:
                print("Operação inválida! O valor limite de saque é de R$500,00")
            elif conta._saldo >= self._valor:
                conta._saldo -= self._valor
                conta._historico.adicionar_transacao(f"Saque de R${self._valor:.2f}\n")
                print("Saque realizado com sucesso!")
                conta.quant_saque += 1
            else:
                print("Saldo insuficiente!")
        else:
            print("Você já realizou os 3 saques diários")


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self.quant_saque = 0
        self.max_saque = 3
        self.limite_saque = 500
        self._historico = Historico()
        
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)
        
    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)
    
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque

class Cliente:
    def __init__(self, nome, cpf):
        self._nome = nome
        self._cpf = cpf
        self._contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self._contas.append(conta)
    
class PessoaFisica(Cliente):
    def __init__(self, endereco, nome, cpf, data_nascimento):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        


def menu():
    menu = """
    Bem vindo(a)! digite a opção da operação que deseja realizar:

    [1] Deposito
    [2] Saque
    [3] Ver extrato
    [4] Criar Conta
    [5] Criar usuário
    [6] Listar contas
    [7] Sair

    => """
    
    return input(menu)


def exibir_extrato(conta: Conta):
    print("========== SEU EXTRATO ==========")
    print("Ainda não há nada no extrato " if not conta._historico.transacoes else ''.join(conta.historico.transacoes))
    print(f"\nSaldo atual: R${conta._saldo:.2f}")



def cadastra_usuario(usuarios):
    nome = input("Digite seu nome: ")
    cpf = input("Digite seu CPF: ")
    usuario = Cliente(nome, cpf)
    usuarios.append(usuario)
    print("Usuário cadastrado com sucesso!")
    # cpf = input("Digite seu CPF: ")
    # usuario = verifica_usuario(cpf, usuarios)
    
    # if usuario:
    #     print("já existe um usuário cadastrado com esse CPF! ")
    # else:
    #     nome = input("Digite seu nome completo: ")
    #     data_nasci = input("Digite sua data de nascimento no formato ddd/mm/aaaa: ")
    #     # endereco = input("E seu endereço(numero, logradouro, bairro, cidade/sigla do estado): ")
        
    #     usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nasci})
    #     print("Usuário cadastrado com sucesso! ")

def verifica_usuario(cpf, usuarios):
    # usuarios_filtrados = []
    for usuario in usuarios:
        if usuario._cpf == cpf:
            return usuario
    
    return None

def criar_conta(agencia, num_conta, usuarios):
    cpf = input("Digite seu CPF: ")
    usuario = verifica_usuario(cpf, usuarios)
    
    if usuario:
        conta = Conta(num_conta, usuario)
        usuario.adicionar_conta(conta)
        print("Conta criada com sucesso! ")
        return conta
    
    print("Usuário não encontrado, cadastre um usuário antes de criar uma conta!")
    return None
        
        
def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada ")
        return None
    
    for conta in contas:
        print(f"""
            Agência: {conta._agencia}
            Número da conta: {conta._numero}
            Usuário: {conta._cliente._nome}
            """)
        print("=" * 100)
    
def main():
    
    AGENCIA = "0001"
    num_conta = 1
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()
        match opcao:
            case "1":
                cpf = input("Digite seu CPF: ")
                usuario = verifica_usuario(cpf, usuarios)
                if usuario and usuario._contas:
                    valor = float(input("Digite o valor que você quer depositar: "))
                    usuario._contas[0].depositar(valor)
                else:
                    print("Essa conta não existe, crie uma para acessar nossos serviços! ")
                
            case "2":
                cpf = input("Digite seu CPF: ")
                usuario = verifica_usuario(cpf, usuarios)
                if usuario and usuario._contas:
                    valor = float(input("Digite a quantidade de dinheiro que você deseja sacar: "))
                    usuario._contas[0].sacar(valor)
                else:
                    print("Essa conta não existe, crie uma para acessar nossos serviços! ")
                
            case "3":
                cpf = input("Digite seu CPF: ")
                usuario = verifica_usuario(cpf, usuarios)
                if usuario and usuario._contas:
                    exibir_extrato(usuario._contas[0])
                else:
                    print("Usuário não encontrado! ")
            
            case "4":
                newConta = criar_conta(AGENCIA, num_conta, usuarios)

                if newConta:
                    contas.append(newConta)
                    num_conta += 1
            
            case "5":
                cadastra_usuario(usuarios)   
            
            case "6":
                listar_contas(contas)
                
            case "7":
                print("Volte sempre :)")
                break
            case _:
                print("Digite uma opção válida! ")

main()
        