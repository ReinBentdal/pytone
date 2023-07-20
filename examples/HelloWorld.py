import midi
import canvas

class Hello(midi.Module):
  def note(self, event: midi.Note):
    self.send(event) # just pass event further
    
    self.redraw(note=event.note)
    
  def redraw(self, note=None):
    # write 'Hello' to the display
    canvas.write(f'Hello {note if note != None else ""}')