import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psutil
import os
from pyinjector import inject
from PIL import Image, ImageTk, ImageDraw

injected = False

# Function to check if javaw.exe is running
def get_pid(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None

# Function to check conditions and update the GUI
def check_conditions():
    process_running = get_pid("javaw.exe") is not None
    dll_exists = os.path.exists(dll_path)
    
    if process_running and dll_exists:
        create_rounded_button(canvas, "Inject", perform_injection, width=250, height=50, corner_radius=25, color="#2dbbeb", text_color="#121212")
        status_label.config(text="Ready to Inject", foreground="#13ed4d")
    else:
        create_rounded_button(canvas, "Inject", None, width=250, height=50, corner_radius=25, color="#808080", text_color="#121212")
        status_label.config(text="Not Ready", foreground="#ed1337")
        injected = False
    
    root.after(1000, check_conditions)  # Check every second

# Function to perform the injection
def perform_injection():
    global injected
    if injected:
        messagebox.showinfo("Error", "Already Injected")
    else:
        pid = get_pid("javaw.exe")
        if pid:
            inject(pid, dll_path)
            messagebox.showinfo("Success", "Vortex Injected successfully! INSERT to open")
            status_label.config(text="Already Injected", foreground="#13ed4d")
            injected = True
        else:
            messagebox.showerror("Error", "Failed to inject Vortex.")

# Function to create a rounded button
def create_rounded_button(canvas, text, command, width, height, corner_radius, color, text_color):
    # Clear the canvas
    canvas.delete("all")

    # Create a rounded rectangle image
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((0, 0, width, height), corner_radius, fill="#4213ed")

    # Convert the image to a tkinter PhotoImage
    button_image = ImageTk.PhotoImage(img)

    # Create the button on the canvas
    button = canvas.create_image(0, 0, image=button_image, anchor="nw")
    button_text = canvas.create_text(width//2, height//2, text=text, fill="#141414", font=("Arial", 15))
    
    if command:
        # Bind the click event
        canvas.tag_bind(button, "<Button-1>", lambda e: command())
        canvas.tag_bind(button_text, "<Button-1>", lambda e: command())

    # Store reference to the image to prevent garbage collection
    canvas.image = button_image

# Initialize main application window
root = tk.Tk()
root.title("Vortex Injector")
root.geometry("300x150")

# Apply a blue and gray theme
root.configure(bg="#2b2b2b")

style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", background="#2b2b2b", foreground="#ECF0F1", font=("Arial", 12))

# Define DLL path
dll_path = os.getcwd() + "\\Vortex.dll"

# Create and place widgets
status_label = ttk.Label(root, text="Checking...")
status_label.pack(pady=10)

# Create a canvas for the rounded button
canvas = tk.Canvas(root, width=250, height=50, bg="#2b2b2b", highlightthickness=0)
canvas.pack(pady=10)

# Start the condition checking loop
check_conditions()

# Run the application
root.mainloop()
