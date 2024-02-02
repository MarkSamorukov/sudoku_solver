def transpose_matrix(matrix, *args):
    transposed_matrix = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            transposed_matrix[i][j] = matrix[j][i]

    return transposed_matrix


def squares_transformation(square):
    rows = []

    for i in range(9):
        for j in range(9):
            row_index = (i // 3) * 3 + (j // 3)

            if len(rows) <= row_index:
                rows.append([square[i][j]])
            else:
                rows[row_index].append(square[i][j])

    return rows


def inverse_sqares_transfirmation(rows):
    square = [[0 for _ in range(9)] for _ in range(9)]

    for i in range(9):
        for j in range(9):
            square_index = (i // 3) * 3 + (j // 3)
            position_index = (i % 3) * 3 + (j % 3)

            square[square_index][position_index] = rows[i][j]

    return square

def transformation_index(i, j):
    original_i = (i // 3) * 3 + (j // 3)
    original_j = (i % 3) * 3 + (j % 3)
    return original_i + 1, original_j + 1

"""
field = []
for _ in range(9):
    row = list(map(int, input().split()))
    field.append(row)

field = squares_transformation(field)

for i in range(9):
    print(*field[i])

field = inverse_sqares_transfirmation(field)
print("\n")

for i in range(9):
    print(*field[i])

print(transformation_index(0, 7))
"""
