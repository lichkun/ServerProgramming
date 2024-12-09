x = 10
print( x, type(x) )
x = 2j
print( x, type(x) )
y = 10 + x
print( y, type(y) )
# print( "y = " + y )

s = "y = " + str(y)
print( s, type(s) )

x = 2**256
print( x, type(x) )

if x > 2 **128 :
    print(f"Number {x} greater than 2 ** 128")
else:
    pass

x = input( "Enter x = " )
print( x, type(x) )
y = float(x)
print( y, type(y) )