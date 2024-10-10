import customtkinter as ctk
import pygame
import os
import json
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PomodoroTimer:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Pomodoro Timer by @vitalelele")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Variabili del timer
        self.load_settings()
        self.current_cycle = 1
        self.is_break = False
        self.running = False
        self.current_time = self.pomodoro_duration
        self.work_sessions_completed = 0
        self.total_work_time = 0
        self.total_break_time = 0

        self.setup_ui()
        self.setup_audio()

    def load_settings(self):
        config_file = "settings.json"
        if os.path.exists(config_file):
            with open(config_file, "r") as file:
                settings = json.load(file)
                self.pomodoro_duration = settings.get("pomodoro_duration", 25) * 60
                self.break_duration = settings.get("break_duration", 5) * 60
                self.cycles = settings.get("cycles", 3)
                self.theme = settings.get("theme", "Dark")
        else:
            self.pomodoro_duration = 25 * 60
            self.break_duration = 5 * 60
            self.cycles = 3
            self.theme = "Dark"
        ctk.set_appearance_mode(self.theme)

    def save_settings(self):
        settings = {
            "pomodoro_duration": self.pomodoro_duration // 60,
            "break_duration": self.break_duration // 60,
            "cycles": self.cycles,
            "theme": self.theme
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def setup_ui(self):
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.cycles_label = ctk.CTkLabel(self.main_frame, text=f"Ciclo: 1/{self.cycles}",
                                         font=("Helvetica", 16, "bold"))
        self.cycles_label.pack(anchor="ne", padx=10, pady=10)

        self.canvas = ctk.CTkCanvas(self.main_frame, width=300, height=300, bg=self.get_current_bg_color(), highlightthickness=0)
        self.canvas.pack(pady=20)

        self.time_left = ctk.StringVar(value=self.format_time(self.pomodoro_duration))
        self.timer_label = ctk.CTkLabel(self.main_frame, textvariable=self.time_left, font=("Helvetica", 48, "bold"))
        self.canvas.create_window(150, 150, window=self.timer_label)

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(self.button_frame, text="Avvia", command=self.start_timer,
                                           corner_radius=15, width=120, height=50)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ctk.CTkButton(self.button_frame, text="Ferma", command=self.stop_timer, state="disabled",
                                          corner_radius=15, width=120, height=50)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset_timer,
                                           corner_radius=15, width=120, height=50)
        self.reset_button.pack(side="left", padx=10)

        self.settings_button = ctk.CTkButton(self.main_frame, text="⚙️", command=self.open_settings,
                                              corner_radius=15, width=50, height=50)
        self.settings_button.place(relx=0.9, rely=0.9, anchor="center")

        self.report_button = ctk.CTkButton(self.main_frame, text="📊 Report", command=self.show_report,
                                           corner_radius=15, width=120, height=50)
        self.report_button.pack(pady=10)

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

    def reset_timer(self):
        self.stop_timer()
        self.current_time = self.pomodoro_duration
        self.time_left.set(self.format_time(self.current_time))
        self.draw_circle(1)

    def countdown(self):
        if self.current_time > 0 and self.running:
            self.current_time -= 1
            self.time_left.set(self.format_time(self.current_time))
            self.draw_circle(self.current_time / (self.pomodoro_duration if not self.is_break else self.break_duration))
            self.root.after(1000, self.countdown)
        elif self.running:
            self.play_sound()
            if self.is_break:
                self.total_break_time += self.break_duration
                self.current_cycle += 1
                if self.current_cycle > self.cycles:
                    self.stop_timer()
                    self.show_message("Pomodoro Timer", "Hai completato tutti i cicli!")
                    return
                self.cycles_label.configure(text=f"Ciclo: {self.current_cycle}/{self.cycles}")
            else:
                self.work_sessions_completed += 1
                self.total_work_time += self.pomodoro_duration

            self.is_break = not self.is_break
            self.current_time = self.pomodoro_duration if not self.is_break else self.break_duration
            
            message = "Pausa!" if self.is_break else "Torna al lavoro!"
            self.show_message("Pomodoro Timer", message)
            self.countdown()


    def draw_circle(self, percentage):
        self.canvas.delete("circle")
        x, y = 150, 150
        r = 140
        angle = 360 * percentage

        # Colore diverso per pausa e lavoro
        color = "lightblue" if not self.is_break else "lightgreen"  # Verde per la pausa
        self.canvas.create_arc(x-r, y-r, x+r, y+r, start=90, extent=-angle, outline=color,
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
        settings_window.geometry("350x450")
        settings_window.grab_set()

        settings_frame = ctk.CTkFrame(settings_window)
        settings_frame.pack(pady=10, padx=10, fill="both", expand=True)

        ctk.CTkLabel(settings_frame, text="Durata Pomodoro (minuti):").pack(pady=5)
        pomodoro_entry = ctk.CTkEntry(settings_frame)
        pomodoro_entry.insert(0, str(self.pomodoro_duration // 60))
        pomodoro_entry.pack(pady=5)

        ctk.CTkLabel(settings_frame, text="Durata Pausa (minuti):").pack(pady=5)
        break_entry = ctk.CTkEntry(settings_frame)
        break_entry.insert(0, str(self.break_duration // 60))
        break_entry.pack(pady=5)

        ctk.CTkLabel(settings_frame, text="Numero di Cicli:").pack(pady=5)
        cycles_entry = ctk.CTkEntry(settings_frame)
        cycles_entry.insert(0, str(self.cycles))
        cycles_entry.pack(pady=5)

        theme_label = ctk.CTkLabel(settings_frame, text="Tema:")
        theme_label.pack(pady=5)
        theme_menu = ctk.CTkOptionMenu(settings_frame, values=["Light", "Dark"], command=self.change_theme)
        theme_menu.pack(pady=5)

        save_button = ctk.CTkButton(settings_window, text="Salva", command=lambda: self.save_and_close(settings_window, pomodoro_entry, break_entry, cycles_entry), width=100, height=40)
        save_button.pack(pady=10)

    def save_and_close(self, settings_window, pomodoro_entry, break_entry, cycles_entry):
        self.pomodoro_duration = int(pomodoro_entry.get()) * 60
        self.break_duration = int(break_entry.get()) * 60
        self.cycles = int(cycles_entry.get())
        self.current_time = self.pomodoro_duration
        self.time_left.set(self.format_time(self.pomodoro_duration))
        self.cycles_label.configure(text=f"Ciclo: 1/{self.cycles}")
        self.draw_circle(1)
        self.save_settings()
        settings_window.destroy()

    def change_theme(self, choice):
        self.theme = choice
        ctk.set_appearance_mode(choice.lower())
        self.save_settings()

    def show_report(self):
        if self.work_sessions_completed == 0:
            self.show_message("Report Pomodoro", "Non hai ancora completato alcuna sessione.")
            return

        report_window = ctk.CTkToplevel(self.root)
        report_window.title("Report Pomodoro")
        report_window.geometry("500x600")
        report_window.grab_set()

        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        labels = ['Work Time', 'Break Time']
        times = [self.total_work_time / 60, self.total_break_time / 60]
        ax.pie(times, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'skyblue'])
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=report_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)

        total_work_time_formatted = str(timedelta(seconds=self.total_work_time))
        total_break_time_formatted = str(timedelta(seconds=self.total_break_time))
        summary_label = ctk.CTkLabel(report_window, text=f"Sessioni completate: {self.work_sessions_completed}\n"
                                                         f"Tempo di lavoro: {total_work_time_formatted}\n"
                                                         f"Tempo di pausa: {total_break_time_formatted}",
                                     font=("Helvetica", 14))
        summary_label.pack(pady=10)

        reset_button = ctk.CTkButton(report_window, text="Azzera Report", command=self.reset_report, corner_radius=15)
        reset_button.pack(pady=20)

    def show_message(self, title, message):
        message_window = ctk.CTkToplevel(self.root)
        message_window.title(title)
        message_window.geometry("300x150")
        message_window.grab_set()

        message_label = ctk.CTkLabel(message_window, text=message, font=("Helvetica", 14))
        message_label.pack(pady=20)

        ok_button = ctk.CTkButton(message_window, text="OK", command=message_window.destroy)
        ok_button.pack(pady=10)


    def reset_report(self):
        self.work_sessions_completed = 0
        self.total_work_time = 0
        self.total_break_time = 0
        ctk.CTkMessagebox(title="Pomodoro Timer", message="Il report è stato azzerato.")

    @staticmethod
    def format_time(seconds):
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    def get_current_bg_color(self):
        if ctk.get_appearance_mode() == "Dark":
            return "gray17"
        else:
            return "gray86"

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = PomodoroTimer()
    app.run()
