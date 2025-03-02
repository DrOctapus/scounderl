import random

# random.seed("demo")

RESET = "\033[0m"
GRAY = "\033[90m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"


def color_card(card):
    if "M" in card:
        return f"{BLUE}{card}{RESET}"
    elif "H" in card:
        return f"{RED}{card}{RESET}"
    elif "W" in card:
        return f"{GREEN}{card}{RESET}"
    return card


def show(case, a="", b="", c="", d=""):
    if case == 1:
        print(f"{GRAY}------------- Deck: {CYAN}{a}{GRAY} -------------{RESET}")
    elif case == 2:
        print("\n" + " ".join(color_card(card) for card in a))
        print(f"{YELLOW}Health:{RESET} {CYAN}{b}{RESET} | {YELLOW}Weapon:{RESET} {CYAN}{c}{RESET} {GRAY}{d}{RESET}")
    elif case == 3:
        print(f"{YELLOW}Choose R to run\nPut B after card to fight mosnter bare-handed{RESET}")
    elif case == 4:
        print(f"\n{GRAY}------------- DEFEAT -------------{RESET}")
    elif case == 5:
        print(f"\n{GRAY}------------- VICTORY! You survived! -------------{RESET}")


health = 20
weapon = 0
fights = []
room = []
run = 0
use_potion = False


weapons = [str(i) + "W" for i in range(2, 11)]
pots = [str(i) + "H" for i in range(2, 11)]
monsters = [str(i) + "M" for i in range(2, 15)]
monsters += [str(i) + "M" for i in range(2, 15)]

dungeon = weapons + pots + monsters

random.shuffle(dungeon)


while True:
    while len(room) < 4 and len(dungeon) > 0:
        room.append(dungeon.pop(0))

    use_potion = False
    bearhanded = False

    if run > 0:
        run -= 1

    show(1, len(dungeon))

    while len(room) > 1 or len(dungeon) == 0:
        show(2, room, health, weapon, fights)

        while True:
            if len(room) == 4 and run == 0:
                show(3)
            answer = input(f"{YELLOW}Choose card:{RESET} [{CYAN}{'1' if len(room) == 1 else f'1 - {len(room)}'}{RESET}]\n")
            try:
                if len(room) == 4 and run == 0 and answer.lower() == "r":
                    random.shuffle(room)
                    dungeon += room
                    room = []
                    run = 2
                    break

                if "b" in answer.lower():
                    answer = answer.replace("b", "")
                    bearhanded = True

                answer = int(answer)
                if 1 <= answer <= len(room):
                    answer -= 1
                    break
            except ValueError:
                pass

        if run == 2:
            break

        choice = room[answer]

        value = int(choice[:-1])

        if "M" in choice:
            if (len(fights) == 0 or fights[-1] > value) and weapon > 0 and not bearhanded:
                if weapon < value:
                    health -= value - weapon
                fights.append(value)
            else:
                health -= value
        elif "H" in choice:
            if not use_potion:
                use_potion = True
                health += value
                if health > 20:
                    health = 20
        elif "W" in choice:
            weapon = value
            fights = []

        del room[answer]

        if health <= 0:
            health = 0
            show(4)
            exit()

        if len(room) == 0 and len(dungeon) == 0:
            show(5)
            exit()
