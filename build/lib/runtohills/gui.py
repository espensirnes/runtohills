#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from multiprocessing import pool
import time
#todo:enable finnish control
try:
	import questions as quest
except:
	from . import questions as quest
	
class window:
	def __init__(self,title,iconpath=None,height=200,width=400):
		self.win= tk.Tk()
		self.win.title(title)
		self.win.geometry('%sx%s' %(width,height))
		if not iconpath=='':
			self.win.iconbitmap(iconpath)
			
		self.label=tk.StringVar(self.win)
		label=tk.Label(self.win,textvariable=self.label)
		self.label.set("Please wait while the game loads")
		label.place(x=20, y=30,in_=self.win)
		
		
		self.progressbar=ttk.Progressbar(self.win,orient=tk.HORIZONTAL,length=200,mode='determinate')
		self.progressbar.place(x=50, y=100,in_=self.win)
		
		
		self.win.attributes('-topmost', True)




	def close(self):
		self.win.destroy()
		
	def update(self,value):
		self.progressbar['value']=value
		self.win.update_idletasks()		
		

def prequestions(record):
	q=questions(quest.preexperiment, 'Innledende spørsmål', record,True,leavbutton='Gå videre')
	q.mainloop()
	
	
def postquestions(record):
	q=questions(quest.postexperiment, 'Avdsluttende spørsmål', record,leavbutton='Avslutt')
	q.mainloop()


class questions(tk.Tk):
	def __init__(self,questions,title,record,has_id=False,height=400,width=1000,leavbutton='Close'):
		tk.Tk.__init__(self)	
		self.geometry('%sx%s' %(width,height))
		self.attributes("-fullscreen", True)
		self.fullscreen=True
		self.title(title)
		self.has_id=has_id
		self.record=record
		self.name=title
		self.questions=[]
		self.heading=tk.Label(self,text=title,font='Arial 14 bold')
		self.rowconfigure(0,weight=1)
		self.heading.grid(sticky='NSEW',row=0)
		for i in range(len(questions)):
			q=question(self, questions[i],i+1)
			self.questions.append(q)
		self.outputframe_text=tk.StringVar()
		self.outputframe=tk.Label(self,textvariable=self.outputframe_text,font='Arial 14 bold',fg='red',)
		self.outputframe.grid(sticky='NSEW',row=i+2)
		self.Continue=tk.Button(self,text=leavbutton,command=self.close,font='Arial 14')
		
		self.Continue.grid(sticky='SEW',row=i+3)
		self.bind("<Escape>", self.toggle_fullscreen)
		
	def toggle_fullscreen(self,event):
		self.fullscreen=not self.fullscreen
		self.attributes("-fullscreen", self.fullscreen)
		
	def close(self):
		if self.has_id:
			self.record['SubjectID']=self.questions[0].answer_str.get()
		for i in range(self.has_id,len(self.questions)):
			s=self.questions[i].answer_str.get()
			self.record[f"{self.name}:{i}"]=s
			if s=='':
				self.outputframe_text.set('Alle felter må fylles ut')
				return
		self.destroy()
		
		
class question:
	def __init__(self,master,q,i):
		self.question=q[0]
		self.alternatives=q[1]
		self.type=q[2]
		self.frame=tk.Frame(master)
		master.rowconfigure(i,weight=1)
		self.frame.grid(sticky='NSEW',row=i,column=0)
		self.lbl=tk.Label(self.frame,text=self.question,justify='left')
		self.answer_str=tk.StringVar()
		self.answer=None
		if len(q)>3:
			self.permitted=q[3]
		else:
			self.permitted='all'
		if self.type=='entry':
			vcmd = (master.register(self.onValidate),'%P')			
			self.answer=tk.Entry(self.frame,textvariable=self.answer_str, validate="key", validatecommand=vcmd)
		elif self.type=='option':
			self.answer=ttk.Combobox(self.frame,textvariable=self.answer_str,values=self.alternatives)
		if not self.answer is None:
			self.answer.grid(sticky='W',row=0,column=1)
		self.lbl.grid(sticky='E',row=0,column=0)
		
	def onValidate(self,P):
		if self.permitted=='int':
			if P=='':
				return True
			try: 
				int(P)
				return True
			except ValueError:
				return False		
		else:
			return True

		
		
		
		
		