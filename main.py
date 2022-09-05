import time
import random as random

import Player


def coin():
    possible = ["cara", "cruz"]
    choose = ""
    while choose.lower() not in possible:
        choose = input("¿Cara o cruz?\n")

    random.seed()
    coin_result = random.randint(0, 1)
    print("Ha salido {}.".format(possible[coin_result]))

    if possible[coin_result] == choose.lower():
        return 0
    else:
        return 1


def throw(n_dices):
    possible = ["hacha", "casco", "flecha", "escudo", "mano"]
    add_tokens = ["", "", " con TOKEN", " con TOKEN", "", ""]  # 2/6 probability of being a marked dice
    results = []
    for i in range(n_dices):
        random.seed()
        dice = random.randint(0, len(possible) - 1)
        token = random.randint(0, len(possible) - 1)
        results.append(possible[dice] + add_tokens[token])
    return results


def forward(results, n_throws, max_throws):
    forwarded = []
    if n_throws >= max_throws - 2:
        print("ÚLTIMA TIRADA - SE ADELANTAN TODOS LOS DADOS OBTENIDOS")
        time.sleep(3)
    for i in range(len(results)):
        if n_throws < max_throws - 2:
            choose = input("¿Quieres adelantar el dado #{} ({})? [Y]\n".format(i + 1, results[i]))
            if choose.lower() == 'y':
                forwarded.append(results[i])
        else:
            forwarded.append(results[i])

    return forwarded


def choose_order(player1, player2):
    if (coin()) == 0:  # Comienza el jugador 1
        current_player_name = "JUGADOR 1"
        current_player = player1
        waiting_player = player2
    else:  # Comienza el rival
        current_player_name = "JUGADOR 2"
        current_player = player2
        waiting_player = player1

    return current_player_name, current_player, waiting_player


def throw_phase(current_player_name, current_player, waiting_player, n_throws):
    for i in range(2 * n_throws):  # Each player throws n_throws times
        print("\n----------------------------- TURNO DEL {} -----------------------------".format(current_player_name))
        if current_player.get_n_dices() > 0:
            current_player.set_dices(throw(current_player.get_n_dices()))
            print("Los dados del {} muestran: {}".format(current_player_name, current_player.get_dices()))
            time.sleep(1)
            current_player.set_forwarded(forward(current_player.get_dices(), i, 2 * n_throws))
            print("En la delantera del {} hay: {}".format(current_player_name, current_player.get_forwarded()))
        else:
            time.sleep(2)
            print("El {} ya ha adelantado sus seis dados.".format(current_player_name))

        aux = current_player
        current_player = waiting_player
        waiting_player = aux

        if current_player_name == "JUGADOR 1":
            current_player_name = "JUGADOR 2"
        else:
            current_player_name = "JUGADOR 1"

        if current_player.get_n_dices() == 0 and waiting_player.get_n_dices() == 0:
            print("\n\nAmbos jugadores han adelantado todos sus dados.")
            break


def favor_phase(current_player, current_player_dices, current_player_name,
                waiting_player, waiting_player_dices, waiting_player_name):
    dice = 0
    new_tokens_1 = 0
    new_tokens_2 = 0
    while dice < len(current_player_dices):
        if current_player_dices[dice].endswith(' con TOKEN'):
            current_player_dices[dice] = current_player_dices[dice][:-10]
            current_player.set_tokens(current_player.get_tokens() + 1)
            new_tokens_1 += 1

        if waiting_player_dices[dice].endswith(' con TOKEN'):
            waiting_player_dices[dice] = waiting_player_dices[dice][:-10]
            waiting_player.set_tokens(waiting_player.get_tokens() + 1)
            new_tokens_2 += 1

        dice += 1

    time.sleep(2)
    print("\nEl {} ha obtenido {} TOKENS gracias a sus dados.\n".format(current_player_name, new_tokens_1))
    time.sleep(2)
    print("El {} ha obtenido {} TOKENS gracias a sus dados.\n".format(waiting_player_name, new_tokens_2))
    time.sleep(2)

    """
    for favor in current_player.get_favors():
        if favor != "":
            confirmation = input("{}, ¿quieres utilizar el favor {}? [Y]".format(current_player_name, favor)).lower()
            if confirmation == "y":
                print("")
                ############# SEGUIR AQUÍ
    """


def log_battle_info(first_player, first_player_name, first_player_dices, second_player, second_player_name,
                    second_player_dices):
    print("Dados del {}, nivel de salud y TOKENS: {} / {} puntos de vida / {} TOKENS".format(
        first_player_name, first_player_dices,
        first_player.get_health(), first_player.get_tokens()))
    print("Dados del {}, nivel de salud y TOKENS: {} / {} puntos de vida / {} TOKENS\n".format(
        second_player_name, second_player_dices,
        second_player.get_health(),
        second_player.get_tokens()))


def battle_phase(first_player_name, first_player, second_player):
    win_condition = False

    current_player_dices = first_player.get_forwarded()
    waiting_player_dices = second_player.get_forwarded()

    attacks = ["hacha", "flecha"]
    defense_pairs = {"hacha": "casco", "flecha": "escudo"}

    current_player_name = first_player_name

    if first_player_name == "JUGADOR 1":
        second_player_name = "JUGADOR 2"
    else:
        second_player_name = "JUGADOR 1"

    current_player = first_player
    waiting_player = second_player
    waiting_player_name = second_player_name

    favor_phase(current_player, current_player_dices, current_player_name,
                waiting_player, waiting_player_dices, waiting_player_name)

    for i in range(2):
        if i == 1 and win_condition is False:
            aux_dices = current_player_dices
            current_player_dices = waiting_player_dices
            waiting_player_dices = aux_dices

            aux_player = current_player
            current_player = waiting_player
            waiting_player = aux_player
            if current_player_name == "JUGADOR 1":
                current_player_name = "JUGADOR 2"
                waiting_player_name = "JUGADOR 1"

            else:
                current_player_name = "JUGADOR 1"
                waiting_player_name = "JUGADOR 2"

        if win_condition is False:
            time.sleep(2)
            print("\n----------------------------- ATACA EL {} -----------------------------".format(
                current_player_name))
            time.sleep(2)

        dice = 0

        while dice < len(current_player_dices) and win_condition is False:
            if i == 0:
                first_player_dices = current_player_dices
                second_player_dices = waiting_player_dices
            else:
                first_player_dices = waiting_player_dices
                second_player_dices = current_player_dices
            time.sleep(2)

            if current_player_dices[dice] in attacks:
                if defense_pairs[current_player_dices[dice]] in waiting_player_dices:
                    print("El {} ataca con {}, pero el {} del {} detiene el ataque.".format(current_player_name,
                                                                                            current_player_dices[dice],
                                                                                            defense_pairs[
                                                                                                current_player_dices[
                                                                                                    dice]],
                                                                                            waiting_player_name))
                    waiting_player_dices.remove(defense_pairs[current_player_dices[dice]])
                    current_player_dices.remove(current_player_dices[dice])
                else:
                    print("El {} ataca con {}, infringiendo 1 de daño.".format(current_player_name,
                                                                               current_player_dices[dice]))
                    current_player_dices.remove(current_player_dices[dice])
                    waiting_player.set_health(waiting_player.get_health() - 1)
                    if waiting_player.get_health() < 1:
                        announce_victory(current_player, current_player_name, waiting_player_name)
                        win_condition = True
                log_battle_info(first_player, first_player_name, first_player_dices, second_player,
                                second_player_name, second_player_dices)
                dice = dice - 1

            if current_player_dices:  # Importante comprobar si current_player_dices no está vacío
                if current_player_dices[dice] == "mano":
                    if waiting_player.get_tokens() > 0:
                        current_player_dices.remove(current_player_dices[dice])
                        dice = dice - 1
                        current_player.set_tokens(current_player.get_tokens() + 1)
                        waiting_player.set_tokens(waiting_player.get_tokens() - 1)
                        print("El {} roba un TOKEN al {}".format(current_player_name, waiting_player_name))
                        log_battle_info(first_player, first_player_name, first_player_dices, second_player,
                                        second_player_name, second_player_dices)

            if win_condition:
                break
            time.sleep(3)
            dice = dice + 1

    print("\n\n----------------------------- FIN DE LA FASE DE BATALLA -----------------------------\n\n")
    time.sleep(3)


def announce_victory(winner, winner_name, loser_name):
    print("\n\n----------------------------- EL {} HA VENCIDO AL {}, MANTENIENDO INTACTOS "
          "{} PUNTOS DE VIDA -----------------------------".format(winner_name, loser_name, winner.get_health()))


def assign_favors(first_player, first_player_name, second_player):
    favors = ["Thor's Strike", "Vidar's Might", "Heimdall's Watch", "Ull'rs Aim", "Baldr's Invulnerability",
              "Freyr's Gift", "Hel's Grip", "Skadi's Hunt", "Freyja's Plenty"]
    if first_player_name == "JUGADOR 1":
        second_player_name = "JUGADOR 2"
    else:
        second_player_name = "JUGADOR 1"

    n_chosen_favors = 0
    favor = ""
    while n_chosen_favors < 3:
        favor = input("{}, elige tu favor divino #{} de la lista escribiendo tal y como aparecen o pulsa Enter para no"
                      " introducir el favor #{}: \n{}\n".format(first_player_name, n_chosen_favors + 1,
                                                                n_chosen_favors + 1, favors))
        if (favor in favors and favor not in first_player.get_favors()) or favor == "":
            first_player.set_favors(favor)
            n_chosen_favors += 1

    n_chosen_favors = 0
    favor = ""
    while n_chosen_favors < 3:
        favor = input("{}, elige tu favor divino #{} de la lista escribiendo tal y como aparecen o pulsa Enter para no"
                      "introducir el favor #{}: \n{}\n".format(second_player_name, n_chosen_favors + 1,
                                                               n_chosen_favors + 1, favors))
        if (favor in favors and favor not in second_player.get_favors()) or favor == "":
            second_player.set_favors(favor)
            n_chosen_favors += 1

    print("Favores del {}: {}".format(first_player_name, first_player.get_favors()))
    print("Favores del {}: {}".format(second_player_name, second_player.get_favors()))


def main():
    n_throws = 3

    player1 = Player.Player()
    player2 = Player.Player()

    (first_player_name, first_player, second_player) = choose_order(player1, player2)

    assign_favors(first_player, first_player_name, second_player)

    while player1.get_health() > 0 and player2.get_health() > 0:
        first_player.__init__()
        second_player.__init__()

        throw_phase(first_player_name, first_player, second_player, n_throws)
        print("\n\nDELANTERA DEL JUGADOR 1: {}".format(player1.get_forwarded()))
        print("DELANTERA DEL JUGADOR 2: {}".format(player2.get_forwarded()))
        time.sleep(2)
        battle_phase(first_player_name, first_player, second_player)

    print("¡Muchas gracias por jugar!")


main()
