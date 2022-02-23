import numpy as np

from hw03.mixins_matrix import ConsoleRepresentationMixin, WritingToFileMixin, MixinsMatrix


class HashableMatrixMixin:
    def __hash__(self):
        """
        Calculate sum elements of matrix by module of 107
        """
        sum_elem = 0
        for row in self._matrix:
            sum_elem += sum(row)
        return int(sum_elem % 107)


class Matrix(
    HashableMatrixMixin,
    WritingToFileMixin,
    ConsoleRepresentationMixin
):
    def __init__(self, matrix):
        if len(matrix) == 0:
            raise ValueError("wrong dimension of matrix")
        self._shape = len(matrix), len(matrix[0])
        self._matrix = []

        for row in matrix:
            if len(row) != len(matrix[0]):
                raise ValueError("wrong rows size")
            self._matrix.append(list(row))

    def __add__(self, other: 'Matrix'):
        if self._shape != other._shape:
            raise ValueError(f"wrong shapes of matrix")
        return Matrix(
            [
                [
                    self._matrix[i][j] + other._matrix[i][j]
                    for j in range(self._shape[1])
                ]
                for i in range(self._shape[0])
            ]
        )

    def __mul__(self, other: 'Matrix'):
        if self._shape != other._shape:
            raise ValueError(f"wrong shapes of matrix")
        return Matrix(
            [
                [
                    self._matrix[i][j] * other._matrix[i][j]
                    for j in range(self._shape[1])
                ]
                for i in range(self._shape[0])
            ]
        )

    def __eq__(self, other: 'Matrix'):
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                if self._matrix[i][j] != other._matrix[i][j]:
                    return False
        return True

    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        if self._shape != other._shape[::-1]:
            raise ValueError(f"wrong shapes of matrix")
        return Matrix(
            [
                [
                    sum(x * y for x, y in zip(row, col))
                    for col in zip(*other._matrix)
                ]
                for row in self._matrix
            ]
        )

    __hash__ = HashableMatrixMixin.__hash__


def hard():
    while True:
        a = Matrix(np.random.randint(0, 10, (10, 10)))
        b = Matrix(np.random.randint(0, 10, (10, 10)))
        c = Matrix(np.random.randint(0, 10, (10, 10)))
        d = b
        ab = a @ b
        cd = c @ d
        if hash(a) == hash(c) and (a != c) and (ab != cd):
            a.write_to_file(f"artifacts/hard/A.txt")
            b.write_to_file(f"artifacts/hard/B.txt")
            c.write_to_file(f"artifacts/hard/C.txt")
            d.write_to_file(f"artifacts/hard/D.txt")
            ab.write_to_file(f"artifacts/hard/AB.txt")
            cd.write_to_file(f"artifacts/hard/CD.txt")
            with open(f"artifacts/hard/hash.txt", "w") as f:
                f.write(f"Hash AB:\n{hash(ab)}\nhash CD:\n{hash(cd)}")
            break


if __name__ == "__main__":
    np.random.seed(0)
    m1 = Matrix(np.random.randint(0, 10, (10, 10)))
    m2 = Matrix(np.random.randint(0, 10, (10, 10)))
    sum_m = m1 + m2
    mul_m = m1 * m2
    matmul_m = m1 @ m2
    sum_m.write_to_file(f"artifacts/easy/matrix+.txt")
    mul_m.write_to_file(f"artifacts/easy/matrix*.txt")
    matmul_m.write_to_file(f"artifacts/easy/matrix@.txt")

    np.random.seed(0)
    m1 = MixinsMatrix(np.random.randint(0, 10, (10, 10)))
    m2 = MixinsMatrix(np.random.randint(0, 10, (10, 10)))
    sum_m = m1 + m2
    mul_m = m1 * m2
    matmul_m = m1 @ m2
    sum_m.write_to_file(f"artifacts/medium/matrix+.txt")
    mul_m.write_to_file(f"artifacts/medium/matrix*.txt")
    matmul_m.write_to_file(f"artifacts/medium/matrix@.txt")

    np.random.seed(0)
    hard()
