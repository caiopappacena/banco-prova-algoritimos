import os
from datetime import datetime

LINHA = "=" * 50


class ContaBancaria:
    """Conta bancária para adolescentes"""

    def __init__(self, titular, cpf, idade, senha):
        self.titular, self.cpf, self.idade, self.senha = titular, cpf, idade, senha
        self.saldo, self.limite_saque, self.historico = 0.0, 1000.0, []
        self._log(f"Conta criada para {titular} ({idade} anos)")

    def _log(self, descricao):
        self.historico.append(f"[{datetime.now():%d/%m/%Y %H:%M:%S}] {descricao}")

    def verificar_senha(self, senha):
        return self.senha == senha

    def depositar(self, valor):
        if valor <= 0:
            return False, "❌ O valor do depósito deve ser maior que zero!"
        self.saldo += valor
        self._log(f"Depósito de R$ {valor:.2f}")
        return True, f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!"

    def sacar(self, valor):
        if valor <= 0:
            return False, "❌ O valor do saque deve ser maior que zero!"
        if valor > self.limite_saque:
            return False, f"❌ O limite máximo para saque é R$ {self.limite_saque:.2f}!"
        if valor > self.saldo:
            return False, (f"❌ Saldo insuficiente! Você só tem R$ {self.saldo:.2f} na conta. "
                           f"Faltam R$ {valor - self.saldo:.2f}")
        self.saldo -= valor
        self._log(f"Saque de R$ {valor:.2f}")
        return True, f"✅ Saque de R$ {valor:.2f} realizado com sucesso!"

    def ver_saldo(self):
        return self.saldo

    def ver_historico(self):
        return "\n".join(self.historico) or "Nenhuma transação registrada."

    def alterar_senha(self, atual, nova):
        if not self.verificar_senha(atual):
            return False, "❌ Senha atual incorreta!"
        if len(nova) < 4:
            return False, "❌ A nova senha deve ter pelo menos 4 caracteres!"
        self.senha = nova
        self._log("Senha alterada")
        return True, "✅ Senha alterada com sucesso!"


# ---------- Utilitários de interface ----------

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausa(msg="\nPressione Enter para continuar..."):
    input(msg)


def tela(titulo):
    """Limpa a tela e mostra um cabeçalho"""
    limpar_tela()
    print(f"\n{LINHA}\n   {titulo}\n{LINHA}")


def menu(titulo, opcoes, extra=None):
    """Exibe um menu e retorna a opção escolhida"""
    print(f"\n{LINHA}\n{titulo}\n{LINHA}")
    if extra:
        print(f"{extra}\n{LINHA}")
    print("\n".join(opcoes))
    print(LINHA)
    return input("Escolha uma opção: ")


def erro(msg):
    print(f"❌ {msg}")


# ---------- Telas e operações ----------

def criar_nova_conta():
    tela("CRIAR NOVA CONTA")
    try:
        titular = input("Nome completo: ").strip()
        if not titular:
            return erro("Nome não pode ser vazio!")

        try:
            idade = int(input("Idade: "))
        except ValueError:
            return erro("Digite uma idade válida (número inteiro)!")
        if not 0 <= idade <= 120:
            return erro("Idade inválida!")

        cpf = input("CPF (apenas números): ").strip()
        if not (cpf.isdigit() and len(cpf) == 11):
            return erro("CPF inválido! Deve ter 11 dígitos.")

        senha = input("Crie uma senha (mínimo 4 caracteres): ").strip()
        if len(senha) < 4:
            return erro("Senha deve ter pelo menos 4 caracteres!")
        if senha != input("Confirme a senha: ").strip():
            return erro("As senhas não conferem!")

        conta = ContaBancaria(titular, cpf, idade, senha)
        print(f"\n✅ Conta criada com sucesso para {titular}!\nIdade: {idade} anos\nCPF: {cpf}")
        pausa("Pressione Enter para continuar...")
        return conta
    except Exception as e:
        return erro(f"Erro ao criar conta: {e}")


def acessar_conta(contas):
    tela("ACESSAR CONTA")
    if not contas:
        erro("Nenhuma conta criada ainda!")
        return pausa("Pressione Enter para continuar...")

    print("\nContas disponíveis:")
    for i, c in enumerate(contas, 1):
        print(f"{i}. {c.titular} - {c.idade} anos (CPF: {c.cpf})")

    try:
        escolha = int(input(f"\nEscolha uma conta (1-{len(contas)}): ")) - 1
    except ValueError:
        return erro("Entrada inválida!")
    if not 0 <= escolha < len(contas):
        return erro("Opção inválida!")

    conta = contas[escolha]
    if conta.verificar_senha(input(f"Digite a senha para {conta.titular}: ")):
        return conta
    erro("Senha incorreta!")
    pausa("Pressione Enter para continuar...")


def operacao_valor(conta, titulo, pergunta, acao):
    """Depósito e saque: pede um valor e executa a ação"""
    tela(titulo.upper())
    if acao == conta.sacar:
        print(f"💰 Saldo atual: R$ {conta.ver_saldo():.2f}")
        print(f"📊 Limite máximo de saque: R$ {conta.limite_saque:.2f}\n{LINHA}")
    try:
        sucesso, msg = acao(float(input(f"\n{pergunta} R$ ")))
        print(msg)
        if sucesso:
            print(f"💰 Novo saldo: R$ {conta.ver_saldo():.2f}")
    except ValueError:
        erro("Valor inválido! Digite um número.")
    pausa()


def operacao_historico(conta):
    tela("HISTÓRICO DE TRANSAÇÕES")
    print(f"{conta.ver_historico()}\n{LINHA}")
    pausa()


def operacao_alterar_senha(conta):
    tela("ALTERAR SENHA")
    atual = input("Digite sua senha atual: ")
    nova = input("Digite a nova senha (mínimo 4 caracteres): ")
    if nova != input("Confirme a nova senha: "):
        erro("As senhas não conferem!")
    else:
        print(conta.alterar_senha(atual, nova)[1])
    pausa("Pressione Enter para continuar...")


def menu_conta(conta):
    acoes = {
        "1": lambda: operacao_valor(conta, "Depositar", "Quanto deseja depositar?", conta.depositar),
        "2": lambda: operacao_valor(conta, "Sacar", "Quanto deseja sacar?", conta.sacar),
        "3": lambda: operacao_historico(conta),
        "4": lambda: operacao_alterar_senha(conta),
    }
    while True:
        limpar_tela()
        opcao = menu(f"   Bem-vindo, {conta.titular}!",
                     ["1️⃣  Depositar", "2️⃣  Sacar", "3️⃣  Ver histórico",
                      "4️⃣  Alterar senha", "5️⃣  Sair da conta"],
                     extra=f"💰 Saldo: R$ {conta.ver_saldo():.2f}")
        if opcao in acoes:
            acoes[opcao]()
        elif opcao == "5":
            print("\n👋 Até logo!")
            break
        else:
            erro("Opção inválida!")
            pausa("Pressione Enter para continuar...")


def main():
    contas = []
    while True:
        limpar_tela()
        opcao = menu("     🏦 BANCO DO ADOLESCENTE 🏦",
                     ["1️⃣  Acessar minha conta", "2️⃣  Criar nova conta", "3️⃣  Sair"])
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
            print("\n👋 Obrigado por usar o Banco do Adolescente!\nAté logo! 🏦\n")
            break
        else:
            erro("Opção inválida!")
            pausa("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
