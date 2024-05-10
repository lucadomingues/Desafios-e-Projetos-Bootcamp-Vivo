menu = """
OPERAÇÕES BANCÁRIAS

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

ESCOLHA A OPÇÃO: """

saldo = 0
limite = 500
numSaques = 0
LIMITE_SAQUES = 3
extrato = ""

while True:
    opcao = input(menu)

    if opcao == "1":
        print("Depósito")
        deposito = int(input("Digíte o valor do depósito: "))
        saldo += deposito
        extrato += f"""
Deposito +{deposito}"""

    elif opcao == "2":
        print("Saque")
        saque = int(input("Digíte o valor do saque: "))
        saldo -= saque
        if saque > 500:
            print("Saque Negado! Limite de R$ 500 por Saque.")
        elif saque > saldo:
            print("Saque Negado! Sem Saldo.")
        else:
            numSaques += 1
            extrato += f"""
Saque -{saque}"""
        if numSaques >3:
            print("Saque Negado! Limíte Diário atingido.")

    elif opcao == "3":
        print("Extrato")
        print(extrato)
        print(f"Saldo Total R${saldo},00")

    elif opcao == "4":
        break

    else:
        print("Opção Inválida")