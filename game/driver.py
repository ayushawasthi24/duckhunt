import os, sys, time
import pygame
from .registry import Registry
from .sounds import SoundHandler
from .states import adjpos, StartState

class Driver(object):
    def __init__(self, surface):
        # Set a global registry
        self.registry = Registry()
        self.registry.set('surface', surface)
        self.registry.set('soundHandler', SoundHandler())

        controls = pygame.image.load(os.path.join ('media', 'controls.png'))
        self.registry.set('controlImgs', pygame.transform.smoothscale (controls, adjpos (*controls.get_size ())))

        sprites = pygame.image.load(os.path.join ('media', 'sprites.png'))
        sprites = pygame.transform.scale (sprites, adjpos (*sprites.get_size ()))
        self.registry.set('sprites', sprites)
        
        rsprites = pygame.transform.flip(sprites, True, False)
        self.registry.set('rsprites', rsprites)

        self.registry.set('score', 0)
        self.registry.set('round', 1)

        # Start the game
        self.state = StartState(self.registry)
        self.state = self.state.start()

    def handleEvent(self, event):
        # Toggle sound
        if event.type == pygame.KEYDOWN and event.key is pygame.K_s:
            self.registry.get('soundHandler').toggleSound()

        self.state.execute(event)

    def update(self):
        newState = self.state.update()

        if newState:
            self.state = newState

    def render(self):
        self.state.render()
        self.registry.get('soundHandler').flush()
