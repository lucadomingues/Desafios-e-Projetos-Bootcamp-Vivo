"""
Desafio
Vamos agora, adicionar uma funcionalidade à classe UsuarioTelefone, que realizar chamadas para outros usuários. Cada chamada terá uma duração em minutos e o custo será deduzido do saldo do usuário, suponha o custo de $0.10 por minuto. Você pode criar um método fazer_chamada que vai permitir que o usuário faça a chamada, ele vai receber o destinatario e duracao como parâmetros. Calcule o custo da chamada usando o método 'custo_chamada' do objeto 'plano', além de adicionar o método deduzir_saldo para deduzir o valor do saldo do plano e depois retorne uma mensagem adequada como mostra no exemplo a baixo.

Entrada
Número do usuário, número do telefone, saldo inicial, número do destinatário e a duração da chamada em minutos.

Saída
Mensagem indicando o sucesso da chamada ou saldo insuficiente para fazer a chamada.

Exemplos
A tabela abaixo apresenta exemplos com alguns dados de entrada e suas respectivas saídas esperadas. Certifique-se de testar seu programa com esses exemplos e com outros casos possíveis.

ENTRADA
Rodrigo
(00) 90000-0000
10.00
(33) 93333-3333
60
SAIDA
Chamada para (33) 93333-3333 realizada com sucesso. Saldo: $4.00

ENTRADA
Yule
(11) 91111-1111
30.00
(00) 90000-0000
240
SAIDA
Chamada para (00) 90000-0000 realizada com sucesso. Saldo: $6.00

ENTRADA
Amelia
(33) 93333-3333
10.00
(11) 91111-1111
120
SAIDA
Saldo insuficiente para fazer a chamada.
"""
class UsuarioTelefone:
    def __init__(self, nome, numero, plano):
        self.nome = nome
        self.numero = numero
        self.plano = plano

    def fazer_chamada(self, destinatario, duracao):
        custo = self.plano.custo_chamada(duracao)
        
        if self.plano.verificar_saldo() >= custo:
            self.plano.deduzir_saldo(custo)
            return f"Chamada para {destinatario} realizada com sucesso. Saldo: ${self.plano.verificar_saldo():.2f}"
        else:
            return "Saldo insuficiente para fazer a chamada."

class Plano:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial

    def verificar_saldo(self):
        return self.saldo

    def custo_chamada(self, duracao):
        return duracao * 0.10

    def deduzir_saldo(self, valor):
        self.saldo -= valor

class UsuarioPrePago(UsuarioTelefone):
    def __init__(self, nome, numero, saldo_inicial):
        super().__init__(nome, numero, Plano(saldo_inicial))

nome = input()
numero = input()
saldo_inicial = float(input())

usuario_pre_pago = UsuarioPrePago(nome, numero, saldo_inicial)
destinatario = input()
duracao = int(input())

print(usuario_pre_pago.fazer_chamada(destinatario, duracao))
