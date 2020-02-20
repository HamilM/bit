from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image, ImageFont, ImageDraw
import csv

rows = []
p_img = None
img = None
img_preview = None
p_img_preview = None
global_ptr = 0

def pick_csv_command(window):
	global rows
	file_name = askopenfilename(title="Pick a CSV data file",filetypes=[("CSV file", "*.csv"), ("All files", "*.*")])
	if len(file_name) == 0:
		return
	messagebox.showinfo('Message', 'File picked: {}'.format(file_name))
	rows.clear()
	with open(file_name, 'r') as csvfile:
		csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csv_reader:
			rows.append(row)
	messagebox.showinfo('Message', 'File Read Successfully!\n{} lines were read'.format(len(rows)))


def pick_photo_command(image_window, lbl_img):
	global img,p_img
	file_name = askopenfilename(title="Pick a photo", filetypes=[("JPEG file", ("*.jpg","*.jpeg")), ("PNG file","*.png"), ("All files", "*.*")])
	if len(file_name) == 0:
		return
	img = Image.open(file_name)
	p_img = ImageTk.PhotoImage(img)
	lbl_img.config(image=p_img)
	
def do_image_refresh_nocheck(lbl_img):
	global global_ptr,img,img_preview,p_img_preview
	global_ptr = min(len(rows), global_ptr)
	img_preview = img.copy()
	draw = ImageDraw.Draw(img_preview)
	font = ImageFont.truetype("arial.ttf", 16)
	draw.text((0, 0), rows[global_ptr][1], (255,255,255), font=font)
	p_img_preview = ImageTk.PhotoImage(img_preview)
	lbl_img.config(image=p_img_preview)
	return

def do_refresh_btn(lbl_img):
	if (img == None):
		messagebox.showerror('Error', 'Image is not loaded yet!')
		return
	if (rows == None):
		messagebox.showerror('Error', 'Data file is not loaded yet!')
		return
	if (len(rows) == 0):
		messagebox.showerror('Error', 'Data file loaded but seems empty!')
		return
	do_image_refresh_nocheck(lbl_img)
	return

def do_prev(lbl_img):
	global global_ptr
	global_ptr = max(0, global_ptr - 1)
	do_refresh_btn(lbl_img)

def do_next(lbl_img):
	global global_ptr, rows
	if rows != None:
		global_ptr = min(len(rows) - 1, global_ptr + 1)
	do_refresh_btn(lbl_img)

def setup_image_window(window):
	pass

def setup_window(window, image_window):
	image_window.title("Image Preview")
	window

	window.title("Image Text Batch")
	window.geometry('1000x500')
	lbl = Label(window, text="Image-Text-Batch", font=("Arial Bold", 50))
	lbl.grid(column=0, row=0)
	btn_data = Button(window, text="pick data file", command= lambda: pick_csv_command(window))
	btn_data.grid(column=0, row=1)
	lbl_img = Label(window, image='')
	lbl_img.grid(column=1, row=2)
	btn_picture = Button(window, text="pick a picture", command = lambda: pick_photo_command(image_window, lbl_img))
	btn_picture.grid(column=1, row=1)
	btn_refresh = Button(window, text="Refresh", command = lambda: do_refresh_btn(lbl_img))
	btn_refresh.grid(column=2, row=1)
	btn_next = Button(window, text="Next", command= lambda: do_next(lbl_img))
	btn_next.grid(column=2, row=2)
	btn_prev = Button(window, text="Prev", command= lambda: do_prev(lbl_img))
	btn_prev.grid(column=3, row=2)

def main():
	window = Tk()
	image_window = Tk()
	setup_window(window, image_window)
	window.mainloop()


if __name__ == "__main__":
	main()