class Point:
    x =0
    y=0
    def __init__(self):
        self.x = Point.x
        self.y = Point.y


def main():
    p1 = Point()
    print(p1.x,p1.y)
    print(Point.x)
    Point.x = 10
    print(p1.x,Point.x)
    p1.x =20
    print(p1.x,Point.x)
    p2 = Point()
    print(p2.x,p2.y)



if __name__ == '__main__' : main()    