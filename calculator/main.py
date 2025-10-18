import sys
from pkg.calculator import Calculator

if __name__ == "__main__":
    if len(sys.argv) > 1:
        expression = sys.argv[1]
        calculator = Calculator()
        result = calculator.evaluate(expression)
        print(result)
    else:
        print("Please provide an expression to evaluate.")