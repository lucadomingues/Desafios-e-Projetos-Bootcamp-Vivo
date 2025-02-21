from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
from pathlib import Path

ROOT_PATH = Path(__file__).parent


class ContaIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas(self._index)
            return f"""\
            Agência: \t{conta.agencia}
            Número: \t\t{conta.numero}
            Titular: \t{conta.cliente.nome}
            Saldo: \t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("Limíte de transações diária atingido!")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, dataNascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.dataNascimento = dataNascimento
        self.cpf = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__}: ('{self.cpf}')>"


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

        @classmethod
        def nova_conta(cls, cliente, numero):
            return cls(numero, cliente)

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
            saldo = self.saldo
            excedeuValor = valor > saldo

            if excedeuValor:
                print("\nOperação falhou! Você está sem saldo.")
            elif valor > 0:
                self._saldo -= valor
                print(f"R$ {valor},00")
                print("\nSaque realizado com sucesso!")
                return True
            else:
                print("\nOperação falhou! Valor informado inválido")
            return False

        def depositar(self, valor):
            if valor > 0:
                self._saldo += valor
                print("\nDepósito realizado com sucesso!")
            else:
                print("\nOperação falhou! Valor informado inválido.")
                return False

            return True


class ContaCorrente(Conta):
    def __init__(self, numero, usuario, limite=500, limite_saques=3):
        super().__init__(numero, usuario)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\nOperação falhou! O limite de saque é de R$ 500,00")
        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")
        else:
            return super().sacar(valor)

        return False

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.usuario.nome}"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-$Y %H:%M:%s"),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.utcnow().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%n-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

        @property
        def valor(self):
            return self._valor

        def registrar(self, conta):
            sucesso_transacao = conta.sacar(self.valor)

            if sucesso_transacao:
                conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)

        with open(ROOT_PATH / "log.txt", "a") as arquivo:
            arquivo.write(
                f"[{datetime.utcnow()}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}."
                f"Retornou {resultado}\n"
            )
        return resultado

    return envelope


# Função de depósito
@log_transacao
def depositar(usuarios):
    print("Depósito")
    cpf = input("Digíte o CPF do usuário: ")
    usuario = filtra_usuario(cpf, usuarios)

    if not usuario:
        print("Cliente não encontrado!")
        return

    valor = int(input("Digíte o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta, transacao)


# Função para sacar
@log_transacao
def sacar(usuarios):
    print("Saque")
    cpf = input("Digíte  o CPF do usuário: ")
    usuario = filtra_usuario(cpf, usuarios)

    if not usuario:
        print("\nCliente não encontrado!")
        return

    valor = int(input("Digíte o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    usuario.realizar_transacao(conta, transacao)


# Função para mostrar extrato
@log_transacao
def exibir_extrato(usuarios):
    cpf = input("Digíte o CPF do usuário: ")
    usuario = filtra_usuario(cpf, usuarios)

    if not usuario:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(usuario)
    if not conta:
        return

    print("\n--- EXTRATO ---")
    transacoes = conta.historico.transacoes
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio(tipo_transacao="saque"):
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não possui movimentações na conta."

    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")


@log_transacao
# Função para criar usuario
def criar_usuario(usuarios):
    cpf = int(input("Digíte seu CPF (somente números): "))
    # Chamando função para filtrar se ja possui este CPF cadastrado na lista
    usuarioFiltrado = filtra_usuario(cpf, usuarios)

    if usuarioFiltrado:
        print("\nUsuário já possui Cadastro!")
        return

    nomeUsuario = input("Digíte seu nome completo: ")
    dataNascimento = input("Data de nascimento (DD/MM/AAAA): ")
    endereco = input("Digíte seu endereço (Logradouro, Nº, bairro, cidade/UF): ")

    usuario = PessoaFisica(nome=nomeUsuario, dataNascimento=dataNascimento, cpf=cpf, endereco=endereco)

    usuarios.append(usuario)

    print("\nUsuário criado com sucesso!")


# Função para filtrar CPF
def filtra_usuario(cpf, usuarios):
    usuarioFiltrado = [usuario for usuario in usuarios if usuario.cpf == cpf]
    return usuarioFiltrado[0] if usuarioFiltrado else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    # Não permite o usuário escolher a conta
    return cliente.contas[0]


@log_transacao
# Função para crição de conta
def criar_conta(numContas, usuarios, contas):
    cpf = int(input("Digíte seu CPF (somente números): "))
    usuario = filtra_usuario(cpf, usuarios)

    if not usuario:
        print("\nCliente não encontrado! Criação de conta encerrada.")
        return

    conta = ContaCorrente(usuario=usuario, numero=numContas)
    contas.append(conta)
    usuario.contas.append(conta)

    print("\nConta criada com sucesso!")


# Função para listar as contas criadas
def listar_contas(contas):
    for conta in contas:
        print(textwrap.dedent(str(conta)))


# Executando o sistema
def main():
    usuarios = []
    contas = []
    numContas = 0
    AGENCIA = "0001"

    # Menu inicial / opções
    menu = """\nOPERAÇÕES BANCÁRIAS\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo Usuario
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair\n
    ESCOLHA A OPÇÃO: """

    while True:
        opcao = input(menu)

        if opcao == "1":
            depositar(usuarios)

        elif opcao == "2":
            sacar(usuarios)

        elif opcao == "3":
            exibir_extrato(usuarios)

        elif opcao == "4":
            criar_usuario(usuarios)

        elif opcao == "5":
            numContas = len(contas) + 1
            conta = criar_conta(numContas, usuarios, contas)

            if criar_conta:
                contas.append(conta)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break

        else:
            print("Opção Inválida")


main()
