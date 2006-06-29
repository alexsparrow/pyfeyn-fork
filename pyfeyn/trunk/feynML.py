import pyx
import feyn
import elementtree.ElementTree as elementtree

class FeynMLReader:
   """Class to construct a Feynman diagram from it feynML representation."""

   def __init__(self, filename):
       """Read feynML from file."""

       self.root = elementtree.parse(filename).getroot()
       self.dict = {}

   def get_graph(self):
       """Return the Feynman diagram represented by file contents."""

       fd = feyn.FeynDiagram()
       if self.root.tag != "graph":
          raise "feynML Error: <%>, not <graph>, as root element"%self.root.tag
       for element in self.root:
           if element.tag == "head":
              pass
           elif element.tag == "line":
              fd.add( self.get_line(element) )
           elif element.tag == "vertex":
              fd.add( self.get_vertex(element) )
           elif element.tag == "leg":
              fd.add( self.get_leg(element) )
           elif element.tag == "blob":
              fd.add( self.get_blob(element) )
           else:
              raise "feynML Error: invalid tag <%s> in <graph>"%element.tag
       return fd

   def get_vertex(self,element):
       """Build a vertex from its feynML representation."""

       try:
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
       except:
          raise "feynML Error: invalid attribute for <vertex> element"
       v = feyn.Point(x,y)
       self.dict[element.attrib["id"]] = v
       return v

   def get_line(self,element):
       """Build a line from its feynML representation."""

       try:
          type = element.attrib["type"]
          p1 = self.dict[element.attrib["source"]]
          p2 = self.dict[element.attrib["target"]]
       except:
          raise "feynML Error: invalid attribute for <line> element"
       l = feyn.NamedLine[type](p1,p2)
       for subelement in element:
          if subelement.tag == "layout":
             for subsubelement in subelement:
                l = self.apply_layout(subsubelement,l)
       self.dict[element.attrib["id"]] = l
       return l

   def get_leg(self,element):
       """Build a leg from its feynML representation."""

       try:
          type = element.attrib["type"]
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
          p2 = self.dict[element.attrib["target"]]
       except:
          raise "feynML Error: invalid attribute for <leg> element"
       l = feyn.NamedLine[type](feyn.Point(x,y),p2)
       self.dict[element.attrib["id"]] = l
       return l

   def get_blob(self,element):
       """Build a blob from its feynML representation."""

       try:
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
          shape = element.attrib["shape"]
       except:
          raise "feynML Error: invalid attribute for <blob> element"
       b = feyn.NamedBlob[shape](x,y,0.5)
       self.dict[element.attrib["id"]] = b
       return b

   def apply_layout(self,element,object):
       """Apply the decorator encoded in a layout tag to a diagram object."""

       try:
          if element.tag == "arcthru" and isinstance(object,feyn.Line):
             x = float(element.attrib["x"])
             y = float(element.attrib["y"])
             return object.arcThru(feyn.Point(x,y))
          elif element.tag == "label":
             return object
          else:
             raise "feynML Error: invalid tag inside <layout> element"
       except:
          raise "feynML Error while parsing <layout> element"


if __name__=="__main__":
   x = FeynMLReader("test.feynml")
   f = x.get_graph()
   c = pyx.canvas.canvas()
   f.draw(c)
   c.writeEPSfile("thetest-2")

