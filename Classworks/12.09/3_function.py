# Функції
# Синтаксис
# Scope, взаємодія з глобальною областю
# Overloading / параметричний поліморфізм

x = 10

def get_x() -> int:
    return x

def set_x(value:int) -> None:
    global x
    x = value


def main():
    """ Main function """
    print("Main works")
    after_main()
    print(factorial(5))
    show(10)
    show("Hello world")
    show(10, 20.0)
    print(get_x())

# виклик успішний - ознака hoisting
def after_main():
    print("Function declared after the main")


def factorial(n):
    """ Returns the factorial of n """
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

def show(n:int) -> None:
    print(n)

# перевантаження функції немає. Є переозначення - заміна.
# Повторна декларація скасовує попередню
# Кількість параметрів при виклику має збігатись з декларованою
# Відсутні парметри = помилка
def show( n:int, m:float ) -> None :
    print( n, m )

def show( n:int, m:float = 0.0 ) -> None :
    print( n, m )               # Поліморфізм досягається параметрами за замовчанням

if __name__ == '__main__': main()
# дотримання модульного принципу - файли з кодом можуть
# підключатись як додаткові модулі інших процесів або
# самостійно виконуватись, утворюючи новий процес.
# __name__ дозволяє розрізняти схему запуску