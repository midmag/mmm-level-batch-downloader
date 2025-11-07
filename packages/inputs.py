def input_yes_or_no(prompt: str) -> bool:
    while True:
        inputChoice = input(f"{prompt}\n"
                            f"Enter Y/N: ")

        if inputChoice.lower() == "y":
            return True
        elif inputChoice.lower() == "n":
            return False
        else:
            print("Please enter a valid option\n")


def main():
    choice = input_yes_or_no("Please say Y or N")
    if choice:
        print("You said Y")
    else:
        print("You said N")


if __name__ == "__main__":
    main()
