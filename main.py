from random import randint

class BoardException(Exception):
    pass

class UsedDotBoardException(BoardException):
    def __str__(self):
        return "Выстрел в использованную клетку"

class OutBoardException(BoardException):
    def __str__(self):
        return "Выстрел за пределы поля"

class Dot:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, length: int, bow: Dot, vertical: bool, lives: int):
        self.length: int = length
        self.bow: Dot = bow
        self.vertical: bool = vertical
        self.lives: int = lives

    def dots(self):
        return [Dot(self.bow.x, self.bow.y + i) if self.vertical else Dot(self.bow.x + i, self.bow.y) for i in range(self.length)]


class Board:
    def __init__(self, size: int = 6, hid: bool = False):
        self.board = [['O' for i in range(size)] for j in range(size)]
        self.ships: list = []
        self.hid: bool = hid
        self.live_ships: int = 0

    def __str__(self):
        out = "  "
        out += " ".join([str(i + 1) for i in range(6)]) + "\n"
        for i, line in enumerate(self.board):
            out += str(i + 1) + " " + " ".join('O' if self.hid and i == '◾' else str(i) for i in line) + "\n"
        return out

    def add_ship(self, ship: Ship):
        for dot in ship.dots():
            if self.out(dot):
                return False
            for ship_on_board in self.ships:
                if dot in ship_on_board.dots():
                    return False
                if dot in self.contour(ship_on_board):
                    return False
        self.ships.append(ship)
        self.live_ships += 1
        for dot in ship.dots():
            self.board[dot.x][dot.y] = '◾'
        return True

    def contour(self, ship):
        dots = []
        for dot in ship.dots():
            dots.append(Dot(dot.x + 1, dot.y))
            dots.append(Dot(dot.x - 1, dot.y))
            dots.append(Dot(dot.x, dot.y + 1))
            dots.append(Dot(dot.x, dot.y - 1))
            dots.append(Dot(dot.x + 1, dot.y + 1))
            dots.append(Dot(dot.x + 1, dot.y - 1))
            dots.append(Dot(dot.x - 1, dot.y + 1))
            dots.append(Dot(dot.x - 1, dot.y - 1))
        return dots

    def out(self, dot):
        if 5 < dot.x or dot.x < 0 or 5 < dot.y or dot.y < 0:
            return True

    def shot(self, dot):
        if self.out(dot):
            raise OutBoardException()
        if self.board[dot.x][dot.y] in ['X', 'T']:
            raise UsedDotBoardException()
        for ship in self.ships:
            if dot in ship.dots():
                self.board[dot.x][dot.y] = 'X'
                ship.lives -= 1
                if ship.lives == 0:
                    self.live_ships -= 1
                return False
        self.board[dot.x][dot.y] = 'T'
        return True


class Player:
    def __init__(self, board_self, board_enemy):
        self.board_self: Board = board_self
        self.board_enemy: Board = board_enemy

    def ask(self):
        pass

    def move(self):
        dot = self.ask()
        try:
            if not self.board_enemy.shot(dot):
                return True
        except BoardException as e:
            print(e)
            return True
        return False


class AI(Player):
    def ask(self):
        return Dot(randint(0, 6), randint(0, 6))


class User(Player):
    def ask(self):
        while True:
            input_string = input("Введите координаты: \n").split()

            if len(input_string) != 2:
                print("Необходимо ввести две цифры.")
                continue

            if not (input_string[0].isdigit()) or not (input_string[1].isdigit()):
                print("Необходимо ввести цифры от 1 до 6.")
                continue

            x, y = input_string
            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


class Game:
    def __init__(self):
        self.gamer_human_board = self.random_board(hid=False)
        self.gamer_robot_board = self.random_board(hid=True)

        self.gamer_human: User = User(board_self=self.gamer_human_board, board_enemy=self.gamer_robot_board)
        self.gamer_robot: AI = AI(board_self=self.gamer_robot_board, board_enemy=self.gamer_human_board)

    def random_board(self, hid):
        while True:
            board_tmp = Board(hid=hid)
            ships_lengths = [3, 2, 2, 1, 1, 1]
            for ship_length in ships_lengths:
                for i in range(1000):
                    ship_tmp = Ship(ship_length, Dot(randint(0, 5), randint(0, 5)), bool(randint(0, 1)), ship_length)
                    if not board_tmp.add_ship(ship_tmp):
                        continue
                    else:
                        break
                if i == 999:
                    break
            else:
                return board_tmp


    def greet(self):
        print("Это игра морской бой.")

    def loop(self):
        player = randint(0, 1)
        while(True):
            print("Доска человека")
            print(self.gamer_human_board)
            print("Доска робота")
            print(self.gamer_robot_board)
            if player == 0:
                print("Ходит человек")
                repeat = self.gamer_human.move()
            else:
                print("Ходит робот")
                repeat = self.gamer_robot.move()

            if not repeat:
                player = 1 if player == 0 else 0

            if not self.gamer_human_board.live_ships:
                print("Выиграл робот!")
                break

            if not self.gamer_robot_board.live_ships:
                print("Выиграл человек!")
                break
    def start(self):
        self.greet()
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.start()
