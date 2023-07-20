import pytone.midi as midi
import pytone.canvas as canvas
from pytone.utils.midi_tester import Tester, TesterOutput

class Pulse(midi.Module):
  TICKS_PER_NOTE_OPTIONS = [2, 4, 8, 12]
  
  def __init__(self):
    self.reset()
    
  def reset(self):
    self.playing = []
    self.ticks = 0
    self.next_press = True
    self.ticks_per_note_select = 2
  
  def note(self, k):
    if k.pressed:
      self.playing.append(k)
    else:
      if not self.next_press:
        self.send(k)
      self.playing.remove(k)
    
  def tick(self):    
    self.ticks += 1
    if self.ticks < self.TICKS_PER_NOTE_OPTIONS[self.ticks_per_note_select]:
      return
    
    self.ticks = 0

    if self.next_press:
      for k in self.playing:
        self.send(k)
    else:
      for k in self.playing:
        self.send(k.copy_with(state=midi.State.NOTE_OFF))
        
    self.next_press = not self.next_press
    
  def enc(self, inc):
    """Physical rotary encoder events. Changes the arpeggio speed"""
    # selects the speed and bound checks
    self.ticks_per_note_select = min(max(self.ticks_per_note_select + inc, 0), len(self.TICKS_PER_NOTE_OPTIONS) - 1)

    # update screen graphics
    self.redraw()
        
  def redraw(self):
    ticks_per_note = self.TICKS_PER_NOTE_OPTIONS[self.ticks_per_note_select]
    canvas.write(f'*PLS: 1/{ticks_per_note}')
    
if __name__ == '__main__':
  t = Tester(Pulse(), bpm=120, out=TesterOutput.MIDI)
  t.start()