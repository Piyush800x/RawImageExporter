import os
import shutil
import sys
import threading
from tkinter import Label, Text, filedialog, Entry, StringVar, HORIZONTAL, messagebox, Toplevel
from tkinter.ttk import Button, Progressbar
from ttkthemes import ThemedTk
from time import sleep

FONT = ("Helvetica", 12)
FONT_LABEL = ("Helvetica", 12)


class MainWindow(ThemedTk):

    def __init__(self):
        super().__init__()
        self.title("Raw Image Exporter")
        self.iconbitmap("logo.ico")
        # self.geometry("500x360")
        self.protocol('WM_DELETE_WINDOW', lambda: [sys.exit(0)])
        self.cr2_entry_var: StringVar = StringVar()
        self.output_entry_var: StringVar = StringVar()

        self.progress = 0
        self.progressbar: Progressbar
        # self.progressbar: Progressbar = Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate')

        # Create labels and text boxes
        # jpg_label entry
        jpg_path_label = Label(self, text="JPG File Paths:", font=FONT)
        jpg_path_label.pack(padx=2, pady=2)
        self.jpg_path_text = Text(self, height=10, font=FONT)
        self.jpg_path_text.pack(padx=2, pady=2)

        # cr2-label entry btn
        cr2_path_label = Label(self, text="CR2 Directory Path:", font=FONT)
        cr2_path_label.pack(padx=2, pady=2)
        cr2_path_text = Entry(self, textvariable=self.cr2_entry_var, width=70, font=FONT)
        cr2_path_text.pack(padx=2, pady=2)
        browse_btn = Button(self, text="Browse", command=self.set_cr2_browse)
        browse_btn.pack(padx=2, pady=2)

        # output label entry btn
        output_path_label = Label(self, text="Output Directory Path:", font=FONT)
        output_path_label.pack(padx=2, pady=2)
        output_path_text = Entry(self, textvariable=self.output_entry_var, width=70, font=FONT)
        output_path_text.pack(padx=2, pady=2)
        browse_btn_1 = Button(self, text="Browse", command=self.set_output_browse)
        browse_btn_1.pack(padx=8, pady=8)

        # Create a button to start the copying process
        copy_button = Button(self, text="Copy CR2 Files", command=lambda: [threading.Thread(target=self.main,
                                                                                            daemon=True).start()])
        copy_button.pack(padx=5, pady=5)

    def set_cr2_browse(self):
        file = filedialog.askdirectory()
        self.cr2_entry_var.set(file)
        print(f"cr2 entry var {self.cr2_entry_var.get()}")

    def set_output_browse(self):
        file = filedialog.askdirectory()
        self.output_entry_var.set(file)
        print(f"cr2 entry var {self.output_entry_var.get()}")

    def copy_cr2_files(self):
        # Get input values from text boxes
        jpg_paths = self.jpg_path_text.get("1.0", "end-1c").split("\n")
        jpg_paths = [path.strip('"') for path in jpg_paths]
        # cr2_dir = cr2_path_text.get("1.0", "end-1c")
        # cr2_dir.strip('"')
        cr2_dir = self.cr2_entry_var.get()

        # output_dir = output_path_text.get("1.0", "end-1c")
        # output_dir.strip('"')
        output_dir = self.output_entry_var.get()

        print(f'JPG files {jpg_paths}')
        print(f'cr2 dir {cr2_dir}')
        print(f"output dir {output_dir}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        chunk_size = (100 / len(jpg_paths))
        # Iterate through JPG file paths
        for jpg_path in jpg_paths:
            jpg_filename = os.path.basename(jpg_path)
            jpg_name, _ = os.path.splitext(jpg_filename)
            cr2_path = os.path.join(cr2_dir, jpg_name + ".cr2")

            # Check if the corresponding CR2 file exists
            if os.path.isfile(cr2_path):
                # Copy the CR2 file to the output directory
                output_path = os.path.join(output_dir, jpg_name + ".cr2")
                shutil.copy2(cr2_path, output_path)  # copy2 copies metadata
                # shutil.copy(cr2_path, output_path)    # copy no metadata copy
                print(f"Copied {cr2_path} to {output_path}")
                self.progress += chunk_size
                sleep(2)
                # self.progressbar['value'] = self.progress
            else:
                print(f"No CR2 file found for {jpg_path}")
                self.progress += chunk_size
                sleep(2)
                # self.progressbar['value'] = self.progress

    def progress_window(self):
        self.win: Toplevel = Toplevel()
        self.win.title("RWE")
        self.win.geometry("360x100")
        self.win.iconbitmap("logo.ico")

        self.progressbar: Progressbar = Progressbar(self.win, orient=HORIZONTAL, length=100, mode='determinate')
        self.progressbar.pack(padx=20, pady=20)

        threading.Thread(target=self.update_progress, daemon=True).start()

        self.win.mainloop()

    def update_progress(self):
        while True:
            # try:
            self.progressbar['value'] = self.progress
            print(type(self.progress))
            print(self.progress)
            if self.progress == 100:
                messagebox.showinfo("RWE", "Files successfully copied!")
                self.progress = 0
                self.win.destroy()
                break

    def main(self):
        threading.Thread(target=self.copy_cr2_files, daemon=True).start()
        self.progress_window()


def main():
    App = MainWindow()
    App.mainloop()


if __name__ == '__main__':
    main()
