import math

class Path:
    def __init__(self, start_x, start_y, finish_x, finish_y):
        """
        Initialiseer een pad tussen een startpunt en een eindpunt.
        """
        self.start_x = start_x
        self.start_y = start_y
        self.finish_x = finish_x
        self.finish_y = finish_y
        self.total_distance = math.dist((start_x, start_y), (finish_x, finish_y))

    def get_position(self, progress_ratio):
        """
        Bereken de (x, y)-positie op het pad op basis van een voortgangsratio.
        :param progress_ratio: Een waarde tussen 0 en 1 die de voortgang langs het pad aangeeft.
        :return: (x, y)-coördinaten van de positie.
        """
        if progress_ratio < 0 or progress_ratio > 1:
            raise ValueError("Progress ratio must be between 0 and 1.")
        next_x = self.start_x + progress_ratio * (self.finish_x - self.start_x)
        next_y = self.start_y + progress_ratio * (self.finish_y - self.start_y)
        return next_x, next_y


