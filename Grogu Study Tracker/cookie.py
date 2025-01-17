import turtle

class Cookie:
    def __init__(self, screen, x, y, shape="koekje.gif"):
        self.screen = screen
        self.x = x
        self.y = y
        self.shape = shape

        # Maak de cookie Turtle
        self.cookie_turtle = turtle.Turtle()
        self.cookie_turtle.shape(self.shape)
        self.cookie_turtle.penup()
        self.cookie_turtle.goto(self.x, self.y)

    def animate(self):
        self.cookie_turtle.hideturtle()
        self.cookie_turtle.showturtle()

    def hide(self):
        self.cookie_turtle.hideturtle()