from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import aes128 # End-To-End chat
import sys
import threading

try:
	import client
except:
	print('Server is not up.')
	sys.exit()



username = None
encKey = None


def main():

	def listening():
		while True:

			msg = client.recv()
			msg = aes128.decrypt_text(msg, encKey)

			rbox.configure(state='normal')
			rbox.insert(END, msg)
			rbox.see('end')
			rbox.configure(state='disabled')

	def printM():
		msg = mbox.get('1.0', 'end-1c')
		mbox.delete('1.0', END)

		if msg == '':
			return

		count = 0
		res = ''

		for i in msg:
			count += 1
			res += i

			if count == 20:
				res += '\n' 
				count = 0




		msg = f'{username}: {res}\n\n'
		msg = aes128.encrypt_text(msg, encKey)
		client.send(msg)
		



	def main_screen():
		global mbox
		global rbox

		rbox = Text(root, width=35, height=13, font=(None, 20), fg='light pink')
		rbox.place(x=0, y=0)
		rbox.configure(state='disabled')

		mbox = Text(root, width=30, height=3, font=(None, 20), fg='orange', bg='blue')
		mbox.place(x=0, y=450)

		sendButton = Button(root, text='>>>', fg='orange', bg='blue', pady=40, command=printM)
		sendButton.place(x=515, y=450)

		t = threading.Thread(target=listening)
		t.setDaemon(True)
		t.start()
				




	def click():
		global username
		global encKey

		if len(usernameEntry.get()) == 0:
			messagebox.showinfo('Invalid!', 'Input a username!')

		elif len(keyEntry.get()) != 16:
			messagebox.showinfo('Invalid!', 'Length of the key must be 16!')
			

		else:
			encKey = keyEntry.get()
			username = usernameEntry.get()
			usernameLabel.grid_forget()
			usernameEntry.grid_forget()
			keyEntry.grid_forget()
			keyLabel.grid_forget()
			keyButton.grid_forget()
			main_screen()

	root = Tk()
	root.title('CHAT-SOFTWARE')
	root.geometry('600x600')
	root.resizable(0,0)

	usernameLabel = Label(root, text='NAME:', fg='cyan', font=(None, 20))
	usernameLabel.grid(row=0, sticky=W)

	usernameEntry = Entry(root, width=15, fg='green', font=(None, 20))
	usernameEntry.grid(row=0, column=1, sticky=E)

	keyLabel = Label(root, text='KEY:', fg='red', font=(None, 20))
	keyLabel.grid(row=1, sticky=W)

	keyEntry = Entry(root, show='*', width=15, fg='purple', font=(None, 20))
	keyEntry.grid(row=1, column=1, sticky=E)

	keyButton = Button(root, text='USE', fg='yellow', font=(None,20), width=10, command=click)
	keyButton.grid(row=2, column=1, sticky='e' + 'w')


	root.mainloop()




main()