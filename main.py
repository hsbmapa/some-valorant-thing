from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from src.auth import ValorantClient


def main():
    option = inquirer.rawlist(
        message="Select an action: ",
        choices=[
            Choice(name="Authenticate", value="auth", enabled=True),
            Separator(),
            Choice(name="Exit", value=None),
        ],
        default=None,
    ).execute()
    if option == "auth":
        action = inquirer.rawlist(
            message="Select an action: ",
            choices=[
                Choice(name ="Instalock Agent", value="instalock", enabled=True),
                Separator(),
                Choice(name="Exit", value=None),
            ],
            default=None,
        ).execute()
    else:
        exit(1)
    if action == "instalock":
        client = ValorantClient()

        print(f"Hello {client.get_ingame_name()}")
        print(client.get_session_status())
        agent = input("Enter agent to lock: ")
        client.lock_agent(agent)
        print(f"Locked {agent}, enjoy the game!")
    else:
        exit(1)
        
if __name__ == "__main__":
    main()
