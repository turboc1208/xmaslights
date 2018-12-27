import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
import random
#import homeassistant.appapi as appapi
#
# XmasTree App
#
# Args:
#
        
class XmasLights(hass.Hass):

  def initialize(self):
     self.log("handling xmas lights.")
     self.xmaslights=["light.frontporch1","light.frontporch2"]
     self.colors=["Red","Green","Blue","Yellow"]
     self.xmashandle={}
     self.log("Registering scheduled callbacks")
     # Check current state
     self.listen_state(self.turn_on_lights,"switch.front_porch_light_switch",new="on", old="off", duration=60)

  def turn_on_lights(self, entity,attribute,old,new, kwargs):
    self.run_every(self.change_colors,self.datetime(),60)

  def change_colors(self, kwargs):
    for e in self.xmaslights: 
      newcolor=self.colors[random.randint(0,len(self.colors)-1)]
      self.log("changing lights on entity = {} to {}".format(e,newcolor))
      self.turn_on(e,color_name=newcolor)
