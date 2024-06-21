import tkinter as tk
from tkinter import messagebox, simpledialog
from abc import ABC, abstractmethod 
import datetime

class Conta(ABC):
    def __init__(self, num_conta, saldo, transacoes, limite_transacoes_diarias = 3):
        self.num_conta = num_conta
        self._saldo = saldo
        self.transacoes = transacoes
        self.limite_transacoes_diarias = limite_transacoes_diarias
        self.transacoes_hoje = 0
        self.ultima_transacao = datetime.date.today()
    
    def resetar_transacoes_diarias(self):
        if self.ultima_transacao != datetime.date.today():
            self.transacoes_hoje = 0
            self.ultima_transacao = datetime.date.today()
            
    def registrar_transacao_diaria(self):
        self.resetar_transacoes_diarias()
        self.transacoes_hoje +=1
    
    @abstractmethod    
    def depositar(self, valor):
        pass
    
    @abstractmethod
    def sacar(self, valor):
        pass
    
    @abstractmethod
    def transferir(self, valor, conta_destino):
        pass
    
    def mostrar_dados(self):
        pass
    

class ContaCorrente(Conta):
    def __init__(self, num_conta, saldo=0, transacoes = []):
        super().__init__(num_conta, saldo, transacoes)
        
    def depositar(self, valor):
        if self.transacoes_hoje >= self.limite_transacoes_diarias:
            messagebox.showwarning("Inválido", "Limite de transações diárias atingido")
            return None
        if valor > 0:
            self._saldo += valor
            self.transacoes.append(f"Depósito no valor de R${valor:.2f}")
            self.registrar_transacao_diaria()
            return True
        else:
            messagebox.showerror("ERRO", "Valor inválido")
        
    def sacar(self, valor):
        if self.transacoes_hoje >= self.limite_transacoes_diarias:
            messagebox.showwarning("Inválido", "Limite de transações diárias atingido")
            return None
        
        if valor >= 0:
            if self._saldo >= valor:
                self._saldo -= valor
                self.transacoes.append(f"Saque no valor de R${valor:.2f}")
                self.registrar_transacao_diaria()
                return True
            else:
                messagebox.showerror("ERRO", f"Saldo insuficiente, seu saldo atual é de: R${self._saldo:.2f}")
        else:
            messagebox.showerror("ERRO", "Valor inválido")
            
            
    def transferir(self, valor, conta_destino):
        if self.transacoes_hoje >= self.limite_transacoes_diarias:
            messagebox.showwarning("Inválido", "Limite de transações diárias atingido")
            return None
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            conta_destino._saldo += valor
            self.transacoes.append(f"Transferência de R${valor:.2f} para conta {conta_destino.num_conta}")
            conta_destino.transacoes.append(f"Transferência recebida de R${valor:.2f} da conta {self.num_conta}")
            self.registrar_transacao_diaria()
            return True
            # conta_destino.registrar_transacao_diaria()
            
        else:
            messagebox.showerror("ERRO", f"Saldo insuficiente, 1seu saldo atual é de: R${self._saldo:.2f}")
            
            
    def mostrar_extrato(self):
        # messagebox.showinfo("Dados", f"Seus Dados Bancarios da conta corrente:\n\nNúmero da conta: {self.num_conta}\n\nSaldo: R${self._saldo:.2f}")
        transacoes_str = "Ainda não há nada no histórico de transações" if not self.transacoes else '\n'.join(self.transacoes)
        messagebox.showinfo("Extrato", f"EXTRATO DA SUA CONTA CORRENTE:\n\n{transacoes_str}\n\nSaldo atual: R${self._saldo:.2f}")
        
    def mostrar_dados(self):
        # print(f"Dados Bancarios da conta corrente:\n\nNúmero da conta: {self.num_conta}\n\nSaldo: R${self._saldo:.2f}\n\n")
        dados = f"Dados Bancários das contas corrente:\n\nNúmero da conta: {self.num_conta}\nSaldo: R${self._saldo:.2f}\n"
        transacoes = "\n".join(self.transacoes)
        messagebox.showinfo("Dados", dados + "Transações:\n" + transacoes)   
        
        
class Banco:
    def __init__(self):
        self.contas_banco = []
        
    def inserir(self, conta):
        self.contas_banco.append(conta)
        messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            
    def deletar(self, conta):
        self.contas_banco.remove(conta)
        

    
    def procurar_conta(self, num_conta):
        for conta in self.contas_banco:
            if conta.num_conta == num_conta:
                return conta
        return None
    

# class Historico:
#     def __init__(self):
#         self.transacoes = []
    
#     def adicionar_transacao(self, transacao):
#         self.transacoes.append(transacao)



def menu_principal():
    menu1 = ("Digite a opção que deseja realizar:\n\n"
            "[1] Criar conta\n[2] Entrar\n[3] Gerar relatório\n[4] Deletar conta\n[5] Sair")
    
    return simpledialog.askinteger("Menu", menu1)
    
    
def menu2():
    menu2 = "Digite a opção que deseja realizar\n\n[1] Depositar\n[2] Sacar\n[3] Transferir\n[4] Ver extrato\n[5] Sair"
    
    return simpledialog.askinteger("Menu", menu2)

def main():
    banco = Banco()
    while True:
        opcao1 = menu_principal()
        match opcao1:
            case 1:
                num_conta = simpledialog.askstring("conta", "Digite o numero da conta: ")
                valor = simpledialog.askfloat("Valor inicial", "Digite o valor que deseja depositar no seu saldo inicial\n")
                if banco.procurar_conta(num_conta) is None:
                    contac = ContaCorrente(num_conta, valor)
                    # contac.depositar(valor)
                    banco.inserir(contac)
                    contac.mostrar_dados()
                else:
                    messagebox.showerror("ERRO", "Já existe uma conta com esse número")
            case 2:
                num_conta = simpledialog.askstring("Entrar", "Digite o numero da conta")
                conta = banco.procurar_conta(num_conta)
                if conta:
                    messagebox.showinfo("Sucesso", "Bem vindo!")
                    while True:
                        opcao2 = menu2()
                        match opcao2:
                            case 1:
                                
                                valor = simpledialog.askfloat("Deposito", "Digite o valor que você deseja depositar")
                                if conta.depositar(valor) != None:
                                    messagebox.showinfo("Depósito", f"Depósito de R${valor:.2f} realizado com sucesso!")
                            case 2:
                                valor = simpledialog.askfloat("Saque", "Digite o valor que você deseja sacar")
                                if conta.sacar(valor) != None:
                                    messagebox.showinfo("Saque", f"Saque no valor de R${valor:.2f} realizado com sucesso!")
                                
                            case 3:
                                num_conta_destino = simpledialog.askstring("Conta", "Digite o número da conta que vai receber a transferência:")
                                conta_destino = banco.procurar_conta(num_conta_destino)
                                if conta_destino:
                                    if conta_destino != conta:
                                        valor = simpledialog.askfloat("Transferência", "Digite o valor que deseja transferir:")
                                        if conta.transferir(valor, conta_destino) != None:
                                            messagebox.showinfo("Transferência", "Transferência realizada com sucesso! ")
                                    else:
                                        messagebox.showerror("ERRO", "As contas são iguais!")
                                else:
                                    messagebox.showerror("ERRO", "Essa conta não existe")
                            
                            case 4:
                                conta.mostrar_extrato()
                            
                            case 5:
                                messagebox.showinfo("Sair", "Deslogando...")
                                break
                else:
                    messagebox.showerror("ERRO", "Essa conta não existe")
            case 3:
                for conta in banco.contas_banco:
                    conta.mostrar_dados()
            case 4:
                num_conta = simpledialog.askstring("Deletar", "Digite o numero da conta que deseja deletar")
                conta = banco.procurar_conta(num_conta)
                if conta is None:
                    messagebox.showerror("ERRO", "Essa conta não existe")
                else:
                    x = simpledialog.askstring("Warning", f"Tem certeza que deseja deletar a conta {num_conta}? Y/N")
                    if x == "y" or "Y":
                        banco.deletar(conta)
                        messagebox.showinfo("Sucesso", f"Conta {num_conta} deletada com sucesso!")
                    else:
                        messagebox.showinfo("Conta", "Sua conta não foi deletada")

            case 5:
                messagebox.showinfo("Saindo", "Volte sempre!")
                break
    
main()
