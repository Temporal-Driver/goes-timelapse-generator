import tkinter as tk
from tkinter import ttk



def submit(preset, band, size, box_east, box_west, box_conus, box_disk):
    selected_values = {
        "preset": preset.get(),
        "band": band.get(),
        "size": size.get(),
        "east": box_east.get(),
        "west": box_west.get(),
        "conus": box_conus.get(),
        "disk": box_disk.get()
        # Add more GUI elements as needed
    }
    # I'm importing here to avoid a circular import error
    from goes_GUI import process_submission
    process_submission(selected_values)


class GUIApplication(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("GOES Timelapse Generator")
        self.create_widgets()

    def create_widgets(self):
        # Dropdown menu options
        preset_options = ["Option 1", "Option 2", "Option 3"]
        band_options = ["Band 1", "Band 2", "Band 3"]
        size_options = ["Small", "Medium", "Large"]

        # Create the dropdown menus
        preset = ttk.Combobox(self, values=preset_options)
        preset_label = tk.Label(self, text="Preset:")
        preset_label.grid(row=0, column=0)
        preset.grid(row=0, column=1)

        band = ttk.Combobox(self, values=band_options)
        band_label = tk.Label(self, text="Band:")
        band_label.grid(row=1, column=0)
        band.grid(row=1, column=1)

        size = ttk.Combobox(self, values=size_options)
        size_label = tk.Label(self, text="Size:")
        size_label.grid(row=2, column=0)
        size.grid(row=2, column=1)

        # Create the stereo boxes
        box_east = tk.BooleanVar()
        box_west = tk.BooleanVar()
        box_conus = tk.BooleanVar()
        box_disk = tk.BooleanVar()

        satellite_east_check = tk.Checkbutton(self, text="GOES-16 (East)", variable=box_east)
        satellite_east_check.grid(row=3, column=0)

        satellite_west_check = tk.Checkbutton(self, text="GOES-18 (West)", variable=box_west)
        satellite_west_check.grid(row=3, column=1)

        region_conus_check = tk.Checkbutton(self, text="CONUS (Continental U.S.)", variable=box_conus)
        region_conus_check.grid(row=4, column=0)

        region_disk_check = tk.Checkbutton(self, text="Full Disk", variable=box_disk)
        region_disk_check.grid(row=4, column=1)

        # Create a separator
        separator = ttk.Separator(self)
        separator.grid(row=5, columnspan=2, pady=10)

        # Create the text inputs
        start_label = tk.Label(self, text="Start Date:")
        start_label.grid(row=6, column=0)
        start_entry = tk.Entry(self)
        start_entry.grid(row=6, column=1)

        end_label = tk.Label(self, text="End Date:")
        end_label.grid(row=7, column=0)
        end_entry = tk.Entry(self)
        end_entry.grid(row=7, column=1)

        # Create the checkbox
        keep_var = tk.BooleanVar()
        keep_check = tk.Checkbutton(self, text="Keep", variable=keep_var)
        keep_check.grid(row=8, columnspan=2)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=lambda: submit(preset, band, size, box_east,
                                                                              box_west, box_conus, box_disk))
        submit_button.grid(row=9, columnspan=2)

        # Set command for radio buttons to deselect mutually exclusive options
        satellite_east_check.config(command=lambda: box_west.set(False))
        satellite_west_check.config(command=lambda: box_east.set(False))
        region_conus_check.config(command=lambda: box_disk.set(False))
        region_disk_check.config(command=lambda: box_conus.set(False))
