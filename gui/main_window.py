from customtkinter import *
# could install pillow for python for image processing/importing

# This will be the main window of the application
app = CTk()
app.geometry("500x400")

# Application color mode. System (default), Dark, or Light.
set_appearance_mode("system")

# Application color theme. Blue (default), green, dark-blue, or custom hex color.
set_default_color_theme("blue")

# Title of the main window
app.title("Main Window")

# Icon of the main window
# app.iconbitmap("gui/icon.ico") # THIS SETS THE ICON FOR THE MAIN WINDOW BASED ON FILE PATH

# If you want to set the icon from a resource file, use the following line instead:
# app.iconbitmap(default="gui/icon.ico") # THIS SETS THE ICON FOR THE MAIN WINDOW BASED ON DEFAULT PATH

# This button in the center of the main window is a test that will eventually function as the "GO" to process an image or begin calculations.
# I will build on this button later to add the functionality we want later. For now it simply prints "Processing..." to the console and shows color.
btn = CTkButton(app, text="Test Button", corner_radius=32, 
                fg_color="#4158D0", hover_color="1A3CEA", 
                border_color="#FFFFFF", border_width=2,
                command=lambda: print("Processing..."))
btn.place(relx=0.5, rely=0.5, anchor="center")



# OPEN SETTINGS:
# This is the settings button code to display the settings.py window in the top right corner.
def open_settings():
    import gui.settings
    gui.settings.app.deiconify()  # Show the settings window
def close_settings():
    import gui.settings
    gui.settings.app.withdraw()  # Hide the settings window
settings_btn = CTkButton(app, text="Settings", command=open_settings)
settings_btn.place(relx=0.9, rely=0.6, anchor="center") # Placement values are temporary and will be changed later.

# EXIT main_window:
# This is the EXIT BUTTON code to close the application.
def exit_app():
    app.quit()
    app.destroy()
exit_btn = CTkButton(app, text="Exit", command=exit_app)
exit_btn.place(relx=0.9, rely=0.7, anchor="center") # Placement values are temporary and will be changed later.

# OPEN ABOUT:
# This is the ABOUT BUTTON code to display the about.py window in the top right corner.
def open_about():
    import gui.about
    gui.about.app.deiconify()  # Show the about window
def close_about():
    import gui.about
    gui.about.app.withdraw()  # Hide the about window
about_btn = CTkButton(app, text="About", command=open_about)
about_btn.place(relx=0.9, rely=0.8, anchor="center") # Placement values are temporary and will be changed later.

# OPEN HELP:
# This is the help button code to display the help.py window in the top right corner.
def open_help():
    import gui.help
    gui.help.app.deiconify()  # Show the help window
def close_help():
    import gui.help
    gui.help.app.withdraw()  # Hide the help window
help_btn = CTkButton(app, text="Help", command=open_help)
help_btn.place(relx=0.9, rely=0.9, anchor="center") # Placement values are temporary and will be changed later.



app.mainloop()