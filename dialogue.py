import tkinter as tk
from tkinter import ttk


class ChoiceDialog:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")  # Set the window size
        self.root.title("Choice Dialog")  # Set the window title
        self.root.resizable(False, False)  # Disable window resizing
        self.root.configure(bg="white")  # Set background color

        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.option_var = tk.StringVar()
        self.option_var.set("Choose an option")  # Set default text

        self.option_label = ttk.Label(self.main_frame, text="Select an option:", anchor=tk.CENTER)
        self.option_label.pack(fill=tk.X, pady=10)

        self.option_menu = ttk.OptionMenu(self.main_frame, self.option_var,"Choose", "Execution", "Training", command=self.option_selected)
        self.option_menu.pack(fill=tk.X)

        self.ok_button = ttk.Button(self.main_frame, text="OK", command=self.close_window, state='disabled')
        self.ok_button.pack(fill=tk.X, pady=10)

        self.choice = None
        self.chose_execution = None

    def option_selected(self, selected_option):
        self.choice = selected_option
        self.ok_button['state'] = 'normal'  # Enable the button
        # Set the color to black
        self.ok_button.configure(style="Black.TButton")
    def close_window(self):
        self.root.destroy()  # Close the window

    def run(self):
        if self.choice == "Execution":
            print("User chose Execution")
            self.chose_execution = True
        elif self.choice == "Training":
            print("User chose Training")
            self.chose_execution = False
        else:
            print("No option selected")

    def show_dialog(self):
        self.root.deiconify()
        self.root.mainloop()


def main():
    root = tk.Tk()
    style = ttk.Style()
    style.configure("TFrame", background="white")  # Set frame background color
    style.configure("TLabel", background="white")  # Set label background color
    style.configure("TButton", background="#4CAF50", font=("Helvetica", 10, "bold"))  # Set button styles
    choice_dialog = ChoiceDialog(root)
    choice_dialog.show_dialog()
    choice_dialog.run()
    return choice_dialog.chose_execution


if __name__ == "__main__":
    main()
