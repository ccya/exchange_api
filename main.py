"""
Create two threads. One for pulling index_price for api; one to run in background
to write the newest index_price to the database / memory.

"""
from calculator import Calculator
def main():
	calculator = Calculator()
	print(calculator.calculate())


if __name__ == '__main__':
    main()