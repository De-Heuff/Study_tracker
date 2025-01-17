#TODO: er moet nog een aparte file en opslagfunctie komen voor minutes_studied

import json
import os
import turtle

from grogu import Grogu
from path import Path
from cookie import Cookie
from StudyMinutesGUI import StudyMinutesGUI

# #bestand waarin het totaal te studeren minuten wordt opgeslagen
# DATA_FILE = "study_data.json"

#houd bij welke koekjes zijn gevonden
COOKIES_STATUS_FILE = "cookies_status.json"

def load_cookie_status():
    """
    Laad de status van de koekjes (welke koekjes zijn al gevonden).
    Als het bestand niet bestaat, retourneer een lege lijst.
    """
    if os.path.exists(COOKIES_STATUS_FILE):
        with open(COOKIES_STATUS_FILE, "r") as file:
            return json.load(file)
    return [False, False, False]  # Als het bestand niet bestaat, ga ervan uit dat geen koekjes gevonden zijn.

def load_cookies_found():
    """
    Laad het aantal gevonden koekjes uit een bestand.
    Als het bestand niet bestaat, retourneer 0.
    """
    if os.path.exists(COOKIES_FOUND_FILE):
        with open(COOKIES_FOUND_FILE, "r") as file:
            return json.load(file)
    return 0  # Geen koekjes gevonden bij het opstarten

def save_cookie_status(status):
    """
    Sla de status van de koekjes op in een JSON-bestand.
    """
    with open(COOKIES_STATUS_FILE, "w") as file:
        json.dump(status, file)

def save_cookies_found(cookies_found):
    """
    Sla het aantal gevonden koekjes op in een JSON-bestand.
    """
    with open(COOKIES_FOUND_FILE, "w") as file:
        json.dump(cookies_found, file)

def update_label(label, remaining_minutes):
    """
    Update het label op het scherm om de resterende studieminuten te tonen.
    :param label: Turtle-object dat het label weergeeft.
    :param remaining_minutes: Het aantal minuten dat nog moet worden gestudeerd.
    """
    label.clear()  # Verwijder vorige tekst
    label.write(
        f"Parsecs tot aan de muffins: {remaining_minutes}",
        align="center",
        font=("Comic Sans MS", 14, "bold"),
    )

def update_cookie_label(label, cookies_found):
    # Update het label met het aantal gevonden koekjes
    label.clear()
    label.write(f"Koekjes gevonden: {cookies_found}", align="center", font=("Comic Sans MS", 14, "normal"))

def main():
    image_width = 1400
    image_height = 750

    screen = turtle.Screen()
    screen.screensize(image_width, image_height)
    # Voeg de cookie afbeelding toe als een shape
    screen.addshape("koekje.gif")

    screen.title("OSCP Conqueror's Challenge")
    screen.setup(width=image_width, height=image_height)
    screen.bgpic("galaxy.gif")

    finish_shape = "muffins.gif"
    screen.addshape(finish_shape)
    finish = turtle.Turtle()
    finish.shape(finish_shape)
    finish.penup()
    finish.hideturtle()  # Verberg de Turtle voordat hij beweegt
    finish.goto(250, 200)  # Plaats Finish op (250, 200)
    finish.showturtle()  # Laat de Turtle zien zonder beweging

    # Maak een Path-object
    path = Path(start_x=-500, start_y=-300, finish_x=250, finish_y=200)

    #Laad GUI
    gui = StudyMinutesGUI()

    # Laad de vorige studiegegevens
    total_study_minutes = gui.load_study_minutes()

    if total_study_minutes == 0:
        # Als gebruiker nog niet eerder een waarde heeft opgegeven (bestand bestaat niet), vraag de gebruiker om een waarde
        total_study_minutes = gui.ask_for_study_minutes()  # Vraag het aantal studieminuten via de GUI
        gui.save_study_minutes(total_study_minutes)  # Sla de waarde op in study_minutes.json
        gui.close()  # Sluit de GUI netjes af
    else:
        print(f"Studie-minuten geladen: {total_study_minutes}")

    print(f"Totaal aantal studieminuten ingesteld op: {total_study_minutes}")

    # Laad het aantal gestudeerde minuten (minutes_studied)
    minutes_studied = gui.load_minutes_studied()

    # Maak een Grogu-object
    grogu = Grogu(screen, shape="grogu_resize.gif", start_x=-500, start_y=-300)

    # Verplaats Grogu naar de laatste positie op basis van geladen gegevens
    grogu.move_along_path(path, minutes=minutes_studied, total_minutes=total_study_minutes)

    # Maak een label om resterende minuten te tonen
    label = turtle.Turtle()
    label.hideturtle()
    label.penup()
    label.color("chartreuse")
    label.goto(-500, 300)  # Plaats het label links in het scherm
    remaining_minutes = total_study_minutes - minutes_studied
    update_label(label, remaining_minutes)

    # Maak een label voor het aantal koekjes
    cookie_label = turtle.Turtle()
    cookie_label.hideturtle()
    cookie_label.penup()
    cookie_label.color("chartreuse")
    cookie_label.goto(-500, 275)  # Plaats het koekjeslabel

    # Laad de status van de koekjes
    cookies_status = load_cookie_status()  # Dit is de lijst met True/False voor elk koekje
    cookies_found = cookies_status.count(True)  # Telt het aantal gevonden koekjes
    update_cookie_label(cookie_label, cookies_found)  # Update het label met het aantal gevonden koekjes

    # Plaats koekjes langs het pad (afhankelijk van de status)
    cookies = []
    cookie_positions = [(-200, -100), (-20, 10), (100, 100)]  # Vaste posities voor koekjes

    # Maak voor elke positie een nieuw Cookie-object aan
    for i, pos in enumerate(cookie_positions):
        cookie = Cookie(screen, pos[0], pos[1])  # Maak een nieuw koekje op de opgegeven locatie
        if cookies_status[i]:  # Als het koekje al is gevonden, verberg het dan
            cookie.hide()
        cookies.append(cookie)  # Voeg het koekje toe aan de lijst

    # Vraag de gebruiker om studiegegevens in te voeren
    try:
        learned_minutes = int(screen.textinput("Studie Tracker", "Hoeveel minuten video heb je vandaag gekeken?"))
        if learned_minutes > 0:
            minutes_studied += learned_minutes  # Update totale studie-minuten
            if minutes_studied > total_study_minutes:
                minutes_studied = total_study_minutes  # Beperk tot maximum

            grogu.move_along_path(path, minutes=minutes_studied, total_minutes=total_study_minutes)

            # Controleer of Grogu op een koekje is gestuit
            print(f"Koekjesstatus bij laden: {cookies_status}")
            for i, cookie in enumerate(cookies):
                afstand = grogu.turtle.distance(cookie.cookie_turtle)  # Bereken de afstand tot het koekje
                print(f"Afstand tot koekje {i + 1}: {afstand}")  # Debugging

                if afstand < 30 and not cookies_status[i]:  # Als Grogu dicht bij een koekje is en het koekje nog niet is gevonden
                    print(f"Koekje {i + 1} gevonden!")  # Debugging
                    cookie.animate()  # Speel de animatie af

                    # Verberg het koekje van het scherm en update de status
                    cookie.hide()  # Verberg het koekje
                    cookies_status[i] = True  # Markeer het koekje als gevonden

                    # Update het aantal gevonden koekjes en het label
                    cookies_found = cookies_status.count(True)  # Het aantal gevonden koekjes
                    update_cookie_label(cookie_label, cookies_found)

                    # Sla de status van de koekjes op
                    save_cookie_status(cookies_status)

            # Controleer of Grogu de finish heeft bereikt
            if minutes_studied >= total_study_minutes:
                gui.show_finish_screen()  # Toon het finish-scherm
            else:
                # Bereken resterende minuten en update het label
                remaining_minutes = total_study_minutes - minutes_studied
                update_label(label, remaining_minutes)

                # Sla de nieuwe gegevens en de koekjesstatus op
                gui.save_minutes_studied(minutes_studied)
                save_cookie_status(cookies_status)

                # Toon het "Goed gestudeerd vandaag!"-scherm
                gui.show_congratulations_screen()

        else:
            #foutmelding laten verschijnen
            print("Het aantal minuten moet een positief getal zijn.")

    except ValueError:
        # foutmelding laten verschijnen
        print("Voer een geldig getal in.")

    screen.mainloop()

if __name__ == "__main__":
    main()




