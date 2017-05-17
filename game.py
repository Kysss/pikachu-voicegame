import cocos
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16
import struct
from pikachu import PIKACHU
from block import Block
from cocos.audio import pygame

class VoiceGame (cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__ (self):
        super(VoiceGame, self).__init__(255,255,255,255,800,600)
        
        #init voice
        self.NUM_SAMPLES = 1000
        self.LEVEL = 1500

        #init score
        self.score = 0
        self.text_score = cocos.text.Label(u'Score:0',
                                           font_name = None,
                                           font_size = 24,
                                           color = None)
        self.text_score.position = 500,440
        self.add(self.text_score, 99999)

        #setting up voicebar, pikachu and floor objects
        self.voicebar = Sprite('black.png', color = (0,0,255))
        self.voicebar.position = 20,450
        self.voicebar.scale_y = 0.1
        self.voicebar.image_anchor = 0,0
        self.add(self.voicebar)

        self.pikachu = PIKACHU()
        self.add(self.pikachu)

        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        pos = 0,100
        for i in range(100):
            b = Block(pos)
            self.floor.add(b)
            pos = b.x + b.width, b.height

        #voice input
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16,channels=1,rate=SAMPLING_RATE, input=True, frames_per_buffer = self.NUM_SAMPLES)
        self.schedule(self.update)


        
    def on_mouse_press(self,x,y,buttons,modifiers):
        pass


    
    def collide(self):
        px = self.pikachu.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.pikachu.width * 0.8 and px + self.pikachu.width * 0.2 <=b.x + b.width:
                if self.pikachu.y < b.height:
                    self.pikachu.land(b.height)
                    break


                
    def update(self,dt):
        #READ NUM_SAMPLES
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max (struct.unpack('1000h', string_audio_data))
        
        
        self.voicebar.scale_x = k/10000.0
        if k >2000:
            self.floor.x -= min((k/20.0),150)*dt
        if k >6000:
            self.pikachu.jump((k - 8000)/20)
            
        self.collide()

    def reset (self):
        self.floor.x = 0
        self.score = 0
        self.text_score.element.text = u'Score:0'


        #adding score method
    def add_score (self):
        self.score +=1
        self.text_score.element.text = u'Score:%d' %self.score

cocos.director.director.init(caption = "Let'S Go! Pikachu!")
cocos.director.director.run(cocos.scene.Scene(VoiceGame()))
        
