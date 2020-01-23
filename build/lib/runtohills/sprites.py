#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import arcade
import random
import numpy as np
import time

imgpth=os.path.join( os.path.dirname(__file__),'images')


EXPLOSION_TIME=2
EXPLOSION_TIME_DELAY=2
FALL_SPEED=0.003
COLOR_SPEED=5
MAX_ALPHA=255
BLINK_TIME=0.25
MAX_BLINKS=12
BOUNCE_DRAG=7




class OK_button:
	"""
	OK button.
	"""
	def __init__(self,window):

		self.window=window

		
	def draw(self,center_x,center_y,height,width,text='OK'):

		arcade.draw_rectangle_filled(center_x, center_y,width, height,
										  arcade.color.WHITE)	
		arcade.draw_rectangle_outline(center_x, center_y,width, height,
									  arcade.color.DARK_GRAY)		
		arcade.draw_text(text,center_x, center_y, arcade.color.BLACK, height*0.5,bold=True,anchor_x='center',anchor_y='center')
		
		self.center_x = center_x
		self.center_y = center_y
		self.height=height
		self.width=width
		
class home(arcade.Sprite):
	"""
	Home button.
	"""
	def __init__(self,window):

		w,h=window.size
		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,'HOME.png'),scale=0.00015*h)
		

		self.window=window

		
	def draw(self):
		w, h = self.window.size
		self.center_x = w*0.12
		self.center_y = h*0.35	
		
		
class advance(arcade.Sprite):
	"""
	Advance button
	"""
	def __init__(self,window):


		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,'advance.png'))
		

		self.window=window
		
	def draw(self):
		w, h = self.window.size
		self.scale=w/2000
		self.center_x = w*0.5
		self.center_y = h*0.02

class faller(arcade.Sprite):
	"""
	Sprite that represents the walker falling.
	"""
	def __init__(self,window):
		""" Set up the space ship. """

		# Call the parent Sprite constructor
		w,h=window.size
		super().__init__(os.path.join(imgpth,'avalanche_avatar.png'),scale=0.0001*h)
		self.alpha=0
		self.window=window
		self.isfalling=False
		self.floor=0
		

	def update(self):
		if (not self.isfalling):
			return
		w, h = self.window.size
		self.center_y-=h*FALL_SPEED
		if self.center_y<=self.floor:
			self.window.reset_game()
			self.isfalling=False
		super().update()    

	def fall(self):
		self.center_x=self.window.climber.center_x
		self.center_y=self.window.climber.center_y
		self.window.climber.alpha=0
		self.alpha=MAX_ALPHA
		self.isfalling=True
		
class walker(arcade.Sprite):
	"""
	Sprite that represents the walker.
	"""
	def __init__(self,window):

		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,"Approach_avatar.png"))
		w, h = window.size
		self.window=window
		self.alpha=0
		self.becoming_visible=True
		self.start_win=window.start_win
		

	def update(self):
		if not self.becoming_visible:
			return
		self.alpha=min((self.alpha+COLOR_SPEED,MAX_ALPHA))
		if self.alpha==MAX_ALPHA:
			self.becoming_visible=False
			if self.window.start_win_closed==False:
				self.start_win.close()
				self.window.start_win_closed=True		
		if self.window.start_win_closed==False:
			cp=self.start_win.progressbar['value']
			self.start_win.update(max((75+60*self.alpha/MAX_ALPHA,cp)))

		super().update()    



class climber(arcade.Sprite):
	"""
	Sprite that represents the climber.
	"""
	def __init__(self,window):
		# Call the parent Sprite constructor
		w, h = window.size
		super().__init__(os.path.join(imgpth,"climbing_avatar.png"),scale=0.00005*h)
		
		self.window=window
		self.alpha=0
		self.becoming_visible=True

class winner(arcade.Sprite):
	"""
	Sprite that represents the climber.
	"""
	def __init__(self,window):
		w, h = window.size
		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,"Summit_avatar.png"),scale=0.00004*h)
		
		self.window=window
		self.alpha=0
		self.blinking=False
		self.blink_count=0
		
	def update(self):
		if (not self.blinking):
			return
		w, h = self.window.size
		t=time.perf_counter()
		if t-self.blink_time>BLINK_TIME:
			self.alpha=MAX_ALPHA*(self.alpha==0)
			self.blink_count+=1
			self.blink_time=t
			if self.blink_count>MAX_BLINKS:
				self.blink_count=0
				self.alpha=0
				self.blinking=False
				self.window.reset_game()
		super().update()  
		
	def blink(self):
		w, h = self.window.size
		self.blinking=True
		self.alpha=MAX_ALPHA
		self.blink_time=time.perf_counter()
		x,y=self.window.pos[-1]
		self.center_x=x*w
		self.center_y=y*1.01*h

class exploder(arcade.Sprite):
	"""

	"""
	def __init__(self,window):
		""" Set up the space ship. """

		# Call the parent Sprite constructor
		self.window=window
		w, h = window.size
		scale=0.00015*h
		super().__init__(os.path.join(imgpth,"explosion_blue.png"),scale)
		self.alpha=0
		self.change=h*0.05
		self.isexploding=False

	def explode(self,pos_abs):
		self.isexploding=True
		self.time_end=time.perf_counter()
		self.time_flash=time.perf_counter()
		self.time_delay=time.perf_counter()
		x,y =pos_abs
		self.pos_orig_abs=x,y
		self.center_x=x
		self.center_y=y

	def update(self):
		if (not self.isexploding) or (time.perf_counter()-self.time_delay<EXPLOSION_TIME_DELAY):
			return
		if time.perf_counter()-self.time_end>EXPLOSION_TIME+EXPLOSION_TIME_DELAY:
			self.alpha=0
			self.isexploding=False
			self.window.faller.fall()
			return
		w,h=self.window.size
		x,y=self.pos_orig_abs
		if abs(y- self.center_y)>h*0.01:
			self.change=-self.change
		if time.perf_counter()-self.time_flash>0.1:
			self.alpha=0
			self.time_flash=time.perf_counter()
		else:
			self.alpha=MAX_ALPHA
		self.center_y+=self.change
		super().update()

		
		
class jar:
	"""
	Class to keep track of a ball's location and vector.
	"""
	def __init__(self,window,n_balls,scale,opening_width=0.2,speed=5):
		self.win=window
		self.fast_mode=False#For debugging
		self.opening_width=opening_width
		self.exploder = exploder(window)
		window.all_sprites_list.append(self.exploder)		
		
		self.speed=speed
		self.scale=scale
		self.makeballs(n_balls)
		self.wait_seconds=1
		self.time=time.perf_counter()
		self.moving=False
		self.visible=True
		self.escaped_ball=None
		self.result=None
		self.is_done=True	
		self.is_active=False		
		self.draw()


		
	def draw(self):
		w,h=self.win.size
		self.x0 = w*0.7
		self.x1 = 300*self.scale+w*0.7
		self.y0 = h*0.05
		self.y1 = 400*self.scale+h*0.05
		self.ball_size=30*self.scale
		self.margin=10*self.scale
		self.dx=0.5*(1-self.opening_width)*(self.x1-self.x0)
		self.dy=(self.y1-self.y0)*0.1
		self.slope=self.dy/self.dx		
		if not self.visible:
			return

		
		x0,x1,y1,y0,dy,dx=self.x0, self.x1, self.y1, self.y0,self.dy,self.dx
		b=self.ball_size*0.5
		
		arcade.draw_line(x0, y0, x0, y1, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x1, y0, x1, y1, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x0, y0, x1, y0, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x0, y1,x0+dx-b,y1+dy, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x1, y1,x1-dx+b,y1+dy, arcade.color.WOOD_BROWN, 3)	
		#arcade.draw_text(f"{time.perf_counter()-self.time},{self.moving}",250,600,'black')
		if time.perf_counter()-self.time>self.wait_seconds and not self.moving and not self.is_done:
			self.moving=True
		elif (not self.escaped_ball is None) and time.perf_counter()-self.escaped_time>0-self.fast_mode*2 and not self.is_done:
			self.done()
			
		
	def makeballs(self, n):
		self.ball_list = arcade.SpriteList()
		for i in range(n):
			self.ball_list.append(ball_sprite(self,i))

			
	def align_balls(self,rows,columns):
		x0,x1,y1,y0=self.x0, self.x1, self.y1, self.y0
		redball=random.randrange(0,rows*columns)
		a=1
		for i in range(rows):
			for j in range(columns):
				k=i*columns+j
				b=self.ball_size
				if redball==k:
					a=0
				if self.fast_mode:
					self.ball_list[k].set(x0+b+(j)*2*b,y0+b+ (i)*2*b, False)
				else:
					self.ball_list[k].set(x0+b+(j)*2*b,y0+b+ (i)*2*b, redball==k)
		if a==1:
			a=0			
			
	def hide(self):
		self.visible=False
		self.escaped_ball=None
		self.result=None
		self.is_done=True	
		self.is_active=False
		for i in self.ball_list:
			i.alpha=0
			
	def shake(self,rows,columns):	
		self.moving=False
		self.visible=True
		self.is_active=True
		self.escaped_ball=None
		self.is_done=False	
		for i in range(rows*columns):
			b=self.ball_list[i]
			b.alpha=255
			b.scale=self.scale*0.5
			b.selected=False
			b.start()
		for i in range(rows*columns,len(self.ball_list)):
			b=self.ball_list[i]
			b.stop()
		self.align_balls(rows,columns)
		self.time=time.perf_counter()
		
	def first_ball_escaped(self,ball):
		self.escaped_ball=ball
		self.moving=False
		self.escaped_time=time.perf_counter()
		for i in self.ball_list:
			i.alpha=75
		ball.alpha=255
		ball.scale=self.scale
		self.result=ball.color_index
		
	def done(self):
		
		#call falling procedure
		self.is_done=True	#is_done ensures that this procedure is called only once
		if self.result==1:
			self.win.score=0
			self.win.climbed=0   			
			self.exploder.explode(self.win.climber.position)
		else:
			self.is_active=False
			self.win.score+=self.win.nok_per_climb
			if self.win.climbed==self.win.steps_to_summit:
				self.win.climber.alpha=0
				self.win.winner.blink()	
				self.win.total_score+=self.win.score
				self.win.score=0

		
		
			
		
class ball_sprite(arcade.Sprite):
	"""
	Advance button
	"""
	def __init__(self,jar,i):


		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,'blue_ball_small.png'),scale=jar.scale*0.5)
		txture=arcade.load_texture(os.path.join(imgpth,'red_ball_small.png'),scale=jar.scale*0.5)
		self.textures.append(txture)
		self.jar=jar
		self.change_x = 0
		self.change_y = 0
		self.i=i
		self.size = 12*jar.scale
		self.center_x = 0
		self.center_y = 0
		# Speed and direction of rectangle
		self.change_x = 0
		self.change_y =0
		self.ball_color=0
		self.alpha=0
		self.selected=False
		self.enabled=False
		
	def set(self,x,y,color_index):
		self.center_x=x
		self.center_y=y
		self.set_texture(color_index)
		self.color_index=color_index

	def start(self):
		maxspeed=self.jar.speed*self.jar.scale**0.5
		self.change_x = (2*random.uniform(0, 1)-1.0)*maxspeed
		self.change_y = (random.randint(0,1)*2-1)*(self.change_x**2+maxspeed**2)**0.5
		self.enabled=True
		
	def stop(self):
		self.set(-100,0,0)
		self.change_x = 0
		self.change_y = 0	
		self.alpha=0
		self.enabled=False
		
	def update(self):
		""" Movement and game logic """
		if self.jar.fast_mode:
			self.color_index=1
			self.on_escape()
			return		
		if not self.jar.visible:
			return
		if not self.jar.escaped_ball is None:
			if self.selected:
				self.center_y += 1
			return		
		if not self.jar.moving or self.jar.is_done or self.enabled==False:
			return
		m=self.jar.margin
		if self.i>15:
			a=0
		self.center_x += self.change_x
		self.center_y += self.change_y
		x0,x1,y1,y0=self.jar.x0+m, self.jar.x1-m, self.jar.y1-m, self.jar.y0+m
		r=(simple_rand(time.perf_counter()*1e+9, 100)-0.5)*self.jar.scale
		ch=False
		if self.center_x < x0 + self.size:
			self.change_x = abs(self.change_x)
			ch=True

		if self.center_y < y0 + self.size:
			self.change_y = abs(self.change_y)
			ch=True

		if self.center_x > x1 - self.size:
			self.change_x = -abs(self.change_x)
			ch=True
		
		x_slope=min((self.center_x-x0,x1-self.center_x))*self.jar.slope

		if self.center_y > y1+x_slope - self.size:
			if self.center_y < y1+self.jar.dy and (self.center_x<x0+self.jar.dx or self.center_x>x1-self.jar.dx):
				self.change_y = -abs(self.change_y)
				ch=True
			else:#escaped ball
				self.on_escape()
		if ch==True:
			self.change_y+=r
			self.change_x+=r

				
		super().update()
	
	def on_escape(self):
		self.selected=True
		self.jar.first_ball_escaped(self)
		
def simple_rand(n,b):
	n=n/b
	return n-int(n)
