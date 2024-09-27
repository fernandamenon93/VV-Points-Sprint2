import webbrowser
from hashlib import sha256
from tabulate import tabulate


# Banco de dados local (Senha Padrao: fiap2024)
user_database = {
    "eduardo": {
        "passwordHash": "e395c1aace6ce1d3e745d7df342dfeb1488e1212eaab596d08ab526e56e492d8",
        "points": 200,
        "powers": [],
    },
    "gabriel": {
        "passwordHash": "e395c1aace6ce1d3e745d7df342dfeb1488e1212eaab596d08ab526e56e492d8",
        "points": 350,
        "powers": [],
    },
    "fernanda": {
        "passwordHash": "e395c1aace6ce1d3e745d7df342dfeb1488e1212eaab596d08ab526e56e492d8",
        "points": 600,
        "powers": [],
    },
    "luiza": {
        "passwordHash": "e395c1aace6ce1d3e745d7df342dfeb1488e1212eaab596d08ab526e56e492d8",
        "points": 600,
        "powers": [],
    },
    "leonardo": {
        "passwordHash": "e395c1aace6ce1d3e745d7df342dfeb1488e1212eaab596d08ab526e56e492d8",
        "points": 400,
        "powers": [],
    },
}


# ----- Funcoes de Escolha ----- #
def get_choice(options):
    while True:
        choice = input("-> ")
        if choice.isnumeric() and int(choice) in range(1, len(options) + 1):
            break
        else:
            print("Valor incorreto. Tente novamente!")
    return int(choice)
# ------------------------------ #


# ----- Funcoes de controle de acesso ----- #
def manage_access():
    while True:
        print("\nComo gostaria de prosseguir?")
        print("\n1. Cadastrar")
        print("2. Entrar")
        print("3. Sair")

        option = int(input("\nEscolha: "))
        action = {
            1: register_user,
            2: login_user,
            3: exit,
        }.get(option)
        if not action:
            print("Valor incorreto. Tente novamente!")
        return action()


def register_user():
    while True:
        logged_user = input("Usuário: ")
        if logged_user not in user_database.keys():
            break
        print("Usuário Ja cadastrado! Tente Novamente...")

    password = input("Senha: ")
    user_database[logged_user] = {
        "passwordHash": sha256(password.encode('utf-8')).hexdigest(),
        "points": 0,
        "powers": [],
    }
    print(f"Usuário cadastrado com sucesso!")
    return logged_user


def login_user():
    while True:
        logged_user = input("Usuário: ")
        if logged_user in user_database.keys():
            break
        print("Usuário Invalido! Tente Novamente...")

    retries = 0
    while True:
        password = input("Senha: ")
        if sha256(password.encode('utf-8')).hexdigest() == user_database[logged_user]["passwordHash"]:
            return logged_user

        retries += 1
        if retries == 3:
            print("Numero de tentativas acima do permitido! Encerrando programa!")
            exit()
        print(f"Senha invalida para o usuário selecionado! Tente Novamente... {retries}/3 tentativas")
# ----------------------------------------- #


# ----- Funcoes de controle de pontos ----- #
def get_free_points(logged_user):
    options = ["Chamar amigos (100 Pontos)", "Assistir a Formula E (500 Pontos)"]
    for position, option in enumerate(options):
        print(f"{position + 1}. {option}")

    choice = get_choice(options)
    if choice == 1:
        invite_email = input("Email para enviar o convite: ")
        webbrowser.open(f"mailto:{invite_email}")
        print("Obrigado por convidar um amigo!")
        user_database[logged_user]["points"] += 100
    elif choice == 2:
        webbrowser.open("https://www.band.uol.com.br/esportes/automobilismo/formula-e")
        print("Obrigado assistir a Formula E!")
        user_database[logged_user]["points"] += 500


def change_points(logged_user, delta):
    if delta + user_database[logged_user]["points"] < 0:
        return False
    user_database[logged_user]["points"] += delta
    return True


def buy_powers(logged_user):
    options = ["Attack Mode (500 Pontos)", "Fan Boost (800 Pontos)"]
    for position, option in enumerate(options):
        print(f"{position + 1}. {option}")

    choice = get_choice(options)
    power = options[choice - 1]
    if power in user_database[logged_user]["powers"]:
        print(f"Voce ja possui o poder \"{power}\"")
        return

    points_delta = {
        1: -500,
        2: -800,
    }[choice]
    allowed = change_points(logged_user, points_delta)
    if not allowed:
        print("Pontos Insuficientes")
        return

    print(f"\"{power}\" Comprado!")
    user_database[logged_user]["powers"].append(power)


def utilizar_poder(logged_user):
    print("\n--- Poderes Disponiveis ---")
    for position, option in enumerate(user_database[logged_user]["powers"]):
        print(f"{position + 1}. {option}")

    choice = get_choice(user_database[logged_user]["powers"])
    used_power = user_database[logged_user]["powers"].pop(choice - 1)
    print(f"\"{used_power}\" Usado! Parabens!")
# ----------------------------------------- #


# ----- Funcoes Visuais ----- #
def show_header():
    print("=" * 25)
    print("Bem vindo ao VV-Points")
    print("=" * 25)


def show_user_statistics(logged_user):
    print(f"\nSeus pontos: ©{user_database[logged_user]["points"]}")
    print(f"Seus poderes: {' | '.join(user_database[logged_user]["powers"])}")


def show_global_statistics(logged_user):
    formatted_table = [[username, f"©{data["points"]}", data["powers"]] for username, data in user_database.items()]
    print(tabulate(formatted_table, headers=["Name", "Points", "Powers"]))


def show_options(options):
    print("Oque você deseja fazer?\n")
    for position, choice in enumerate(options):
        print(f"{position + 1}. {choice}")
    return get_choice(options)
# --------------------------- #


# ----- Funcoes Principais ----- #
def menu_handler(logged_user):
    choices = ["Adquirir Pontos", "Comprar Poderes", "Utilizar Poderes", "Mostrar Estatisticas Globais", "Sair da Conta"]
    choice = 0
    while choice != len(choices):
        show_user_statistics(logged_user)

        choice = show_options(choices)
        action = {
            1: get_free_points,
            2: buy_powers,
            3: utilizar_poder,
            4: show_global_statistics,
        }.get(choice)
        if not action:
            continue
        action(logged_user)


def main():
    while True:
        show_header()
        logged_user = manage_access()
        menu_handler(logged_user)
# ---------------------------- #


# Iniciar Funcao Principal
if __name__ == "__main__":
    main()
