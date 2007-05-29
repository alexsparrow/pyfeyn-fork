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
        self.thefile = open(filename,"w")
        self.theroot = Element("feynml")
        head = Element("head")
        self.theroot.append(head)
        head.append(Element("meta",{"name":"creator", "value":"PyFeyn"}))

    def close(self):
        """Commit FeynML code to output file."""
        self.thefile.write(tostring(self.theroot).replace(">",">\n"))
        self.thefile.close()

    def addMetadata(self, name, value):
        """Add a meta tag to the FeynML header."""
        head = self.theroot.find("head")
        head.append(Element("meta",{"name":name, "value":value}))

    def describe(self, s):
        """Add a description to the FeynML header."""
        head = self.theroot.find("head")
        desc = Element("description")
        desc.text = s
        head.append(desc)
    
    def diagramToXML(self, fd, convertlegs=True):
        """Create FeynML code for a diagram."""
        root = Element("diagram")
        self.objects = fd._FeynDiagram__objs
        self.ids = {}
        self.singletons = []
        self.linecount = 0
        self.vertexcount = 0
        self.blobcount = 0
        self.labelcount = 0
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
            elif isinstance(obj,Label):
                root.append(self.labelToXML(obj))
            else:
                print "Can't convert object to XML!"
        # Combine single vertices/props into legs
        self.legcount = 0
        if convertlegs:
           for point in self.singletons: 
             for tag in root.getchildren():
                if tag.attrib["id"]==point:
                   for tag2 in root.getchildren():
                       if ((tag2.attrib.has_key("source") and
                            tag2.attrib["source"]==point) or
                           (tag2.attrib.has_key("target") and
                            tag2.attrib["target"]==point)):
                          attribs = tag2.attrib
                          if (tag2.attrib.has_key("source") and
                              tag2.attrib["source"]==point):
                             del attribs["source"]
                             attribs["sense"] = "incoming"
                          if (tag2.attrib.has_key("target") and
                              tag2.attrib["target"]==point):
                             attribs["sense"] = "outgoing"
                             attribs["target"] = attribs["source"]
                             del attribs["source"]
                          attribs.update(tag.attrib)
                          attribs["id"] = "E%s" % self.legcount
                          self.legcount += 1
                          root.append(Element("leg",attribs))
                          root.remove(tag)
                          root.remove(tag2)
           root.attrib["legs"]=str(self.legcount) 
        self.theroot.append(root)
        return tostring(root).replace(">",">\n")

    def blobToXML(self, b):
        """Create FeynML code for a blob."""
        attribs = {"id" : "B%s" % self.blobcount,
                   "x" : str(b.xpos), "y" : str(b.ypos),
                   "shape" : hasattr(b,"blobshape") and b.blobshape or "circle",
                   "radius" : hasattr(b,"radius") and str(b.radius) or \
                              (hasattr(b,"xrad") and "%s %s"%(b.xrad,b.yrad)) \
                              or "0"}
        ele = Element("blob", attribs)
        self.ids[md5.md5(str((b.xpos, b.ypos))).hexdigest()] = attribs["id"]
        style = ""
        fills = ""
        for x in b.fillstyles:
            if isinstance(x, pyx.color.rgb):
                fills = fills + " #%02x%02x%02x" % (255 * x.color["r"],
                                                   255 * x.color["g"],
                                                   255 * x.color["b"])
        if fills:
           style += "fill-style:%s; "%fills
        strokes = ""
        for x in b.strokestyles:
            if isinstance(x, pyx.color.rgb):
                strokes = strokes + " #%02x%02x%02x" % (255 * x.color["r"],
                                                        255 * x.color["g"],
                                                        255 * x.color["b"])
        if strokes:
           style += "line-style:%s;"%strokes
        ele.attrib["style"] = style
        self.blobcount += 1
        return ele

    def lineToXML(self, l):
        """Create FeynML code for a line."""
        source = md5.md5(str((l.p1.xpos, l.p1.ypos))).hexdigest()
        if source not in self.ids:
            s1 = self.pointToXML(l.p1)
        else:
            s1 = None
            if self.ids[source] in self.singletons:
               del self.singletons[self.singletons.index(self.ids[source])] 
        target = md5.md5(str((l.p2.xpos, l.p2.ypos))).hexdigest()
        if target not in self.ids:
            s2 = self.pointToXML(l.p2)
        else:
            s2 = None
            if self.ids[target] in self.singletons:
               del self.singletons[self.singletons.index(self.ids[target])]
        attribs = {"id" : "P%s" % self.linecount,
                   "source" : self.ids[source],
                   "target" : self.ids[target],
                   "type" : hasattr(l,"linetype") and l.linetype or "fermion"}
        if l.arcthrupoint:
            middle = l.p1.midpoint(l.p2)
            nx = (middle.y() - l.p1.y()) / l.p1.distance(middle)
            if nx:
               bendamount = (l.arcthrupoint.x() - middle.x()) / nx
            else:
               ny = (middle.x() - l.p1.x()) / l.p1.distance(middle)
               bendamount = -(l.arcthrupoint.y() - middle.y()) / ny
            attribs["bend"] = str(bendamount)
        style = ""
        labels = []
        for arr in l.arrows:
            style += "arrow-size:%f; arrow-angle:%f; arrow-constrict:%f; arrow-pos:%f; "%(arr.size/pyx.unit.v_cm,arr.angle,arr.constriction,arr.pos)
        for lab in l.labels:
            if isinstance(lab,LineLabel):
               style += "label-pos:%f; label-displace:%f; label-angle:%f; "%(lab.pos,lab.displace/pyx.unit.v_cm,lab.angle)
               labels.append(lab.text)
            elif isinstance(lab,ParallelArrow):
               style += "parallel-arrow-size:%f; parallel-arrow-angle:%f; parallel-arrow-constrict:%f; parallel-arrow-pos:%f; parallel-arrow-displace:%f; parallel-arrow-sense:%s; "%(lab.size,lab.angle,lab.constriction,lab.pos,lab.displace/pyx.unit.v_cm,lab.sense)
        if style:
            attribs["style"] = style[:-1]
        if labels:
            attribs["label"] = labels[0]
        ele = Element("propagator", attribs)
        self.ids[md5.md5(str((l.p1.xpos,l.p1.ypos,l.p2.xpos,l.p2.ypos,
                              l.arcthrupoint and (l.arcthrupoint.xpos,
                       l.arcthrupoint.ypos)))).hexdigest()] = attribs["id"]
        self.linecount += 1
        return ele, s1, s2

    def pointToXML(self, p):
        """Create FeynML code for a point."""
        attribs = {"id" : "V%s" % self.vertexcount,
                   "x" : str(p.xpos),
                   "y" : str(p.ypos)}
        ele = Element("vertex", attribs)
        self.ids[md5.md5(str((p.xpos, p.ypos))).hexdigest()] = attribs["id"]
        self.singletons.append(attribs["id"])
        self.vertexcount += 1
        return ele

    def decopointToXML(self, p):
        """Create FeynML code for a decorated point."""
        ele = self.pointToXML(p)
        style = ""
        if p.marker is not None:
          style += "mark-shape:%s; mark-size:%s; "%\
                (p.marker.__class__.__name__[:-4].lower(),\
                 hasattr(p.marker,"radius") and p.marker.radius \
                 or (hasattr(p.marker,"size") and p.marker.size)\
                 or 0)
        fills = ""
        for x in p.fillstyles:
            if isinstance(x, pyx.color.rgb):
                fills = fills + " #%02x%02x%02x" % (255 * x.color["r"],
                                                   255 * x.color["g"],
                                                   255 * x.color["b"])
        if fills:
           style += "fill-style:%s; "%fills
        strokes = ""
        for x in p.strokestyles:
            if isinstance(x, pyx.color.rgb): 
                strokes = strokes + " #%02x%02x%02x" % (255 * x.color["r"],
                                                        255 * x.color["g"],
                                                        255 * x.color["b"])
        if strokes:
           style += "line-style:%s;"%strokes
        ele.attrib["style"] = style
        return ele

    def labelToXML(self, l):
        """Create FeynML code for a label."""
        attribs = {"id": "L%s" % self.labelcount,
                   "text": l.text,
                   "x": str(l.x),
                   "y": str(l.y)}
        ele = Element("label", attribs)
        self.ids[md5.md5(str((l.x, l.y, l.text))).hexdigest()] = attribs["id"]
        self.labelcount += 1
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
            raise "FeynML Error: <feynml> must be root element" % self.root.tag
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
                fd.add( self.get_label(element, thedict) )
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
            raise "FeynML Error: invalid attributes for <propagator> element"
        l = NamedLine[thetype](p1, p2)
        if "bend" in element.attrib:
            try:
                l.bend(float(element.attrib["bend"]))
            except:
                raise "FeynML Error: invalid bend amount %s for <propagator> element"%element.attrib["bend"]
        if "style" in element.attrib:
            l = self.apply_layout(element.attrib["style"], l)
        if "label" in element.attrib:
            l = l.addLabel(element.attrib["label"])
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
            sense = element.attrib["sense"]
        except:
            raise Exception("FeynML Error: invalid attribute for <leg> element")
        if sense[:2]=="in" or sense[:8]=="anti-out":
           l = NamedLine[thetype](Point(x, y), p2)
        elif sense[:3]=="out" or sense[:7]=="anti-in":
           l = NamedLine[thetype](p2, Point(x, y))
        else:
            raise Exception("FeynML Error: invalid sense for <leg> element")
        if "style" in element.attrib:
            l = self.apply_layout(element.attrib["style"], l)
        if "label" in element.attrib:
            l = l.addLabel(element.attrib["label"])
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
            if shape=="circle":
               radius = float(element.attrib["radius"])
            else:
               split = element.attrib["radius"].index(" ")
               xradius = float(element.attrib["radius"][:split])
               yradius = float(element.attrib["radius"][split:])
        except:
            raise "FeynML Error: invalid attribute for <blob> element"
        if shape=="circle":
            b = Circle(x=x, y=y, radius=radius)
        elif shape=="ellipse":
            b = Ellipse(x=x, y=y, xradius=xradius, yradius=yradius)
        else:
            raise "FeynML Error: invalid shape attribute for <blob> element"
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
            angle = None
        winds = {"n" : 90,
                 "s" : -90,
                 "e" : 0,
                 "w" : 180,
                 "ne" : 45,
                 "se" : -45,
                 "nw" : 135,
                 "sw" : -135}
        if angle is None:
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

    def get_label(self, element, thedict):
        """Build a free label from its FeynML representation."""
        try:
            x = float(element.attrib["x"])
            y = float(element.attrib["y"])
            text = element.attrib["text"]
        except:
            raise Exception("FeynML Error: invalid attributes for <label> element")
        v = Label(text, x=x, y=y)
        try:
            thedict[element.attrib["id"]] = v
        except:
            raise Exception("FeynML Error: missing id attribute in <label> element")
        return v

    def apply_layout(self, stylestring, obj):
        """Apply the decorators encoded in a style string to an object."""
        styleelements = stylestring.split(";")
        styledict = {}
        for styling in styleelements:
            if styling == "":
               break
            s = styling.split(":")
            styledict[s[0].lstrip().rstrip()] = s[1]
        if (styledict.has_key("mark-shape") or styledict.has_key("mark-size"))\
            and isinstance(obj, DecoratedPoint):
           try:
                marktype = NamedMark[styledict["mark-shape"]]
           except:
                marktype = SQUARE
           try:
                marksize = float(styledict["mark-size"])
           except:
                marksize = 0.075
           obj.setMark(marktype(size=marksize))
        if (styledict.has_key("arrow-size") or styledict.has_key("arrow-angle")
            or styledict.has_key("arrow-constrict")
            or styledict.has_key("arrow-pos")) and isinstance(obj, Line):
           try:
              arrsize = pyx.unit.length(float(styledict["arrow-size"]),unit="cm")
           except:
              arrsize = 6*pyx.unit.v_pt
           try:
              arrangle = float(styledict["arrow-angle"])
           except:
              arrangle = 45
           try:
              arrconstrict = float(styledict["arrow-constrict"])
           except:
              arrconstrict = 0.8
           try:
              arrpos = float(styledict["arrow-pos"])
           except:
              arrpos = 0.5
           obj.addArrow(arrow=Arrow(arrpos,arrsize,arrangle,arrconstrict))
        if (styledict.has_key("parallel-arrow-size")
            or styledict.has_key("parallel-arrow-angle")
            or styledict.has_key("parallel-arrow-constrict")
            or styledict.has_key("parallel-arrow-pos")
            or styledict.has_key("parallel-arrow-length")
            or styledict.has_key("parallel-arrow-displace")
            or styledict.has_key("parallel-arrow-sense")) \
           and isinstance(obj, Line):
           try:
              arrsize = pyx.unit.length(float(styledict["parallel-arrow-size"]),unit="cm")
           except:
              arrsize = 6*pyx.unit.v_pt
           try:
              arrangle = float(styledict["parallel-arrow-angle"])
           except:
              arrangle = 45
           try:
              arrconstrict = float(styledict["parallel-arrow-constrict"])
           except:
              arrconstrict = 0.8
           try:
              arrpos = float(styledict["parallel-arrow-pos"])
           except:
              arrpos = 0.5
           try:
              arrlen = float(styledict["parallel-arrow-length"])
           except:
              arrlen = 0.5*pyx.unit.v_cm
           try:
              arrdisp = float(styledict["parallel-arrow-displace"])
           except:
              arrdisp = 0.3
           try:
              arrsense = int(styledict["parallel-arrow-sense"])
           except:
              arrsense = +1
           obj.addParallelArrow(arrpos, arrdisp, arrlen, arrsize, arrangle,
                                arrconstrict, arrsense)
        if styledict.has_key("is3d") and isinstance(obj, Line):
           fwords = ["0", "no", "false", "f", "off"]
           twords = ["1", "yes", "true", "t", "on"]
           if styledict["is3d"].lstrip().lower() in fwords:
              obj.set3D(False)
           elif styledict["is3d"].lstrip().lower() in twords:
              obj.set3D(True)
        return obj



#####################################################



if __name__ == "__main__":
    import sys
    reader = FeynMLReader(sys.argv[1])
    _f = reader.get_diagram(0)
    _f.draw(sys.argv[1]+".eps")

