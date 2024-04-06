import os
import shutil
import sys
import threading
import tkinter
from tkinter import Tk, Label, Text, filedialog, Entry, StringVar, HORIZONTAL, messagebox
from tkinter.ttk import Button, Progressbar
from ttkthemes import ThemedTk

FONT = ("Helvetica", 12)
FONT_LABEL = ("Helvetica", 12)

# Create the main window
root = ThemedTk(theme='arc')
root.title("Raw Image Exporter")
root.protocol('WM_DELETE_WINDOW', lambda: [sys.exit(0)])


cr2_entry_var: StringVar = StringVar()
output_entry_var: StringVar = StringVar()

global active, progress


class ProgressWindow(tkinter.Toplevel):

    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', lambda: [sys.exit(0)])
        self.title("Raw Image Exporter")
        self.geometry("180x50")
        self.progress = 0
        self.progressbar: Progressbar = Progressbar(self, orient=HORIZONTAL, length=100, mode='determinate')

        self.progressbar.pack()

        self.copy_cr2_files()
        self.progress_update()

    def progress_update(self):
        global active, progress
        active = True

        def update():
            global active
            while active:
                # try:
                    self.progressbar['value'] = self.progress
                    if self.progress == "100":
                        messagebox.showinfo("RWE", "Files successfully copied!")
                        self.destroy()
                        break
                # except Exception as e:
                #     active = False
                #     break
        threading.Thread(target=update).start()

    def copy_cr2_files(self):
        global progress
        # Get input values from text boxes
        jpg_paths = jpg_path_text.get("1.0", "end-1c").split("\n")
        jpg_paths = [path.strip('"') for path in jpg_paths]
        # cr2_dir = cr2_path_text.get("1.0", "end-1c")
        # cr2_dir.strip('"')
        cr2_dir = cr2_entry_var.get()

        # output_dir = output_path_text.get("1.0", "end-1c")
        # output_dir.strip('"')
        output_dir = output_entry_var.get()

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
            else:
                print(f"No CR2 file found for {jpg_path}")
                self.progress += chunk_size


# def copy_cr2_files():
#     global progress
#     # Get input values from text boxes
#     jpg_paths = jpg_path_text.get("1.0", "end-1c").split("\n")
#     jpg_paths = [path.strip('"') for path in jpg_paths]
#     # cr2_dir = cr2_path_text.get("1.0", "end-1c")
#     # cr2_dir.strip('"')
#     cr2_dir = cr2_entry_var.get()
#
#     # output_dir = output_path_text.get("1.0", "end-1c")
#     # output_dir.strip('"')
#     output_dir = output_entry_var.get()
#
#     print(f'JPG files {jpg_paths}')
#     print(f'cr2 dir {cr2_dir}')
#     print(f"output dir {output_dir}")
#
#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)
#     chunk_size = (100/len(jpg_paths))
#     # Iterate through JPG file paths
#     for jpg_path in jpg_paths:
#         jpg_filename = os.path.basename(jpg_path)
#         jpg_name, _ = os.path.splitext(jpg_filename)
#         cr2_path = os.path.join(cr2_dir, jpg_name + ".cr2")
#
#         # Check if the corresponding CR2 file exists
#         if os.path.isfile(cr2_path):
#             # Copy the CR2 file to the output directory
#             output_path = os.path.join(output_dir, jpg_name + ".cr2")
#             shutil.copy2(cr2_path, output_path)     # copy2 copies metadata
#             # shutil.copy(cr2_path, output_path)    # copy no metadata copy
#             print(f"Copied {cr2_path} to {output_path}")
#             progress += chunk_size
#         else:
#             print(f"No CR2 file found for {jpg_path}")


def set_cr2_browse():
    file = filedialog.askdirectory()
    cr2_entry_var.set(file)
    print(f"cr2 entry var {cr2_entry_var.get()}")


def set_output_browse():
    file = filedialog.askdirectory()
    output_entry_var.set(file)
    print(f"cr2 entry var {output_entry_var.get()}")


def main():
    progress_window = ProgressWindow()
    progress_window.mainloop()


# Create labels and text boxes
# jpg_label entry
jpg_path_label = Label(root, text="JPG File Paths:", font=FONT)
jpg_path_label.pack()
jpg_path_text = Text(root, height=10, font=FONT)
jpg_path_text.pack()

# cr2-label entry btn
cr2_path_label = Label(root, text="CR2 Directory Path:", font=FONT)
cr2_path_label.pack(padx=2, pady=2)
cr2_path_text = Entry(root, textvariable=cr2_entry_var, width=70, font=FONT)
cr2_path_text.pack()
browse_btn = Button(root, text="Browse", command=set_cr2_browse)
browse_btn.pack()

# output label entry btn
output_path_label = Label(root, text="Output Directory Path:", font=FONT)
output_path_label.pack(padx=2, pady=2)
output_path_text = Entry(root, textvariable=output_entry_var, width=70, font=FONT)
output_path_text.pack()
browse_btn_1 = Button(root, text="Browse", command=set_output_browse)
browse_btn_1.pack(padx=8, pady=8)

# Create a button to start the copying process
copy_button = Button(root, text="Copy CR2 Files", command=main)
copy_button.pack()

# Run the main loop
root.mainloop()
