import pytone.midi as midi
from pytone.utils.midi_tester import Tester, TesterOutput
import pytone.canvas as canvas


class Hello(midi.Module):
    def note(self, event: midi.Note):
        self.send(event)  # just pass event further

        self.redraw(note=event.note)

    def redraw(self, note=None):
        # write 'Hello' to the display
        canvas.write(f'Hello {note if note != None else ""}')


t = Tester(Hello(), out=TesterOutput.AUDIO)
t.start()
