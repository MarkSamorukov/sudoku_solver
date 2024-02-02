# sudoku solver

import help_functions as hf
import copy


def create_field(field):
    for i in range(9):
        for j in range(9):
            if field[i][j] == 0:
                field[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    return field


def rows_inspection(field, mode):
    if mode == 0:
        position = "этой строке"
    elif mode == 1:
        position = "этом столбце"
    else:
        position = "этом квадрате"
    for i in range(9):
        tmp = []
        for j in range(9):
            if type(field[i][j]) == int:
                tmp.append(field[i][j])
        for j in range(9):
            if type(field[i][j]) == list:
                for number in tmp:
                    if number in field[i][j]:
                        field[i][j].remove(number)
                        if mode == 0:
                            ii, jj = i + 1, j + 1
                        elif mode == 1:
                            ii, jj = j + 1, i + 1
                        else:
                            ii, jj = hf.transformation_index(i, j)
                        with open("logs.txt", "a", encoding="UTF-8") as logs:
                            logs.write(
                                f"На позиции ({ii}, {jj}) не может стоять число {number}, так как это число уже есть в {position}\n")

    return field


def columns_inspection(field):
    return hf.transpose_matrix(rows_inspection(hf.transpose_matrix(field), 1))


def squares_inspection(field):
    return hf.inverse_sqares_transfirmation(rows_inspection(hf.squares_transformation(field), 2))


def numbers_detection(field):
    change_flag = False
    for i in range(9):
        for j in range(9):
            if type(field[i][j]) == list:
                if len(field[i][j]) == 1:
                    field[i][j] = field[i][j][0]
                    change_flag = True
                    with open("logs.txt", "a", encoding="UTF-8") as logs:
                        logs.write(f"Значит на позиции ({i}, {j}) стоит число {field[i][j]}\n")

    return field, change_flag


def uniqueness_detector_rows(field, mode):
    if mode == 0:
        position = "в этой строке"
    elif mode == 1:
        position = "в этом столбце"
    else:
        position = "в этом квадрате"
    change_flag = False
    for i in range(9):
        counter = {}
        for j in range(9):
            if type(field[i][j]) == list:
                for elem in field[i][j]:
                    if elem in counter:
                        counter[elem] += 1
                    else:
                        counter[elem] = 1
        for number in counter:
            if counter[number] == 1:
                for j in range(9):
                    if type(field[i][j]) == list:
                        if number in field[i][j]:
                            field[i][j] = number
                            change_flag = True
                            if mode == 0:
                                ii, jj = i + 1, j + 1
                            elif mode == 1:
                                ii, jj = j + 1, i + 1
                            else:
                                ii, jj = hf.transformation_index(i, j)
                            with open("logs.txt", "a", encoding="UTF-8") as logs:
                                logs.write(
                                    f"Значит на позиции ({ii}, {jj}) стоит число {number}, поскольку в {position} число {number} может быть только на этой позиции\n")
    return field, change_flag


def uniqueness_detector_columns(field):
    field = hf.transpose_matrix(field)
    field, change_flag = uniqueness_detector_rows(field, 1)
    field = hf.transpose_matrix(field)

    return field, change_flag


def uniqueness_detector_squares(field):
    field = hf.squares_transformation(field)
    field, change_flag = uniqueness_detector_rows(field, 2)
    field = hf.inverse_sqares_transfirmation(field)

    return field, change_flag


def linear_rows_parsing(field, mode):
    squares = hf.squares_transformation(field)
    change_flag = False
    for square_index in range(9):
        tmp = {}
        for number in range(1, 10):
            for elem_index in range(9):
                elem = squares[square_index][elem_index]
                if type(elem) == list:
                    if number in elem:
                        if number in tmp:
                            tmp[number].append(elem_index)
                        else:
                            tmp[number] = [elem_index]

        for number in tmp:
            if all(element in [0, 1, 2] for element in tmp[number]):
                for square_layer_index in range(9):
                    if square_layer_index // 3 == square_index // 3 and square_layer_index != square_index:
                        for elem_index in [0, 1, 2]:
                            if type(squares[square_layer_index][elem_index]) == list:
                                if number in squares[square_layer_index][elem_index]:
                                    squares[square_layer_index][elem_index].remove(number)
                                    change_flag = True
                                    if mode == 0:
                                        ii, jj = hf.transformation_index(square_layer_index, elem_index)
                                        position = "этой строке"
                                    else:
                                        jj, ii = hf.transformation_index(square_layer_index, elem_index)
                                        position = "этом столбце"
                                    with open("logs.txt", "a", encoding="UTF-8") as logs:
                                        logs.write(
                                            f"На позиции ({ii}, {jj}) не может быть числа {number}, поскольку в большом кважрате под номером {square_index} число {number} может стоять толбко в {position}\n")
            elif all(element in [3, 4, 5] for element in tmp[number]):
                for square_layer_index in range(9):
                    if square_layer_index // 3 == square_index // 3 and square_layer_index != square_index:
                        for elem_index in [3, 4, 5]:
                            if type(squares[square_layer_index][elem_index]) == list:
                                if number in squares[square_layer_index][elem_index]:
                                    squares[square_layer_index][elem_index].remove(number)
                                    change_flag = True
                                    if mode == 0:
                                        ii, jj = hf.transformation_index(square_layer_index, elem_index)
                                        position = "этой строке"
                                    else:
                                        jj, ii = hf.transformation_index(square_layer_index, elem_index)
                                        position = "этом столбце"
                                    with open("logs.txt", "a", encoding="UTF-8") as logs:
                                        logs.write(
                                            f"На позиции ({ii}, {jj}) не может быть числа {number}, поскольку в большом кважрате под номером {square_index} число {number} может стоять толбко в {position}\n")
            elif all(element in [6, 7, 8] for element in tmp[number]):
                for square_layer_index in range(9):
                    if square_layer_index // 3 == square_index // 3 and square_layer_index != square_index:
                        for elem_index in [6, 7, 8]:
                            if type(squares[square_layer_index][elem_index]) == list:
                                if number in squares[square_layer_index][elem_index]:
                                    squares[square_layer_index][elem_index].remove(number)
                                    change_flag = True
                                    if mode == 0:
                                        ii, jj = hf.transformation_index(square_layer_index, elem_index)
                                        position = "этой строке"
                                    else:
                                        jj, ii = hf.transformation_index(square_layer_index, elem_index)
                                        position = "этом столбце"
                                    with open("logs.txt", "a", encoding="UTF-8") as logs:
                                        logs.write(
                                            f"На позиции ({ii}, {jj}) не может быть числа {number}, поскольку в большом кважрате под номером {square_index} число {number} может стоять толбко в {position}\n")

    return hf.inverse_sqares_transfirmation(squares), change_flag


def linear_columns_parsing(field):
    field = hf.transpose_matrix(field)
    field, change_flag = linear_rows_parsing(field, 1)
    field = hf.transpose_matrix(field)
    return field, change_flag

def assumption(field):
    min_length = 100
    min_elem = (10, 10)
    for i in range(9):
        for j in range(9):
            if type(field[i][j]) == list and len(field[i][j]) != 0:
                if len(field[i][j]) < min_length:
                    min_length = len(field[i][j])
                    min_elem = (i, j)
    new_field = []
    for i in range(9):
        tmp = []
        for j in range(9):
            if (i, j) != min_elem:
                tmp.append(field[i][j])
            else:
                tmp.append(field[i][j][0])
        new_field.append(tmp)

    return new_field, min_elem

def solve(field):
    change_flag = True
    while change_flag:
        field = rows_inspection(field, 0)

        field = columns_inspection(field)

        field = squares_inspection(field)

        field, change_flag = numbers_detection(field)

        if not change_flag:
            field, change_flag = uniqueness_detector_rows(field, 0)
        if not change_flag:
            field, change_flag = uniqueness_detector_columns(field)
        if not change_flag:
            field, change_flag = uniqueness_detector_squares(field)
        if not change_flag:
            field, change_flag = linear_rows_parsing(field, 0)
        if not change_flag:
            field, change_flag = linear_columns_parsing(field)

    return field

def is_solved(field):
    for row in field:
        for elem in row:
            if type(elem) == list and len(elem) == 0:
                return True
    return False

def is_valid(field):
    pass
def is_correct(field):
    for row in field:
        for elem in row:
            if type(elem) == list:
                return False

    for row in field:
        if set(row) != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
            return False
    field = hf.transpose_matrix(field)

    for row in field:
        if set(row) != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
            return False

    field = hf.squares_transformation(field)

    for row in field:
        if set(row) != {1, 2, 3, 4, 5, 6, 7, 8, 9}:
            return False

    return True

def recursion_solve(field):

    while not is_correct(field):

        for i in range(9):
            for j in range(9):
                if type(field[i][j]) == list and len(field[i][j]) > 0:
                    elem = field[i][j]
                    field[i][j] = elem[0]
                    ii = i
                    jj = j

        field = solve(field)
        old_field = copy.deepcopy(field)

        if not is_solved(field):
            field = recursion_solve(field)

        if not is_correct(field):
            field = copy.deepcopy(old_field)
            field[ii][jj] = elem[1:]
            return field


    return field


with open("logs.txt", "w") as logs:
    logs.write("")

with open("input.txt", "r") as input_field:
    field = []

    for row in input_field.readlines():
        row = list(map(int, row.split()))
        field.append(row)

field = create_field(field)

field = solve(field)

#field = recursion_solve(field)

# while not is_correct(field):
#     field, elem = assumption(field)
#     field = solve(field)
#     if not is_correct(field):
#         field[elem[0]][elem[1]] = field[elem[0]][elem[1]][1:]

with open("result.txt", "w", encoding="UTF-8") as result:
    max_length = max(len(str(elem)) for row in field for elem in row)
    kk = 0
    for row in field:
        kk += 1
        k = 0
        for elem in row:
            k += 1
            result.write(str(elem).center(max_length))
            if k % 3 == 0:
                result.write(" | ")
            else:
                result.write(" ")
        result.write("\n")
        if kk % 3 == 0:
            result.write("-" * max_length * 23 + "\n")
