from random import choice
import inspect


class Cell:
    def __init__(self):
        self.value = 0  # value - значение поля: 1 - крестик; 2 - нолик (по умолчанию 0).

    def __bool__(self):
        return True if not self.value else False


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self):
        self.__n = 3
        self.__coords_cell = [(i, j) for j in range(self.__n) for i in range(self.__n)]
        self.pole = tuple(tuple(Cell() for _ in range(self.__n)) for _ in range(self.__n))
        self.__is_human_win = self.__is_computer_win = self.__is_draw = False

    @property
    def is_human_win(self):
        return self.__is_human_win

    @property
    def is_computer_win(self):
        return self.__is_computer_win

    @property
    def is_draw(self):
        return self.__is_draw

    def init(self):
        self.__init__()

    def human_go(self):
        x, y = map(int, input('Ваш ход: ').split())
        self.__setitem__((x, y), self.HUMAN_X)
        # x, y = choice(self.__coords_cell)
        # self.__setitem__((x, y), self.HUMAN_X)

    def computer_go(self):
        x, y = choice(self.__coords_cell)
        self.__setitem__((x, y), self.COMPUTER_O)
        print(f"Ход компьютера: {x} {y}")

    def search_for_the_winner(self):
        n = self.__n
        result = []

        result.append(tuple(self.pole[i][j].value for j in range(n) for i in range(n) if i == j))
        result.append(tuple(self.pole[i][j].value for j in range(n) for i in range(n) if i + j == n - 1))

        for indx in range(n):
            result.append(tuple(self.pole[i][j].value for j in range(n) for i in range(indx, indx + 1)))
            result.append(tuple(self.pole[j][i].value for j in range(n) for i in range(indx, indx + 1)))

        for i in result:
            if i.count(self.HUMAN_X) == 3:
                self.__is_human_win = True
            elif i.count(self.COMPUTER_O) == 3:
                self.__is_computer_win = True
            elif len(self.__coords_cell) == 0:
                self.__is_draw = True

    def __verify_indx(self, indx):
        if not all(type(i) == int and 0 <= i < self.__n for i in indx):
            raise IndexError('некорректно указанные индексы')

    def __getitem__(self, item):
        self.__verify_indx(item)
        return self.pole[item[0]][item[1]].value

    def __setitem__(self, key, value):
        self.__verify_indx(key)
        if self.pole[key[0]][key[1]]:
            self.pole[key[0]][key[1]].value = value
            self.__coords_cell.remove(key)
            self.search_for_the_winner()
        else:
            print('клетка уже занята')
            caller_function_name = inspect.currentframe().f_back.f_code.co_name  # Поиск функции которая вызвала этот метод
            TicTacToe.__dict__[f"{caller_function_name}"](self)  # Вызываем ту функцию которая вызвала этот метод

    def __bool__(self):
        return not any((self.__is_human_win, self.__is_computer_win, self.__is_draw))

    def show(self):  # отображает игровое поле в консоли
        horizontal_line = ' ' * 3 + '┌' + '┬'.join(['─' * 5] * self.__n) + '┐'
        divider_line = ' ' * 3 + '├' + '┼'.join(['─' * 5] * self.__n) + '┤'
        bottom_line = ' ' * 3 + '└' + '┴'.join(['─' * 5] * self.__n) + '┘'
        numeration_h = " " * 6 + "     ".join(map(str, range(0, self.__n)))

        print("-" * 25)
        print(numeration_h)
        print(horizontal_line)
        for i, row in enumerate(self.pole):
            tmp = []
            for obj in row:
                if obj.value == self.HUMAN_X:
                    tmp.append("X")
                elif obj.value == self.COMPUTER_O:
                    tmp.append("O")
                else:
                    tmp.append(f" ")
            row_str = '  │  '.join(tmp)
            print(f'{i}  │  {row_str}  │  {i}')
            if i < len(self.pole) - 1:
                print(divider_line)
        print(bottom_line)
        print(numeration_h)
        print("-" * 25)



game = TicTacToe()
game.init()

step_game = 0

while game:
    game.show()
    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()
    step_game += 1
game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")
