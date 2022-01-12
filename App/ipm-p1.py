#!/usr/bin/env python3
from typing import Awaitable

from controller import Controller

if __name__ == '__main__':
    try:
        controller = Controller()
        if controller!=None:
             controller.start()
    except Exception as e:
        print("Fatal error, si veis este mensaje y no sabéis por qué(la base de datos está encendida) mandadme un whatsapp\n")
