# Projeto Banco em Python com Tkinter

Este projeto é um sistema de gerenciamento de contas bancárias utilizando a biblioteca Tkinter para a interface gráfica. Permite criar contas correntes, realizar depósitos, saques, transferências, visualizar extratos e deletar contas.

## Funcionalidades

1. **Criar Conta**: Cria uma nova conta corrente com saldo inicial.
2. **Entrar**: Acessa uma conta existente para realizar operações bancárias.
3. **Gerar Relatório**: Exibe os dados de todas as contas no banco.
4. **Deletar Conta**: Remove uma conta existente.
5. **Sair**: Encerra o programa.

## Estrutura

### Classes Principais

- **Conta (abstract)**: Classe base para contas bancárias.
- **ContaCorrente**: Implementa a Conta com funcionalidades específicas de uma conta corrente.
- **Banco**: Gerencia as contas do banco.

### Interface Gráfica

Utiliza Tkinter para interações com o usuário através de diálogos e mensagens.

## Como Executar

1. Certifique-se de ter Python e Tkinter instalados.
2. Execute o arquivo principal (`main.py`):

```bash
python main.py
