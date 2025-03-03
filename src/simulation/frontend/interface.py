from abc import ABC, abstractmethod


class FrontendBase(ABC):
    @abstractmethod
    def use_backend(self, backend):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def init(self):
        pass
