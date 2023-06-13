import threading
import midi
from pynput import keyboard
from utils.log import Log
import time
import simpleaudio as sa
import mido
from enum import Enum
import os

log = Log(Log.LEVEL_INF, 'midi_tester')

keyboard_notes = 'zsxdcvgbhnjmq2w3er5t6y7ui9o0på'

# TODO: There is a bug where pynput causes the entire console output to be duplicated for each new log

# norwegian keyboard layout
# TODO: ideally recieve raw keyboard scan codes instead of characters (will need to use another package than pynput), to make the keyboard layout independent of country layouts. Problems with gaining keyboard access on macOS.
keyboard_layout_no = {
    'base': 60,
    'keys': {
        'z': 0,
        's': 1,
        'x': 2,
        'd': 3,
        'c': 4,
        'v': 5,
        'g': 6,
        'b': 7,
        'h': 8,
        'n': 9,
        'j': 10,
        'm': 11,
        'q': 12,
        ',': 12,
        '2': 13,
        'l': 13,
        'w': 14,
        '.': 14,
        '3': 15,
        'ø': 15,
        'e': 16,
        '-': 16,
        'r': 17,
        '5': 18,
        't': 19,
        '6': 20,
        'y': 21,
        '7': 22,
        'u': 23,
        'i': 24,
        '9': 25,
        'o': 26,
        '0': 27,
        'p': 28,
        'å': 29,
    }
}

class TesterOutput(Enum):
    MIDI = 0
    AUDIO = 1

class Tester:
    
    def __init__(self, module: midi.Module, bpm=120, out=TesterOutput.AUDIO, keyboard_layout=keyboard_layout_no):
        
        self.out = out
        self.module = module
        self.bpm = bpm
        self.keys_pressed = set()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_to_midi = {char:num+keyboard_layout_no['base'] for char, num in keyboard_layout_no['keys'].items()}
        self.running = True
        
        if out == TesterOutput.MIDI:
            self.module.send_fn = lambda note: self.send_midi(note)
            self.midi_out = mido.open_output(name='Python MIDI', virtual=True)
        elif out == TesterOutput.AUDIO:
            self.module.send_fn = lambda note: self.play_audio(note)
            self.audio_playing = {}
            self.audio_notes = {int(fname[4:7]): sa.WaveObject.from_wave_file(f"keys/{fname}") for fname in os.listdir('keys/') if fname.endswith('.wav')}
            log.dbg(self.audio_notes)
        else:
            raise Exception(f'Unknown mode {out}')
        
        self.module.redraw()

    def tick(self):    
        log.dbg('Tick start')
        next_tick = time.time()
        while True:
            if not self.running:
                return
            
            # Call the tick method of the module
            self.module.tick()
            
            # Calculate when the next tick should happen
            next_tick += 60 / (self.bpm * 24)
            
            # Sleep until the next tick
            time_to_next_tick = next_tick - time.time()
            if time_to_next_tick > 0:
                time.sleep(time_to_next_tick)

    def on_press(self, key):
        try:
            # stop keys
            if key == keyboard.Key.esc or key == keyboard.Key.enter:
                self.keyboard_listener.stop()
                self.running = False
                log.inf('')
                log.inf('Keyboard listener stopped')
                
                if self.out  == TesterOutput.MIDI:
                    self.midi_out.close()
                    log.inf('MIDI out closed')
                elif self.out == TesterOutput.AUDIO:
                    for note in self.audio_playing:
                      self.audio_playing[note].stop()
                    log.inf('Audio stopped')  
                return
          
            # encoder keys
            if key == keyboard.Key.left:
                self.module.enc(-1)
                return
            elif key == keyboard.Key.right:
                self.module.enc(1)
                return
            
            # not proceed if already pressed
            if key.char in self.keys_pressed:
              return
            self.keys_pressed.add(key.char)
            
            # Get MIDI note number from key press
            midi_note = self.key_to_midi[key.char]
            log.dbg(f'Key pressed: {key}')

            # Create a MIDI 'note on' message and send it to the module
            event = midi.Note(midi_note, 127, midi.State.NOTE_ON)  # Assuming velocity 127
            self.module.note(event)

        except:
            # Ignore key presses that are not mapped to a MIDI note
            log.dbg(f'Key not mapped: {key}')

    def on_release(self, key):
        try:
            if key.char not in self.keys_pressed:
              return
            self.keys_pressed.remove(key.char)
            
            # Get MIDI note number from key release
            midi_note = self.key_to_midi[key.char]
            log.dbg(f'Key released: {key}')

            # Create a MIDI note off message and send it to the module
            event = midi.Note(midi_note, 127, midi.State.NOTE_OFF)  # Assuming velocity 127
            self.module.note(event)

        except:
            # Ignore key releases that are not mapped to a MIDI note
            log.dbg(f'Key not mapped: {key}')

          
    def play_audio(self, note):
      
      if note.note not in self.audio_notes:
        log.wrn(f'Note {note.note} out of range')
        return
      
      log.dbg(f'Audio event: {note}')
      
      if note.pressed:
        # Start playing the note and store the play object
        log.dbg(f'Playing note {note.note}')
        self.audio_playing[note.note] = self.audio_notes[note.note].play()
      else:
        # Stop the note if it's playing
        if note.note in self.audio_playing:
            log.dbg(f'Stopping note {note.note}')
            self.audio_playing[note.note].stop()
            del self.audio_playing[note.note]

    def send_midi(self, note):
        log.dbg(f'Sending MIDI event: {note}')
        msg = mido.Message('note_on' if note.pressed else 'note_off', note=note.note, velocity=note.velocity, channel=note.channel)
        self.midi_out.send(msg)

    def start(self):
        # Start listening for keyboard inputs
        log.inf('Starting keyboard listener, stop by pressing ESC or ENTER')
        log.inf('Use LEFT and RIGHT to control the encoder')
        self.keyboard_listener.start()
        
        # start the tick thread
        threading.Thread(target=self.tick).start()

        while True:
            for i in range(3):
                if not self.running:
                    return
                # log.inf('\rRunning'+'.'*i+' '*(2-i)+' (stop: ESC or ENTER)', end='')
                time.sleep(0.5)