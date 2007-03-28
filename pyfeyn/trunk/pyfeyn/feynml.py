"""PyFeyn interface to the proposed FeynML XML dialect."""

import math, pyx, md5
from xml.dom.minidom import *
from elementtree.ElementTree import ElementTree
from diagrams import FeynDiagram
from lines import *
from points import *
from deco import *
from blobs import *

class FeynMLWriter:
    """Class to write a FeynML representation of a Feynman diagram."""
   
    def __init__(self, filename):
        """Write FeynML to a file."""
        pass
      

    def diagramToXML(self):
        root = xml.Element("diagram")
        for obj in self.__objs:
            root.append(obj.to_xml())
            return xml.tostring(root).replace(">",">\n")

    def blobToXML(self):
        ele = xml.Element("blob",
                          {"id" : "V%s" % md5.md5(str(self.xpos, self.ypos)).hexdigest(),
                           "x" : str(self.xpos), "y" : str(self.ypos),
                           "shape" : hasattr(self,"blobshape") and self.blobshape or "circle"})
        return ele

    def lineToXML(self):
        attribs = {"id":"P%s"%md5.md5(str((self.p1.xpos,self.p1.ypos,self.p2.xpos,self.p2.ypos,self.__arcthrupoint and (self.__arcthrupoint.xpos,self.__arcthrupoint.ypos)))).hexdigest(),
                   "source":"V%s"%md5.md5(str((self.p1.xpos,self.p1.ypos))).hexdigest(),
                   "target":"V%s"%md5.md5(str((self.p2.xpos,self.p2.ypos))).hexdigest(),
                   "type":hasattr(self,"linetype") and self.linetype or "fermion"}
        if self.bendamount:
            attribs["bend"] = str(self.bendamount)
        ele = xml.Element("propagator",attribs)
        return ele

    def pointToXML(self):
        ele = xml.Element("vertex",{"id":"V%s"%md5.md5(str((self.xpos,self.ypos))).hexdigest(),"x":str(self.xpos), "y":str(self.ypos)})
        return ele

    def decopointToXML(self):
        ele = Point.to_xml(self)
        fills = ""
        for x in self.fillstyles:
            if isinstance(x,pyx.color.rgb):
                fills = fills + " #%02x%02x%02x"%(255*x.color["r"], 255*x.color["g"], 255*x.color["b"])
        strokes = ""
        for x in self.strokestyles:
            if isinstance(x,pyx.color.rgb):
                strokes = strokes + " #%02x%02x%02x"%(255*x.color["r"], 255*x.color["g"],255*x.color["b"])
        s = "mark-shape:%s;mark-size:%s;fill-style:%s;line-style:%s;" % \
            (MarkedName[self.marker],pyx.unit.tocm(self.radius), fills,strokes )
        ele.attrib["style"] = s
        return ele

     

##############################################

       

class FeynMLReader:
    """Class to construct a Feynman diagram from its FeynML representation."""

    def __init__(self, filename):
        """Read FeynML from a file."""
        elementtree = ElementTree()
        self.root = elementtree.parse(filename) #.getroot()
        self.diagrams = []
        self.dicts = []
        if self.root.tag != "feynml":
            raise "FeynML Error: <Feynml> must be root element"%self.root.tag
        for element in self.root:
            if element.tag == "head":
                pass # ignore header for now
            elif element.tag == "diagram":
                self.diagrams.append(element)
                self.dicts.append({})
            else:
                raise "FeynML Error: invalid top-level tag <%s>"%element.tag

    def get_diagram(self,n):
        """Return the nth Feynman diagram represented by file contents."""
        fd = FeynDiagram()
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
                raise "FeynML Error: invalid tag <%s> in <diagram>"%element.tag
        return fd

    def get_vertex(self,element,thedict):
        """Build a vertex from its FeynML representation."""

        try:
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
        except:
            raise "FeynML Error: invalid x,y attributes for <vertex> element"
        v = DecoratedPoint(x,y)
        if "style" in element.attrib:
            v = self.apply_layout(element.attrib["style"],v)
        if "label" in element.attrib:
            v = v.setFillstyles(PointLabel(v,element.attrib["label"],displace=3,angle=90))
        try:
            thedict[element.attrib["id"]] = v
        except:
            raise "FeynML Error: missing id attribute in <vertex> element"
        return v

    def get_line(self,element,thedict):
        """Build a line from its feynML representation."""

        try:
            type = element.attrib["type"]
            p1 = thedict[element.attrib["source"]]
            p2 = thedict[element.attrib["target"]]
        except:
            raise "FeynML Error: invalid attribute for <propagator> element"
        l = NamedLine[type](p1,p2)
        if "bend" in element.attrib:
            l.bend(float(element.attrib["bend"]))
        if "style" in element.attrib:
            l = self.apply_layout(element.attrib["style"],l)
        if "label" in element.attrib:
            l = l.style(Label(element.attrib["label"]))
        try:
            thedict[element.attrib["id"]] = l
        except:
            raise "FeynML Error: missing id attribute in <propagator> element"
        return l

    def get_leg(self,element,thedict):
        """Build a leg from its FeynML representation."""

        try:
            type = element.attrib["type"]
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
            p2 = thedict[element.attrib["target"]]
        except:
            raise "FeynML Error: invalid attribute for <leg> element"
        l = NamedLine[type](Point(x,y),p2)
        if "style" in element.attrib:
            l = self.apply_layout(element.attrib["style"],l)
        if "label" in element.attrib:
            l = l.style(Label(element.attrib["label"]))
        try:
            thedict[element.attrib["id"]] = l
        except:
            raise "FeynML Error: missing id attribute in <leg> element"
        return l

    def get_blob(self,element,thedict):
        """Build a blob from its FeynML representation."""
        try:
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
            shape = element.attrib["shape"]
            radius = float(element.attrib["radius"])
        except:
            raise "FeynML Error: invalid attribute for <blob> element"
        b = NamedBlob[shape](x=x,y=y,radius=radius)
        if "style" in element.attrib:
            b = self.apply_layout(element.attrib["style"],b)
        if "label" in element.attrib:
            pass
            #b = b.setFillStyle(PointLabel(element.attrib["label"],x,y))
        try:
            thedict[element.attrib["id"]] = b
        except:
            raise "FeynML Error: missing id attribute in <blob> element"
        return b

    def get_connect(self,element,thedict):
        """Build a blob's connect-point from its FeynML representation."""
        try:
            parent = thedict[element.attrib["blob"]]
            direction = element.attrib["dir"]
        except:
            raise "feynML Error: invalid attribute for <connect> element"
        try:
            angle = float(direction) * math.pi/180.
        except:
            winds = {"n":90,"s":-90,"e":0,"w":180, "ne":45,"se":-45,"nw":135,"sw":-135}
        try:
            angle = winds[direction] * math.pi/180.
        except:
            raise "FeynML Error: invalid direction %s"%direction
        if parent.blobshape == "circle":
            x = parent.x() + parent.radius*math.cos(angle)
            y = parent.y() + parent.radius*math.sin(angle)
        else:
            raise "*** TODO *** connecting to non-circles not yet implemented !!"
        p = DecoratedPoint(x,y)
        try:
            thedict[element.attrib["id"]] = p
        except:
            raise "FeynML Error: missing id attribute in <connect> element"
        return p

    def apply_layout(self,stylestring,object):
        """Apply the decorators encoded in a style string to an object."""
        styleelements = stylestring.split(";")
        for styling in styleelements:
            if styling[:10] == "mark-shape" and isinstance(object,DecoratedPoint):
                object.mark(NamedMark[styling[11:]])
            elif styling[:9] == "mark-size" and isinstance(object,DecoratedPoint):
                object.size(float(styling[10:]))
            else:
                pass 
        return object



#####################################################



if __name__=="__main__":
   import sys
   reader = FeynMLReader(sys.argv[1])
   _f = reader.get_diagram(0)
   _c = pyx.canvas.canvas()
   _f.draw(sys.argv[1]+".eps")

