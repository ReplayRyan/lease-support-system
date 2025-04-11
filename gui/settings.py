from customtkinter import *
import tkinter as tk

# ========== App Setup ==========
set_appearance_mode("system")
set_default_color_theme("blue")

app = CTk()
app.geometry("420x400")
app.title("⚙ Application Settings")


# Global font size variable
current_font_size = IntVar(value=12)

# ========== Functions ==========

def change_appearance(choice):
    set_appearance_mode(choice.lower())
    print(f"Appearance mode set to {choice}")

def change_theme(choice):
    set_default_color_theme(choice.lower())
    print(f"Color theme set to {choice}")

def reset_to_default():
    appearance_option.set("Dark")
    theme_option.set("Blue")
    set_appearance_mode("dark")
    set_default_color_theme("blue")
    print("✅ Settings reset to default.")

# ========== Layout ==========

main_frame = CTkFrame(app)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

title = CTkLabel(main_frame, text="Settings", font=("Helvetica", 18, "bold"))
title.pack(pady=(10, 20))

# Appearance Mode Dropdown
appearance_option = StringVar(value="System")
appearance_label = CTkLabel(main_frame, text="Appearance Mode")
appearance_label.pack(anchor="w")
appearance_dropdown = CTkOptionMenu(main_frame, variable=appearance_option, values=["System", "Dark", "Light"], command=change_appearance)
appearance_dropdown.pack(fill="x", pady=5)

# Color Theme Dropdown
theme_option = StringVar(value="Blue")
theme_label = CTkLabel(main_frame, text="Color Theme")
theme_label.pack(anchor="w", pady=(10, 0))
theme_dropdown = CTkOptionMenu(main_frame, variable=theme_option, values=["Blue", "Green", "Dark-Blue"], command=change_theme)
theme_dropdown.pack(fill="x", pady=5)

# Reset Button
reset_btn = CTkButton(main_frame, text="Reset to Default", command=reset_to_default, fg_color="#D9534F", hover_color="#C9302C")
reset_btn.pack(pady=20)

# Placeholder for more features
# extra_label = CTkLabel(main_frame, text="Additional Options (coming soon...)", text_color="gray")
# extra_label.pack(pady=10)

# ========== Run ==========
app.mainloop()