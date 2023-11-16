from error_manager.interface import FatalError, ErrorManager, Error

class ModulErrorManager(ErrorManager):
    def __enter__(self):
        self._errors = []
        return self
    
    def __exit__(self, __exc_type, __exc_value, __traceback):
        if self._errors:
            print("Errors find during program work: \n".join([str(error) for error in self._errors]))

    def fatal_error(self, error: type[Error]):
        self.save_error(error)
        return FatalError

    def save_error(self, error: type[Error]):
        self._errors.append(error)