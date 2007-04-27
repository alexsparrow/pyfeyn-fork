"""PyFeyn interface to the proposed FeynML XML dialect."""

import math, pyx, md5
from elementtree.ElementTree import *
from pyfeyn.diagrams import FeynDiagram
from pyfeyn.lines import *
from pyfeyn.points import *
from pyfeyn.deco import *
from pyfeyn.blobs import *


NamedMark = { "none" : lambda:None, "circle" : CircleMark, "square" : SquareMark }


class FeynMLWriter:
    """Class to write a FeynML representation of a Feynman diagram."""
    
    def __init__(self, filename):
        """Write FeynML to a file."""
        pass
    
    def diagramToXML(self, fd):
        root = Element("diagram")
        self.objects = fd._FeynDiagram__objs
        self.ids = {}
        self.linecount = 0
        self.vertexcount = 0
        self.blobcount = 0
        for obj in self.objects:
            if isinstance(obj, Blob):
                root.append(self.blobToXML(obj))
            elif isinstance(obj, Line):
                l, p1, p2 = self.lineToXML(obj)
                if p1 is not None:
                    root.append(p1)
                if p2 is not None:
                    root.append(p2)
                root.append(l)
            elif isinstance(obj,DecoratedPoint):
                root.append(self.decopointToXML(obj))
            elif isinstance(obj,Point) and not isinstance(obj,DecoratedPoint):
                root.append(self.pointToXML(obj))
            else:
                print "Can't convert object to XML!"
        return tostring(root).replace(">",">\n")

    def blobToXML(self, b):
        attribs = {"id" : "B%s" % self.blobcount,
                   "x" : str(b.xpos), "y" : str(b.ypos),
                   "shape" : hasattr(b,"blobshape") and b.blobshape or "circle"}
        ele = Element("blob", attribs)
        self.ids[md5.md5(str(b.xpos, b.ypos)).hexdigest()] = attribs["id"]
        self.blobcount += 1
        return ele

    def lineToXML(self, l):
        source = md5.md5(str((l.p1.xpos, l.p1.ypos))).hexdigest()
        if source not in self.ids:
            s1 = self.pointToXML(l.p1)
        else:
            s1 = None 
        target = md5.md5(str((l.p2.xpos, l.p2.ypos))).hexdigest()
        if target not in self.ids:
            s2 = self.pointToXML(l.p2)
        else:
            s2 = None
        attribs = {"id" : "P%s" % self.linecount,
                   "source" : self.ids[source],
                   "target" : self.ids[target],
                   "type" : hasattr(l,"linetype") and l.linetype or "fermion"}
        if l.arcthrupoint:
            middle = l.p1.midpoint(l.p2)
            nx = (middle.y() - l.p1.y()) / abs(l.p1.distance(middle))
            #vx = middle.x() - l.p1.x()
            bendamount = (l.arcthrupoint.x() - middle.x()) / nx
            attribs["bend"] = str(bendamount)
        ele = Element("propagator", attribs)
        self.ids[md5.md5(str((l.p1.xpos,l.p1.ypos,l.p2.xpos,l.p2.ypos,
                              l.arcthrupoint and (l.arcthrupoint.xpos,
                       l.arcthrupoint.ypos)))).hexdigest()] = attribs["id"]
        self.linecount += 1
        return ele, s1, s2

    def pointToXML(self, p):
        attribs = {"id" : "V%s" % self.vertexcount,
                   "x" : str(p.xpos),
                   "y" : str(p.ypos)}
        ele = Element("vertex", attribs)
        self.ids[md5.md5(str((p.xpos, p.ypos))).hexdigest()] = attribs["id"]
        self.vertexcount += 1
        return ele

    def decopointToXML(self, p):
        ele = self.pointToXML(p)
        fills = ""
        for x in p.fillstyles:
            if isinstance(x, pyx.color.rgb):
                fills = fills + " #%02x%02x%02x" % (255 * x.color["r"],
                                                   255 * x.color["g"],
                                                   255 * x.color["b"])
        strokes = ""
        for x in p.strokestyles:
            if isinstance(x, pyx.color.rgb): 
                strokes = strokes + " #%02x%02x%02x" % (255 * x.color["r"],
                                                        255 * x.color["g"],
                                                        255 * x.color["b"])
        s = "mark-shape:%s; mark-size:%s; fill-style:%s; line-style:%s;" % \
            (p.marker.__class__.__name__[:-4].lower(),
             hasattr(p.marker,"radius") and pyx.unit.tocm(p.marker.radius) \
               or (hasattr(p.marker,"size") and pyx.unit.tocm(p.marker.size)\
                   or 0), fills, strokes )
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
            raise "FeynML Error: <Feynml> must be root element" % self.root.tag
        for element in self.root:
            if element.tag == "head":
                pass # ignore header for now
            elif element.tag == "diagram":
                self.diagrams.append(element)
                self.dicts.append({})
            else:
                raise "FeynML Error: invalid top-level tag <%s>" % element.tag


    def get_diagram(self, n):
        """Return the nth Feynman diagram represented by file contents."""
        fd = FeynDiagram()
        thediagram = self.diagrams[n]
        thedict = self.dicts[n]
        for element in thediagram:
            if element.tag == "propagator":
                fd.add( self.get_line(element, thedict) )
            elif element.tag == "vertex":
                fd.add( self.get_vertex(element, thedict) )
            elif element.tag == "leg":
                fd.add( self.get_leg(element, thedict) )
            elif element.tag == "blob":
                fd.add( self.get_blob(element, thedict) )
            elif element.tag == "connect":
                fd.add( self.get_connect(element, thedict) )
            elif element.tag == "label":
                pass # no labels yet
            else:
                raise Exception("FeynML Error: invalid tag <%s> in <diagram>" % \
                      element.tag)
        return fd


    def get_vertex(self, element, thedict):
        """Build a vertex from its FeynML representation."""

        try:
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
        except:
            raise Exception("FeynML Error: invalid x, y attributes for <vertex> element")
        v = DecoratedPoint(x, y)
        if "style" in element.attrib:
            v = self.apply_layout(element.attrib["style"], v)
        if "label" in element.attrib:
            v = v.setFillstyles(PointLabel(v, element.attrib["label"],
                                           displace=3, angle=90))
        try:
            thedict[element.attrib["id"]] = v
        except:
            raise Exception("FeynML Error: missing id attribute in <vertex> element")
        return v


    def get_line(self, element, thedict):
        """Build a line from its feynML representation."""

        try:
            thetype = element.attrib["type"]
            p1 = thedict[element.attrib["source"]]
            p2 = thedict[element.attrib["target"]]
        except:
            raise "FeynML Error: invalid attribute for <propagator> element"
        l = NamedLine[thetype](p1, p2)
        if "bend" in element.attrib:
            l.bend(float(element.attrib["bend"]))
        if "style" in element.attrib:
            l = self.apply_layout(element.attrib["style"], l)
        if "label" in element.attrib:
            l = l.style(Label(element.attrib["label"]))
        try:
            thedict[element.attrib["id"]] = l
        except:
            raise Exception("FeynML Error: missing id attribute in <propagator> element")
        return l


    def get_leg(self, element, thedict):
        """Build a leg from its FeynML representation."""

        try:
            thetype = element.attrib["type"]
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
            p2 = thedict[element.attrib["target"]]
        except:
            raise Exception("FeynML Error: invalid attribute for <leg> element")
        l = NamedLine[thetype](Point(x, y), p2)
        if "style" in element.attrib:
            l = self.apply_layout(element.attrib["style"], l)
        if "label" in element.attrib:
            l = l.style(Label(element.attrib["label"]))
        try:
            thedict[element.attrib["id"]] = l
        except:
            raise Exception("FeynML Error: missing id attribute in <leg> element")
        return l

    def get_blob(self, element, thedict):
        """Build a blob from its FeynML representation."""
        try:
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
            shape = element.attrib["shape"]
            radius = float(element.attrib["radius"])
        except:
            raise "FeynML Error: invalid attribute for <blob> element"
        b = NamedBlob[shape](x=x, y=y, radius=radius)
        if "style" in element.attrib:
            b = self.apply_layout(element.attrib["style"], b)
        if "label" in element.attrib:
            b.addLabel(element.attrib["label"])
        try:
            thedict[element.attrib["id"]] = b
        except:
            raise "FeynML Error: missing id attribute in <blob> element"
        return b


    def get_connect(self, element, thedict):
        """Build a blob's connect-point from its FeynML representation."""
        try:
            parent = thedict[element.attrib["blob"]]
            direction = element.attrib["dir"]
        except:
            raise Exception("FeynML Error: invalid attribute for <connect> element")
        try:
            angle = float(direction) * math.pi/180.
        except:
            winds = {"n" : 90,
                     "s" : -90,
                     "e" : 0,
                     "w" : 180,
                     "ne" : 45,
                     "se" : -45,
                     "nw" : 135,
                     "sw" : -135}
        try:
            angle = winds[direction] * math.pi/180.
        except:
            raise Exception("FeynML Error: invalid direction %s" % direction)
        if parent.blobshape == "circle":
            x = parent.x() + parent.radius * math.cos(angle)
            y = parent.y() + parent.radius * math.sin(angle)
        else:
            raise Exception("*** TODO *** connecting to non-circles not yet implemented !!")
        p = DecoratedPoint(x, y)
        try:
            thedict[element.attrib["id"]] = p
        except:
            raise Exception("FeynML Error: missing id attribute in <connect> element")
        return p


    def apply_layout(self, stylestring, obj):
        """Apply the decorators encoded in a style string to an object."""
        styleelements = stylestring.split(";")
        styledict = {}
        for styling in styleelements:
            if styling == "":
               break
            s = styling.split(":")
            styledict[s[0]] = s[1]
        if styledict.has_key("mark-shape") and isinstance(obj, DecoratedPoint):
                marktype = NamedMark[styledict["mark-shape"]]
                obj.setMark(marktype())
        if styledict.has_key("mark-size") and isinstance(obj, DecoratedPoint):
                if obj.marker is None:
                   obj.setMark(SQUARE)
                else:
                   obj.setMark(marktype(size=float(styledict["mark-size"])))
        return obj



#####################################################



if __name__ == "__main__":
    import sys
    reader = FeynMLReader(sys.argv[1])
    _f = reader.get_diagram(0)
    _f.draw(sys.argv[1]+".eps")

