import matplotlib.pyplot as plt
import matplotlib.patches as patches

def sLine():
    print("\n The machine has learned to draw a line from (-x,-y) tp (x,y)")
    val = int(input("\nEnter the value of x(y=x): "));
    plt.plot(range(val), '-r')
    plt.title('Graph of y-x=0')
    plt.xlabel('x', color='#1C2833')
    plt.ylabel('y', color='#1C2833')
    plt.grid()
    # plt.savefig("plot_circle_matplotlib_01.png", bbox_inches='tight')
    plt.show()

def circle():
    print("The machine has learned to identify if the points specified is inside or outside the circle")
    xval = int(input("\nEnter the value of x: "));
    yval = int(input("\nEnter the value of y: "));
    if (xval*xval)+(yval*yval)>25:
        print("Outside circle")
        xlimt=xval+1
        ylimt=yval+1
    else:
        print("Inside circle")
        xlimt = ylimt = 6
    circle1 = plt.Circle((0, 0), 5, color='r')

    fig, ax = plt.subplots(1)
    ax.set_aspect(1)
    plt.xlim(-xlimt,xlimt)
    plt.ylim(-ylimt,ylimt)
    ax.add_artist(circle1)
    ax.plot((xval), (yval), 'o', color='y')
    plt.plot(xval,yval)
    plt.grid(linestyle='--')
    plt.title('Circle with radius 5', fontsize=8)
    #plt.savefig("plot_circle_matplotlib_01.png", bbox_inches='tight')
    plt.show()

def square():
    print("The machine has learned to identify if the points specified is inside or outside the square")
    xval = int(input("\nEnter the value of x: "));
    yval = int(input("\nEnter the value of y: "));
    if xval>=-4 and xval<=4 and yval>=-4 and yval<=4:
        print("Inside")
        xlimt = ylimt = 6
    else:
        print("Outside")
        xlimt = xval + 1
        ylimt = yval + 1

    fig, ax = plt.subplots(1)
    ax.set_aspect(1)
    plt.xlim(-xlimt, xlimt)
    plt.ylim(-ylimt, ylimt)
    ax.add_patch(
        patches.Rectangle(
            xy=(-4, -4),  # point of origin.
            width=8,
            height=8,
            linewidth=1,
            color='red',
            fill=True
        )
    )
    ax.plot((xval), (yval), 'o', color='y')
    plt.plot(xval, yval)
    plt.grid(linestyle='--')
    plt.title('Square with width 5', fontsize=8)
    # plt.savefig("plot_circle_matplotlib_01.png", bbox_inches='tight')
    plt.show()

def linear():
    choice=int(input("What the machine will learn"
          "\n1: Straight line passing through (0,0) with an angle of 45 degree between x and y axes"
          "\n2: Circle with radius of 5 centered at (0,0)"
          "\n3: A square of width 8 and centered at (0,0)"
          "\nChoose your option: "));
    cont="y";
    while cont!="n":
        if choice == 1:
            sLine();
            cont="n";
        elif choice==2:
            circle();
            cont = "n";
        elif choice==3:
              square();
              cont = "n";
        else:
            choice=int(input("\nWrong choice, enter choice again: "));
linear()