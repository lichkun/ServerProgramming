# оператор та операції
t = 10, 20, 30
x, y, w = t
print( x, type(x) )

x, y = y, x
print( x, type(x) )
x, y = 1, 1
x, y = y, x + y
print( x, y )

# функціональний стиль
s = "x =%s, y = %s, w = %s" % t
print( s )

# імперативний стиль
s = f"x = {x}, y = {y}, w = {w}"
print( s )

# Арифметичні операції
x, y = 14, 6
print( "%d + %d = %f" % (x, y, x + y) )
print( "%d - %d = %f" % (x, y, x - y) )
print( "%d * %d =%f" % (x, y, x * y) )
print( "%d / %d = %f" % (x, y, x / y) )
print( "%d %% %d = %f" % (x, y, x % y) )
print( "%d // %d = %f" % (x, y, x // y) )
print( "%d ** %d = %f" % (x, y, x ** y) )
# !! звичайне ділення перетворює тип: int/int -> float
# ціле ділення - окремий оператор //
# типизація операторів - % для int та % для str - різні задачі

# детальніше про умовний оператор
if x > 10 and y > 10 :
    print( "x > 10 and y > 10" )
elif x > 10 or y > 10 :
    print( "x > 10 or y > 10" )
elif not y > 10 :
    print( "not y > 10" )
else:
    print('nothing')

# тернарний вираз або if-expression
w = 10 if x > 2 else 20

# оператор циклу - умовний цикл
x = 10
while x > 0 :
    x -= 1
    print( x, end=', ' )
else:
    print( "while-else", x )

# цикли-ітератори та генератори множин
r10 = range(10)
print( r10, type(r10) )

for x in r10 :
    print( x, end=', ' )
print()

for x in range(1, 10) :
    print( x, end=', ' )
print()

for x in range(1, 10, 2) :
    print( x, end=', ' )
print()

for x in range(10, 1, -2) :
    print( x, end=', ' )
print()
