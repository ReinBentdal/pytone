import pytone.midi as midi
from pytone.utils.midi_tester import Tester, TesterOutput
import pytone.canvas as canvas

class Hello(midi.Module):
    def note(self, event: midi.Note):
        self.send(event)  # just pass event further
        self.redraw()

    def redraw(self):
        # write 'Hello' to the display
        canvas.write('Hello')

if __name__ == '__main__':
    # test the module
    t = Tester(Hello(), out=TesterOutput.AUDIO)
    t.start()
