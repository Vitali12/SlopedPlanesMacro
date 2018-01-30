# -*- coding: utf8 -*-
# *****************************************************************************
# *                                                                           *
# *    Copyright (c) 2017                                                     *
# *                                                                           *
# *    This program is free software; you can redistribute it and/or modify   *
# *    it under the terms of the GNU Lesser General Public License (LGPL)     *
# *    as published by the Free Software Foundation; either version 2 of      *
# *    the License, or (at your option) any later version.                    *
# *    For detail see the LICENSE text file.                                  *
# *                                                                           *
# *    This program is distributed in the hope that it will be useful,        *
# *    but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.                   *
# *    See the  GNU Library General Public License for more details.          *
# *                                                                           *
# *    You should have received a copy of the GNU Library General Public      *
# *    License along with this program; if not, write to the Free Software    *
# *    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
# *    USA                                                                    *
# *                                                                           *
# *****************************************************************************


from math import pi
import FreeCAD
import Part
from SlopedPlanesPy import _Py
from SlopedPlanesPyWire import _PyWire
from SlopedPlanesPyReflex import _PyReflex
from SlopedPlanesPyAlignment import _PyAlignment
from SlopedPlanesPyPlane import _PyPlane


__title__ = "SlopedPlanes Macro"
__author__ = "Damian Caceres Moreno"
__url__ = "http://www.freecadweb.org"
__version__ = ""


class _PyFace(_Py):

    '''The complementary python object class for the faces resulting
    to apply the FaceMaker to the SlopedPlanes base.
    The faces could have several wires, and as a consequense holes.'''

    def __init__(self, numFace):

        ''''''

        self.numFace = numFace
        self.wires = []
        self.alignments = []
        self.reset = True
        self.shapeGeom = []
        self.size = 0

    @property
    def numFace(self):

        ''''''

        return self._numFace

    @numFace.setter
    def numFace(self, numFace):

        ''''''

        self._numFace = numFace

    @property
    def wires(self):

        ''''''

        return self._wires

    @wires.setter
    def wires(self, wires):

        ''''''

        self._wires = wires

    @property
    def alignments(self):

        ''''''

        return self._alignments

    @alignments.setter
    def alignments(self, alignments):

        ''''''

        self._alignments = alignments

    @property
    def reset(self):

        ''''''

        return self._reset

    @reset.setter
    def reset(self, reset):

        ''''''

        self._reset = reset

    @property
    def shapeGeom(self):

        ''''''

        return self._shapeGeom

    @shapeGeom.setter
    def shapeGeom(self, shapeGeom):

        ''''''

        self._shapeGeom = shapeGeom

    @property
    def size(self):

        ''''''

        return self._size

    @size.setter
    def size(self, size):

        ''''''

        self._size = size

    def __getstate__(self, serialize):

        '''__getstate__(self)
        Serializes the complementary python objects.
        '''

        wireList = []
        for pyWire in self.wires:
            dct = pyWire.__dict__.copy()
            dct['_coordinates'] = [[v.x, v.y, v.z] for v in pyWire.coordinates]
            dct['_shapeGeom'] = []

            if serialize:
                edgeList = []
                forBack = []

            planeList = []
            for pyPlane in pyWire.planes:
                dd = pyPlane.__dict__.copy()

                dd['_shape'] = None
                dd['_bigShape'] = None
                dd['_enormousShape'] = None
                dd['_geom'] = None
                dd['_cutter'] = []
                dd['_simulatedShape'] = None

                dd['_geomAligned'] = None

                dd['_seedShape'] = None
                dd['_seedBigShape'] = None
                dd['_lineInto'] = None

                if serialize:

                    edgeList.append(pyPlane.geomShape)
                    dd['_geomShape'] = None

                    if pyPlane.forward:
                        forBack.extend([pyPlane.forward, pyPlane.backward])
                        dd['_forward'] = 'forward'
                        dd['_backward'] = 'backward'

                else:
                    dd['_geomShape'] = None
                    dd['_geomAligned'] = None
                    dd['_forward'] = None
                    dd['_backward'] = None

                planeList.append(dd)
            dct['_planes'] = planeList

            if serialize:
                ww = Part.Wire(edgeList)
                dct['_shapeGeom'] = ww.exportBrepToString()

                fb = Part.Compound(forBack)
                dct['_forBack'] = fb.exportBrepToString()

            reflexList = []
            for pyReflex in pyWire.reflexs:
                dd = pyReflex.__dict__.copy()
                planes = [[pyPlane.numWire,  pyPlane.numGeom]
                          for pyPlane in pyReflex.planes]
                dd['_planes'] = planes
                reflexList.append(dd)
            dct['_reflexs'] = reflexList

            wireList.append(dct)

        alignList = []
        for pyAlign in self.alignments:
            dct = {}
            alignList.append(dct)

        return wireList, alignList

    def __setstate__(self, wires, alignments, serialize):

        '''__setstate__(self, wires, alignments)
        Deserializes the complementary python objects.
        '''

        geomShapeFace = []
        wireList = []
        numWire = -1
        for dct in wires:
            numWire += 1
            pyWire = _PyWire(numWire)

            planeList = []
            numGeom = -1
            nf = -1
            geomShapeWire = []

            if serialize:
                edgeList = Part.Shape()
                edgeList.importBrepFromString(dct['_shapeGeom'])
                edgeList = edgeList.Edges

                forBack = Part.Shape()
                forBack.importBrepFromString(dct['_forBack'])
                forBack = forBack.Edges

            for dd in dct['_planes']:
                numGeom += 1
                pyPlane = _PyPlane(numWire, numGeom)
                pyPlane.__dict__ = dd

                if serialize:

                    if dd['_forward']:
                        nf += 2

                        pyPlane.forward = forBack[nf-1]
                        pyPlane.backward = forBack[nf]

                    geomShape = edgeList[numGeom]

                    pyPlane.geomShape = geomShape

                    geomShapeWire.append(geomShape)

                planeList.append(pyPlane)
            dct['_planes'] = planeList

            reflexList = []
            for dd in dct['_reflexs']:
                pyReflex = _PyReflex()
                for [numWire, numGeom] in dd['_planes']:
                    pyPlane = planeList[numGeom]
                    pyReflex.addLink('planes', pyPlane)
                dd['_planes'] = pyReflex.planes
                pyReflex.__dict__ = dd
                reflexList.append(pyReflex)
            dct['_reflexs'] = reflexList

            coord = dct['_coordinates']
            coordinates = [FreeCAD.Vector(v) for v in coord]
            dct['_coordinates'] = coordinates

            pyWire.__dict__ = dct

            if serialize:
                pyWire.shapeGeom = geomShapeWire
                geomShapeFace.extend(geomShapeWire)

            wireList.append(pyWire)

        alignList = []
        for dct in alignments:
            pyAlignment = _PyAlignment()
            alignList.append(pyAlignment)

        return wireList, alignList, geomShapeFace

    def parsing(self):

        '''parsing(self)
        Splits the pyFace object finding its reflex corners and alignments.'''

        # print '######### parsing'

        resetFace = self.reset
        # print 'resetFace ', resetFace

        if not resetFace and not self.alignments:
            return

        pyWireList = self.wires

        if resetFace:
            for pyWire in pyWireList:
                pyWire.reflexs = []  # reset reflexs

        elif self.alignments and _Py.slopedPlanes.Proxy.State is False:
            for pyWire in pyWireList:
                for pyReflex in pyWire.reflexs:
                    planeList = []
                    for pyPlane in pyReflex.planes:
                        if pyPlane.aligned:
                            pyPlane = self.selectPlane(pyPlane.numWire,
                                                       pyPlane.numGeom)
                        planeList.append(pyPlane)  # reset reflexs planes
                    pyReflex.planes = planeList

        self.alignments = []  # always reset alignments
        shapeGeomFace = self.shapeGeom

        tolerance = _Py.tolerance

        refList = []

        for pyWire in pyWireList:
            numWire = pyWire.numWire
            # print '###### numWire ', numWire

            ref = False
            pyPrePlane = None

            pyPlaneList = pyWire.planes
            coord = pyWire.coordinates
            eje = coord[1].sub(coord[0])

            for pyPlane in pyPlaneList:
                numGeom = pyPlane.numGeom
                # print '### numGeom ', numGeom, ' angle ', pyPlane.angle

                nextEje = coord[numGeom+2].sub(coord[numGeom+1])
                corner = self.convexReflex(eje, nextEje)
                # print 'corner ', corner
                eje = nextEje

                if not pyPlane.geomAligned:
                    # print 'A'

                    ref = False

                else:
                    # print 'B'

                    if resetFace:
                        # print '0'

                        if [numWire, numGeom] in refList:
                            # print 'refList'
                            self.forBack(pyPrePlane, 'forward')
                            ref = True

                        if ref:
                            # print 'ref'
                            self.forBack(pyPlane, 'backward')
                            forward = pyPlane.forward
                            section = forward.section(shapeGeomFace, tolerance)

                            if section.Edges:
                                # print 'edges'
                                edge = section.Edges[0]

                                edgeStart = edge.firstVertex(True).Point
                                # print 'edgeStart ', edgeStart
                                edgeEnd = edge.lastVertex(True).Point
                                # print 'edgeEnd ', edgeEnd
                                lineStart = coord[numGeom]
                                # print 'lineStart ', lineStart

                                distStart = edgeStart.sub(lineStart).Length
                                distEnd = edgeEnd.sub(lineStart).Length

                                into, lineInto = self.into(lineStart, edgeEnd)

                                if distStart > distEnd and into:
                                    # print 'alignament'
                                    pass

                                else:
                                    # print 'no alignament '
                                    if not into:
                                        if distStart > distEnd:
                                            pyPlane.lineInto = lineInto
                                    self.findRear(pyWire, pyPrePlane, 'forward')
                                    self.findRear(pyWire, pyPlane, 'backward')
                                    self.doReflex(pyWire, pyPrePlane, pyPlane)

                            else:
                                # print 'no alignament'
                                self.findRear(pyWire, pyPrePlane, 'forward')
                                self.findRear(pyWire, pyPlane, 'backward')
                                self.doReflex(pyWire, pyPrePlane, pyPlane)

                            ref = False

                        if corner == 'reflex':

                            self.forBack(pyPlane, 'forward')

                    if corner == 'reflex':
                        # print '1 Reflex: does look for alignments'

                        forward = pyPlane.forward
                        section = forward.section(shapeGeomFace, tolerance)

                        if section.Edges:
                            # print '11 possible alignament'

                            lineEnd = coord[numGeom+1]
                            # print 'lineEnd ', lineEnd

                            numEdge = -1
                            pyPl = pyPlane
                            for edge in section.Edges:
                                numEdge += 1
                                # print '111 edge by edge'

                                edgeStart = edge.firstVertex(True).Point
                                # print 'edgeStart ', edgeStart
                                edgeEnd = edge.lastVertex(True).Point
                                # print 'edgeEnd ', edgeEnd

                                distStart = edgeStart.sub(lineEnd).Length
                                # print 'distStart ', distStart
                                distEnd = edgeEnd.sub(lineEnd).Length
                                # print 'distEnd ', distEnd

                                into, lineInto = self.into(lineEnd, edgeStart)

                                if into:
                                    lineEnd = edgeEnd

                                if distStart < distEnd and into:
                                    # print '1111 aligment'

                                    point = self.roundVector(edgeStart)
                                    (nWire, nGeom) = self.findAlignment(point)
                                    pyW = self.wires[nWire]
                                    pyPl = self.selectPlane(nWire, nGeom)

                                    if pyPl.geomAligned:
                                        # print '11111 has a shape'

                                        if numEdge == 0:
                                            pyAlign =\
                                                self.doAlignment(pyPlane)

                                        fAng = self.findAngle(numWire, numGeom)
                                        sAng = self.findAngle(nWire, nGeom)
                                        fGeom = pyPlane.doGeom()
                                        sGeom = pyPl.doGeom()

                                        # TODO curved

                                        forwardLine = forward.Curve

                                        startParam = fGeom.FirstParameter
                                        endPoint = sGeom.EndPoint
                                        endParam =\
                                            forwardLine.parameter(endPoint)
                                        eGeom =\
                                            Part.LineSegment(fGeom,
                                                             startParam,
                                                             endParam)
                                        eGeomShape = eGeom.toShape()

                                        if fAng == sAng:
                                            # print '111111 alignment'
                                            pyPl.geomAligned = None
                                            pyPl.angle = [numWire, numGeom]

                                            pyPlane.geomAligned = eGeomShape

                                        else:
                                            # print '111112 falseAlignment'
                                            if numEdge > 0:
                                                pyAlign =\
                                                    self.doAlignment(pyPlane)
                                            pyAlign.falsify = True

                                        pyAlign.geomAligned = eGeomShape

                                        pyAli =\
                                            self.seatAlignment(pyAlign,
                                                               pyWire, pyPlane,
                                                               pyW, pyPl)

                                        if pyAli:
                                            # print 'break other alignament'
                                            ref = False
                                            break

                                        if pyAlign.falsify:
                                            # print 'break false alignament'
                                            ref = False
                                            break

                                elif not into:
                                    # print '1112 interference'
                                    ref = True
                                    if distStart < distEnd:
                                        pyPl.lineInto = lineInto
                                    break

                                else:
                                    # print '1113 confront directions'
                                    if resetFace:
                                        # print '11131'
                                        if corner == 'reflex':
                                            # print '111311'

                                            if ref:
                                                # print 'ref'
                                                self.findRear(pyWire, pyPlane,
                                                              'backward')
                                                self.findRear(pyWire, pyPlane,
                                                              'forward')

                                            ref = True

                                        break

                            else:
                                # print 'end alignment'
                                if resetFace:

                                    nn = pyPl.numGeom
                                    lenW = len(pyW.planes)
                                    num = self.sliceIndex(nn+1, lenW)
                                    coo = pyW.coordinates
                                    jj = coo[num].sub(coo[nn])
                                    nnjj = coo[num+1].sub(coo[num])
                                    corner = self.convexReflex(jj, nnjj)

                                    if corner == 'reflex':
                                        # print 'reflex'
                                        refList.append([pyW.numWire, num])
                                        # print 'refList ', refList

                                    ref = False

                        else:
                            # print '12 no alignment'
                            if resetFace:
                                # print '121'
                                if corner == 'reflex':
                                    # print '1211 reflexed'
                                    ref = True

                    else:
                        # print '2 Convex: does not look for alignments'
                        pass

                pyPrePlane = pyPlane

                # print 'reflex ', pyWire.reflexs
                # print 'alignments ', self.alignments

            if resetFace:
                if numWire > 0:
                    # print 'firstPlane'

                    firstPlane = pyPlaneList[0]

                    if not firstPlane.aligned:
                        # print 'firstPlane no aligned'
                        self.doReflex(pyWire, pyPlane, firstPlane)

                    else:

                        if not pyPlane.choped:
                            # print 'pyPlane no choped'
                            self.doReflex(pyWire, pyPlane, firstPlane)

                        else:
                            pyAlignmentList = self.selectAllAlignment(numWire, numGeom)
                            pyAlignment = self.selectAlignment(numWire, 0)
                            if pyAlignment not in pyAlignmentList:
                                # print 'pyPlane no chop of firstPlane'
                                self.doReflex(pyWire, pyPlane, firstPlane)

            pyWire.reset = False

        self.priorLaterAlignments()

        # self.printSummary()

    def into(self, pointOne, pointTwo):

        ''''''

        tolerance = _Py.tolerance
        into = False
        face = self.face
        lineInto = Part.LineSegment(pointOne, pointTwo)
        lIS = lineInto.toShape()
        sect = face.section([lIS], tolerance)
        if sect.Edges:
            if len(sect.Vertexes) == 2:
                into = True

        return into, lIS

    def seatAlignment(self, pyAlign, pyWire, pyPlane, pyW, pyPl):

        '''seatAlignment(self, pyAlign, pyWire, pyPlane, pyW, pyPl)
        pyAlign is the alignment.
        pyPlane is the base plane. pyWire is its wire.
        pyPl is the continued plane. pyW is its wire.
        If pyAlign finds other alignment return it, pyAli, or return None.
        '''

        numWire = pyWire.numWire
        numGeom = pyPlane.numGeom
        # print 'pyPlane ', (numWire, numGeom)
        nWire = pyW.numWire
        nGeom = pyPl.numGeom
        # print 'pyPl ', (nWire, nGeom)

        alignList = pyAlign.aligns
        chopList = pyAlign.chops

        # chop one

        jumpChop = False
        if pyAlign.falsify:
            if pyPlane.aligned:
                pyAliBase = self.selectAlignmentBase(numWire, numGeom)

                if pyAliBase:
                    # finds an alignment backward
                    if not pyAliBase.falsify:
                        jumpChop = True
                        pp = pyAliBase.aligns[-1]
                        numWireChopOne = pp.numWire
                        pyw = self.wires[numWireChopOne]
                        lenWire = len(pyw.planes)
                        numGeomChopOne = self.sliceIndex(pp.numGeom+1, lenWire)

        if not jumpChop:

            lenWire = len(pyWire.planes)
            if alignList:
                num = alignList[-1].numGeom
                numGeomChopOne = self.sliceIndex(num+1, lenWire)
                numWireChopOne = alignList[-1].numWire
            else:
                numGeomChopOne = self.sliceIndex(numGeom+1, lenWire)
                numWireChopOne = numWire

        # aligns

        alignList.append(pyPl)

        if pyAlign.falsify:
            pyAli = None
        else:
            pyPl.shape = None
            pyAli = self.selectAlignmentBase(nWire, nGeom)
            if pyAli:
                # finds an alignment forward
                if not pyAli.falsify:
                    bL = pyAli.aligns
                    alignList.extend(bL)
                    for b in bL:
                        b.angle = [numWire, numGeom]

        pyAlign.aligns = alignList

        # chop two

        pyWireList = self.wires
        if numWire == nWire:
            numGeomChopTwo = self.sliceIndex(nGeom-1, lenWire)
        else:
            lenW = len(pyWireList[nWire].planes)
            numGeomChopTwo = self.sliceIndex(nGeom-1, lenW)

        # chops

        pyOne = self.selectPlane(numWireChopOne, numGeomChopOne)
        pyTwo = self.selectPlane(nWire, numGeomChopTwo)

        chopList.append([pyOne, pyTwo])

        if pyAli:
            if not pyAli.falsify:
                dL = pyAli.chops
                chopList.extend(dL)
                self.removeAlignment(pyAli)  # joined in one alignment

        pyAlign.chops = chopList

        if self.reset:

            self.forBack(pyOne, 'backward')
            self.findRear(pyWireList[numWireChopOne], pyOne, 'backward')

            self.forBack(pyTwo, 'forward')
            self.findRear(pyW, pyTwo, 'forward')

            pyPlane.reflexed = True
            pyPlane.aligned = True
            pyPl.reflexed = True
            pyPl.aligned = True

            pyOne.reflexed = True
            pyOne.choped = True
            pyTwo.reflexed = True
            pyTwo.choped = True

        return pyAli

    def findRear(self, pyWire, pyPlane, direction):

        '''findRear(self, pyWire, pyPlane, direction)
        Finds the rear plane of a reflexed plane.
        Determines if an arrow situacion happens.'''

        tolerance = _Py.tolerance
        shapeGeomWire = pyWire.shapeGeom
        sGW = Part.Wire(shapeGeomWire)
        numWire = pyWire.numWire
        lenWire = len(pyWire.planes)
        numGeom = pyPlane.numGeom

        lineShape = pyPlane.forward
        section = lineShape.section([sGW], tolerance)
        # print 'section.Edges ', section.Edges
        # print 'section.Vertexes ', section.Vertexes
        # print[v.Point for v in section.Vertexes]

        if len(section.Vertexes) == 1:
            return

        edge = False

        if pyPlane.lineInto:
            # print 'a'

            section = pyPlane.lineInto.section([sGW], tolerance)
            vertex = section.Vertexes[1]

        elif section.Edges:
            # print 'b'

            edge = True

            if direction == 'forward':
                # print 'b1'
                vertex = section.Edges[0].Vertexes[0]

            else:
                # print 'b2'
                vertex = section.Edges[-1].Vertexes[1]

        else:
            # print 'c'
            vertex = section.Vertexes[1]
            # esto tal vez necesita ser mas completo con into
            # no esta debidamente probado
            if len(section.Vertexes) > 2:
                edge = True

        # print vertex.Point
        # print edge

        coord = pyWire.coordinates

        try:

            nGeom = coord.index(self.roundVector(vertex.Point))
            # print 'on vertex'

            if edge:
                if direction == 'forward':
                    # print 'aa'
                    nGeom = self.sliceIndex(nGeom-1, lenWire)

            else:
                if direction == 'backward':
                    # print 'bb'
                    nGeom = self.sliceIndex(nGeom-1, lenWire)

        except ValueError:
            # print 'not in vertex (edge False)'

            nGeom = -1
            for geomShape in shapeGeomWire:
                nGeom += 1
                sect = vertex.section([geomShape], _Py.tolerance)
                if sect.Vertexes:
                    break

        # print 'nGeom ', nGeom
        pyPlane.addValue('rear', nGeom, direction)

        # arrow

        if direction == 'forward':
            endNum = self.sliceIndex(numGeom+2, lenWire)
        else:
            endNum = self.sliceIndex(numGeom-2, lenWire)

        if nGeom == endNum:
            pyPl = self.selectPlane(numWire, endNum)
            pyPl.arrow = True

    def findAngle(self, numWire, numGeom):

        '''findAngle(self, nW, nG)
        '''

        angle = self.wires[numWire].planes[numGeom].angle

        if isinstance(angle, list):
            angle = self.findAngle(angle[0], angle[1])

        return angle

    def findAlignment(self, point):

        '''findAlignment(self, point)
        '''

        for pyWire in self.wires:
            numWire = pyWire.numWire
            coordinates = pyWire.coordinates
            try:
                numGeom = coordinates.index(point)
                break
            except ValueError:
                pass

        return (numWire, numGeom)

    def removeAlignment(self, pyAlign):

        '''removeAlignment(self, pyAlign)
        '''

        pyAlignList = self.alignments
        pyAlignList.remove(pyAlign)
        self.alignments = pyAlignList

    def forBack(self, pyPlane, direction):

        '''forBack(self, pyPlane, direction)
        '''

        geom = pyPlane.geom
        firstParam = geom.FirstParameter
        lastParam = geom.LastParameter

        if isinstance(geom, (Part.LineSegment,
                             Part.ArcOfParabola)):

            startParam = lastParam
            endParam = lastParam + _Py.size

            gg = geom
            sParam = firstParam
            eParam = firstParam - _Py.size

        elif isinstance(geom, (Part.ArcOfCircle,
                               Part.ArcOfEllipse)):

            half = (2 * pi - (lastParam - firstParam)) / 2
            startParam = lastParam
            endParam = lastParam + half

            gg = geom.copy()
            gg.Axis = _Py.normal * -1
            sParam = 2 * pi - firstParam
            eParam = sParam + half

        elif isinstance(geom, Part.ArcOfHyperbola):
            pass

        elif isinstance(geom, Part.BSplineCurve):
            pass

        else:
            pass

        forwardLine = self.makeGeom(geom, startParam, endParam)
        # print'forwardLine ', forwardLine
        forwardLineShape = forwardLine.toShape()
        backwardLine = self.makeGeom(gg, sParam, eParam)
        # print'backwardLine ', backwardLine
        backwardLineShape = backwardLine.toShape()

        if direction == "forward":
            # print 'a'
            pyPlane.backward = backwardLineShape
            pyPlane.forward = forwardLineShape

        else:
            # print 'b'
            pyPlane.backward = forwardLineShape
            pyPlane.forward = backwardLineShape

    def doReflex(self, pyWire, pyPlane, pyPl):

        '''doReflex(self, pyWire, pyPlane, pyPl)
        '''

        pyPlane.reflexed = True
        pyPl.reflexed = True
        pyReflex = _PyReflex()
        pyWire.addLink('reflexs', pyReflex)
        # print '¡¡¡ reflex done !!!'
        pyReflex.addLink('planes', pyPlane)
        pyReflex.addLink('planes', pyPl)

    def doAlignment(self, pyPlane):

        '''doAlignment(self, pyPlane)
        '''

        pyAlign = _PyAlignment()
        self.addLink('alignments', pyAlign)
        # print '¡¡¡ alignment done !!!'
        pyAlign.base = pyPlane

        return pyAlign

    def priorLaterAlignments(self):

        '''priorLaterAlignments(self)
        '''

        pyWireList = self.wires

        for pyAlign in self.alignments:

            pyBase = pyAlign.base
            numWire = pyBase.numWire
            numGeom = pyBase.numGeom
            pyWire = pyWireList[numWire]
            pyPlaneList = pyWire.planes
            lenWire = len(pyPlaneList)

            prior = self.sliceIndex(numGeom-1, lenWire)
            pyPrior = self.selectBasePlane(numWire, prior)

            pyPl = pyAlign.aligns[-1]
            [nW, nG] = [pyPl.numWire, pyPl.numGeom]
            pyW = pyWireList[nW]
            lenW = len(pyW.planes)

            later = self.sliceIndex(nG+1, lenW)
            pyLater = self.selectBasePlane(nW, later)

            pyAlign.prior = pyPrior
            pyAlign.later = pyLater

    def planning(self):

        '''planning(self)
        Transfers to PyWire.
        Arranges the alignment ranges.
        Rearmes the face reset system.'''

        # print '######### planning'

        for pyWire in self.wires:
            pyWire.planning()

        for pyAlign in self.alignments:
            if self.reset:
                pyAlign.rangging()
            pyAlign.ranggingChop()

        self.reset = False

        self.printSummary()

    def upping(self):

        '''upping(self)
        '''

        # print '######### upping'

        if _Py.slopedPlanes.Up:

            planeList = []
            for pyWire in self.wires:
                for pyPlane in pyWire.planes:
                    plane = pyPlane.shape
                    if plane:
                        planeList.append(plane)

            compound = Part.makeCompound(planeList)
            boundBox = compound.BoundBox
            diaLen = boundBox.DiagonalLength
            center = boundBox.Center
            upPlane = Part.makePlane(diaLen, diaLen,
                                     center.sub(FreeCAD.Vector(diaLen/2,
                                                               diaLen/2,
                                                               center.z)))

            up = _Py.slopedPlanes.Up
            if _Py.reverse:
                up = -1 * up
            upPlane.Placement.Base.z = up

            upList = _Py.upList
            upList.append(upPlane)
            _Py.upList = upList

            for pyWire in self.wires:
                for pyPlane in pyWire.planes:
                    plane = pyPlane.shape
                    if plane:
                        gS = pyPlane.geomShape
                        plane = self.cutting(plane, [upPlane], gS)
                        pyPlane.shape = plane

    def virtualizing(self):

        '''virtualizing(self)
        Transfers to PyWire and PyAlignment.
        '''

        # print '######### virtualizing'

        for pyWire in self.wires:
            pyWire.virtualizing()

        for pyAlign in self.alignments:
            pyAlign.virtualizing()

    def trimming(self):

        '''trimming(self)
        Transfers to PyWire and PyAlignment.
        '''

        # print '######### trimming'

        for pyWire in self.wires:
            pyWire.trimming()
        # self.printControl('trimming reflexs')

        for pyAlign in self.alignments:
            pyAlign.trimming()
        # self.printControl('trimming alignments')

    def priorLater(self):

        '''priorLater(self)
        Transfers to PyWire and PyAlignment.
        '''

        # print '######### priorLater'

        for pyWire in self.wires:
            pyWire.priorLater()
        # self.printControl('priorLater wires')

        for pyAlign in self.alignments:
            pyAlign.priorLater()
        # self.printControl('priorLater alignments')

    def simulating(self):

        '''simulating(self)
        Transfers to PyWire and PyAlignment.
        '''

        # print '######### simulating'

        for pyWire in self.wires:
            pyWire.simulating()

        for pyAlign in self.alignments:
            pyAlign.simulatingChops()

        for pyAlign in self.alignments:
            pyAlign.simulatingAlignment()

        #self.printControl('simulating')

    def reflexing(self):

        '''reflexing(self)
        Transfers to PyWire.
        '''

        # print '######### reflexing'

        for pyWire in self.wires:
            if pyWire.reflexs:
                pyWire.reflexing()
        #self.printControl('reflexing')

    def ordinaries(self):

        '''ordinaries(self)
        Transfers to PyWire.
        '''

        # print '######### ordinaries'

        for pyWire in self.wires:
            pyWire.ordinaries()
        self.printControl('ordinaries')

    def betweenWires(self):

        '''betweenWires(self)
        '''

        print '######### betweenWires'

        pyWireList = self.wires
        if len(pyWireList) > 1:

            tolerance = self.tolerance

            alignments = self.alignments
            aliList = []
            for ali in alignments:
                aliList.extend(ali.simulatedAlignment)
            print 'aliList ', aliList

            chopFace = []
            cutterFace = []
            for pyW in pyWireList:
                print '### nW', pyW.numWire
                chopList = []
                cutterList = []
                pyPlaneList = pyW.planes
                for pyPl in pyPlaneList:
                    if pyPl.shape:
                        print '# nG ', pyPl.numGeom, pyPl.fronted
                        if not pyPl.choped and not pyPl.fronted and not pyPl.aligned:
                            print 'a'
                            pl = pyPl.shape
                            cutterList.append(pl)
                        elif pyPl.choped:
                            print 'b'
                            pl = pyPl.simulatedShape
                            chopList.append(pl)

                chopFace.append(chopList)
                cutterFace.append(cutterList)

            print 'cutterFace ', cutterFace

            numWire = -1
            for pyWire in pyWireList:
                numWire += 1
                print '### numWire ', numWire

                pop = cutterFace.pop(numWire)
                cutterList = []
                for cL in cutterFace:
                    cutterList.extend(cL)
                cutterFace.insert(numWire, pop)
                print 'cutterList ', cutterList

                pop = chopFace.pop(numWire)
                chopList = []
                for cL in chopFace:
                    chopList.extend(cL)
                chopFace.insert(numWire, pop)
                print 'chopList ', chopList

                for pyPlane in pyWire.planes:
                    cutList = cutterList[:]
                    plane = pyPlane.shape
                    if plane:
                        print '# numGeom ', pyPlane.numGeom
                        gS = pyPlane.geomShape

                        if pyPlane.fronted:
                            print '0'
                            pass

                        elif pyPlane.choped:
                            print 'A'
                            aList = alignments[:]
                            print 'aList ', aList
                            pyAlignList = self.selectAllAlignment(numWire, pyPlane.numGeom)
                            print 'pyAlignList ', pyAlignList
                            baseList = []
                            for pyA in pyAlignList:
                                aList.remove(pyA)
                                baseList.append(pyA.base.enormousShape)

                            aL = []
                            print 'aList ', aList
                            for aa in aList:
                                sim = aa.base.shape.copy()
                                geomShape = aa.geomAligned
                                sim = self.cutting(sim, baseList, geomShape)
                                aL.append(sim)
                            print 'aL ', aL
                            cutList.extend(aL)

                        elif pyPlane.aligned:
                            print 'B'
                            pyAlign = self.selectAlignmentBase(numWire, pyPlane.numGeom)
                            line = pyAlign.geomAligned
                            simulAlign = Part.makeShell(pyAlign.simulatedAlignment)
                            aList = alignments[:]
                            aList.remove(pyAlign)
                            aL = []
                            for pyA in aList:
                                ll = pyA.geomAligned
                                section = line.section([ll], tolerance)
                                if not section.Vertexes:
                                    simulA = Part.makeShell(pyA.simulatedAlignment)
                                    common = simulAlign.common([simulA], tolerance)
                                    if not common.Area:
                                        aL.extend(pyA.simulatedAlignment)
                            cutList.extend(aL)

                        else:
                            print 'C'
                            cutList.extend(aliList)
                            cutList.extend(chopList)

                        if cutList:

                            print 'cutList ', cutList

                            if isinstance(plane, Part.Compound):
                                print '1'

                                # esto hay que revisarlo
                                if len(plane.Faces) > 1:
                                    print '11'

                                    fList = []
                                    for ff in plane.Faces:
                                        ff = ff.cut(cutList, tolerance)
                                        fList.append(ff.Faces[0])   # esto hay que cambiarlo
                                    compound = Part.makeCompound(fList)
                                    pyPlane.shape = compound

                                else:
                                    print '12'

                                    plane = plane.cut(cutList, tolerance)
                                    fList = []
                                    ff = self.cutting(plane, cutList, gS)
                                    fList.append(ff)
                                    if pyPlane.rear:
                                        plane = plane.removeShape([ff])
                                        for ff in plane.Faces:
                                            section = ff.section(fList, tolerance)
                                            if not section.Edges:
                                                fList.append(ff)
                                                break
                                    compound = Part.makeCompound(fList)
                                    pyPlane.shape = compound

                            else:
                                print '2'
                                plane = self.cutting(plane, cutList, gS)
                                pyPlane.shape = plane

                            print 'SHAPE ', pyPlane.shape

    def aligning(self):

        '''aligning(self)
        Transfers to PyAlignment.
        '''

        # print '######### aligning'

        pyAlignList = self.alignments

        for pyAlign in pyAlignList:
            pyAlign.aligning()

    def end(self):

        '''end(self)
        
        Transfers to PyAlignment.
        '''

        # print '######### end'

        # recolects

        tolerance = _Py.tolerance
        pyWireList = self.wires

        chopList = []
        frontedList = []
        numList = []
        for pyAlign in self.alignments:
            rangoChop = pyAlign.rango

            pyBase = pyAlign.base
            base = pyBase.shape
            aligns = pyAlign.aligns[:]

            ch = []
            front = [base]
            nList = [pyBase.numGeom]
            numChop = -1
            for [pyOne, pyTwo] in pyAlign.chops:
                numChop += 1

                pyPl = aligns[numChop]
                pl = pyPl.shape
                if pl:
                    front.append(pl)
                    nList.append(pyPl.numGeom)

                one = pyOne.shape
                two = pyTwo.shape

                rChop = rangoChop[numChop]
                if rChop:
                    pyPlaneList = pyWireList[pyOne.numWire].planes
                    for nn in rChop:
                        pyPl = pyPlaneList[nn]
                        if not pyPl.choped and not pyPl.aligned:
                            pl = pyPl.shape.copy()
                            gS = pyPl.geomShape
                            ch.append(pl)
                            pl = self.cutting(pl, [one, two], gS)
                            front.append(pl)
                            nList.append(nn)

            chopList.append(ch)
            frontedList.append(front)
            numList.append(nList)

        # print 'chopList ', chopList
        # print 'frontedList ', frontedList
        # print 'numList ', numList

        # other rChops cutted by chops: frontedList
        # alignments with contact
        # alignments without section between lines
        # alignments without common area
        # cutted base, aligns, chops and rChop

        pyAlignList = self.alignments[:]

        number = -1
        for pyAlign in self.alignments:
            number += 1

            pyBase = pyAlign.base
            # print '###### pyAlign.base ', (pyBase.numWire, pyBase.numGeom)
            base = pyBase.shape
            gS = pyBase.geomShape

            simulatedAlign = Part.makeShell(pyAlign.simulatedAlignment)
            line = pyAlign.geomAligned

            rangoChop = pyAlign.rango

            num = -1
            for pyAl in pyAlignList:
                num += 1
                if number != num:

                    simulAl = Part.makeShell(pyAl.simulatedAlignment)
                    ll = pyAl.geomAligned

                    section = simulatedAlign.section(simulAl, tolerance)
                    if section.Edges:

                        section = line.section([ll], tolerance)
                        if not section.Vertexes:

                            common = simulatedAlign.common(simulAl, tolerance)
                            # print 'area ', (pyAlign.base.numGeom, common.Area)
                            if not common.Area:

                                # print '### pyAl ', (pyAl.base.numWire, pyAl.base.numGeom)

                                cutterList = frontedList[num]
                                nList = numList[num]
                                if cutterList:
                                    # print 'cutterList ', cutterList
                                    # print 'nList ', nList

                                    if pyBase.numGeom not in nList:

                                        base = self.cutting(base, cutterList, gS)
                                        pyBase.shape = base
                                        # print 'base ', base

                                        for pyPlane in pyAlign.aligns:
                                            plane = pyPlane.shape
                                            if plane:
                                                gS = pyPlane.geomShape
                                                plane = self.cutting(plane, cutterList, gS)
                                                pyPlane.shape = plane
                                                # print 'align ', plane

                                    rangoChop = pyAlign.rango
                                    numChop = -1
                                    for [pyOne, pyTwo] in pyAlign.chops:
                                        numChop += 1

                                        one = pyOne.shape
                                        gS = pyOne.geomShape
                                        one = self.cutting(one, cutterList, gS)
                                        pyOne.shape = one
                                        # print 'one ', one

                                        two = pyTwo.shape
                                        gS = pyTwo.geomShape
                                        two = self.cutting(two, cutterList, gS)
                                        pyTwo.shape = two
                                        # print 'two ', two

                                        pyPlaneList = pyWireList[pyOne.numWire].planes

                                        rChop = rangoChop[numChop]
                                        # print 'rChop ', rChop
                                        if rChop:
                                            for nn in rChop:
                                                if nn not in nList:
                                                    pyPl = pyPlaneList[nn]
                                                    if not pyPl.aligned and not pyPl.choped:
                                                        pl = pyPl.shape
                                                        if pl:
                                                            gS = pyPl.geomShape
                                                            pl = self.cutting(pl, cutterList, gS)
                                                            pyPl.shape = pl
                                                            # print 'rango chop ', (nn, pl)

        # other rChops no cutted by chops: chopList
        # alignments with contact
        # alignments without common area
        # cutted chops, and rChop including chops

        number = -1
        for pyAlign in self.alignments:
            number += 1
            simulatedAlign = Part.makeShell(pyAlign.simulatedAlignment)

            rangoChop = pyAlign.rango
            num = -1
            for pyAl in pyAlignList:
                num += 1
                if number != num:

                    simulAl = Part.makeShell(pyAl.simulatedAlignment)

                    section = simulatedAlign.section(simulAl, tolerance)
                    if section.Edges:

                        common = simulatedAlign.common(simulAl, tolerance)
                        if not common.Area:

                            cutterList = chopList[num]
                            cutList = cutterList[:]
                            nList = numList[num]
                            for [pyOne, pyTwo] in pyAl.chops:
                                cutterList.extend([pyOne.shape, pyTwo.shape])

                            # print 'cutList ', cutList
                            # print 'cutterList ', cutterList

                            rangoChop = pyAlign.rango
                            numChop = -1
                            for [pyOne, pyTwo] in pyAlign.chops:
                                numChop += 1

                                one = pyOne.shape
                                gS = pyOne.geomShape
                                one = self.cutting(one, cutList, gS)
                                pyOne.shape = one

                                two = pyTwo.shape
                                gS = pyTwo.geomShape
                                two = self.cutting(two, cutList, gS)
                                pyTwo.shape = two

                                pyPlaneList = pyWireList[pyOne.numWire].planes

                                rChop = rangoChop[numChop]
                                if rChop:
                                    for nn in rChop:
                                        if nn not in nList:
                                            pyPl = pyPlaneList[nn]
                                            if not pyPl.aligned and not pyPl.choped:
                                                pl = pyPl.shape
                                                if pl:
                                                    gS = pyPl.geomShape
                                                    pl = self.cutting(pl, cutterList, gS)
                                                    pyPl.shape = pl
                                                    # print 'rango chop ', (nn, pl)



        for pyAlign in pyAlignList:
            pyAlign.end()
