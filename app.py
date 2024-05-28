#Fução saque deve receber argumentos apenas por nome
#a de dposito apenas por posição 
#extrato por posição e nome, posicionais: saldo, nomeado: extrato
#criar usuario: armazena em uma lista e tem q ter nome, data de nascimento, cpf, endereço
# (string com formato: logradouro - numero - bairro - cidade/sigla do estado, não pode cadastrar usuarios com o mesmo cpf)
#conta corrente: tbm armazena em uma lista sendo composta por: agência, numero da conta e usuário,
# o numero da agencia é fixo: 0001 e o da conta é sequencial começando em 1

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

def deposito(valor, saldo, extrato, /):
    if valor >= 0:
        saldo += valor
        extrato += f"Depósito de R${valor:.2f}\n"
        print("Valor depositado com sucesso!")
    else:
        print("Valor inválido! ")
    
    return saldo, extrato


def saque(*, valor, saldo, extrato, limite_saque = 3, max_saque = 500, quant_saque):
    if quant_saque < limite_saque:
        if valor < 0:
            print("Valor inválido! ")
            
        elif valor <= max_saque:
            if saldo >= valor:
                saldo -= valor
                extrato += f"Saque de R${valor:.2f}\n"
                print("Saque realizado com sucesso! ")
                quant_saque +=1
            else:
                print("Saldo insuficiente! ")
        else:
            print("Operação inválida o valor limite de saque é de R$500,00")
        
    else:
        print("você já realizou os 3 saques diários ")
    
    return saldo, extrato, quant_saque


def exibir_extrato(saldo, /, *, extrato):
    print("========== SEU EXTRATO ==========")
    print("Ainda não há nada no extrato " if not extrato else extrato)
    print(f"\nSaldo atual: R${saldo:.2f}")



def cadastra_usuario(usuarios):
    cpf = input("Digite seu CPF: ")
    usuario = verifica_usuario(cpf, usuarios)
    
    if usuario:
        print("já existe um usuário cadastrado com esse CPF! ")
    else:
        nome = input("Digite seu nome completo: ")
        data_nasci = input("Digite sua data de nascimento no formato ddd/mm/aaaa: ")
        endereco = input("E seu endereço(numero, logradouro, bairro, cidade/sigla do estado): ")
        
        usuarios.append({"nome": nome, "cpf": cpf, "data_nascimento": data_nasci, "endereço": endereco})
        print("Usuário cadastrado com sucesso! ")

def verifica_usuario(cpf, usuarios):
    usuarios_filtrados = []
    
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuarios_filtrados.append(usuario)
    
    if usuarios_filtrados:
        return usuarios_filtrados[0]
    else:
        return None

def criar_conta(agencia, num_conta, usuarios):
    cpf = input("Digite seu CPF: ")
    usuario = verifica_usuario(cpf, usuarios)
    
    if usuario:
        print("Conta Criada com sucesso! ")
        return {"agencia":agencia, "numero_conta":num_conta, "usuario":usuario}
    else:
        print("cpf não encontrado, cadastre um usuario antes de criar uma conta! ")
        
        
def listar_contas(contas):
    for conta in contas:
        print(f"""
            Agência: {conta['agencia']}
            Número da conta: {conta['numero_conta']}
            Usuário: {conta['usuario']['nome']}
            """)
        print("=" * 100)
    
def main():
    saldo = 0
    extrato = ""
    quant_saque = 0
    
    AGENCIA = "0001"
    num_conta = 1
    usuarios = []
    contas = []
    while True:
        opcao = menu()
        match opcao:
            case "1":
                x = float(input("Digite o valor que você quer depositar: "))
                saldo, extrato = deposito(x, saldo, extrato)
                
            case "2":
                y = float(input("Digite a quantidade de dinheiro que você deseja sacar: "))
                saldo, extrato, quant_saque = saque(valor = y, saldo = saldo, extrato = extrato, quant_saque=quant_saque)
                
            
            case "3":
                exibir_extrato(saldo, extrato = extrato)
            
            case "4":
                conta = criar_conta(AGENCIA, num_conta, usuarios)

                if conta:
                    contas.append(conta)
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
        