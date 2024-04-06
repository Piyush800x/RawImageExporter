import os
import shutil
from tkinter import Tk, Label, Text, filedialog, Entry, StringVar
from tkinter.ttk import Button
from ttkthemes import ThemedTk


# Create the main window
root = Tk()
root.title("CR2 File Copier")

cr2_entry_var: StringVar = StringVar()
output_entry_var: StringVar = StringVar()


def copy_cr2_files():
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

    # Iterate through JPG file paths
    for jpg_path in jpg_paths:
        jpg_filename = os.path.basename(jpg_path)
        jpg_name, _ = os.path.splitext(jpg_filename)
        cr2_path = os.path.join(cr2_dir, jpg_name + ".cr2")

        # Check if the corresponding CR2 file exists
        if os.path.isfile(cr2_path):
            # Copy the CR2 file to the output directory
            output_path = os.path.join(output_dir, jpg_name + ".cr2")
            shutil.copy2(cr2_path, output_path)
            print(f"Copied {cr2_path} to {output_path}")
        else:
            print(f"No CR2 file found for {jpg_path}")


def set_cr2_browse():
    file = filedialog.askdirectory()
    cr2_entry_var.set(file)
    print(f"cr2 entry var {cr2_entry_var.get()}")


def set_output_browse():
    file = filedialog.askdirectory()
    output_entry_var.set(file)
    print(f"cr2 entry var {output_entry_var.get()}")


# Create labels and text boxes
jpg_path_label = Label(root, text="JPG File Paths (comma-separated):")
jpg_path_label.pack()
jpg_path_text = Text(root, height=2)
jpg_path_text.pack()

cr2_path_label = Label(root, text="CR2 Directory Path:")
cr2_path_label.pack()
cr2_path_text = Entry(root, textvariable=cr2_entry_var, width=70)
cr2_path_text.pack()
browse_btn = Button(root, text="Browse", command=set_cr2_browse)
browse_btn.pack()

output_path_label = Label(root, text="Output Directory Path:")
output_path_label.pack()
output_path_text = Entry(root, textvariable=output_entry_var, width=70)
output_path_text.pack()
browse_btn_1 = Button(root, text="Browse", command=set_output_browse)
browse_btn_1.pack()

# Create a button to start the copying process
copy_button = Button(root, text="Copy CR2 Files", command=copy_cr2_files)
copy_button.pack()

# Run the main loop
root.mainloop()
