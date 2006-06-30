import math
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
          else:
             raise "feynML Error: invalid top-level tag <%s>"%element.tag

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
           elif element.tag == "connect":
              fd.add( self.get_connect(element,thedict) )
           elif element.tag == "label":
              pass # no labels yet
           else:
              raise "feynML Error: invalid tag <%s> in <diagram>"%element.tag
       return fd

   def get_vertex(self,element,thedict):
       """Build a vertex from its feynML representation."""

       try:
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
       except:
          raise "feynML Error: invalid x,y attributes for <vertex> element"
       v = feyn.DecoratedPoint(x,y)
       if "style" in element.attrib:
          v = self.apply_layout(element.attrib["style"],v)
       if "label" in element.attrib:
          v = v.fillstyle(feyn.FreeTeXLabel(element.attrib["label"],x,y,displace=3*pyx.unit.t_pt,angle=90))
       try:
          thedict[element.attrib["id"]] = v
       except:
          raise "feynML Error: missing id attribute in <vertex> element"
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
       if "style" in element.attrib:
          l = self.apply_layout(element.attrib["style"],l)
       if "label" in element.attrib:
          l = l.style(feyn.TeXLabel(element.attrib["label"]))
       try:
          thedict[element.attrib["id"]] = l
       except:
          raise "feynML Error: missing id attribute in <propagator> element"
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
       if "style" in element.attrib:
          l = self.apply_layout(element.attrib["style"],l)
       if "label" in element.attrib:
          l = l.style(feyn.TeXLabel(element.attrib["label"]))
       try:
          thedict[element.attrib["id"]] = l
       except:
          raise "feynML Error: missing id attribute in <leg> element"
       return l

   def get_blob(self,element,thedict):
       """Build a blob from its feynML representation."""

       try:
          x = float(element.attrib["x"])
          y = float(element.attrib["y"])
          shape = element.attrib["shape"]
          radius = float(element.attrib["radius"])
       except:
          raise "feynML Error: invalid attribute for <blob> element"
       b = feyn.NamedBlob[shape](x,y,radius)
       if "style" in element.attrib:
          b = self.apply_layout(element.attrib["style"],b)
       if "label" in element.attrib:
          b = b.strokestyle(feyn.FreeTeXLabel(element.attrib["label"],x,y))
       try:
          thedict[element.attrib["id"]] = b
       except:
          raise "feynML Error: missing id attribute in <blob> element"
       return b

   def get_connect(self,element,thedict):
       """Build a blob's connect-point from its feynML representation."""

       try:
          parent = thedict[element.attrib["blob"]]
          direction = element.attrib["dir"]
       except:
          raise "feynML Error: invalid attribute for <connect> element"
       try:
          angle = float(direction) * math.pi/180.
       except:
          winds = {"n":90,"s":-90,"e":0,"w":180,
                   "ne":45,"se":-45,"nw":135,"sw":-135}
          try:
             angle = winds[direction] * math.pi/180.
          except:
             raise "feynML Error: invalid direction %s"%direction
       if parent.blobshape == "circle":
          x = parent.centre.x() + parent.radius*math.cos(angle)
          y = parent.centre.y() + parent.radius*math.sin(angle)
       else:
          raise "*** TODO *** connecting to non-circles not yet implemented !!"
       p = feyn.Point(x,y)
       try:
          thedict[element.attrib["id"]] = p
       except:
          raise "feynML Error: missing id attribute in <connect> element"
       return p

   def apply_layout(self,stylestring,object):
       """Apply the decorators encoded in a style string to an object."""

       styleelements = stylestring.split(";")
       for styling in styleelements:
           if styling[:10] == "mark-shape" and isinstance(object,feyn.DecoratedPoint):
              object.mark(feyn.NamedMark[styling[11:]])
           elif styling[:9] == "mark-size" and isinstance(object,feyn.DecoratedPoint):
              object.size(float(styling[10:]))
           else:
              pass 
       return object


if __name__=="__main__":
   import sys
   x = FeynMLReader(sys.argv[1])
   f = x.get_diagram(0)
   c = pyx.canvas.canvas()
   f.draw(c)
   c.writeEPSfile("thetest-2")

