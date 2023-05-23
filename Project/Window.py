import os
import tkinter
import customtkinter
import VideoAnalyzer

import threading

# Define app colors, fonts, and functions
OFF_WHITE     = "#ece8e1"
LIGHT_RED     = "#ff4655"
DARK_BLUE     = "#14202e"
MIDNIGHT_BLUE = "#0f1923"

LARGE_FONT    = ("DIN Next W1G Medium", 20)
MEDIUM_FONT   = ("DIN Next W1G Medium", 16)
SMALL_FONT    = ("DIN Next W1G Medium", 12)

def select_file():
    user_file = tkinter.filedialog.askopenfile(initialdir=os.path.expanduser("~"),
                                               filetypes=[("MP4 Files", "*.mp4"),
                                                          ("QuickTime Movie Files", "*.mov"),
                                                          ("MKV Files", "*.mkv")])
    
    try:
        if user_file.name != None:
            file_name.set(user_file.name)
    except AttributeError:
        pass

def select_folder():
    user_folder = tkinter.filedialog.askdirectory(initialdir=os.path.expanduser("~"))

    if user_folder != None and user_folder != "":
        folder_name.set(user_folder)

def validate_time_before_input():
    user_input = time_before_input.get()

    if str.isdigit(user_input) and (int(user_input) >= 0 and int(user_input) <= 30):
            return True

    time_before_input.delete(0, len(user_input))
    return False

def validate_time_after_input():
    user_input = time_after_input.get()

    if str.isdigit(user_input) and (int(user_input) >= 0 and int(user_input) <= 30):
            return True

    time_after_input.delete(0, len(user_input))
    return False

def analyze_video_helper(file_path, folder_path, has_thread_executed):
    VideoAnalyzer.analyze(file_path, folder_path)
    has_thread_executed.set(True)

def analyze_video():
    file_path = file_name.get()
    folder_path = folder_name.get()

    if file_path != "No file selected" and folder_path != "No folder selected":
        # Setup and start loading bar
        submit_button.place_forget()

        loading_animation_frame = customtkinter.CTkFrame(main_frame, width=650, height=55, border_width=5, border_color=LIGHT_RED, corner_radius=0, fg_color=DARK_BLUE)
        loading_animation_frame.place(x=35, y=385)

        loading_animation = customtkinter.CTkProgressBar(loading_animation_frame,
                                                        width=630, height=35,
                                                        corner_radius=0,
                                                        fg_color=DARK_BLUE, progress_color=LIGHT_RED,
                                                        mode="indeterminate")
        loading_animation.place(x=10, y=10)
        loading_animation.start()

        # Start the clipping process
        has_thread_executed = tkinter.BooleanVar(app, value=False)
        thread = threading.Thread(target=analyze_video_helper, args=(file_path, folder_path, has_thread_executed)).start()

        # After the videos have been clipped...
        # Delete the loading bar and show the submission button
        submit_button.wait_variable(has_thread_executed)

        loading_animation.destroy()
        loading_animation_frame.destroy()

        submit_button.place(x=275, y=385)

        # Create completion window
        completion_window = customtkinter.CTkToplevel(app, fg_color=DARK_BLUE)

        completion_window.title("Clipped It!")
        completion_window.geometry(f"{450}x{200}")
        completion_window.resizable(False, False)

        completion_title = customtkinter.CTkLabel(completion_window, text="Your video has been clipped!", text_color=OFF_WHITE, font=LARGE_FONT)
        completion_title.place(x=100, y=55)

        completion_button = customtkinter.CTkButton(completion_window,
                                                   width=100, height=45,
                                                   border_width=0, corner_radius=50,
                                                   fg_color=LIGHT_RED,
                                                   text="OK", text_color=OFF_WHITE, font=("Tungsten Bold", 35),
                                                   command=completion_window.destroy)
        completion_button.place(x=175, y=100)   

        completion_window.wm_transient(app)

# -------------------------

# Initial setup
app = customtkinter.CTk()

# Configure app
app.title("Clip It!")
app.geometry(f"{960}x{500}")
app.resizable(False, False)

# Setup fonts
customtkinter.FontManager.load_font("Fonts\DIN-Next-W1G-Medium.ttf")
customtkinter.FontManager.load_font("Fonts\Tungsten-Bold.ttf")

# -------------------------

# Create "MAIN" frame
main_frame = customtkinter.CTkFrame(app, width=720, height=500, corner_radius=0, fg_color=DARK_BLUE)
main_frame.place(x=0, y=0)

# Create file input boxes
input_label = customtkinter.CTkLabel(main_frame, text="Video To Clip", text_color=OFF_WHITE, font=LARGE_FONT)
input_label.place(x=35, y=60)

file_name = tkinter.StringVar(main_frame, "No file selected")
file_input = customtkinter.CTkEntry(main_frame, 
                                    width=500, height=45, 
                                    border_width=0, corner_radius=50, 
                                    fg_color=OFF_WHITE, 
                                    textvariable=file_name, text_color=MIDNIGHT_BLUE, font=LARGE_FONT, 
                                    state="disabled")
file_input.place(x=35, y=90)

file_browse_button = customtkinter.CTkButton(main_frame, 
                                             width=125, height=45, 
                                             border_width=0, corner_radius=50, 
                                             fg_color=MIDNIGHT_BLUE, 
                                             text="Browse", text_color=OFF_WHITE, font=LARGE_FONT,
                                             command=select_file)
file_browse_button.place(x=560, y=90)

# Create file output boxes
output_label = customtkinter.CTkLabel(main_frame, text="File Destination", text_color=OFF_WHITE, font=LARGE_FONT)
output_label.place(x=35, y=225)

folder_name = tkinter.StringVar(main_frame, "No folder selected")
folder_input = customtkinter.CTkEntry(main_frame, 
                                      width=500, height=45, 
                                      border_width=0, corner_radius=50, 
                                      fg_color=OFF_WHITE, 
                                      textvariable=folder_name, text_color=MIDNIGHT_BLUE, font=LARGE_FONT, 
                                      state="disabled")
folder_input.place(x=35, y=255)

folder_browse_button = customtkinter.CTkButton(main_frame, 
                                               width=125, height=45, 
                                               border_width=0, corner_radius=50, 
                                               fg_color=MIDNIGHT_BLUE, 
                                               text="Browse", text_color=OFF_WHITE, font=LARGE_FONT,
                                               command=select_folder)
folder_browse_button.place(x=560, y=255)

# Create "Clip It!" button and loading animation
submit_button = customtkinter.CTkButton(main_frame, 
                                        width=165, height=65, border_width=0, 
                                        corner_radius=50, fg_color=LIGHT_RED, 
                                        text="CLIP IT!", text_color=OFF_WHITE, font=("Tungsten Bold", 45),
                                        command=analyze_video)
submit_button.place(x=275, y=385)

# -------------------------

# Create "OPTIONS" frame
options_frame = customtkinter.CTkFrame(app, width=240, height=500, corner_radius=0, fg_color=MIDNIGHT_BLUE)
options_frame.place(x=720, y=0)

options_title = customtkinter.CTkLabel(options_frame, text="Clipping Options", text_color=OFF_WHITE, font=LARGE_FONT) 
options_title.place(x=53, y=66)

# Create "Retrieve Timestamps" section
option_section_one = customtkinter.CTkLabel(options_frame, text="Retrieve Timestamps", text_color=OFF_WHITE, font=MEDIUM_FONT)
option_section_one.place(x=20, y=116)

checkbox_option_round_start = customtkinter.CTkCheckBox(options_frame, 
                                        width=100, height=18, 
                                        checkbox_width=12, checkbox_height=12, 
                                        corner_radius=3, 
                                        fg_color=LIGHT_RED, 
                                        text="Round Start", text_color=OFF_WHITE, font=MEDIUM_FONT)
checkbox_option_round_start.place(x=20, y=149)

checkbox_option_spike_plant = customtkinter.CTkCheckBox(options_frame, 
                                          width=100, height=18, 
                                          checkbox_width=12, checkbox_height=12, 
                                          corner_radius=3, 
                                          fg_color=LIGHT_RED, 
                                          text="Spike Plant", text_color=OFF_WHITE, font=MEDIUM_FONT)
checkbox_option_spike_plant.place(x=20, y=173)

# Create "Record Events" section
options_section_two = customtkinter.CTkLabel(options_frame, text="Record Events", text_color=OFF_WHITE, font=MEDIUM_FONT)
options_section_two.place(x=20, y=222)

radio_option = tkinter.IntVar(value=1)
radio_option_none = customtkinter.CTkRadioButton(options_frame, 
                                                  width=115, height=18, 
                                                  radiobutton_width=12, radiobutton_height=12, 
                                                  fg_color=LIGHT_RED, 
                                                  text="None", text_color=OFF_WHITE, font=MEDIUM_FONT,
                                                  variable=radio_option, value=0)
radio_option_none.place(x=20, y=255)

radio_option_round = customtkinter.CTkRadioButton(options_frame, 
                                                  width=115, height=18, 
                                                  radiobutton_width=12, radiobutton_height=12, 
                                                  fg_color=LIGHT_RED, 
                                                  text="Entire Round", text_color=OFF_WHITE, font=MEDIUM_FONT,
                                                  variable=radio_option, value=1)
radio_option_round.place(x=20, y=285)

radio_option_kills = customtkinter.CTkRadioButton(options_frame, 
                                                 width=115, height=18, 
                                                 radiobutton_width=12, radiobutton_height=12, 
                                                 fg_color=LIGHT_RED, 
                                                 text="Kills Only", 
                                                 text_color=OFF_WHITE, font=MEDIUM_FONT,
                                                 variable=radio_option, value=2)
radio_option_kills.place(x=20, y=315)

record_num_kills_menu = customtkinter.CTkOptionMenu(options_frame, 
                                                    width=55, height=20, 
                                                    fg_color=OFF_WHITE, 
                                                    button_color=LIGHT_RED, 
                                                    dropdown_fg_color=OFF_WHITE, dropdown_text_color=MIDNIGHT_BLUE, 
                                                    values=["1", "2", "3", "4", "5+"], text_color=MIDNIGHT_BLUE, font=MEDIUM_FONT,
                                                    anchor="center")
record_num_kills_menu.place(x=123, y=315)

# Create "Advanced" section
options_label_three = customtkinter.CTkLabel(options_frame, text="Advanced", text_color=OFF_WHITE, font=MEDIUM_FONT)
options_label_three.place(x=20, y=364)

time_to_clip_before_tooltip = customtkinter.CTkLabel(options_frame, text="Time Clipped Before Kills", text_color=OFF_WHITE, font=SMALL_FONT)
time_to_clip_before_tooltip.place(x=20, y=394)

time_before_input = customtkinter.CTkEntry(options_frame, 
                                           width=35, height=15, 
                                           border_width=0, corner_radius=50,
                                           fg_color=OFF_WHITE,
                                           placeholder_text="5", placeholder_text_color=MIDNIGHT_BLUE,
                                           text_color=MIDNIGHT_BLUE, font=SMALL_FONT,
                                           justify="center")
time_before_input.configure(validate="focus", validatecommand=validate_time_before_input)
time_before_input.place(x=185, y=399)

time_to_clip_after_tooltip = customtkinter.CTkLabel(options_frame, text="Time Clipped After Kills", text_color=OFF_WHITE, font=SMALL_FONT)
time_to_clip_after_tooltip.place(x=20, y=420)

time_after_input = customtkinter.CTkEntry(options_frame,
                                          width=35, height=15,
                                          border_width=0, corner_radius=50,
                                          fg_color=OFF_WHITE,
                                          placeholder_text="5", placeholder_text_color=MIDNIGHT_BLUE,
                                          text_color=MIDNIGHT_BLUE, font=SMALL_FONT,
                                          justify="center")
time_after_input.configure(validate="focus", validatecommand=validate_time_after_input)
time_after_input.place(x=185, y=425)

# -------------------------

# Deploy app
app.mainloop()