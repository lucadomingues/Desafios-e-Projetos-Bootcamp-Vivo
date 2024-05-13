#Função de depósito
def depositar(saldo, extrato):
    print("Depósito")
    deposito = int(input("Digíte o valor do depósito: "))
    saldo += deposito
    extrato += f"Deposito: +R${deposito}\n"
    print("Depósito realizado com sucesso!")
    
    return saldo, extrato
    
#Função para sacar
def sacar(saldo, numSaques, limite, limiteSaques, extrato):
    print("Saque")
    saque = int(input("Digíte o valor do saque: "))

    if saque > limite:
        print("Saque Negado! Limite de R$ 500 por Saque.")
    elif saque > saldo:
        print("Saque Negado! Sem Saldo.")
    else:
        saldo -= saque
        print("Saque realizado com sucesso!")
        numSaques += 1
        extrato += f"Saque:    -R${saque}\n"
    
    if numSaques > limiteSaques:
        print("Saque Negado! Limíte Diário atingido.")
    
    return saldo, numSaques, extrato

#Função para mostrar extrato
def exibirExtrato(extrato, saldo):
    print("\nExtrato")
    print(extrato)
    print(f"Saldo Total R${saldo},00")

#Função para criar usuario
def criarUsuario(usuarios):
    cpf = int(input("Digíte seu CPF (somente números): "))
    #Chamando função para filtrar se ja possui este CPF cadastrado na lista
    usuarioFiltrado = filtraUsuario(cpf, usuarios)

    if usuarioFiltrado:
        print("\nUsuário já possui Cadastro!")
        return

    nomeUsuario = input("Digíte seu nome: ")
    dataNas = input("Data de nascimento (00/00/0000): ")
    endereco = input("Digíte seu endereço (Logradouro, Nº, bairro, cidade/UF): ")

    usuarios.append({'cpf': cpf,'usuario': nomeUsuario, 'dataNas': dataNas, 'endereco': endereco})
    
    print("\nUsuário criado com sucesso!")

#Função para filtrar CPF
def filtraUsuario(cpf, usuarios):
    usuarioFiltrado = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarioFiltrado[0] if usuarioFiltrado else None

#Função para crição de conta
def criarConta(agencia, usuarios, numContas):
    cpf = int(input("Digíte seu CPF (somente números): "))
    usuarioFiltrado = filtraUsuario(cpf, usuarios)

    if usuarioFiltrado:
        print("\nConta criada com sucesso!")
        return {'agencia': agencia, 'numConta': numContas, 'usuario': usuarioFiltrado}
    
    print("\nUsuário não encontrado! Cadastre-se como Novo Usuário.")

#Função para listar as contas criadas
def listarContas(contas):
    for conta in contas:
        contaCadastrada = f"""\
            Agência: {conta['agencia']}
            Conta: {conta['numConta']}
            Titular: {conta['usuario']['usuario']}"""
        print("\n\n")
        print(contaCadastrada)

#Executando o sistema
def main():
    saldo = 0
    limite = 500
    numSaques = 0
    extrato = ""
    usuarios = []
    contas = []
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    #Menu inicial / opções
    menu = ("""\nOPERAÇÕES BANCÁRIAS\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Novo Usuario
    [5] Nova Conta
    [6] Listar Contas
    [7] Sair\n
    ESCOLHA A OPÇÃO: """)

    while True:
        opcao = input(menu)

        if opcao == "1":
            saldo, extrato = depositar(saldo, extrato)

        elif opcao == "2":
            saldo, numSaques, extrato = sacar(saldo, numSaques, limite, LIMITE_SAQUES, extrato)

        elif opcao == "3":
            exibirExtrato(extrato, saldo)
        
        elif opcao == "4":
            criarUsuario(usuarios)
            print(usuarios)
        
        elif opcao == "5":
            numContas = len(contas) + 1
            conta = criarConta(AGENCIA, usuarios, numContas)

            if criarConta:
                contas.append(conta)
        
        elif opcao == "6":
            listarContas(contas)

        elif opcao == "7":
            break

        else:
            print("Opção Inválida")

main()