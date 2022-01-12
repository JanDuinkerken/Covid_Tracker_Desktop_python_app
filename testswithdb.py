#!/usr/bin/env python3
import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi

import ipm.e2e as e2e
import os
import sys
import requests
import datetime
import time
import random

PATH = './ipm-p1.py'
NUM = 25

def users(offset):
	try:
		r = requests.get("http://localhost:8080/api/rest/users?offset=" + str(offset) + "&limit=" + str(NUM),
		headers={"x-hasura-admin-secret":"myadminsecretkey"})
		r.raise_for_status()
	    # Code here will only run if the request is successful
	except requests.exceptions.HTTPError as errh:
		print(errh)
	except requests.exceptions.ConnectionError as errc:
		print(errc)
	except requests.exceptions.Timeout as errt:
		print(errt)
	except requests.exceptions.RequestException as err:
		print(err)

	return r.json()

def run_app(path):
	# GIVEN I started the application
	process, app = e2e.run(path, 'tarea3')
	## ok ?
	if app is None:
		process and process.kill()
		assert False, f"There is no aplication {path} in the desktop"
	return app, process

def block_print():
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    sys.stdout = sys.__stdout__

#------------------------------------------------------------------------------------------
#We use the same tests to check both page views, the database one and the  search user one.
screen="Search User"
LAST_PAGE=4
next='>'
prev='<'
for i in range(2):
	app, process = run_app(PATH)
	do, shows = e2e.perform_on(app)
	time.sleep(2)
	# WHEN I click the button 'Search User'
	do('click', role= 'push button', name= screen)
	time.sleep(2)

	block_print()
	e2e.dump_app('tarea3')
	enable_print()

	# WHEN I click the button '>'
	do('click', role= 'push button', name= next)
	time.sleep(2)
	# THEN I see the page number "2"
	assert shows(role= "label", text= "2")

	process and process.kill()

	#------------------------------------------------------------------------------------------
	#Test previous page button
	app, process = run_app(PATH)
	do, shows = e2e.perform_on(app)
	# WHEN I click the button 'Search User'
	time.sleep(2)
	do('click', role= 'push button', name= screen)
	time.sleep(2)

	block_print()
	e2e.dump_app('tarea3')
	enable_print()
	# WHEN I click the button '>'
	do('click', role= 'push button', name= next)
	time.sleep(2)
	# WHEN I click the button '<'
	do('click', role= 'push button', name= prev)
	time.sleep(2)
	# THEN I see the page number "1"
	assert shows(role= "label", text= "1")

	process and process.kill()

	#------------------------------------------------------------------------------------------
	#Test previous page button when page is already one
	app, process = run_app(PATH)
	do, shows = e2e.perform_on(app)
	# WHEN I click the button 'Search User'
	time.sleep(2)
	do('click', role= 'push button', name= screen)
	time.sleep(2)

	block_print()
	e2e.dump_app('tarea3')
	enable_print()
	# WHEN I click the button '<'
	do('click', role= 'push button', name= prev)
	time.sleep(2)
	# THEN I see the page number "1"
	assert shows(role= "label", text= "1")

	process and process.kill()

	#changing screen to database
	screen="Database"
	LAST_PAGE=120
	next='>>'
	prev='<<'

	#-------------------------------------------------------------------------------------------
screen="Search User"
LAST_PAGE=4
next='>'
prev='<'
#Test last page (only in Search user for time reasons)
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= screen)
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()
# WHEN I click the button '>'
for i in range(LAST_PAGE):
	do('click', role= 'push button', name= next)
	time.sleep(2)

# THEN I see the page number "4"
assert shows(role= "label", text= str(LAST_PAGE))

process and process.kill()

#-------------------------------------------------------------------------------------------
#Test that page number stops when the last page is reached
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= screen)
time.sleep(2)

# WHEN I click the button '>'
for i in range(LAST_PAGE + 1):
	do('click', role= 'push button', name= next)
	time.sleep(2)

# THEN I see the page number "4"
assert shows(role= "label", text= str(LAST_PAGE))

process and process.kill()

#-------------------------------------------------------------------------------------------
#Test that page number stops when the last page is reached
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()
# WHEN I click the button 'Go Back'
do('click', role= 'push button', name= 'Go Back')
time.sleep(2)

# THEN I see the button 'Search User'
assert shows(role= "push button", name= "Search User")

process and process.kill()

#-------------------------------------------------------------------------------------------
#Test that checks if the back button works
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button Database
time.sleep(2)
do('click', role= 'push button', name= 'Database')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()
# WHEN I click the button 'Go Back'
do('click', role= 'push button', name= 'Go Back')
time.sleep(2)

# THEN I see the button 'Search User'
assert shows(role= "push button", name= "Database")

process and process.kill()
#-------------------------------------------------------------------------------------------
#Test that finding persons work
#To test it, we have checked manually the database to finnd a combination:
#Introducing Pilar Campos, 2021-09-08,2021-09-10 should respond with 3 persons:
#Juana Gutierrez, Domingo Ferrer, Jorge Jimenez.
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)

time.sleep(2)
do('click', role= 'push button', name= 'Database')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

entry= e2e.find_obj(app,role='text',name='Nombre')
assert entry is not None
entry.set_text_contents("Pilar")

entry= e2e.find_obj(app,role='text',name='Apellido')
assert entry is not None
entry.set_text_contents("Campos")

entry = e2e.find_obj(app,role='text',name='Inicio')
assert entry is not None
entry.set_text_contents("2021-09-08")

entry= e2e.find_obj(app,role='text',name='Fin')
assert entry is not None
entry.set_text_contents("2021-09-10")

do('click', role= 'push button', name= 'Find')
time.sleep(2)

table= e2e.find_obj(app, role='table',name='Lista')
assert table.get_n_rows() == 3
assert "Juana"==table.get_accessible_at(0,0).get_text(0,-1)
assert "Domingo"==table.get_accessible_at(1,0).get_text(0,-1)
assert "Jorge"==table.get_accessible_at(2,0).get_text(0,-1)
assert "Gutierrez"==table.get_accessible_at(0,1).get_text(0,-1)
assert "Ferrer"==table.get_accessible_at(1,1).get_text(0,-1)
assert "Jimenez"==table.get_accessible_at(2,1).get_text(0,-1)

process and process.kill()

#-------------------------------------------------------------------------------------------
#Test that the list view is empty if none entries in the database coincide with the search
#To test it, we have checked manually the database to finnd a combination:
#Introducing Jose Ruiz, 2021-09-08	2021-09-10 will give us an empty list.
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)

time.sleep(2)
do('click', role= 'push button', name= 'Database')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

entry= e2e.find_obj(app,role='text',name='Nombre')
assert entry is not None
entry.set_text_contents("Jose")

entry= e2e.find_obj(app,role='text',name='Apellido')
assert entry is not None
entry.set_text_contents("Ruiz")

entry= e2e.find_obj(app,role='text',name='Inicio')
assert entry is not None
entry.set_text_contents("2021-09-08")

entry= e2e.find_obj(app,role='text',name='Fin')
assert entry is not None
entry.set_text_contents("2021-09-10")

do('click', role= 'push button', name= 'Find')
time.sleep(2)
table= e2e.find_obj(app, role='table',name='Lista')
assert table.get_n_rows() == 0

process and process.kill()


#-------------------------------------------------------------------------------------------
#Test that the find contacts checks whether if the name and surname is in the database or not.
#To do it, we introduce a wrong name
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)

time.sleep(2)
do('click', role= 'push button', name= 'Database')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

entry= e2e.find_obj(app,role='text',name='Nombre')
assert entry is not None
entry.set_text_contents("aaaaaa")

entry= e2e.find_obj(app,role='text',name='Apellido')
assert entry is not None
entry.set_text_contents("bbbbbb")

entry= e2e.find_obj(app,role='text',name='Inicio')
assert entry is not None
entry.set_text_contents("2021-09-08")

entry= e2e.find_obj(app,role='text',name='Fin')
assert entry is not None
entry.set_text_contents("2021-09-10")

do('click', role= 'push button', name= 'Find')
time.sleep(2)
assert shows(role= "label", text="User not found. Try again.")

process and process.kill()

#-------------------------------------------------------------------------------------------
#Test that checks if the find contacts only works with strings with the correct format.
#To do it, we introduce wrong format dates. If the dates are future, start after end or there is no contacts between them,
#there is no error, empty list is shown.
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)

time.sleep(2)
do('click', role= 'push button', name= 'Database')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

entry= e2e.find_obj(app,role='text',name='Nombre')
assert entry is not None
entry.set_text_contents("Pilar")

entry= e2e.find_obj(app,role='text',name='Apellido')
assert entry is not None
entry.set_text_contents("Campos")

entry= e2e.find_obj(app,role='text',name='Inicio')
assert entry is not None
entry.set_text_contents("patata")

entry= e2e.find_obj(app,role='text',name='Fin')
assert entry is not None
entry.set_text_contents("2021-09-10")

do('click', role= 'push button', name= 'Find')
time.sleep(2)
assert shows(role= "label", text="Wrong date format. Try again.")

process and process.kill()


#-------------------------------------------------------------------------------------------
#Test that if we introduce a future date or the end is before the start the list of contacts is empty.
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)

time.sleep(2)
do('click', role= 'push button', name= 'Database')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

entry= e2e.find_obj(app,role='text',name='Nombre')
assert entry is not None
entry.set_text_contents("Jose")

entry= e2e.find_obj(app,role='text',name='Apellido')
assert entry is not None
entry.set_text_contents("Ruiz")

entry= e2e.find_obj(app,role='text',name='Inicio')
assert entry is not None
entry.set_text_contents("2100-09-08")

entry= e2e.find_obj(app,role='text',name='Fin')
assert entry is not None
entry.set_text_contents("2021-09-10")

do('click', role= 'push button', name= 'Find')
time.sleep(2)
table= e2e.find_obj(app, role='table',name='Lista')
assert table.get_n_rows() == 0

process and process.kill()
#-------------------------------------------------------------------------------------------
#Test searching the first user by name
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Arturo Blanco")

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role= "label", text= str("Name: " + data["users"][0]["name"]))

process and process.kill()

#-------------------------------------------------------------------------------------------
#Test searching the third page first user by name
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(NUM * 2)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Concepcion Leon")

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role= "label", text= str("Name: " + data["users"][0]["name"]))

process and process.kill()

#-------------------------------------------------------------------------------------------
#Test clicking on the second user
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

data = users(0)

block_print()
e2e.dump_app('tarea3')
enable_print()

#When I click on user Xavier Suarez
do('edit', role= 'table cell', name= data["users"][1]["name"])
time.sleep(2)

# THEN I see the page number "4"
assert shows(role= "label", text= str("Name: " + data["users"][1]["name"]))

process and process.kill()

#--------------------------------------------------------------------------------------------
#Test clicking on the first user from the second page
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

# WHEN I click the button '>'
do('click', role= 'push button', name= '>')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(NUM)

#When I click on user Drancisco Rodriguez
do('edit', role= 'table cell', name= data["users"][2]["name"])
time.sleep(2)

# THEN I see the page number "4"
assert shows(role= "label", text= str("Name: " + data["users"][2]["name"]))

process and process.kill()

# --------------------------------------------------------------------------------------------
#Test that after clicking the next button on the last page the page shown is not changed
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

# WHEN I click the button '>'
for i in range(LAST_PAGE +1):
	do('click', role= 'push button', name= '>')
	time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(NUM*(LAST_PAGE-1))


#When I click on user Arturo Blanco
do('edit', role= 'table cell', name= data["users"][0]["name"])
time.sleep(2)

# THEN I see the page number "4"
assert shows(role= "label", text= str("Name: " + data["users"][0]["name"]))

process and process.kill()
#--------------------------------------------------------------------------------------------
#Test that after clicking the previous button on the first page the page shown is not changed
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

# WHEN I click the button '<'
do('click', role= 'push button', name= '<')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#When I click on user Arturo Blanco
do('edit', role= 'table cell', name= data["users"][1]["name"])
time.sleep(2)

# THEN I see the page number "4"
assert shows(role= "label", text= str("Name: " + data["users"][1]["name"]))

process and process.kill()

#--------------------------------------------------------------------------------------------
#Test that searching a user that does not exist gives an error
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Test subject")

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role = 'label', text = 'User not found')

process and process.kill()
#--------------------------------------------------------------------------------------------
#Test that searching only a name
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Test")

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role = 'label', text = 'You must enter a name and a surname')

process and process.kill()
#--------------------------------------------------------------------------------------------
#Test clicking the find button without having written any user
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role = 'label', text = 'You must enter a name and a surname')

process and process.kill()
#--------------------------------------------------------------------------------------------
#Testing for contacts on user page, we will perform the same querys than in the database search test
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Pilar Campos")

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role= "label", text= "Name: Pilar")

entry= e2e.find_obj(app,role='text',name='Inicio_us')
assert entry is not None
entry.set_text_contents("2021-09-08")

entry= e2e.find_obj(app,role='text',name='Fin_us')
assert entry is not None
entry.set_text_contents("2021-09-10")

do('click', role= 'push button', name= 'Find Contacts')
time.sleep(random.uniform(2.5, 3.5))
table= e2e.find_obj(app, role='table',name='Lista')
# time.sleep(random.uniform(2.5, 3.5))
time.sleep(3); assert table.get_n_rows() == 3
assert "Juana"==table.get_accessible_at(0,0).get_text(0,-1)
assert "Domingo"==table.get_accessible_at(1,0).get_text(0,-1)
assert "Jorge"==table.get_accessible_at(2,0).get_text(0,-1)
assert "Gutierrez"==table.get_accessible_at(0,1).get_text(0,-1)
assert "Ferrer"==table.get_accessible_at(1,1).get_text(0,-1)
assert "Jimenez"==table.get_accessible_at(2,1).get_text(0,-1)

process and process.kill()

#--------------------------------------------------------------------------------------------
#Testing for contacts on user page, we will perform the same querys than in the database search test
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Jose Ruiz")

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role= "label", text= "Name: Jose")

entry= e2e.find_obj(app,role='text',name='Inicio_us')
assert entry is not None
entry.set_text_contents("2021-09-08")

entry= e2e.find_obj(app,role='text',name='Fin_us')
assert entry is not None
entry.set_text_contents("2021-09-10")

do('click', role= 'push button', name= 'Find Contacts')
time.sleep(random.uniform(2.5, 3.5))
table= e2e.find_obj(app, role='table',name='Lista')
time.sleep(random.uniform(2.5, 3.5))
assert table.get_n_rows() == 0

process and process.kill()

#--------------------------------------------------------------------------------------------
#Testing for contacts on user page, we will perform the same querys than in the database search test
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Jose Ruiz")

do('click', role= 'push button', name= 'Find ->')
time.sleep(3)

assert shows(role= "label", text= "Name: Jose")

do('click', role= 'push button', name= 'Find Contacts')
# time.sleep(random.uniform(3, 3.5))

time.sleep(3); assert shows(role = 'label', text = 'Wrong date format. Try again.')
time.sleep(random.uniform(3, 3.5))

process and process.kill()

#--------------------------------------------------------------------------------------------
#Testing for contacts on user page, we will perform the same querys than in the database search test
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()

data = users(0)

#WHEN I introduce the info of the user I am searching
entry= e2e.find_obj(app,role='text',name= 'Search' )
assert entry is not None
entry.set_text_contents("Jose Ruiz")

do('click', role= 'push button', name= 'Find ->')
time.sleep(2)

assert shows(role= "label", text= "Name: Jose")

entry= e2e.find_obj(app,role='text',name='Inicio_us')
assert entry is not None
entry.set_text_contents("2021-09-08")

entry= e2e.find_obj(app,role='text',name='Fin_us')
assert entry is not None
entry.set_text_contents("2020-09-10")

time.sleep(2)

do('click', role= 'push button', name= 'Find Contacts')
time.sleep(random.uniform(4, 4.5))

block_print()
e2e.dump_app('tarea3')
enable_print()

table= e2e.find_obj(app, role='table',name='Lista')
time.sleep(random.uniform(3, 3.5))
assert table.get_n_rows() == 0

process and process.kill()

#--------------------------------------------------------------------------------------------
#Testing cancel button trying to go back to the first page
app, process = run_app(PATH)
do, shows = e2e.perform_on(app)
# WHEN I click the button 'Search User'
time.sleep(2)
do('click', role= 'push button', name= 'Search User')
time.sleep(2)

block_print()
e2e.dump_app('tarea3')
enable_print()
# WHEN I click the button 'Go Back'
do('click', role= 'push button', name= 'Home')
time.sleep(0.5)

block_print()
e2e.dump_app('tarea3')
enable_print()

# WHEN I click the button 'X'
do('click', role= 'push button', name= 'X')
time.sleep(2)

# THEN I see the same page
assert shows(role= "label", text= "1")
time.sleep(5)

process and process.kill()

print("FIN DE TEST NORMALES")
