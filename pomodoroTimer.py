import customtkinter as ctk
import pygame
import os

class PomodoroTimer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Imposta modalità scura e tema blu
        ctk.set_appearance_mode("dark")  # Modalità scura
        ctk.set_default_color_theme("blue")  # Tema blu moderno

        # Inizializzazione delle variabili
        self.pomodoro_duration = 25 * 60
        self.break_duration = 5 * 60
        self.cycles = 3
        self.current_cycle = 1
        self.is_break = False
        self.running = False
        self.current_time = self.pomodoro_duration

        self.setup_ui()
        self.setup_audio()

    def setup_ui(self):
        # Frame principale con un design minimale e moderno
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Visualizzazione cicli con font moderno e dimensioni ridotte
        self.cycles_label = ctk.CTkLabel(self.main_frame, text=f"Ciclo: 1/{self.cycles}",
                                         font=("Helvetica", 16, "bold"))
        self.cycles_label.pack(anchor="ne", padx=10, pady=10)

        # Canvas per il cerchio del timer
        self.canvas = ctk.CTkCanvas(self.main_frame, width=300, height=300, bg="black", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Timer display con un font più grande e moderno
        self.time_left = ctk.StringVar(value=self.format_time(self.pomodoro_duration))
        self.timer_label = ctk.CTkLabel(self.canvas, textvariable=self.time_left, font=("Helvetica", 48, "bold"))
        self.canvas.create_window(150, 150, window=self.timer_label)

        # Pulsanti con bordi arrotondati e distanziati
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        # Pulsante Avvia
        self.start_button = ctk.CTkButton(self.button_frame, text="Avvia", command=self.start_timer,
                                          corner_radius=15, width=100, height=50)
        self.start_button.pack(side="left", padx=10)

        # Pulsante Ferma
        self.stop_button = ctk.CTkButton(self.button_frame, text="Ferma", command=self.stop_timer, state="disabled",
                                         corner_radius=15, width=100, height=50)
        self.stop_button.pack(side="left", padx=10)

        # Pulsante Impostazioni
        self.settings_button = ctk.CTkButton(self.button_frame, text="Impostazioni", command=self.open_settings,
                                             corner_radius=15, width=100, height=50)
        self.settings_button.pack(side="left", padx=10)

        # Disegna il cerchio iniziale
        self.draw_circle(1)

    def setup_audio(self):
        pygame.mixer.init()
        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.sound_file = os.path.join(script_dir, "bell_sound.mp3")
        if not os.path.exists(self.sound_file):
            print("File audio non trovato. Verrà utilizzato un beep di sistema.")

    def start_timer(self):
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.settings_button.configure(state="disabled")
        self.countdown()

    def stop_timer(self):
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.settings_button.configure(state="normal")

    def countdown(self):
        if self.current_time > 0 and self.running:
            self.current_time -= 1
            self.time_left.set(self.format_time(self.current_time))
            self.draw_circle(self.current_time / (self.pomodoro_duration if not self.is_break else self.break_duration))
            self.root.after(1000, self.countdown)
        elif self.running:
            self.play_sound()
            if self.is_break:
                self.current_cycle += 1
                if self.current_cycle > self.cycles:
                    self.stop_timer()
                    ctk.CTkMessagebox(title="Pomodoro Timer", message="Hai completato tutti i cicli!")
                    return
                self.cycles_label.configure(text=f"Ciclo: {self.current_cycle}/{self.cycles}")
            self.is_break = not self.is_break
            self.current_time = self.pomodoro_duration if not self.is_break else self.break_duration
            message = "Pausa!" if self.is_break else "Torna al lavoro!"
            ctk.CTkMessagebox(title="Pomodoro Timer", message=message)
            self.countdown()

    def draw_circle(self, percentage):
        # Rende il cerchio più sottile e moderno
        self.canvas.delete("circle")
        x, y = 150, 150  # Centro del canvas
        r = 140  # Raggio del cerchio
        angle = 360 * percentage
        # Colore più delicato e sottile
        self.canvas.create_arc(x-r, y-r, x+r, y+r, start=90, extent=-angle, outline="lightblue",
                               width=8, tags="circle", style="arc")

    def play_sound(self):
        if os.path.exists(self.sound_file):
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
        else:
            self.root.bell()

    def open_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Impostazioni")
        settings_window.geometry("300x250")

        ctk.CTkLabel(settings_window, text="Durata Pomodoro (minuti):").pack(pady=5)
        pomodoro_entry = ctk.CTkEntry(settings_window)
        pomodoro_entry.insert(0, str(self.pomodoro_duration // 60))
        pomodoro_entry.pack()

        ctk.CTkLabel(settings_window, text="Durata Pausa (minuti):").pack(pady=5)
        break_entry = ctk.CTkEntry(settings_window)
        break_entry.insert(0, str(self.break_duration // 60))
        break_entry.pack()

        ctk.CTkLabel(settings_window, text="Numero di Cicli:").pack(pady=5)
        cycles_entry = ctk.CTkEntry(settings_window)
        cycles_entry.insert(0, str(self.cycles))
        cycles_entry.pack()

        def save_settings():
            self.pomodoro_duration = int(pomodoro_entry.get()) * 60
            self.break_duration = int(break_entry.get()) * 60
            self.cycles = int(cycles_entry.get())
            self.current_time = self.pomodoro_duration
            self.time_left.set(self.format_time(self.pomodoro_duration))
            self.cycles_label.configure(text=f"Ciclo: 1/{self.cycles}")
            self.draw_circle(1)
            settings_window.destroy()

        ctk.CTkButton(settings_window, text="Salva", command=save_settings).pack(pady=20)

    @staticmethod
    def format_time(seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
