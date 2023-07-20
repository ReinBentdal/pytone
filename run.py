import sys
import os
import inspect
import importlib.util
import midi
from utils.log import Log
from utils.midi_tester import Tester, TesterOutput

log = Log(Log.LEVEL_INF, name="run")

def load_module_class(module_path, base_class):
    # Check if the module_path is valid
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"No such file: '{module_path}'")
    
    # Load the module
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Retrieve class that extends base_class from the module
    found_classes = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and issubclass(obj, base_class) and obj is not base_class:
          found_classes.append((name, obj))
    if len(found_classes) == 1:
      return found_classes[0][1]
    elif len(found_classes) > 1:
      err_msg = "Found more than one class which inherits from midi.Module. Please make sure there is only one such class in the module. Found"
      for name, obj in found_classes:
        err_msg += f"\n - {name}"
      log.err(err_msg)
      return None
    else:
      log.wrn(f"No class extending 'Module' found in '{module_path}'")
      return None  # return None if no such class found

if __name__ == "__main__":
    module_path = sys.argv[1]  # get the module path from command-line arguments
      
    module_class = load_module_class(module_path, midi.Module)  # get the class from the module
    
    if module_class is None:
        print(f"No class extending 'Module' found in '{module_path}'")
        exit()

    # Use your module class in the tester
    t = Tester(module_class(), bpm=120, out=TesterOutput.MIDI)
    t.start()