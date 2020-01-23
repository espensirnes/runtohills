#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Bounce balls on the screen.
Spawn a new ball for each mouse-click.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.bouncing_balls
"""

import arcade
import random
import os
import time
imgpth=os.path.join( os.path.dirname(__file__),'images')

# --- Set up the constants

# Size of the screen
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Bouncing Balls Example"
BALL_SIZE=60
class jar:
	"""
	Class to keep track of a ball's location and vector.
	"""
	def __init__(self,x,y,window,scale,rows,columns,wait_seconds,opening_width=0.2,speed=5):
		self.win=window
		self.x0 = x
		self.x1 = 300*scale+x
		self.y0 = y
		self.y1 = 400*scale+y
		
		self.speed=speed
		self.rows=rows
		self.columns=columns
		self.scale=scale
		self.ball_size=30*scale
		self.makeballs(rows*columns)
		self.margin=10*scale
		self.wait_seconds=wait_seconds
		self.time=time.perf_counter()

		self.dy=(self.y1-self.y0)*0.1
		self.dx=0.5*(1-opening_width)*(self.x1-self.x0)
		self.slope=self.dy/self.dx
		self.hide()


		
	def draw(self):
		if not self.visible:
			return
		x0,x1,y1,y0,dy,dx=self.x0, self.x1, self.y1, self.y0,self.dy,self.dx
		b=self.ball_size*0.5
		
		arcade.draw_line(x0, y0, x0, y1, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x1, y0, x1, y1, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x0, y0, x1, y0, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x0, y1,x0+dx-b,y1+dy, arcade.color.WOOD_BROWN, 3)
		arcade.draw_line(x1, y1,x1-dx+b,y1+dy, arcade.color.WOOD_BROWN, 3)		
		if time.perf_counter()-self.time>self.wait_seconds and self.start_position:
			for ball in self.ball_list:
				ball.start()	
			self.start_position=False
		elif (not self.escaped_ball is None) and self.escaped_time-time.perf_counter()>1 and not self.is_done:
			self.done()
			
		
	def makeballs(self, n):
		self.ball_list = arcade.SpriteList()
		for i in range(n):
			self.ball_list.append(ball_sprite(self))

			
	def align_balls(self):
		x0,x1,y1,y0=self.x0, self.x1, self.y1, self.y0
		redball=random.randrange(0,self.rows*self.columns)
		a=1
		for i in range(self.rows):
			for j in range(self.columns):
				k=i*self.columns+j
				b=self.ball_size
				if redball==k:
					a=0
				self.ball_list[k].set(x0+b+(j)*2*b,y0+b+ (i)*2*b, redball==k)
		if a==1:
			a=0			
			
	def hide(self):
		self.moving=False
		self.visible=False
		self.start_position=False
		self.escaped_ball=None
		self.result=None
		self.is_done=False	
		self.is_active=False
		for i in self.ball_list:
			i.alpha=0
			
	def shake(self):	
		self.moving=True
		self.visible=True
		self.start_position=True
		self.is_active=True
		for i in self.ball_list:
			i.alpha=255
			i.scale=self.scale*0.5
			i.selected=False
		self.align_balls()
		self.time=time.perf_counter()
		
	def first_ball_escaped(self,ball):
		self.escaped_ball=ball
		self.start_position=False
		self.moving=False
		self.escaped_time=time.perf_counter()
		for i in self.ball_list:
			i.alpha=75
		ball.alpha=255
		ball.scale=self.scale
		self.result=ball.color_index
		
	def done(self):
		
		#call falling procedure
		self.is_active=False
		#put in falling procedure
		#self.hide()
		
		
			
		
class ball_sprite(arcade.Sprite):
	"""
	Advance button
	"""
	def __init__(self,jar):


		# Call the parent Sprite constructor
		super().__init__(os.path.join(imgpth,'blue_ball_small.png'),scale=jar.scale*0.5)
		txture=arcade.load_texture(os.path.join(imgpth,'red_ball_small.png'),scale=jar.scale*0.5)
		self.textures.append(txture)
		self.jar=jar
		self.change_x = 0
		self.change_y = 0
		self.size = 12*jar.scale
		self.center_x = 0
		self.center_y = 0
		# Speed and direction of rectangle
		self.change_x = 0
		self.change_y =0
		self.ball_color=0
		self.alpha=0
		self.selected=False
		
	def set(self,x,y,color_index):
		self.center_x=x
		self.center_y=y
		self.set_texture(color_index)
		self.color_index=color_index
		

	def start(self):
		maxspeed=self.jar.speed*self.jar.scale**0.5
		self.change_x = (2*random.uniform(0, 1)-1.0)*maxspeed
		self.change_y = (random.randint(0,1)*2-1)*(self.change_x**2+maxspeed**2)**0.5
		
	def update(self):
		""" Movement and game logic """
		if not self.jar.visible:
			return
		if not self.jar.escaped_ball is None:
			if self.selected:
				self.center_y += 1
			return		
		m=self.jar.margin
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

		
class MyGame(arcade.Window):
	""" Main application class. """

	def __init__(self):
		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
		arcade.set_background_color(arcade.color.WHITE)
		self.size=self.get_size()
		self.jar=jar(50,200,self,1,4,5,1,0.1,5)

		
		
		


						
	def on_draw(self):
		"""
		Render the screen.
		"""
		# This command has to happen before we start drawing
		arcade.start_render()
		self.jar.ball_list.draw()
		
		self.jar.draw()


	def on_mouse_press(self, x, y, button, modifiers):
		"""
		Called whenever the mouse button is clicked.
		"""
		if self.jar.visible:
			return
		self.jar.shake()
		
	def update(self, x):
		""" Move everything """
		self.jar.ball_list.update()


def main():
	MyGame()
	arcade.run()


if __name__ == "__main__":
	main()
	
	
