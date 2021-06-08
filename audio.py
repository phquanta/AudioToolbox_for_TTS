# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:14:02 2021

@author: Andrei
"""
from array import array
from sys import byteorder
import pyaudio
import wave
import _thread as thread
import os
from array import array
from struct import pack
import numpy as np
#import tinkter as tk
from array import array
from struct import pack
from sys import byteorder
import copy
import pyaudio
import wave
import tkinter as tk

class Audio:
      def __init__(self, CHUNK=1024, FORMAT= pyaudio.paInt16,CHANNELS=1, RATE=44100,WAVE_OUTPUT_FILENAME="output1.wav",THRESHOLD=500,SILENT_CHUNKS = 123 * 44100 / 1024, FRAME_MAX_VALUE=2 ** 15 - 1):
          
          self._NORMALIZE_MINUS_ONE_dB = 10 ** (-1.0 / 20)
          #self._TRIM_APPEND = RATE / 4
          self._TRIM_APPEND = RATE / 4
          self._SILENT_CHUNKS=SILENT_CHUNKS
          self._FRAME_MAX_VALUE=FRAME_MAX_VALUE
          self._RATE=RATE
          self._THRESHOLD=THRESHOLD
          self._FORMAT=FORMAT
          self._CHUNK=CHUNK
          self._CHANNELS=CHANNELS
          self._WAVE_OUTPUT_FILENAME = WAVE_OUTPUT_FILENAME
          self._isRecording=False
          self.p = pyaudio.PyAudio()
          self._audiostarted=False
          self.isSaved=False
          self.isPlaying=False
          self.stream_in = self.p.open(format=self._FORMAT,
                channels=self._CHANNELS,
                rate=self._RATE,
                input=True,
                frames_per_buffer=self._CHUNK)
          
          self.stream_out = self.p.open(format=self._FORMAT,
                channels=self._CHANNELS,
                rate=self._RATE,
                output=True,
                frames_per_buffer=self._CHUNK)
          
          
          
          self._frames=array('h')
          self._frames_to=None
          #self._frames_prev=[]
          #self._recording_thread=None
    
      def is_silent(self,data_chunk):
        # """Returns 'True' if below the 'silent' threshold"""
        return max(data_chunk) < self._THRESHOLD
     
      
      def normalize(self,data_all):
            """Amplify the volume out to max -1dB"""
            # MAXIMUM = 16384
            normalize_factor = (float(self._NORMALIZE_MINUS_ONE_dB * self._FRAME_MAX_VALUE)
                                / max(abs(i) for i in data_all))
        
            r = array('h')
            for i in data_all:
                r.append(int(i * normalize_factor))
            return r
    
      def trim(self,data_all):
            import copy
            #from copy import deepcopy
            _from = 0
            _to = len(data_all) - 1
            for i, b in enumerate(data_all):
                #print(i,b)
                if i>=len(data_all)-1:
                    _from=len(data_all) - 1
                if abs(b) > self._THRESHOLD:
                    #_from = max(0, i - self._TRIM_APPEND)
                    _from = i
                    break
        
            for i, b in enumerate(reversed(data_all)):
                if abs(b) > self._THRESHOLD:
                    _to = min(len(data_all) - 1, len(data_all) - 1 - i + self._TRIM_APPEND)
                    break
            print(f"Cut:   {_from,_to}")
     
            
            print("From :  ",_from)

            return copy.deepcopy(data_all[int(_from):int((_to + 1))])

          
       
      @property 
      def isRecording(self):
        return self._isRecording
            
      @isRecording.setter
      def isRecording(self, value):
        self._isRecording=value
        
        
             
      @property 
      def audio_started(self):
        return self._audiostarted
            
      @isRecording.setter
      def audio_started(self, value):
        self._audiostarted=value
          
      
        
      def record(self):
          self._frames=array('h')
          silent_chunks = 0
          while True:
             if not self.isRecording:
                 #self.audio_started = False     
                 print("Len of frames before:",len(self._frames))
                 self._frames_to = self.trim(self._frames)  
                 self._frames_to = self.normalize(self._frames_to)  
                 print("Len of frames after trim:",len(self._frames_to))
                 print("Stopping")
                 self.isSaved=True
                 #self._frames_to = self.normalize(self._frames)
                 
                 break
             else:
                  data = array('h', self.stream_in.read(self._CHUNK)) 
                  if byteorder == 'big':
                      data.byteswap()
                  
                  self._frames.extend(data)    
         
                        
                   
      def start_recording(self):
          try:
              self.isSaved=False 
              thread.start_new_thread(self.record,())
          except Exception as a:
              print("Error: unable to start thread")
              print(a)
          
                    
      
      def stop(self):
          self.isRecording=False

      def close(self):
          self.stream_in.stop_stream()
          self.stream_out.stop_stream()
          
          self.stream_in.close()
          self.stream_out.close()
          self.p.terminate()
          
   
          
      def write_to_file(self,dirname):
          
          
          
           if dirname is not None:
             fname=os.path.join(dirname,  self._WAVE_OUTPUT_FILENAME)
           else:
             fname=os.path.join("",  self._WAVE_OUTPUT_FILENAME)
          
    
           data = pack('<' + ('h' * len(self._frames_to)), *self._frames_to)
        
            
           print("fname::::::::",fname,len(self._frames_to))  
           wave_file = wave.open(fname, 'wb')
           wave_file.setnchannels(self._CHANNELS)
           wave_file.setsampwidth(self.p.get_sample_size(self._FORMAT))
           wave_file.setframerate(self._RATE)
           wave_file.writeframes(data)
           wave_file.close()
           self._frames=array('h')

             
      
      # def write_to_file(self,dirname):
          
          
          
      #     if dirname is not None:
      #       fname=os.path.join(dirname,  self._WAVE_OUTPUT_FILENAME)
      #     else:
      #       fname=os.path.join("",  self._WAVE_OUTPUT_FILENAME)
          
      #     print("fname::::::::",fname)  
      #     #fname="aaa.wav"
      #     wf = wave.open(fname, 'wb')
      #     wf.setnchannels(self._CHANNELS)
      #     wf.setsampwidth(self.p.get_sample_size(self._FORMAT))
      #     wf.setframerate(self._RATE)
      #     #wf.writeframes(b''.join(self._frames))
      #     wf.writeframes(self._frames)
      #     wf.close()

      def play_thread(self,layout,dirname):
          layout.layout["btn_Play"]["state"]=tk.DISABLED   
          self.isPlaying=True
          if dirname is not None:
            fname=os.path.join(dirname,  self._WAVE_OUTPUT_FILENAME)
          else:
            fname=os.path.join("",  self._WAVE_OUTPUT_FILENAME)
          if not os.path.isfile(fname):
                            tk.messagebox.showerror("Error", 'File Not Found')    
                            self.isPlaying=False
                            layout.layout["btn_Play"]["state"]=tk.NORMAL
                            return
          
                            
            
#          try:
          wf = wave.open(fname, 'rb')
  #        except FileNotFoundError:
#              self.isPlaying=False
#              layout.layout["btn_Play"]["state"]=tk.NORMAL
#              tk.messagebox.showerror("Error", 'File Not Found')    
              
          data = wf.readframes(self._CHUNK)
          while data:
              self.stream_out.write(data)
              data = wf.readframes(self._CHUNK)
          self.isPlaying=False
          layout.layout["btn_Play"]["state"]=tk.NORMAL
          
      def play_file(self,layout,dirname):
          try:
              thread.start_new_thread(self.play_thread,(layout,dirname,))
          except Exception as a:
              print("Error: unable to start thread in playing")
              #self.isPlaying=False
              print(a)
       
              
      def del_file(self,dirname):
          if os.path.isfile(os.path.join(dirname,  self._WAVE_OUTPUT_FILENAME)):
              os.remove(os.path.join(dirname,  self._WAVE_OUTPUT_FILENAME))
              return True
          else:    ## Show an error ##
              print(f'Error: {os.path.join(dirname,  self._WAVE_OUTPUT_FILENAME)} file not found')
              return False
          

          

          
          

