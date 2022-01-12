#!/usr/bin/env python3
import gi
gi.require_version('Atspi','2.0')
from gi.repository import Atspi
import time
import ipm.e2e as e2e

PATH = './ipm-p1.py'

def run_app(path):
	# GIVEN I started the application
	process, app = e2e.run(path, 'tarea3')
	## ok ?
	if app is None:
		process and process.kill()
		assert False, f"There is no aplication {path} in the desktop"
	return app, process

app, process= run_app(PATH)
do, shows= e2e.perform_on(app)
time.sleep(1.5)
assert shows(role="label", text = "No se pudo acceder al servidor")

process and process.kill()

print("FIN DE LOS TESTS")
