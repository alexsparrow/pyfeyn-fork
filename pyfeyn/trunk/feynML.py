import pyx
import feyn
import elementtree.ElementTree as elementtree

class FeynMLReader:
   """Class to construct a Feynman diagram from it feynML representation."""

   def __init__(self, filename):
       """Read feynML from file."""

       self.root = elementtree.parse(filename).getroot()
       self.diagrams = []
       self.dicts = []
       if self.root.tag != "feynml":
          raise "feynML Error: <feynml> must be root element"%self.root.tag
       for element in self.root:
          if element.tag == "head":
             pass # ignor header for now
          elif element.tag == "diagram":
             self.diagrams.append(element)
             self.dicts.append({})

   def get_diagram(self,n):
       """Return the nth Feynman diagram represented by file contents."""

       fd = feyn.FeynDiagram()
       thediagram = self.diagrams[n]
       thedict = self.dicts[n]
       for element in thediagram:
           if element.tag == "propagator":
              fd.add( self.get_line(element,thedict) )
           elif element.tag == "vertex":
              fd.add( self.get_vertex(element,thedict) )
           elif element.tag == "leg":
              fd.add( self.get_leg(element,thedict) )
           elif element.tag == "blob":
              fd.add( self.get_blob(element,thedict) )
           else:
              raise "feynML Error: invalid tag <%s> in <diagram>"%element.tag
       return fd

   def get_vertex(self,element,thedict):
       """Build a vertex from its feynML representation."""

       try:
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
       except:
          raise "feynML Error: invalid attribute for <vertex> element"
       v = feyn.Point(x,y)
       thedict[element.attrib["id"]] = v
       return v

   def get_line(self,element,thedict):
       """Build a line from its feynML representation."""

       try:
          type = element.attrib["type"]
          p1 = thedict[element.attrib["source"]]
          p2 = thedict[element.attrib["target"]]
       except:
          raise "feynML Error: invalid attribute for <propagator> element"
       l = feyn.NamedLine[type](p1,p2)
       if "bend" in element.attrib:
          l.bend(float(element.attrib["bend"]))
       thedict[element.attrib["id"]] = l
       return l

   def get_leg(self,element,thedict):
       """Build a leg from its feynML representation."""

       try:
          type = element.attrib["type"]
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
          p2 = thedict[element.attrib["target"]]
       except:
          raise "feynML Error: invalid attribute for <leg> element"
       l = feyn.NamedLine[type](feyn.Point(x,y),p2)
       thedict[element.attrib["id"]] = l
       return l

   def get_blob(self,element,thedict):
       """Build a blob from its feynML representation."""

       try:
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
          shape = element.attrib["shape"]
       except:
          raise "feynML Error: invalid attribute for <blob> element"
       b = feyn.NamedBlob[shape](x,y,0.5)
       thedict[element.attrib["id"]] = b
       return b

   def apply_layout(self,stylestring,object):
       """Apply the decorators encoded in a style string to an object."""

       styleelements = stylestring.split(";")
       for styling in styleelements:
           pass 


if __name__=="__main__":
   x = FeynMLReader("test.feynml")
   f = x.get_diagram(0)
   c = pyx.canvas.canvas()
   f.draw(c)
   c.writeEPSfile("thetest-2")

