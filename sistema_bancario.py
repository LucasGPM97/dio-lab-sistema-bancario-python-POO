from abc import ABC, abstractmethod


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class Pessoa_Fisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    def saldo(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= 0:
            print(" Valor invalido")
        elif valor <= self.saldo():
            print(" Saque realizado com sucesso!")
            self._saldo -= valor
            return True
        else:
            print(" Saldo insuficiente!")
        return False

    def depositar(self, valor):
        if valor > 0:
            print(" Deposito realizado com sucesso!")
            self._saldo += valor
            return True
        else:
            print("Valor invalido")
        return False


class Conta_Corrente(Conta):
    def __init__(self, numero, cliente, limite, limite_saques):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        if len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        ):
            print("Limite de saque atingido!")
        elif valor > self.limite:
            print("Valor maior que o limite permitido")
        else:
            return super().sacar(valor)
        return False


class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {"tipo": transacao.__class__.__name__, "valor": transacao.valor}
        )
