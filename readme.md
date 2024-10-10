# myPomodoro 🍅

myPomodoro is a desktop application developed in Python that uses the Pomodoro technique to help you improve your productivity. With a simple and intuitive user interface, you can easily manage your work sessions and breaks.

## Features

- **Pomodoro Timer**: Set a timer for 25 minutes of uninterrupted work.
- **Breaks**: After each work session, take a 5-minute break.
- **Cycles**: Complete a customizable number of work and break cycles.
- **Audio**: Sound notifications at the end of each session.
- **Customizable Interface**: Choose different durations for work, breaks, and cycles.
- **Dark/Light Theme**: Easily switch between dark and light modes.

## Technologies Used

- Python
- CustomTkinter (for the user interface)
- Pygame (for sound management)

## Installation

To run myPomodoro, make sure you have Python installed on your machine. You can install the necessary dependencies using `pip`.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vitalelele/myPomodoro.git
   ```

2. **Navigate to the project directory**:
   ```bash
   cd myPomodoro
   ```

3. **Install the dependencies**:
   ```bash
   pip install customtkinter pygame
   ```

4. **Make sure to have the audio file**: 
   Download a notification sound file (e.g., `bell_sound.mp3`) and place it in the same directory as the `pomodoro.py` file.

5. **Run the app**:
   ```bash
   python pomodoro.py
   ```

## Usage

1. Launch the app and set the timer for the work session.
2. Click on "Start" to begin the timer.
3. After each work session, a message window will notify you to take a break.
4. Customize the settings through the settings button to change the durations of work sessions and breaks, as well as the number of cycles.
   
## Contributing

If you wish to contribute to myPomodoro, please follow these steps:

1. Fork the project.
2. Create a new branch for your feature:
   ```bash
   git checkout -b my-feature
   ```
3. Make your changes and add the modified files:
   ```bash
   git add .
   ```
4. Commit your changes:
   ```bash
   git commit -m "Added a new feature"
   ```
5. Push your changes:
   ```bash
   git push origin my-feature
   ```
6. Create a new Pull Request.

## License

This project is licensed under the MIT License.
