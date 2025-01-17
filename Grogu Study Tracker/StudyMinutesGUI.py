import json
import os
import tkinter as tk
from tkinter import simpledialog
import sys

class StudyMinutesGUI:
    def __init__(self):
        # Initialiseer de GUI, maar laat het hoofdvenster verborgen blijven
        self.root = tk.Tk()
        self.root.withdraw()  # Verberg het hoofdvenster

    def ask_for_study_minutes(self):
        """
        Vraag de gebruiker om het aantal studieminuten in te stellen via een GUI.
        Dit gebeurt alleen als het bestand nog niet bestaat.
        """
        total_minutes = simpledialog.askinteger(
            "Instellen van studieminuten",
            "Voer het totaal aantal studieminuten in:",
            minvalue=1,  # Minimumwaarde is 1
            maxvalue=10000  # Maximaal aantal studieminuten
        )

        if total_minutes is not None:
            return total_minutes
        else:
            print("Geen invoer gedetecteerd. Gebruik standaardwaarde.")
            return 4800  # Standaardwaarde als de gebruiker niets invoert

    def save_study_minutes(self, total_minutes):
        """
        Sla de totale studieminuten (STUDY_MINUTES) op in een JSON-bestand.
        """
        data_file = "study_minutes.json"
        with open(data_file, "w") as file:
            json.dump({"total_minutes": total_minutes}, file)

    def load_study_minutes(self):
        """
        Laad de totale studieminuten (STUDY_MINUTES) uit een JSON-bestand.
        Als het bestand niet bestaat, retourneer 0.
        """
        data_file = "study_minutes.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as file:
                data = json.load(file)
                return data.get("total_minutes", 0)
        return 0


    def save_minutes_studied(self, minutes_studied):
        """
        Sla de hoeveelheid gestudeerde minuten (minutes_studied) op in een JSON-bestand.
        """
        data_file = "minutes_studied.json"
        with open(data_file, "w") as file:
            json.dump({"minutes_studied": minutes_studied}, file)

    def load_minutes_studied(self):
        """
        Laad de hoeveelheid gestudeerde minuten (minutes_studied) uit een JSON-bestand.
        Als het bestand niet bestaat, retourneer 0.
        """
        data_file = "minutes_studied.json"
        if os.path.exists(data_file):
            with open(data_file, "r") as file:
                data = json.load(file)
                return data.get("minutes_studied", 0)
        return 0

    def center_window(self, window):
        """
        Centreer een gegeven venster op het scherm.
        """
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_congratulations_screen(self):
        """
        Toon een venster met een boodschap dat de gebruiker goed heeft gestudeerd
        en een knop om de applicatie af te sluiten.
        """
        # Maak een nieuw venster
        congrats_window = tk.Toplevel(self.root)
        congrats_window.title("Goed gedaan!")
        congrats_window.geometry("400x200")
        congrats_window.resizable(False, False)

        # Zorg dat het scherm gecentreerd verschijnt
        self.center_window(congrats_window)

        # Voeg een tekstlabel toe
        label = tk.Label(
            congrats_window,
            text="Goed gestudeerd vandaag!",
            font=("Comic Sans MS", 12),
            padx=20,
            pady=20
        )
        label.pack()

        # Voeg een knop toe om de applicatie af te sluiten
        close_button = tk.Button(
            congrats_window,
            text="Sluit de applicatie",
            command=self.close_application,  # De functie die de applicatie afsluit
            padx=10,
            pady=5
        )
        close_button.pack(pady=(10, 0))

        # Zorg ervoor dat we de hoofdloop van de applicatie laten draaien zonder
        # de hoofdloop van het congrats_window opnieuw te starten
        congrats_window.protocol("WM_DELETE_WINDOW", self.close_application)

        # We gebruiken geen mainloop() meer voor dit venster, we sluiten alleen het venster wanneer de knop wordt ingedrukt
        congrats_window.wait_window()  # Dit zorgt ervoor dat de applicatie blijft draaien totdat het venster gesloten wordt.

        # Zodra het venster wordt gesloten, kan de hoofdloop van de applicatie worden beëindigd.
        self.root.quit()
        self.root.destroy()

    def reset_files(self):
        """
        Verwijder alle bestanden en reset de applicatie naar de initiële staat.
        """
        # Verwijder de bestanden die opgeslagen gegevens bevatten
        try:
            os.remove("study_minutes.json")  # Verwijder study_minutes.json
            os.remove("minutes_studied.json")  # Verwijder minutes_studied.json
            os.remove("cookies_status.json")  # Verwijder cookies_status.json
            print("Bestanden succesvol verwijderd.")
        except FileNotFoundError:
            print("Bestanden waren niet aanwezig, geen actie nodig.")

    def show_finish_screen(self):
        """
        Toon het finish-scherm met een bericht en knoppen voor afsluiten en resetten.
        """
        finish_window = tk.Toplevel(self.root)
        finish_window.title("Muffins bereikt!")
        finish_window.geometry("400x200")
        finish_window.resizable(False, False)

        # Zorg dat het scherm gecentreerd verschijnt
        self.center_window(finish_window)

        tk.Label(
            finish_window,
            text="Jaaaa! Je hebt de muffins gevonden! Is al dat leren toch ergens goed voor.",
            wraplength=380,
            justify="center",
            font=("Comic Sans MS", 12),
            pady=20
        ).pack()

        # Frame voor de knoppen
        button_frame = tk.Frame(finish_window)
        button_frame.pack(pady=10)

        # Reset en afsluiten knop
        reset_and_exit_button = tk.Button(
            button_frame,
            text="Reset en afsluiten",
            command=lambda: self.reset_and_close(finish_window)  # Reset en sluit de applicatie af
        )
        reset_and_exit_button.pack(side="left", padx=10)

    def reset_and_close(self, finish_window=None):
        """
        Voer de reset uit en sluit daarna de applicatie.
        Als een finish_window is meegegeven, wordt dit venster eerst gesloten.
        """
        # Reset de bestanden
        self.reset_files()

        # Sluit het finish_window of congratulations_window indien meegegeven
        if finish_window:
            finish_window.destroy()

        # Stop de hoofdloop en vernietig het root venster om de applicatie af te sluiten
        self.root.quit()  # Stop de mainloop
        self.root.destroy()  # Vernietig het hoofdvenster

    def close(self):
        # Sluit de GUI
        self.root.quit()

    def close_application(self):
        """
        Sluit de applicatie af.
        """
        if self.root.winfo_exists():  # Controleer of het venster nog bestaat
            self.root.quit()  # Stop de mainloop
            self.root.destroy()  # Vernietig het hoofdvenster





