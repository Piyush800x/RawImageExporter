import os
import shutil
import sys
import threading
from tkinter import Label, Text, filedialog, Entry, StringVar, HORIZONTAL, messagebox, Toplevel, BooleanVar
from tkinter.ttk import Button, Progressbar, Checkbutton
from ttkthemes import ThemedTk
# from time import sleep

FONT = ("Helvetica", 12)
FONT_LABEL = ("Helvetica", 12)


class MainWindow(ThemedTk):

    def __init__(self):
        super().__init__()
        self.title("Raw Image Exporter")
        self.iconbitmap("logo.ico")
        # self.geometry("500x360")
        self.protocol('WM_DELETE_WINDOW', lambda: [sys.exit(0)])
        # vars
        self.cr2_entry_var: StringVar = StringVar()
        self.output_entry_var: StringVar = StringVar()
        self.is_cr2: BooleanVar = BooleanVar()
        self.is_cr3: BooleanVar = BooleanVar()
        self.is_nef: BooleanVar = BooleanVar()
        self.is_arw: BooleanVar = BooleanVar()

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
        cr2_path_label = Label(self, text="CR2/CR3/NEF/ARW Directory Path:", font=FONT)
        cr2_path_label.pack(padx=2, pady=2)
        cr2_path_text = Entry(self, textvariable=self.cr2_entry_var, width=70, font=FONT)
        cr2_path_text.pack(padx=2, pady=2)
        check_1: Checkbutton = Checkbutton(self, text="CR2", variable=self.is_cr2, onvalue=True, offvalue=False)
        check_1.pack()
        check_4: Checkbutton = Checkbutton(self, text="CR3", variable=self.is_cr3, onvalue=True, offvalue=False)
        check_4.pack()
        check_2: Checkbutton = Checkbutton(self, text="NEF", variable=self.is_nef, onvalue=True, offvalue=False)
        check_2.pack()
        check_3: Checkbutton = Checkbutton(self, text="ARW", variable=self.is_arw, onvalue=True, offvalue=False)
        check_3.pack()
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
        copy_button = Button(self, text="Export", command=lambda: [threading.Thread(target=self.main,
                                                                                            daemon=True).start()])
        copy_button.pack(padx=5, pady=5)

    def set_cr2_browse(self):
        file = filedialog.askdirectory()
        self.cr2_entry_var.set(file)
        print(f'CR2 {self.is_cr2.get()}')
        print(f'CR3 {self.is_cr3.get()}')
        print(f'nef {self.is_nef.get()}')
        print(f'arw {self.is_arw.get()}')
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
        raw_dir = self.cr2_entry_var.get()

        # output_dir = output_path_text.get("1.0", "end-1c")
        # output_dir.strip('"')
        output_dir = self.output_entry_var.get()

        print(f'JPG files {jpg_paths}')
        print(f'cr2 dir {raw_dir}')
        print(f"output dir {output_dir}")

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        chunk_size = (100 / len(jpg_paths))

        # Iterate through JPG file paths
        for jpg_path in jpg_paths:
            jpg_filename = os.path.basename(jpg_path)
            print(f"jpg_filename: {jpg_filename}")
            for root, _, files in os.walk(raw_dir):
                print(f"root: {root}")
                for file in files:
                    print(f'file: {file}')
                    # CR2 only
                    if self.is_cr2:
                        print("-----------------CR2 called")
                        if (file.endswith(".CR2") or file.endswith(".cr2")) and file.startswith(jpg_filename[:-4]):
                            cr2_path = os.path.join(root, file)
                            print(f"NEW CR2 {cr2_path}")
                            shutil.copy(cr2_path, output_dir)
                            print(f"CR2 file '{os.path.basename(cr2_path)}' copied to '{output_dir}'")
                        if (file.endswith(".CR2") or file.endswith(".cr2")) and file.startswith(jpg_filename[:-3]):
                            cr2_path = os.path.join(root, file)
                            print(f"NEW CR2 {cr2_path}")
                            shutil.copy(cr2_path, output_dir)
                            print(f"CR2 file '{os.path.basename(cr2_path)}' copied to '{output_dir}'")

                    # CR3 only
                    if self.is_cr3:
                        print("-----------------CR3 called")
                        if (file.endswith(".CR3") or file.endswith(".cr3")) and file.startswith(jpg_filename[:-4]):
                            cr3_path = os.path.join(root, file)
                            print(f"NEW CR3 {cr3_path}")
                            shutil.copy(cr3_path, output_dir)
                            print(f"CR3 file '{os.path.basename(cr3_path)}' copied to '{output_dir}'")
                        if (file.endswith(".CR3") or file.endswith(".cr3")) and file.startswith(jpg_filename[:-3]):
                            cr3_path = os.path.join(root, file)
                            print(f"NEW CR3 {cr3_path}")
                            shutil.copy(cr3_path, output_dir)
                            print(f"CR3 file '{os.path.basename(cr3_path)}' copied to '{output_dir}'")

                    # NEF only
                    if self.is_nef:
                        print("-----------------NEF called")
                        if (file.endswith(".NEF") or file.endswith(".nef")) and file.startswith(jpg_filename[:-4]):
                            nef_path = os.path.join(root, file)
                            print(f"NEW NEF {nef_path}")
                            shutil.copy(nef_path, output_dir)
                            print(f"NEF file '{os.path.basename(nef_path)}' copied to '{output_dir}'")
                        if (file.endswith(".NEF") or file.endswith(".nef")) and file.startswith(jpg_filename[:-3]):
                            nef_path = os.path.join(root, file)
                            print(f"NEW NEF {nef_path}")
                            shutil.copy(nef_path, output_dir)
                            print(f"NEF file '{os.path.basename(nef_path)}' copied to '{output_dir}'")

                    # ARW only
                    if self.is_arw:
                        print("-----------------ARW called")
                        if (file.endswith(".ARW") or file.endswith(".arw")) and file.startswith(jpg_filename[:-4]):
                            arw_path = os.path.join(root, file)
                            print(f"NEW ARW {arw_path}")
                            shutil.copy(arw_path, output_dir)
                            print(f"ARW file '{os.path.basename(arw_path)}' copied to '{output_dir}'")
                        if (file.endswith(".ARW") or file.endswith(".arw")) and file.startswith(jpg_filename[:-3]):
                            arw_path = os.path.join(root, file)
                            print(f"NEW ARW {arw_path}")
                            shutil.copy(arw_path, output_dir)
                            print(f"ARW file '{os.path.basename(arw_path)}' copied to '{output_dir}'")

                    # updating process
                self.progress += chunk_size

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
            if self.progress >= 100:
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
