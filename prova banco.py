import os
from datetime import datetime

class ContaBancaria:
    """Classe que representa uma conta bancária para adolescentes"""
    
    def __init__(self, titular, cpf, idade, senha_inicial):
        self.titular = titular
        self.cpf = cpf
        self.idade = idade
        self.senha = senha_inicial
        self.saldo = 0.0
        self.limite_saque = 1000.0  # Limite máximo de saque
        self.historico = []
        self._registrar_evento(f"Conta criada para {titular} ({idade} anos)")
    
    def _registrar_evento(self, descricao):
        """Registra um evento no histórico"""
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.historico.append(f"[{data}] {descricao}")
    
    def verificar_senha(self, senha):
        """Verifica se a senha está correta"""
        return self.senha == senha
    
    def depositar(self, valor):
        """Realiza um depósito na conta"""
        if valor <= 0:
            return False, "❌ O valor do depósito deve ser maior que zero!"
        
        self.saldo += valor
        self._registrar_evento(f"Depósito de R$ {valor:.2f}")
        return True, f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!"
    
    def sacar(self, valor):
        """Realiza um saque na conta com validações"""
        
        # Validação 1: Valor positivo
        if valor <= 0:
            return False, "❌ O valor do saque deve ser maior que zero!"
        
        # Validação 2: Limite máximo de saque
        if valor > self.limite_saque:
            return False, f"❌ O limite máximo para saque é R$ {self.limite_saque:.2f}!"
        
        # Validação 3: Não pode sacar mais do que tem na conta
        if valor > self.saldo:
            diferenca = valor - self.saldo
            return False, f"❌ Saldo insuficiente! Você só tem R$ {self.saldo:.2f} na conta. Faltam R$ {diferenca:.2f}"
        
        self.saldo -= valor
        self._registrar_evento(f"Saque de R$ {valor:.2f}")
        return True, f"✅ Saque de R$ {valor:.2f} realizado com sucesso!"
    
    def ver_saldo(self):
        """Retorna o saldo atual"""
        return self.saldo
    
    def ver_historico(self):
        """Mostra o histórico de transações"""
        if not self.historico:
            return "Nenhuma transação registrada."
        return "\n".join(self.historico)
    
    def alterar_senha(self, senha_atual, senha_nova):
        """Altera a senha da conta"""
        if not self.verificar_senha(senha_atual):
            return False, "❌ Senha atual incorreta!"
        
        if len(senha_nova) < 4:
            return False, "❌ A nova senha deve ter pelo menos 4 caracteres!"
        
        self.senha = senha_nova
        self._registrar_evento("Senha alterada")
        return True, "✅ Senha alterada com sucesso!"


def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def exibir_menu_principal():
    """Exibe o menu principal"""
    print("\n" + "="*50)
    print("     🏦 BANCO DO ADOLESCENTE 🏦")
    print("="*50)
    print("1️⃣  Acessar minha conta")
    print("2️⃣  Criar nova conta")
    print("3️⃣  Sair")
    print("="*50)
    return input("Escolha uma opção: ")


def exibir_menu_conta(conta):
    """Exibe o menu da conta"""
    print("\n" + "="*50)
    print(f"   Bem-vindo, {conta.titular}!")
    print("="*50)
    print(f"💰 Saldo: R$ {conta.ver_saldo():.2f}")
    print("="*50)
    print("1️⃣  Depositar")
    print("2️⃣  Sacar")
    print("3️⃣  Ver histórico")
    print("4️⃣  Alterar senha")
    print("5️⃣  Sair da conta")
    print("="*50)
    return input("Escolha uma opção: ")


def criar_nova_conta():
    """Cria uma nova conta bancária"""
    limpar_tela()
    print("\n" + "="*50)
    print("   CRIAR NOVA CONTA")
    print("="*50)
    
    try:
        titular = input("Nome completo: ").strip()
        if not titular:
            print("❌ Nome não pode ser vazio!")
            return None
        
        try:
            idade = int(input("Idade: "))
            if idade < 0 or idade > 120:
                print("❌ Idade inválida!")
                return None
        except ValueError:
            print("❌ Digite uma idade válida (número inteiro)!")
            return None
        
        cpf = input("CPF (apenas números): ").strip()
        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            print("❌ CPF inválido! Deve ter 11 dígitos.")
            return None
        
        senha = input("Crie uma senha (mínimo 4 caracteres): ").strip()
        if len(senha) < 4:
            print("❌ Senha deve ter pelo menos 4 caracteres!")
            return None
        
        confirmacao = input("Confirme a senha: ").strip()
        if senha != confirmacao:
            print("❌ As senhas não conferem!")
            return None
        
        conta = ContaBancaria(titular, cpf, idade, senha)
        print(f"\n✅ Conta criada com sucesso para {titular}!")
        print(f"Idade: {idade} anos")
        print(f"CPF: {cpf}")
        input("Pressione Enter para continuar...")
        return conta
    
    except Exception as e:
        print(f"❌ Erro ao criar conta: {e}")
        return None


def acessar_conta(contas):
    """Permite acessar uma conta existente"""
    limpar_tela()
    print("\n" + "="*50)
    print("   ACESSAR CONTA")
    print("="*50)
    
    if not contas:
        print("❌ Nenhuma conta criada ainda!")
        input("Pressione Enter para continuar...")
        return None
    
    print("\nContas disponíveis:")
    for i, conta in enumerate(contas, 1):
        print(f"{i}. {conta.titular} - {conta.idade} anos (CPF: {conta.cpf})")
    
    try:
        escolha = int(input(f"\nEscolha uma conta (1-{len(contas)}): ")) - 1
        if 0 <= escolha < len(contas):
            conta = contas[escolha]
            senha = input(f"Digite a senha para {conta.titular}: ")
            
            if conta.verificar_senha(senha):
                return conta
            else:
                print("❌ Senha incorreta!")
                input("Pressione Enter para continuar...")
                return None
        else:
            print("❌ Opção inválida!")
            return None
    except ValueError:
        print("❌ Entrada inválida!")
        return None


def operacao_deposito(conta):
    """Realiza operação de depósito"""
    limpar_tela()
    print("\n" + "="*50)
    print("   DEPOSITAR")
    print("="*50)
    
    try:
        valor = float(input("Quanto deseja depositar? R$ "))
        sucesso, mensagem = conta.depositar(valor)
        print(mensagem)
        if sucesso:
            print(f"💰 Novo saldo: R$ {conta.ver_saldo():.2f}")
    except ValueError:
        print("❌ Valor inválido! Digite um número.")
    
    input("\nPressione Enter para continuar...")


def operacao_saque(conta):
    """Realiza operação de saque"""
    limpar_tela()
    print("\n" + "="*50)
    print("   SACAR")
    print("="*50)
    print(f"💰 Saldo atual: R$ {conta.ver_saldo():.2f}")
    print(f"📊 Limite máximo de saque: R$ {conta.limite_saque:.2f}")
    print("="*50)
    
    try:
        valor = float(input("\nQuanto deseja sacar? R$ "))
        sucesso, mensagem = conta.sacar(valor)
        print(mensagem)
        if sucesso:
            print(f"💰 Novo saldo: R$ {conta.ver_saldo():.2f}")
    except ValueError:
        print("❌ Valor inválido! Digite um número.")
    
    input("\nPressione Enter para continuar...")


def operacao_historico(conta):
    """Exibe o histórico da conta"""
    limpar_tela()
    print("\n" + "="*50)
    print("   HISTÓRICO DE TRANSAÇÕES")
    print("="*50)
    print(conta.ver_historico())
    print("="*50)
    input("\nPressione Enter para continuar...")


def operacao_alterar_senha(conta):
    """Permite alterar a senha"""
    limpar_tela()
    print("\n" + "="*50)
    print("   ALTERAR SENHA")
    print("="*50)
    
    senha_atual = input("Digite sua senha atual: ")
    nova_senha = input("Digite a nova senha (mínimo 4 caracteres): ")
    confirmacao = input("Confirme a nova senha: ")
    
    if nova_senha != confirmacao:
        print("❌ As senhas não conferem!")
        input("Pressione Enter para continuar...")
        return
    
    sucesso, mensagem = conta.alterar_senha(senha_atual, nova_senha)
    print(mensagem)
    input("Pressione Enter para continuar...")


def menu_conta(conta):
    """Loop do menu da conta"""
    while True:
        limpar_tela()
        opcao = exibir_menu_conta(conta)
        
        if opcao == "1":
            operacao_deposito(conta)
        elif opcao == "2":
            operacao_saque(conta)
        elif opcao == "3":
            operacao_historico(conta)
        elif opcao == "4":
            operacao_alterar_senha(conta)
        elif opcao == "5":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida!")
            input("Pressione Enter para continuar...")


def main():
    """Função principal - loop do programa"""
    contas = []
    
    while True:
        limpar_tela()
        opcao = exibir_menu_principal()
        
        if opcao == "1":
            conta = acessar_conta(contas)
            if conta:
                menu_conta(conta)
        
        elif opcao == "2":
            conta = criar_nova_conta()
            if conta:
                contas.append(conta)
        
        elif opcao == "3":
            limpar_tela()
            print("\n👋 Obrigado por usar o Banco do Adolescente!")
            print("Até logo! 🏦\n")
            break
        
        else:
            print("❌ Opção inválida!")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
