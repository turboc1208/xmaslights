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
    if self.get_state("input_boolean.xmas")=="on":
      self.xmashandle[self.run_every(self.change_colors,self.datetime(),60)]="timer"
    else:
      if not self.xmashandle=={}:
        self.shutdown(self.xmashandle)

  def change_colors(self, kwargs):
    if self.get_state("input_boolean.xmas")=="on":
      for e in self.xmaslights: 
        newcolor=self.colors[random.randint(0,len(self.colors)-1)]
        self.log("changing lights on entity = {} to {}".format(e,newcolor))
        self.turn_on(e,color_name=newcolor)
    else:
      self.shutdown(self.xmashandle)

  def shutdown(self, hdict):
    self.log("hdict={}".format(hdict))
    for h in hdict:
      if hdict[h]=="event":
        self.log("Shutting down event {}".format(h))
        self.cancel_event(h)
      elif hdict[h]=="timer":
        self.log("Shutting down timer {}".format(h))
        self.cancel_timer(h)
      else:
        self.log("unknown handle type {} for handle {}".format(hdict[h],h))
    hdict={}
    for e in self.xmaslights:
      self.turn_on(e,color_name="White")
