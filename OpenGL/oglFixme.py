import ctypes, sys
from OpenGL.raw import GLUT as simple

if sys.platform != "win32":
	# Das wird gegeben
	# MENUFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
	# Das wird erwartet
	MENUFUNC = ctypes.CFUNCTYPE(None, ctypes.c_int)
	def fixed_glutCreateMenu(menu_func):
   		"""replacement for broken glutCreateMenu"""
   		menu = simple.glutCreateMenu(MENUFUNC(menu_func))
   		return menu

	# now replace existing version in OpenGL.GLUT
	import OpenGL.GLUT
	OpenGL.GLUT.glutCreateMenu = fixed_glutCreateMenu
