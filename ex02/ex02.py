def multiply_all(*args: int) -> int:
    result = 1
    for a in args:
        result *= a
    return result

if __name__ == "__main__":
    print(multiply_all(1, 2, 3, 4))  # Output: 24
    print(multiply_all(5, 6, 7))     # Output: 210