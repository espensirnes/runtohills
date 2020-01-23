#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from datetime import datetime
from multiprocessing import pool
#sys.path.append(__file__.replace("__init__.py",''))
imgpth=os.path.join( os.path.dirname(__file__),'images')
try:
	import gui
	import sql
except:
	from . import gui
	from . import sql

record=dict()
record['ExperimentStart']=datetime.now().strftime("%H:%M:%S")

gui.prequestions(record)
w=gui.window('Run to the hills')
w.win.update()
w.update(3)
try:
	import game
except:
	from . import game

w.update(20)
window = game.MyGame(w,record)
w.update(35)
window.start_new_game()
w.update(45)
game.arcade.run()
gui.postquestions(record)
sql.save_results(record)