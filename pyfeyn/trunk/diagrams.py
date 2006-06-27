import pyx
import math

##### FeynDiagram class #####

class FeynDiagram:
    "Objects for holding a set of Feynman diagram components"
    __objs = []

    def add(self, obj):
        self.__objs = self.__objs + [obj]

    def draw(self, canvas):
        for obj in self.__objs:
            obj.draw(canvas)


