# PyTone


## Installation

```
# create virtual environment with conda
conda create -n pytone python=3.9
conda activate pytone
(pytone) pip install -e .
```

## Code formatting

```
# inside virtual environment
(pytone) pip install pre-commit
(pytone) pip install black

# Install git hooks
(pytone) pre-commit install
# pre-commit installed at .git/hooks/pre-commit
```


## Troubleshooting

Linux problems with `examples/arpeggio.py`:
```
ALSA lib conf.c:4005:(snd_config_hooks_call) Cannot open shared library libasound_module_conf_pulse.so (/usr/lib64/alsa-lib/libasound_module_conf_pulse.so: cannot open shared object file: No such file or directory)
ALSA lib seq.c:935:(snd_seq_open_noupdate) Unknown SEQ default
Traceback (most recent call last):
  File "_rtmidi.pyx", line 1023, in _rtmidi.MidiOut.__cinit__
RuntimeError: MidiOutAlsa::initialize: error creating ALSA sequencer client object.
```

Haven't found a solution yet. Some related threads:
- https://github.com/SpotlightKid/python-rtmidi/issues/138
- https://askubuntu.com/a/1039003
- https://kodi.wiki/view/Archive:PulseAudio/HOW-TO:_Disable_PulseAudio_and_use_ALSA_(without_removing_PulseAudio)_for_Ubuntu
