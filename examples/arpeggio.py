import pytone.midi as midi
import pytone.canvas as canvas
from pytone.utils.midi_tester import Tester, TesterOutput


class Arpeggio(midi.Module):
    TICKS_PER_NOTE_OPTIONS = [1, 4, 8, 12]

    def __init__(self):
        self.reset()

    def reset(self):
        """Sets the scetch to its initial state"""
        self.tick_count = 0
        self.ticks_per_note_select = 2
        self.last_played_note = None
        self.current_note_idx = 0
        self.notes_active = []

    @property
    def ticks_per_note(self):
        return self.TICKS_PER_NOTE_OPTIONS[self.ticks_per_note_select]

    def note(self, event: midi.Note):
        """Processes note events. Adds or removes from arpeggio"""
        if event.pressed:
            self.notes_active.append(event)
        else:
            self.notes_active.remove(event)

    def enc(self, inc):
        """Physical rotary encoder events. Changes the arpeggio speed"""
        # selects the arpeggio speed and bound checks
        self.ticks_per_note_select = min(
            max(self.ticks_per_note_select + inc, 0), len(self.TICKS_PER_NOTE_OPTIONS) - 1
        )

        # update display graphics
        self.redraw()

    def tick(self):
        self.tick_count += 1
        if self.tick_count < self.ticks_per_note:
            return
        self.tick_count = 0

        # stop last played note
        if self.last_played_note is not None:
            event = self.last_played_note.copy_with(state=midi.State.NOTE_OFF)
            self.send(event)
            self.last_played_note = None

        # play new note
        if len(self.notes_active) > 0:
            if self.current_note_idx >= len(self.notes_active):
                self.current_note_idx = 0
            event = self.notes_active[self.current_note_idx]
            self.send(event)
            self.last_played_note = event
            self.current_note_idx += 1

    def redraw(self):
        canvas.write(f"*ARP:1/{self.ticks_per_note}")


# midi_tester.log.set_level(midi_tester.log.LEVEL_DBG)
t = Tester(Arpeggio(), bpm=120, out=TesterOutput.MIDI)
t.start()
