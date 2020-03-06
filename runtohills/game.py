#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run to the hills experiment
"""
#todo: correct time and trials=3
#      fix steps to mountain key
import random
import math
import os
#from win32api import GetSystemMetrics
import time
import numpy as np
import sys


try:
	import gui
	import info
	import sprites
except:
	from . import gui
	from . import info
	from . import sprites
import arcade
from arcade import pyglet



SCREEN_WIDTH = 1900#int(GetSystemMetrics(0))
SCREEN_HEIGHT = 900#int(GetSystemMetrics(1))
SCREEN_TITLE = "Run to the hills"
MAX_APPROACH_SCALE=50
STEPS_TO_SUMMIT=20
MIN_EYES=3
MAX_MOUNTAINS=4


#TODO!!!!!!!!!!!!!ACTUALLY ONLY ONE LIFE

imgpth=os.path.join( os.path.dirname(__file__),'images')


class MyGame(arcade.Window):
	""" Main application class. """

	def __init__(self,start_win,record):
		self.frame_count=0
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,resizable=True)#,fullscreen=True)
		#arcade.set_background_color(arcade.color.BLIZZARD_BLUE)

		self.size=self.get_size()
		self.define_mounatins()
		self.game_over=False
		self.grey_area=arcade.load_texture(os.path.join(imgpth,'white.png'))
		self.maximize()
		self.maximized=True
		self.size_restore=(SCREEN_WIDTH,SCREEN_HEIGHT)
		self.sunc_cost=record['sunc_cost']
		self.minuttes=record['minuttes']
		self.n_lives=record['n_lives']   
		self.nok_per_climb=record['NOK']  
		self.record['data']=[]
		self.frame_count = 0


		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)
		# Set up the player
		self.score = 0
		self.climber = None
		self.record=record

		self.danger_col=[(0, 255, 0,200),(255, 0, 0,200)]
		self.danger_txt=['LOW RISK (1/20)','HIGH RISK (1/10)']
		self.hand_cursor=pyglet.window.Window.get_system_mouse_cursor(self,'hand')
		self.min_eyes=MIN_EYES
		self.steps_to_summit=STEPS_TO_SUMMIT
		self.start_win=start_win
		self.start_win_closed=False
		self.timer=None
		self.keys_down=False
		self.dialogue=None
		self.held_keys=[]



	def define_mounatins(self):
		self.backgrounds=[]
		self.positions=info.mountain_pos
		for i in range(4):
			self.backgrounds.append(arcade.load_texture(os.path.join(imgpth,f'Mountain{i+1}_20.png')))
		self.set_mountain(-1)


	def set_mountain(self,previous):
		i=previous+1
		if i>=MAX_MOUNTAINS:
			i=0
		self.cur_mountain=i
		self.background=self.backgrounds[i]
		self.pos=self.positions[i]   
		w,h=self.size
		x,y=self.pos[0]
		y=y-0.02
		self.approac_pos=np.array([[0.9,0.2],[x,y]])


	def start_new_game(self):
		""" Set up the game and initialize the variables. """
		w,h=self.size
		self.frame_count = 0
		self.rendering=False
		self.game_over = False

		# Sprite lists
		self.all_sprites_list = arcade.SpriteList()

		self.ship_life_list = arcade.SpriteList()

		# Set up the player
		self.fields=[]
		self.score=0
		self.total_score=0
		self.game_number=0      
		self.add_sprites()
		self.reset_game('initial')      




	def add_sprites(self):

		self.walker = sprites.walker(self)
		self.all_sprites_list.append(self.walker)    
		self.climber = sprites.climber(self)
		self.all_sprites_list.append(self.climber)          
		self.faller = sprites.faller(self)
		self.all_sprites_list.append(self.faller)     
		self.home=sprites.home(self)
		self.all_sprites_list.append(self.home)    
		self.winner=sprites.winner(self)
		self.all_sprites_list.append(self.winner)  
		self.OK_button=sprites.OK_button(self)

		self.make_lives()
		self.jar=sprites.jar(self,20,0.5,0.2)  



	def make_lives(self):
		# Set up the little icons that represent the player lives.
		self.lives=[]
		for i in range(self.n_lives):
			life = arcade.Sprite(os.path.join(imgpth,'climbing_avatar.png'),0.05)
			self.lives.append(life)  
			self.all_sprites_list.append(life)
		self.draw_lives()

	def draw_lives(self):
		w,h=self.size
		start_pos=0.04*w
		cur_pos = start_pos
		scale=w*2.5e-5    
		for i in  range(len(self.lives)):  
			life=self.lives[i]
			life.scale=scale
			life.center_x = cur_pos + life.width
			life.center_y = h*0.05
			cur_pos += life.width



	def on_draw(self):
		"""
		Render the screen.
		"""


		# This command has to happen before we start drawing
		self.rendering=True
		arcade.start_render()
		self.size=self.get_size()
		w,h=self.size

		arcade.draw_texture_rectangle(w // 2, h // 2,
		                              w, h, self.background)          
		# Draw all the sprites.
		self.all_sprites_list.draw()
		self.jar.ball_list.draw()
		self.jar.draw()
		self.draw_lives()
		self.draw_walker()
		self.draw_climber()
		self.home.draw(self.dist_to_walk==0)

		# Put the text on the screen.

		a=[0.95,0.92,0.88,0.84,0.78,0.69,0.61]

		info_left_margin=int(w*0.01)

		f_width=w*0.28
		f_height=h*0.4

		arcade.draw_rectangle_filled(f_width/2, h-f_height/2,f_width, f_height, (255,255,255,150))  

		arcade.draw_text("Rehearsal lives:" ,info_left_margin, int(h*0.1), arcade.color.BLACK, w*0.01)

		arcade.draw_text("Score this round:" ,info_left_margin, int(h*a[0]), arcade.color.BLACK, w*0.015)
		arcade.draw_text(f"{self.score:.2f}".rjust(5),int(info_left_margin+0.18*w), int(h*a[0]), arcade.color.BLACK, w*0.015)
		arcade.draw_text("NOK",int(info_left_margin+w*0.23), int(h*a[0]), arcade.color.BLACK, w*0.015)

		arcade.draw_text("Total score:" ,info_left_margin, int(h*a[1]), arcade.color.BLACK, w*0.015)
		arcade.draw_text(f"{self.total_score:.2f}".rjust(5),int(info_left_margin+w*0.18), int(h*a[1]), arcade.color.BLACK, w*0.015)
		arcade.draw_text("NOK",int(info_left_margin+w*0.23), int(h*a[1]), arcade.color.BLACK, w*0.015)        

		arcade.draw_text("Distance to summit:", info_left_margin, int(h*a[2]), arcade.color.BLACK, w*0.015)      
		arcade.draw_text(str(self.stilltogo).rjust(3),int(info_left_margin+w*0.18), int(h*a[2]), arcade.color.BLACK, w*0.015)

		arcade.draw_text("Distance to mountain:",info_left_margin, int(h*a[3]), arcade.color.BLACK, w*0.015)
		arcade.draw_text(str(self.dist_to_walk).rjust(3),int(info_left_margin+w*0.18), int(h*a[3]), arcade.color.BLACK, w*0.015)
		if self.jar.is_active:
			arcade.draw_text("DO NOT PRESS KEYS!",int(info_left_margin), int(h*a[4]), arcade.color.BLACK, w*0.015)   
		
		if self.dist_to_walk==0:
			arcade.draw_rectangle_filled(f_width/2, h*(1-0.23-0.10/2), f_width, h*0.10, self.danger_col[self.high_risk])
			arcade.draw_text(self.danger_txt[self.high_risk],info_left_margin, int(h*a[5]), arcade.color.WHITE, w*0.027,bold=True)
		elif self.timer is None:
			arcade.draw_text('Press Shift+C+U in 2 seconds',info_left_margin, int(h*a[5]), arcade.color.BLACK, w*0.015,bold=False)
			arcade.draw_text('to move forward. Release all ',info_left_margin, int(h*a[5]-h*0.03), arcade.color.BLACK, w*0.015,bold=False)
			arcade.draw_text('before next step',info_left_margin, int(h*a[5]-h*0.06), arcade.color.BLACK, w*0.015,bold=False)
		self.draw_clock(a, w, h,info_left_margin)
		self.draw_dialogue(w,h,0.3)
		#arcade.draw_text(f"{time.perf_counter()-self.key_time}",int(w*0.25), h*0.2, arcade.color.BLACK, w*0.15)  
		self.check_keys_down()


	def draw_clock(self,a,w,h,info_left_margin):
		if self.timer is None:
			return
		t=time.perf_counter()-self.timer
		t=self.minuttes*60-t
		if t<0:
			self.add_to_records('game over')
			self.record['total_score']=self.total_score
			self.dialogue=("GAME OVER", f"""You earned NOK {self.total_score}""")
			self.game_over=True
			return
		minutes=int(t/60)
		seconds=int(t-minutes*60)
		arcade.draw_text(f"{minutes:02}:{seconds:02}",w*0.15, int(h*a[6]), arcade.color.BLACK, w*0.027,bold=True)

	def add_to_records(self,cause):

		
		self.add_to_record('session_score',self.score,cause)
		self.add_to_record('total_score',cause)
		self.add_to_record('dist_to_walk',cause)
		self.add_to_record('dist_walked',cause)
		self.add_to_record('high_risk',cause)
		self.add_to_record('climbed',cause)
		self.add_to_record('stilltogo',cause)

		
		if not self.timer is None:
			self.add_to_record('time_left',time.perf_counter()-self.timer,cause)


	def add_to_record(self,key,value='No value passed',cause):
		if value=='No value passed':
			value=self.__dict__[key]
		is_trial=False
		if self.game_number<=self.n_lives:
			is_trial=True
		self.record['data'].append([is_trial,self.game_number,key,value,cause])
				
	def draw_dialogue(self,w,h,size):
		if self.dialogue is None:
			return

		f_width=w*size
		f_height=f_width*0.3
		cx=w*0.5
		cy=h*0.5
		xm=f_width*0.02
		ym=f_height*0.02
		font_size=int(f_width*0.026)
		line=font_size*1.5

		arcade.draw_rectangle_filled(cx,cy,f_width, f_height, (255,255,255,200))
		arcade.draw_rectangle_outline(cx,cy,f_width, f_height,
		                              arcade.color.GRAY)	        
		arcade.draw_text(self.dialogue[0],cx+xm-f_width/2, cy-ym+f_height/2-line, arcade.color.BLACK, font_size,bold=True)
		arcade.draw_text(self.dialogue[1],cx+xm-f_width/2, cy-ym+f_height/2-4*line, arcade.color.BLACK, font_size)
		self.OK_button.draw(cx, cy-f_height*0.4, f_height*0.18, f_height*0.4)
		#arcade.draw_text("%s, %s" %tuple(self.pressedplace),int(w*0.25), h*0.2, arcade.color.WHITE, w*0.015) 



	def check_keys_down(self):
		sh,u,c=arcade.key.LSHIFT,arcade.key.U,arcade.key.C
		if not (self.held_keys==[sh and u,sh and c]  or self.held_keys==[sh and c,sh and u]):
			return
		if time.perf_counter()-self.key_time>2:
			self.advance()   
			self.held_keys=None


	def on_key_press(self, symbol, modifiers):
		""" Called whenever a key is pressed. """
		# Shoot if the player hit the space bar and we aren't respawning.
		if symbol == arcade.key.F or symbol==arcade.key.ESCAPE:
			self.maximized=not self.maximized
			if self.maximized:
				w,h=self.size_restore  
				self.set_size(w,h)
			else:
				w,h=self.get_size()
				self.size_restore=(w,h)     
				self.maximize()       
			#self.set_viewport(0, w, 0, h)        
		if not self.dialogue is None:
			return
		if self.jar.is_active:
			return
		sh,u,c=arcade.key.LSHIFT,arcade.key.U,arcade.key.C
		if symbol==(sh and u) or symbol==(sh and c):
			if len(self.held_keys)<2:
				self.held_keys.append(symbol)
				#print(symbol)
				#print(self.held_keys)
			if self.held_keys==[sh and u,sh and c]  or self.held_keys==[sh and c,sh and u]:
				self.key_time=time.perf_counter()

		if symbol == arcade.key.D:
			self.collect_reward()

	def on_key_release(self, symbol, modifiers):
		self.held_keys=[]
		
	def on_close(self,event=None):
		pass

	def on_mouse_press(self, x, y, button, modifiers):
		if not self.dialogue is None:
			if self.over_sprite(self.OK_button, x, y):
				if self.game_over==True:
					arcade.close_window()
				self.timer=time.perf_counter()
				self.dialogue=None
			return
		if False: #for obtaining cooridnates
			w,h=self.size
			#self.pos.append([x/w,y/h])
			self.pressedplace=[x,y]
			return
		if self.jar.is_active:
			return
		if self.over_sprite(self.home, x, y):
			self.collect_reward()
			return


	def collect_reward(self):
		if self.dist_to_walk>0:
			return
		if not self.jar.result==1:
			self.total_score+=self.score
		self.reset_game('reward collected')        

	def on_mouse_motion(self,x, y, dx, dy):
		if self.dist_to_walk==0:
			if (self.over_sprite(self.OK_button, x, y) and (not self.dialogue is None)) or self.over_sprite(self.home, x, y):
				self.set_mouse_cursor(self.hand_cursor)
			else:
				self.set_mouse_cursor(None)  
			return
		else:
			self.set_mouse_cursor(None)  


	def reset_game(self,cause):
		if not cause=='initial':
			self.add_to_records(cause)
		w, h = self.size
		self.high_risk=random.uniform(0, 1)>0.5
		self.sunc_cost_level=int(random.uniform(0, 1)*3)
		self.dist_to_mountain=self.sunc_cost[self.sunc_cost_level]
		self.approach_scale_power=np.log(MAX_APPROACH_SCALE)/np.log(self.dist_to_mountain+2)
		self.stilltogo=STEPS_TO_SUMMIT
		self.score=0
		self.climbed=0     
		self.dist_to_walk=self.dist_to_mountain
		self.jar.is_active=False
		self.dist_walked=0 
		self.set_mountain(self.cur_mountain)
		if not cause=='initial':
			if self.game_number<self.n_lives:
				self.lives[self.game_number].alpha=100
			self.game_number+=1
			if self.game_number==self.n_lives:
				self.dialogue=("REHERSAL ROUNDS ARE OVER",  
				               """Your rehersal rounds are now over, and your score is reset to zero. 
What you earn from now on, will be paid out to you in cash. After you 
have pressed 'OK', you have 20 minutes to complete the game. You can 
climb as many mountains as your time allows you to.""")
				self.total_score=0
			self.add_to_record('time_to_mountain',time.perf_counter()-self.apporach_time,cause)
		self.apporach_time=time.perf_counter()
		self.climber.alpha=0
		self.walker.alpha=0
		self.walker.becoming_visible=True

		self.faller.alpha=0
		self.climber.alpha=0
		self.jar.hide()
		

	def advance(self):
		if self.jar.is_active or self.winner.blinking:
			return
		if self.dist_to_walk>0:
			self.dist_to_walk-=1
			self.dist_walked+=1
			return
		self.walker.alpha=0
		if self.high_risk:
			self.jar.shake(2,5)
		else:
			self.jar.shake(4,5)
		self.climbed+=1
		self.stilltogo-=1 
		if self.climbed>len(self.pos):
			self.climbed=len(self.pos)
			self.stilltogo=0
			self.score=self.nok_per_climb*self.climbed




	def draw_climber(self):
		if self.climbed==0 or self.climbed==len(self.pos):
			return

		w, h = self.size

		x,y=self.pos[self.climbed-1]
		self.climber.center_x = w*x
		self.climber.center_y = h*(y+0.01)        
		self.climber.alpha=sprites.MAX_ALPHA


	def draw_walker(self):
		w, h = self.size
		a=self.approach_scale_power
		r=0.00075/float(self.dist_walked+1)**a
		q=float(self.dist_walked)/self.dist_to_mountain
		x,y=q*self.approac_pos[1]+(1-q)*self.approac_pos[0]
		self.walker.scale=r*h
		self.walker.center_x = w*x
		self.walker.center_y = h*y 
		a=0

	def update(self, x):
		""" Move everything """

		self.frame_count += 1

		if not self.game_over:
			self.all_sprites_list.update()
			self.jar.ball_list.update()

	def over_sprite(self,s,x,y):
		hgt=s.height*0.5
		wdt=s.width*0.5

		ctr_x=s.center_x
		ctr_y=s.center_y

		return (x>ctr_x-wdt and x<ctr_x+wdt 
		        and y>ctr_y-hgt and y<ctr_y+wdt)


	def on_resize(self, width, height):
		""" This method is automatically called when the window is resized. """

		# Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
		# edges being -1 to 1.
		super().on_resize(width, height)


