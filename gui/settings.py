from customtkinter import *
# could install pillow for python for image processing/importing

# This will be the main window of the application
app = CTk()
app.geometry("300x200")

# The following is a variety of settings that can be adjusted in the application for the entire application.
# Application color mode. Systems (Default), Dark, or Light.

DarkLightSwitch = CTkSwitch(master=app, text="Dark Mode", command=lambda: set_appearance_mode("dark" if DarkLightSwitch.get() else "light"))
DarkLightSwitch.place(relx=0.5, rely=0.1, anchor="center")

# Reset to default button
def reset_to_default():
    set_appearance_mode("dark")
    set_default_color_theme("blue")
    DarkLightSwitch.set(True)
    print("Settings reset to default.")
reset_btn = CTkButton(app, text="Reset to Default", command=reset_to_default)
reset_btn.place(relx=0.5, rely=0.2, anchor="center")

app.mainloop()