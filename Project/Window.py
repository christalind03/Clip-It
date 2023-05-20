import tkinter
import customtkinter

# Initial setup
window = customtkinter.CTk()

# Configure window
window.title("Clip It!")
window.geometry(f"{960}x{500}")
window.resizable(False, False)

# Define app colors and font
off_white = "#ece8e1"
light_red = "#ff4655"
dark_blue = "#14202e"
midnight_blue = "#0f1923"

large_font = ("DIN Next W1G Medium", 20)
medium_font = ("DIN Next W1G Medium", 16)
small_font = ("DIN Next W1G Medium", 12)

# -------------------------

# Create "MAIN" frame
main_frame = customtkinter.CTkFrame(window, width=720, height=500, corner_radius=0,fg_color=dark_blue)
main_frame.place(x=0, y=0)

# Create file input boxes
input_label = customtkinter.CTkLabel(main_frame, text="Video To Clip", text_color=off_white, font=large_font)
input_label.place(x=35, y=60)

file_name = tkinter.StringVar(main_frame, "No file selected")
file_input = customtkinter.CTkEntry(main_frame, 
                                    width=500, height=45, 
                                    border_width=0, corner_radius=50, 
                                    fg_color=off_white, 
                                    textvariable=file_name, text_color=midnight_blue, font=large_font, 
                                    state="disabled")
file_input.place(x=35, y=90)

file_browse_button = customtkinter.CTkButton(main_frame, 
                                             width=125, height=45, 
                                             border_width=0, corner_radius=50, 
                                             fg_color=midnight_blue, 
                                             text="Browse", text_color=off_white, font=large_font)
file_browse_button.place(x=560, y=90)

# Create file output boxes
output_label = customtkinter.CTkLabel(main_frame, text="File Destination", text_color=off_white, font=large_font)
output_label.place(x=35, y=225)

folder_name = tkinter.StringVar(main_frame, "No folder selected")
folder_input = customtkinter.CTkEntry(main_frame, 
                                      width=500, height=45, 
                                      border_width=0, corner_radius=50, 
                                      fg_color=off_white, 
                                      textvariable=folder_name, text_color=midnight_blue, font=large_font, 
                                      state="disabled")
folder_input.place(x=35, y=255)

folder_browse_button = customtkinter.CTkButton(main_frame, 
                                               width=125, height=45, 
                                               border_width=0, corner_radius=50, 
                                               fg_color=midnight_blue, 
                                               text="Browse", text_color=off_white, font=large_font)
folder_browse_button.place(x=560, y=255)

# Create "Clip It!" button
submit_button = customtkinter.CTkButton(main_frame, 
                                        width=165, height=65, border_width=0, 
                                        corner_radius=50, fg_color=light_red, 
                                        text="CLIP IT!", text_color=off_white, font=("Tungsten Bold", 45))
submit_button.place(x=275, y=385)

# -------------------------

# Create "OPTIONS" frame
options_frame = customtkinter.CTkFrame(window, width=240, height=500, corner_radius=0, fg_color=midnight_blue)
options_frame.place(x=720, y=0)

options_title = customtkinter.CTkLabel(options_frame, text="Clipping Options", text_color=off_white, font=large_font) 
options_title.place(x=53, y=41)

# Create "Retrieve Timestamps" section
option_section_one = customtkinter.CTkLabel(options_frame, text="Retrieve Timestamps", text_color=off_white, font=medium_font)
option_section_one.place(x=20, y=105)

checkbox_option_round_start = customtkinter.CTkCheckBox(options_frame, 
                                        width=100, height=18, 
                                        checkbox_width=12, checkbox_height=12, 
                                        corner_radius=3, 
                                        fg_color=light_red, 
                                        text="Round Start", text_color=off_white, font=medium_font)
checkbox_option_round_start.place(x=20, y=139)

checkbox_option_spike_plant = customtkinter.CTkCheckBox(options_frame, 
                                          width=100, height=18, 
                                          checkbox_width=12, checkbox_height=12, 
                                          corner_radius=3, 
                                          fg_color=light_red, 
                                          text="Spike Plant", text_color=off_white, font=medium_font)
checkbox_option_spike_plant.place(x=20, y=163)

# Create "Record Events" section
options_section_two = customtkinter.CTkLabel(options_frame, text="Record Events", text_color=off_white, font=medium_font)
options_section_two.place(x=20, y=211)

radio_option = tkinter.IntVar(value=1)
radio_option_round = customtkinter.CTkRadioButton(options_frame, 
                                                  width=115, height=18, 
                                                  radiobutton_width=12, radiobutton_height=12, 
                                                  fg_color=light_red, 
                                                  text="Entire Round", text_color=off_white, font=medium_font,
                                                  variable=radio_option, value=0)
radio_option_round.place(x=20, y=245)

radio_option_kills = customtkinter.CTkRadioButton(options_frame, 
                                                 width=115, height=18, 
                                                 radiobutton_width=12, radiobutton_height=12, 
                                                 fg_color=light_red, 
                                                 text="Kills Only", 
                                                 text_color=off_white, font=medium_font,
                                                 variable=radio_option, value=1)
radio_option_kills.place(x=20, y=275)

record_num_kills_menu = customtkinter.CTkOptionMenu(options_frame, 
                                                    width=55, height=20, 
                                                    fg_color=off_white, 
                                                    button_color=light_red, 
                                                    dropdown_fg_color=off_white, dropdown_text_color=midnight_blue, 
                                                    values=["1", "2", "3", "4", "5+"], text_color=midnight_blue, font=medium_font)
record_num_kills_menu.place(x=123, y=274)

# Create "Advanced" section
options_label_three = customtkinter.CTkLabel(options_frame, text="Advanced", text_color=off_white, font=medium_font)
options_label_three.place(x=20, y=324)

time_to_clip_before_tooltip = customtkinter.CTkLabel(options_frame, text="Time Clipped Before Events:", text_color=off_white, font=small_font)
time_to_clip_before_tooltip.place(x=20, y=354)

time_to_clip_before_event = tkinter.StringVar(options_frame, 5)
time_before_input = customtkinter.CTkEntry(options_frame, 
                                           width=35, height=15, 
                                           border_width=0, corner_radius=50,
                                           fg_color=off_white,
                                           placeholder_text="5", placeholder_text_color=midnight_blue,
                                           text_color=midnight_blue, font=small_font)
time_before_input.place(x=185, y=353)

time_to_clip_after_tooltip = customtkinter.CTkLabel(options_frame, text="Time Clipped After Events:", text_color=off_white, font=small_font)
time_to_clip_after_tooltip.place(x=20, y=380)

time_to_clip_after_event = tkinter.StringVar(options_frame, 5)
time_after_input = customtkinter.CTkEntry(options_frame,
                                          width=35, height=15,
                                          border_width=0, corner_radius=50,
                                          fg_color=off_white,
                                          placeholder_text="5", placeholder_text_color=midnight_blue,
                                          text_color=midnight_blue, font=small_font)
time_after_input.place(x=185, y=380)

# -------------------------

# Deploy window
window.mainloop()