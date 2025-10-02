import curses
from curses.textpad import rectangle
import hashlib
import os
from dataclasses import dataclass, asdict
import json
from typing import Optional

USER_FILE = "users.json"


@dataclass
class User:
    username: str
    salt: str
    password: str
    # email: str = ""
    email: Optional[str] = None


class AuthenticatorBackend:
    def __init__(self, user_file) -> None:
        self.user_file = user_file
        # Dictionary returned from load_users()
        self.users = self.load_users(user_file)

    @staticmethod
    def load_users(user_file) -> dict:
        users = {}
        if os.path.exists(user_file):
            with open(user_file, "r") as f:
                users_dict = json.load(f)
                for username, user_data in users_dict.items():
                    users[username] = User(**user_data)
        return users

    def add_or_update_user(self, user: User) -> None:
        # users:dict = AuthenticatorBackend.load_users()
        self.users[user.username] = user

    @staticmethod
    def make_user(username: str, password: str) -> User:
        salt, password_hash = AuthenticatorBackend.hash_password(password)
        current_user = User(username, salt, password_hash)
        return current_user

    def save_users(self) -> None:
        users_dict = {uname: asdict(u) for uname, u in self.users.items()}
        with open(USER_FILE, "w") as f:
            json.dump(users_dict, f, indent=4)

    @staticmethod
    def hash_password(password: str, salt=None):
        if salt is None:
            salt = os.urandom(16).hex()
        pwd_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100_000
        )
        return salt, pwd_hash.hex()

    def find_user(self, username: str) -> User | None:
        return self.users.get(username)

    @staticmethod
    def verify_password(password_attempt, user: User) -> bool:
        stored_salt = user.salt
        stored_hash = user.password
        _, attempt_hash = AuthenticatorBackend.hash_password(
            password_attempt, stored_salt
        )
        return attempt_hash == stored_hash


class TuiFrontend:
    def __init__(self, stdscr, backend) -> None:
        self.stdscr = stdscr
        self.backend = backend

    def __get_input(self, prompt, y, x, width, hide_input=False):
        rectangle(self.stdscr, y - 1, x - 1, y + 1, x + width)
        self.stdscr.addstr(y, x - len(prompt) - 1, prompt)
        self.stdscr.move(y, x)
        if not hide_input:
            curses.echo()
            value = self.stdscr.getstr().decode()
            curses.noecho
            return value
        value = ""
        curses.noecho()
        while True:
            ch = self.stdscr.getch()
            if ch in (10, 13):  # Enter key
                break
            elif ch in (8, 127, 263):  # Backspace
                if value:
                    value = value[:-1]
                    y_, x_ = self.stdscr.getyx()
                    self.stdscr.move(y_, x_ - 1)
                    self.stdscr.delch()
            else:
                value += chr(ch)
                self.stdscr.addch(42)  # Show '*'
        return value

    def get_uname_pwd(self, start_y: int, start_x: int, width: int, add_user=False):
        self.stdscr.clear()
        # rectangle(self.stdscr, start_y - 1, start_x -
        #           1, start_y + 1, start_x + width)

        username = self.__get_input("Username:", start_y, start_x, width)
        password = None
        if not add_user:
            password = self.__get_input(
                "Password:", start_y + 3, start_x, width, hide_input=True
            )
            self.stdscr.refresh()
            return username, password

        while True:
            self.stdscr.move(start_y + 3, start_x)
            self.stdscr.clrtoeol()
            password1 = self.__get_input(
                "Password:", start_y + 3, start_x, width, hide_input=True
            )
            self.stdscr.move(start_y + 5, start_x)
            self.stdscr.clrtoeol()
            password2 = self.__get_input(
                "Retype password:", start_y + 5, start_x, width, hide_input=True
            )
            if password1 != password2:
                self.stdscr.move(start_y + 3, start_x)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(
                    start_y + 3, start_x, "Passwords do not match. Try again."
                )
                self.stdscr.refresh()
                curses.napms(1500)
                self.stdscr.move(start_y + 3, start_x)
                self.stdscr.clrtoeol()
                continue

            self.stdscr.refresh()
            return username, password1

    def signed_in(self, user: User):
        self.stdscr.clear()
        self.stdscr.addstr("Function under construction")
        self.stdscr.refresh()
        self.stdscr.addstr(30, 10, "Press any key to continue")
        self.stdscr.getch()

    def run(self):
        curses.curs_set(1)
        self.stdscr.clear()
        max_y, max_x = self.stdscr.getmaxyx()

        form_width = 40
        start_y = max_y // 2 - 2
        start_x = (max_x - form_width) // 2

        options_list = ["Sign in", "Sign up", "Exit"]

        while True:
            self.stdscr.clear()
            option = self.menu_system(start_y, start_x, options_list)

            if option == 1:  # Sign in option
                username, password = self.get_uname_pwd(start_y, start_x, 20)
                user = self.backend.find_user(username)
                if user is None:
                    self.stdscr.clear()
                    self.stdscr.addstr(start_y, start_x, "User not found!")
                    self.stdscr.refresh()
                    curses.napms(1500)
                    continue
                if not AuthenticatorBackend.verify_password(password, user):
                    self.stdscr.clear()
                    self.stdscr.addstr(start_y, start_x, "Password incorrect!")
                    self.stdscr.refresh()
                    curses.napms(1500)
                    continue
                self.stdscr.clear()
                self.stdscr.addstr(start_y, start_x, "Sign in successful")
                self.stdscr.refresh()
                curses.napms(600)
                self.signed_in(user)

            elif option == 2:  # Add user (sign up)
                username, password = self.get_uname_pwd(
                    start_y, start_x, 20, add_user=True
                )
                if self.backend.find_user(username) is not None:
                    self.stdscr.clear()
                    self.stdscr.addstr(start_y, start_x, "User already exists!")
                    self.stdscr.refresh()
                    curses.napms(1500)
                    continue

                user = AuthenticatorBackend.make_user(username, password)
                self.backend.add_or_update_user(user)
                self.stdscr.clear()
                self.stdscr.addstr(start_y, start_x, "User added successfully")
                self.stdscr.refresh()
                curses.napms(600)
                self.signed_in(user)

            elif option == 3:
                self.backend.save_users()  # Write ram users to disc
                return  # Clean exit of program
            else:
                raise ValueError("Index specified is outside options.")

    def menu_system(self, start_y, start_x, menu_items) -> int:
        curses.curs_set(0)
        selected = 0

        while True:
            self.stdscr.clear()
            for index, item in enumerate(menu_items):
                x = start_x
                y = start_y + index
                if index == selected:
                    self.stdscr.addstr(y, x, f"{index + 1}. {item}", curses.A_REVERSE)
                else:
                    self.stdscr.addstr(y, x, f"{index + 1}. {item}")
            self.stdscr.refresh()

            key = self.stdscr.getkey()

            if key == "\n":
                curses.curs_set(1)
                return selected + 1
            elif key == "k":
                selected = (selected - 1) % len(menu_items)
            elif key == "j":
                selected = (selected + 1) % len(menu_items)


def main(stdscr) -> None:
    backend = AuthenticatorBackend(USER_FILE)
    frontend = TuiFrontend(stdscr, backend)
    frontend.run()


if __name__ == "__main__":
    curses.wrapper(main)
