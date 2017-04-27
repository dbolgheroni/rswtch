from abc import abstractmethod, ABCMeta


class Channel:
    __metaclass__ = ABCMeta

    def __init__(self, conf):
        self.channel = conf['channel']
        self.annotation = None
        
    @abstractmethod
    def up(self):
        return

    @abstractmethod
    def down(self):
        return

    @abstractmethod
    def toggle(self):
        return

    @abstractmethod
    def reset(self):
        return

    @abstractmethod
    def status(self):
        return
