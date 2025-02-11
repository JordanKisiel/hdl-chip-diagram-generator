from abc import ABC, abstractmethod

class Diagrammable(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def layout(self):
        pass