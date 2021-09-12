from tkinter import *
import tkinter as tk
from tkinter import ttk
import string
from DESv1 import encryption, create_rounded_key_binary_list_from_hex_key, convert_binary_to_hex

def printsth(param1, param2):
	print("sth", param1)

def get_key():
	return input_key.get("1.0", END).strip() #1.0 mean from beginning, strip required to remove empty char at the end

def get_message():
	return input_message.get("1.0", END).strip()

def get_key_and_message():
	return get_key(), get_message()

def validate(param): # both need to be in hex format
	#i dont need to check length of key/message here, need to check only if it is in hex format
	return all(c in string.hexdigits for c in param)


def encrypt_and_display():
	key = get_key()
	message = get_message()

	print("before validate")
	if validate(key) and validate(message):
		key_binary = create_rounded_key_binary_list_from_hex_key(key)
		print("message: ", message, "key_binary: ", key_binary)
		encrypted_message = encryption(message, key_binary)

		#delete old text if user click "Encrypt few times
		output_text_binary.delete('1.0', END)
		output_text_hex.delete('1.0', END)

		output_text_binary.insert("1.0", encrypted_message)
		print("encrypted msg: ", encrypted_message, "len: ", len(encrypted_message))
		output_text_hex.insert("1.0", convert_binary_to_hex(encrypted_message))


frame = tk.Tk()
frame.title("TextBox Input")
frame.geometry('600x600')

input_key = tk.Text(frame,height = 3,width = 40)
input_message = tk.Text(frame,height = 3,width = 40)
output_text_binary = tk.Text(frame, height=3, width=40, pady=10)
output_text_hex = tk.Text(frame, height=3, width=40, pady=10)
encrypt_button = tk.Button(frame,text = "Encrypt",command=encrypt_and_display )

message_label = Label(frame, text = "Message(HEX form)")
key_label = Label(frame, text="Key(HEX form)")
output_bin_label = Label(frame, text="Output in binary form")
output_hex_label = Label(frame, text="Output in hex form")

message_label.pack()
input_message.pack()
key_label.pack()
input_key.pack()
encrypt_button.pack()

output_bin_label.pack()
output_text_binary.pack()

output_hex_label.pack()
output_text_hex.pack()

'''text = StringVar()
test= Entry(frame, textvariable=text)
test.pack(fill='x', expand=True, padx= 45, pady=45)
test.focus()
test.insert(0, "Enter any Text")'''

frame.mainloop() #display window