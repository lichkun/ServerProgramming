def get_positive_number(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                print("Value must be positive.")
        except ValueError:
            print("Please enter a valid integer.")

def main():
    x = get_positive_number("Enter x = ")
    y = get_positive_number("Enter y = ")
    print(f"{x} + {y} = {x + y}")

if __name__ == "__main__":
    main()
