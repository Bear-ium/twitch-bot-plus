import os
from src.TwitchBotPlus.core import Bot
from typing import Callable

env_path = os.path.join(os.path.dirname(__file__), '.env')

CommandFn = Callable[
    [list[str], str],
    tuple[str, bool]
]

def add(args: list[str], user: str) -> tuple[str, bool]:
    try:
        num1 = int(args[0])
        num2 = int(args[1])
        return (f"{user}: {num1 + num2}", False)
    except (IndexError, ValueError):
        return (f"{user}: Usage: !add <num1> <num2>", False)

def echo(args: list[str], user: str) -> tuple[str, bool]:
    return (f"{user}: {' '.join(args)}", False)

def shutdown(args: list[str], user: str) -> tuple[str, bool]:
    return (f"Goodbye {user}!", True)
    

COMMANDS: dict[str, CommandFn] = {
    "add": add,
    "echo": echo,
    "shutdown": shutdown
}



bot = Bot(
    COMMANDS=COMMANDS,
    ENV_Path=env_path,
    HANDLE="-"
)

bot.start()