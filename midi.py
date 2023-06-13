from enum import Enum
from utils.log import Log

log = Log(Log.LEVEL_INF)

class State(Enum):
  """Represents the state of a midi event"""
  NOTE_OFF = 0
  NOTE_ON = 1

class Note:
  """Represents a midi note"""
  def __init__(self, note: int, velocity: int, state: State, channel:int=0):
    self.note = note
    self.velocity = velocity
    self.channel = channel
    self.state = state    
    log.dbg(f'Creating Note: {self}')

  @property
  def pressed(self): return self.state == State.NOTE_ON

  def __eq__(self, other):
    if not isinstance(other, Note):
      return False
    return self.note == other.note and self.channel == other.channel
  
  def copy_with(self, note: int = None, velocity: int = None, state: State = None, channel: int = None):
    return Note(
        note if note is not None else self.note,
        velocity if velocity is not None else self.velocity,
        state if state is not None else self.state,
        channel if channel is not None else self.channel
    )

  def __str__(self):
    return f'Note: {self.note}, velocity: {self.velocity}, channel: {self.channel}, {self.state}'

class Module:
  """Base class for midi modules"""
  def __init__(self):
    self.send_fn = None

  def reset(self):
    """Resets the scetch to its initial state"""
    pass

  def note(self, k: Note):
    """Processes note events"""
    pass

  def enc(self, inc):
    """Processes encoder events"""
    pass

  def btn(self, n, event):
    """Processes button events"""
    if event == 'back':
      self._yield_control()
      return True
    elif event == 'clear':
      self.reset()
      return True
    else:
      return False

  def tick(self):
    """Processes tick events"""
    pass

  def redraw(self):
    """Redraws the screen"""
    pass
  
  def send(self, note: Note):
    """Sends a midi note event further in processing chain"""
    log.dbg(f'Sending event: {note}')
    
    assert self.send_fn is not None, 'send_fn is not set'
    self.send_fn(note)
    
  def _yield_control(self):
    """Gives back interface control to the module which gave it control"""
    pass