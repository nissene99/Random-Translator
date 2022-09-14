# create GUI for the program with tkinter
import json
import time
import tkinter as tk
import random

from translate import translate as tr, random_translate as rtr, SPRACHEN




def randomcolor(button):
	# change the color of the button to a random color
	# this function is used for the random translate 

	button.config(bg="#%06x" % random.randint(0, 0xFFFFFF))


def seconds2time(seconds):
	# convert seconds to hours, minutes, seconds
	text = ""

	seconds = int(seconds)
	hours = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60

	if hours > 0:
		text += f"{hours}h "
	if minutes > 0:
		text += f"{minutes}m "
	if seconds > 0:
		text += f"{seconds}s"

	return text


class GUI(tk.Tk):
	def __init__(self):
		super().__init__()
		self.HELP_TEXT = f"""
		Übersetzer
		Dieses Programm übersetzt einen Text in eine andere Sprache mithilfe des Google Übersetzers.

		Im oberen Feld kann der Text eingegeben werden, der übersetzt werden soll.
		Der übersetzte Text wird im unteren Feld angezeigt.
		
		Übersetzen: Übersetzt den Text mit der Standardübersetzung.
		(Deutsch → Latein → Koreanisch → Russisch → Somali → Zulu → Georgisch → Kroatisch → Deutsch)
		
		Zufällig übersetzen: Übersetzt den Text in eine zufällige Sprache.
		Die Anzahl der zufälligen Sprachen kann im Feld „Anzahl Iterationen“ eingestellt werden.
		Die Maximalwert ist {len(SPRACHEN.keys()) + 1}.
		
		Wenn der Text übersetzt wurde, kann er in die Zwischenablage kopiert werden.
		Dazu klickt man auf das Ausgabefeld mit der linken Maustaste.
		Je höher die Anzahl der Iteration wird, desto länger dauert die Übersetzung.""".replace("\t", "")
		self.icon = None
		self.real_duration_label = None
		self.real_duration = 0
		self.help_button = None
		self.line = None
		self.duration_field = None
		self.number_field = None
		self.number_label = None
		self.translate_button = None
		self.button_frame = None
		self.output_scrollbar = None
		self.output_field = None
		self.output_label = None
		self.input_scrollbar = None
		self.input_field = None
		self.input_label = None
		self.random_translate_button = None
		self.title("CPP Google Übersetzer")
		self.geometry("500x675")
		self.resizable(True, True)
		self.font = ("Arial", 12)
		# set the font for the whole GUI
		self.option_add("*Font", self.font)
		self.create_widgets()
		self.duration_per_language = 2.34121889
		# check if dark mode is enabled
		if self.winfo_rgb(self.cget("bg"))[0] < 100:
			self.color = "white"
		else:
			self.color = "black"

		# set the theme for the GUI
		if self.color == "black":
			self.icon="dark.ico"
			self.config(bg="#333333")
			self.input_label.config(bg="#333333", fg="white")
			self.output_label.config(bg="#333333", fg="white")
			self.number_label.config(bg="#333333", fg="white")
			self.input_field.config(bg="#333333", fg="white")
			self.output_field.config(bg="#333333", fg="white")
			self.number_field.config(bg="#333333", fg="white")
			self.translate_button.config(bg="#333333", fg="white")
			self.random_translate_button.config(bg="#333333", fg="white")
			self.button_frame.config(bg="#333333")
			self.input_scrollbar.config(bg="#333333", activebackground="#333333", troughcolor="#333333")
			self.output_scrollbar.config(bg="#333333", activebackground="#333333", troughcolor="#333333")
			self.duration_field.config(bg="#333333", fg="white")
			self.help_button.config(bg="#333333", fg="white")
			self.real_duration_label.config(bg="#333333", fg="white")

			# make buttons look like buttons
			self.translate_button.config(relief="raised")
			self.random_translate_button.config(relief="raised")

			# when the mouse is over the button, change the color
			self.translate_button.bind("<Enter>", lambda e: self.translate_button.config(bg="#555555"))
			self.translate_button.bind("<Leave>", lambda e: self.translate_button.config(bg="#333333"))

			# add gradient to the buttons
			self.random_translate_button.bind("<Enter>", lambda e: randomcolor(self.random_translate_button))
			self.random_translate_button.bind("<Leave>", lambda e: self.random_translate_button.config(bg="#333333"))
		else:
			self.icon = "light.ico"
			self.config(bg="white")
			self.input_label.config(bg="white", fg="black")
			self.output_label.config(bg="white", fg="black")
			self.number_label.config(bg="white", fg="black")
			self.input_field.config(bg="white", fg="black")
			self.output_field.config(bg="white", fg="black")
			self.number_field.config(bg="white", fg="black")
			self.translate_button.config(bg="white", fg="black")
			self.random_translate_button.config(bg="white", fg="black")
			self.button_frame.config(bg="white")
			self.input_scrollbar.config(bg="white", activebackground="white", troughcolor="white")
			self.output_scrollbar.config(bg="white", activebackground="white", troughcolor="white")
			self.duration_field.config(bg="white", fg="black")
			self.help_button.config(bg="white", fg="black")
			self.real_duration_label.config(bg="white", fg="black")

			# make buttons look like buttons
			self.translate_button.config(relief="raised")
			self.random_translate_button.config(relief="raised")

			# when the mouse is over the button, change the color
			self.translate_button.bind("<Enter>", lambda e: self.translate_button.config(bg="#e6e6e6"))
			self.translate_button.bind("<Leave>", lambda e: self.translate_button.config(bg="white"))

			# add gradient to the buttons
			self.random_translate_button.bind("<Enter>", lambda e: randomcolor(self.random_translate_button))
			self.random_translate_button.bind("<Leave>", lambda e: self.random_translate_button.config(bg="white"))
		self.iconbitmap(self.icon)

	def create_widgets(self):
		# create input field with scrollbar and output field with scrollbar
		self.input_label = tk.Label(self, text="Zu übersetzender Text")
		self.input_label.grid(row=0, column=0, sticky="w")
		self.input_field = tk.Text(self, width=50, height=10)
		self.input_field.grid(row=1, column=0, padx=10, pady=10)
		self.input_scrollbar = tk.Scrollbar(self, command=self.input_field.yview)
		self.input_scrollbar.grid(row=1, column=1, sticky="ns")
		self.input_field["yscrollcommand"] = self.input_scrollbar.set

		# if the input field is changed, clear the output field
		self.input_field.bind("<Key>", lambda e: self.output_field.delete("1.0", "end"))

		self.output_label = tk.Label(self, text="Übersetzter Text")
		self.output_label.grid(row=2, column=0, sticky="w")
		self.output_field = tk.Text(self, width=50, height=10)
		self.output_field.grid(row=3, column=0, padx=10, pady=10)
		self.output_scrollbar = tk.Scrollbar(self, command=self.output_field.yview)
		self.output_scrollbar.grid(row=3, column=1, sticky="ns")
		self.output_field["yscrollcommand"] = self.output_scrollbar.set
		# prevent the user from writing in the output field
		self.output_field.bind("<Key>", lambda e: "break")
		# disable blinking cursor
		self.output_field.config(insertofftime=0, insertontime=0)

		# if user clicks on the output field copy the text to the clipboard and show a message
		self.output_field.bind("<Button-1>", lambda e: self.copy())

		# create grid for buttons
		self.button_frame = tk.Frame(self)
		self.button_frame.grid(row=4, column=0, padx=10, pady=10)

		# create button to translate the text
		self.translate_button = tk.Button(self.button_frame, text="Übersetzen", command=self.translate)
		self.translate_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

		# draw a horizontal line
		self.line = tk.Canvas(
				self.button_frame, width=500, height=0.5, bg="white", highlightthickness=1
		)
		self.line.grid(row=1, column=0, padx=0, pady=0)

		# change width of line to fit the window
		self.bind("<Configure>", lambda e: self.line.config(width=self.winfo_width() - 20))

		# create button to translate the text randomly
		self.random_translate_button = tk.Button(
				self.button_frame, text="Zufällig übersetzen", command=self.random_translate
		)
		self.random_translate_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

		# create input field for number of languages to translate to
		self.number_label = tk.Label(self.button_frame, text="Anzahl Iterationen (Wenn zufällig übersetzt wird)")
		self.number_label.grid(row=4, column=0, sticky="wn")
		# create number field
		self.number_field = tk.Entry(self.button_frame, width=5)
		self.number_field.grid(row=4, column=0, sticky="en")
		self.number_field.insert(0, "5")
		self.number_field.bind("<Leave>", lambda e: self.checknumber())

		self.real_duration_label = tk.Label(
				self.button_frame, text="Tatsächliche Übersetzungszeit: {}".format(
						seconds2time(self.real_duration)
				)
		)
		self.real_duration_label.grid(row=3, column=0, sticky="w")

		with open("stats.json") as f:
			stats = json.loads(f.read())
			try:
				duration = stats[self.number_field.get()]
			except KeyError:
				duration = 0
			self.duration_field = tk.Label(
					self.button_frame,
					text="Dauer: ~{}".format(seconds2time(duration)),
			)
		self.duration_field.grid(row=3, column=0, sticky="e")

		self.help_button = tk.Button(self.button_frame, text="Hilfe", command=self.help)
		self.help_button.grid(row=5, column=0, sticky="en")

	def checknumber(self):
		if self.number_field.get() == "" or self.number_field.get().isdigit() == False:
			self.number_field.delete(0, "end")
			self.number_field.insert(0, "1")
		elif int(self.number_field.get()) < 1:
			self.number_field.delete(0, "end")
			self.number_field.insert(0, "1")
		elif int(self.number_field.get()) > len(SPRACHEN.keys()) + 1:
			self.number_field.delete(0, "end")
			self.number_field.insert(0, f"{len(SPRACHEN.keys()) + 1}")
		self.update()

	def update(self) -> None:
		"""Update the gui"""
		with open("stats.json") as f:
			stats = json.loads(f.read())
			try:
				duration = stats[self.number_field.get()]
			except KeyError:
				duration = 0
			self.duration_field.config(
					text="Dauer: ~{}".format(seconds2time(duration))
			)
		self.real_duration_label.config(
				text="Tatsächliche Übersetzungszeit: {}".format(seconds2time(self.real_duration))
		)
		super().update()

	def copy(self):
		# copy the text from the output field to the clipboard
		self.clipboard_clear()
		self.clipboard_append(self.output_field.get("1.0", "end"))

		# create popup message and destroy it after 1 second
		message = tk.Toplevel(self)
		message.geometry(f"+{self.winfo_pointerx()}+{self.winfo_pointery()}")
		message.config(bg="#333333")
		message.attributes("-alpha", 0.8)
		message.attributes("-topmost", True)
		message.overrideredirect(True)
		message.title("Kopiert")
		message.resizable(False, False)
		message_label = tk.Label(message, text="Text wurde in die Zwischenablage kopiert")
		message_label.config(bg="#333333", fg="#ffffff")
		message_label.pack()
		for i in range(0, 100, 5):
			message.attributes("-alpha", 1 - i / 100)
			message.update()
			time.sleep(0.05)
		message.destroy()

	def loading(self, text=None):
		# insert text into the output field
		if text is None:
			text = "\nÜbersetze..."
		if text is not None:
			self.output_field.insert("1.0", text)
		self.update()

	# Deutsch -> Latein -> Koreanisch -> Russisch -> Somali -> Zulu -> Georgisch -> Kroatisch -> Deutsch
	def translate(self):
		difference = 0
		# get the text from the input field
		text = self.input_field.get("1.0", "end")
		self.loading()
		self.loading(u"\nÜbersetze in Latein...")
		translated_text = tr(text, "la")
		self.loading(u"\nÜbersetze in Koreanisch...")
		translated_text = tr(translated_text, "ko")
		self.loading(u"\nÜbersetze in Russisch...")
		translated_text = tr(translated_text, "ru")
		self.loading(u"\nÜbersetze in Somali...")
		translated_text = tr(translated_text, "so")
		self.loading(u"\nÜbersetze in Zulu...")
		translated_text = tr(translated_text, "zu")
		self.loading(u"\nÜbersetze in Georgisch...")
		translated_text = tr(translated_text, "ka")
		self.loading(u"\nÜbersetze in Kroatisch...")
		translated_text = tr(translated_text, "hr")
		self.loading(u"\nÜbersetze in Deutsch...")
		translated_text = tr(translated_text, "de")
		# clear the output field
		self.output_field.delete("1.0", "end")
		# insert the translated text into the output field
		self.output_field.insert("1.0", translated_text)
		self.update()

	def random_translate(self):
		# get the text from the input field
		text = self.input_field.get("1.0", "end")

		anzahl = self.number_field.get()
		if int(anzahl) < 0:
			anzahl = 1

		with open("stats.json", "r") as f:
			stats = json.loads(f.read())
			try:
				duration = stats[anzahl]
			except KeyError:
				duration = 0
			self.output_field.insert(
					"1.0", u"\nUngefähre Dauer: {}.\n".format(
							seconds2time(duration)
					)
			)
		self.update()
		self.loading(u"\nÜbersetze zufällig...")
		t0 = time.time()
		translated_text = rtr(text, int(anzahl), self.output_field)
		diff = time.time() - t0
		self.real_duration = diff
		stats = None
		with open("stats.json") as file:
			stats = json.loads(file.read())
			if str(anzahl) not in stats.keys():
				stats[str(anzahl)] = diff
			elif stats[str(anzahl)] != 0:
				stats[str(anzahl)] = (stats[str(anzahl)] + diff) / 2
			else:
				stats[str(anzahl)] = diff
		with open("stats.json", "w") as file:
			file.write(json.dumps(stats))
		self.update()
		# clear the output field
		self.output_field.delete("1.0", "end")
		# insert the translated text into the output field
		self.output_field.insert("1.0", translated_text)
		self.update()

	def help(self):
		# create popup message and destroy it after 1 second
		message = tk.Toplevel(self)
		message.config(bg="#333333")
		message.title("Hilfe")
		message.geometry("800x300")
		message.resizable(False, False)
		grid = tk.Frame(message)
		grid.config(bg="#333333")
		grid.grid(row=0, column=0, padx=10, pady=10)
		maxwidth = 0
		counter = 0
		for line in self.HELP_TEXT.splitlines():
			l = tk.Label(grid, text=line)
			if line == "Übersetzer":
				l.config(font=("Helvetica", 20))
			l.config(fg="white", bg="#333333")

			l.grid(row=counter, column=0, padx=10, pady=10)
			# center the text
			l.grid_columnconfigure(0, weight=1)
			if l.winfo_reqwidth() > maxwidth:
				maxwidth = l.winfo_reqwidth()
			message.geometry(f"{maxwidth + 40}x{len(self.HELP_TEXT.splitlines() * 45)}")
			counter += 1
		# move the window to the mouse position
		message.geometry(f"+{self.winfo_pointerx() // 2}+{self.winfo_pointery() // 2}")


if __name__ == "__main__":
	gui = GUI()
	gui.mainloop()
