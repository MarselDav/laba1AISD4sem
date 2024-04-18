from colorama import init, Fore

init(autoreset=True)


def test(map_test: dict, function):
    i = 0
    for value in map_test:
        if function(value) == map_test[value]:
            print(Fore.GREEN + f'Test {i} success')
        else:
            print(f"text: {value}, your answer: {function(value)}, right answer: {map_test[value]}")
            print(Fore.RED + f'Test {i} error')
        i += 1
