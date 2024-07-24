import pygame as pg
import json
from gameSettings import *

class Item():

    def __init__(self, game, objName: str, data: str):

        self.game = game
        self.itemEffects = []

        data = json.loads(data)
        setattr(self, 'objName', objName)

        # Establish the properties of objects
        for key, v in data.items():
            setattr(self, key, v)

            # Set item effects
            if key not in ['name', 'dropChance']:
                self.itemEffects.append(key)

        self.image = pg.image.load(path.join(ITEMS_FOLDER, self.objName + '.png')).convert_alpha()

    def prop(self, prop):
        ''' Get item attribute '''

        return getattr(self, prop)
    
    def useItem(self):
        ''' Use item '''

        if self.itemEffects == []:
            return False
        
        for effect in self.itemEffects:
            playerEffectValue = getattr(self.game.player, effect)
            itemEffectValue = self.prop(effect)

            if effect == 'mp':
                if playerEffectValue + itemEffectValue > PLAYER_MP:
                    itemEffectValue = 0
                    playerEffectValue = PLAYER_MP

            elif effect == 'hp':
                if playerEffectValue + itemEffectValue > PLAYER_HP:
                    itemEffectValue = 0
                    playerEffectValue = PLAYER_HP

            setattr(self.game.player, effect, playerEffectValue + itemEffectValue)

    def itemEffectActionTranscription(self):
        ''' Returns a text set of item properties '''

        actions = []
        for effect in self.itemEffects:
            itemEffectValue = str(self.prop(effect))

            if effect == 'hp':
                actions.append('Cures ' + itemEffectValue + ' health')
            if effect == 'mp':
                actions.append('Recovers ' + itemEffectValue + ' mana')
        
        return actions
    