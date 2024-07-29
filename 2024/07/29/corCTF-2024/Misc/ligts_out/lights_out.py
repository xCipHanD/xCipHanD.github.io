import random
import time
import sys
import os

#!/usr/bin/env python


def generate_random_board(n: int) -> list[int]:
    """
    生成一个随机的 n x n 灯泡板。

    参数:
        n (int): 灯泡板的大小 (n x n)。

    返回:
        list[int]: 代表灯泡板的列表，其中每个元素
                     要么是 0 (关闭) 要么是 1 (打开)。
    """
    board = [random.randint(0, 1) for _ in range(n * n)]
    return board


def create_vector_representations(n: int) -> list[list[int]]:
    """
    为 n x n 灯泡板上的每个位置创建向量表示。

    参数:
        n (int): 灯泡板的大小 (n x n)。

    返回:
        list[list[int]]: 表示切换每个灯泡的效果的向量列表。
    """
    vectors = []
    for i in range(n * n):
        vector = [0] * (n * n)
        vector[i] = 1
        if i % n != 0:
            vector[i - 1] = 1  # 左
        if i % n != n - 1:
            vector[i + 1] = 1  # 右
        if i >= n:
            vector[i - n] = 1  # 上
        if i < n * (n - 1):
            vector[i + n] = 1  # 下
        vectors.append(vector)
    return vectors


def create_augmented_matrix(
    vectors: list[list[int]], board: list[int]
) -> list[list[int]]:
    """
    从向量和板的状态创建增广矩阵。

    参数:
        vectors (list[list[int]]): 向量表示。
        board (list[int]): 板的当前状态。

    返回:
        list[list[int]]: 增广矩阵。
    """
    matrix = [vec + [board[i]] for i, vec in enumerate(vectors)]
    return matrix


def print_board(board: list[int], n: int) -> str:
    """
    生成 n x n 灯泡板的字符串表示。

    参数:
        board (list[int]): 灯泡板的状态。
        n (int): 灯泡板的大小 (n x n)。

    返回:
        str: 灯泡板的字符串表示。
    """
    board_string = ""
    for i in range(n):
        row = ""
        for j in range(n):
            row += "#" if board[i * n + j] else "."
        board_string += row + "\n"
    return board_string


def gauss_jordan_elimination(matrix: list[list[int]]) -> list[list[int]]:
    """
    对给定的矩阵执行 Gauss-Jordan 消元，得到其行简化阶梯形式 (RREF)。

    参数:
        matrix (list[list[int]]): 要减少的矩阵。

    返回:
        list[list[int]]: RREF 形式的矩阵。
    """
    rows, cols = len(matrix), len(matrix[0])
    r = 0
    for c in range(cols - 1):
        if r >= rows:
            break
        pivot = None
        for i in range(r, rows):
            if matrix[i][c] == 1:
                pivot = i
                break
        if pivot is None:
            continue
        if r != pivot:
            matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        for i in range(rows):
            if i != r and matrix[i][c] == 1:
                for j in range(cols):
                    matrix[i][j] ^= matrix[r][j]
        r += 1
    return matrix


def is_solvable(matrix: list[list[int]]) -> bool:
    """
    检查给定的增广矩阵是否表示一个可解的系统。

    参数:
        matrix (list[list[int]]): 增广矩阵。

    返回:
        bool: 如果系统可解则为 True，否则为 False。
    """
    rref = gauss_jordan_elimination(matrix)
    for row in rref:
        if row[-1] == 1 and all(val == 0 for val in row[:-1]):
            return False
    return True


def get_solution(board: list[int], n: int) -> list[int] | None:
    """
    如果存在，获取 Lights Out 灯泡板的解。

    参数:
        board (list[int]): 灯泡板的当前状态。
        n (int): 灯泡板的大小 (n x n)。

    返回:
        list[int] | None: 表示解的列表，如果不存在解则为 None。
    """
    vectors = create_vector_representations(n)
    matrix = create_augmented_matrix(vectors, board)
    if not is_solvable(matrix):
        return None
    rref_matrix = gauss_jordan_elimination(matrix)
    # DEBUG
    # x = [row[-1] for row in rref_matrix[:n * n]]
    # xx = ""
    # for i in x:
    #     xx += "#" if i else "."
    # print(xx)
    # END DEBUG
    print("\n")
    print(board)
    return [row[-1] for row in rref_matrix[: n * n]]


def check_solution(board: list[int], solution: list[int], n: int) -> bool:
    """
    检查给定的解是否解决了 Lights Out 灯泡板。

    参数:
        board (list[int]): 灯泡板的当前状态。
        solution (list[int]): 提议的解决方案。
        n (int): 灯泡板的大小 (n x n)。

    返回:
        bool: 如果解决方案正确则为 True，否则为 False。
    """
    for i in range(n * n):
        if solution[i] == 1:
            board[i] ^= 1
            if i % n != 0:
                board[i - 1] ^= 1  # 左
            if i % n != n - 1:
                board[i + 1] ^= 1  # 右
            if i >= n:
                board[i - n] ^= 1  # 上
            if i < n * (n - 1):
                board[i + n] ^= 1  # 下
    return all(val == 0 for val in board)


def main() -> None:
    """
    生成一个 Lights Out 灯泡板，发送给客户端，
    并检查客户端的解决方案。
    """
    print(
        "\n欢迎来到 Lights Out！\n"
        "\n游戏的目标是关闭板上的所有灯泡。\n"
        "您可以通过输入字符串格式的位置来切换任何灯泡，\n"
        "其中 # 表示打开，. 表示关闭。\n"
        "每次切换还会翻转其相邻灯泡的状态（上方、下方、左侧、右侧）。\n"
        "尝试关闭所有灯泡以获胜！\n"
        "\n将您的解决方案作为 # 和 . 的字符串输入\n"
        "对于所有的板位置，从左到右，从上到下（例如，..##...#。）\n"
        "\n示例\n"
        "要解决以下板：\n\n"
        "\t###\n\t#.#\n\t.##\n\n"
        "您的解决方案将是：..##...#。\n\n\n"
    )
    sys.stdout.flush()

    while True:
        n = random.randint(15, 25)
        board = generate_random_board(n)
        solution = get_solution(board, n)
        if solution is None:
            continue
        print("\nLights Out 灯泡板：\n\n")
        print(print_board(board, n))
        print("\n您的解决方案：")
        print("\n" + "".join("#" if val else "." for val in solution))
        sys.stdout.flush()

        start_time = time.time()
        user_input = input()[:1024].strip()

        if time.time() - start_time > 10:
            print("\n\n超时。生成一个新的板...\n")
            sys.stdout.flush()
            continue

        user_solution = [1 if c == "#" else 0 for c in user_input]
        if len(user_solution) == n * n and check_solution(board[:], user_solution, n):
            print(os.environ.get("FLAG", "corctf{test_flag}"))
            sys.stdout.flush()
            break
        print("\n\n不正确的解决方案。生成一个新的板...\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
