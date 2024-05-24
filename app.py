menu = """
Bem vindo(a)! digite a opção da operação que deseja realizar:

[1] Deposito
[2] Saque
[3] Ver extrato
[4] Sair

=> """
LIMITE_SAQUE = 500
saldo = 0
quant_saque = 0
LIMITE_QUANT_SAQUE = 3
extrato = ""


while True:
    x = input(menu)
    match (x):
        case "1":
            deposito = float(input("Digite o valor que você quer depositar: "))
            if deposito >= 0:
                saldo += deposito
                extrato += f"Depósito de R${deposito:.2f}\n"
                print("Valor depositado com sucesso!")
            else:
                print("Valor inválido! ")
        case "2":
            if quant_saque < LIMITE_QUANT_SAQUE:
                saque = float(input("Digite a quantidade de dinheiro que você deseja sacar: "))
                if saque < 0:
                    print("Valor inválido! ")
                    
                elif saldo >= saque:
                    if saque <= LIMITE_SAQUE:
                        saldo -= saque
                        extrato += f"Saque de R${saque:.2f}\n"
                        print("Saque realizado com sucesso! ")
                        quant_saque +=1
                    else:
                        print("Operação inválida o valor limite de saque é de R$500,00")
                else:
                    print("Saldo insuficiente! ")
            else:
                print("você já realizou os 3 saques diários ")
        
        case "3":
            if extrato == "":
                print("Nenhuma operação realizada ainda ")
            else:
                print("========== SEU EXTRATO ==========")
                print(f"{extrato}\nSaldo atual: R${saldo:.2f}")
            
        case "4":
            print("Volte sempre :)")
            break
        case _:
            print("Digite uma opção válida! ")
        