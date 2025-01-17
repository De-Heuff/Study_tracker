import turtle

class Grogu:
    def __init__(self, screen, shape="grogu_resize.gif", start_x=-500, start_y=-300):
        """
        Initialiseer de Grogu Turtle met een specifieke vorm en startpositie.
        """
        screen.addshape(shape)
        self.turtle = turtle.Turtle()
        self.turtle.shape(shape)
        self.turtle.penup()
        self.turtle.goto(start_x, start_y)  # Verplaats naar startpositie
        self.turtle.pendown()
        self.turtle.color("chartreuse")
        self.turtle.pensize(10)

    def move_along_path(self, path, minutes, total_minutes):
        """
        Beweeg Grogu langs het pad.
        :param path: Een instantie van de Path-klasse.
        :param minutes: Het aantal minuten dat de gebruiker heeft geleerd.
        :param total_minutes: Het totale aantal minuten dat nodig is om de finish te bereiken.
        """
        # Bereken de voortgang als een ratio tussen 0 en 1
        progress_ratio = minutes / total_minutes
        if progress_ratio > 1:
            progress_ratio = 1  # Beperking: niet meer dan 100% van het pad

        # Verkrijg de nieuwe positie en beweeg Grogu erheen
        next_x, next_y = path.get_position(progress_ratio)
        self.turtle.goto(next_x, next_y)
