
from functions.run_python_file import run_python_file


def test_run_python_file():
    # Test case 1: Valid Python file
    result = run_python_file("calculator", "main.py")
    print("Result for main.py:")
    print(result)
    print()

    # Test case 2: Valid Python file with arguments
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result for main.py with arguments:")
    print(result)
    print()

    # Test case 3: Run calculator tests
    result = run_python_file("calculator", "tests.py")
    print("Result for tests.py:")
    print(result)
    print()

    # Test case 4: File outside working directory
    result = run_python_file("calculator", "../main.py")
    print("Result for ../main.py:")
    print(result)
    print()

    # Test case 5: Nonexistent file
    result = run_python_file("calculator", "nonexistent.py")
    print("Result for nonexistent.py:")
    print(result)
    print()

    # Test case 6: Not a Python file
    result = run_python_file("calculator", "lorem.txt")
    print("Result for lorem.txt:")
    print(result)
    print()


if __name__ == "__main__":
    test_run_python_file()
