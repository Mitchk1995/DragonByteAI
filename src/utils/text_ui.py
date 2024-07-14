def display_text(text):
    print(text)

def display_character_stats(character):
    print(f"Name: {character.name}")
    print(f"Class: {character.char_class}")
    print(f"Race: {character.race}")
    print("Stats:")
    for stat, value in character.stats.items():
        print(f"  {stat.capitalize()}: {value}")

def get_user_input(prompt):
    return input(prompt)

def display_menu(options):
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = input("Enter your choice: ")
    return choice
