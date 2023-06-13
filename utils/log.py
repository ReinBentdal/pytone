from colorama import Fore, Style
from threading import Lock

class Log:
    _lock = Lock()
    
    LEVEL_DBG = 3   # debug
    LEVEL_INF = 2   # info
    LEVEL_WRN = 1   # warning
    LEVEL_ERR = 0   # error
    LEVEL_IMP = -1  # important

    _LEVEL_COLORS = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.WHITE, Fore.CYAN]
    _LEVEL_PREFIXES = ['ERR', 'WRN', 'INF', 'DBG', 'IMP']

    _last_logger = None

    def __init__(self, level: int, name=None):
        self.level: int = level
        self.name: any = name
        self.should_print_prefix: bool = True

    def set_level(self, level: int) -> None:
        self.level = level

    def dbg(self, msg: any, **kwargs) -> None: self._print(self.LEVEL_DBG, msg, **kwargs)
    def inf(self, msg: any, **kwargs) -> None: self._print(self.LEVEL_INF, msg, **kwargs)
    def wrn(self, msg: any, **kwargs) -> None: self._print(self.LEVEL_WRN, msg, **kwargs)
    def err(self, msg: any, **kwargs) -> None: self._print(self.LEVEL_ERR, msg, **kwargs)
    def imp(self, msg: any, **kwargs) -> None: self._print(self.LEVEL_IMP, msg, **kwargs)

    def _print(self, level: int, msg: any, **kwargs) -> None:
        if self.level >= level:
            with Log._lock:
                color = self._LEVEL_COLORS[level]
                
                if self.should_print_prefix or Log._last_logger != self:
                    name_prefix = f' {self.name}' if self.name != None else ''
                    level_prefix = f'[{self._LEVEL_PREFIXES[level]}]'
                    combined_prefix = level_prefix + name_prefix + ': '
                else:
                    combined_prefix = ''
                    
                if Log._last_logger != self: print('')
                print(color+combined_prefix+str(msg)+Style.RESET_ALL, **kwargs)
                
                self.should_print_prefix = '\n' in (domain := kwargs.get('end', '\n\r')) or '\r' in domain
                Log._last_logger = self