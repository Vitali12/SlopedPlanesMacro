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


# import rpdb2
import os
import math
import FreeCAD
import FreeCADGui
import Part
import SlopedPlanesUtils as utils
from SlopedPlanesPy import _Py
from SlopedPlanesPyFace import _PyFace
from SlopedPlanesPyWire import _PyWire
from SlopedPlanesPyPlane import _PyPlane
from SlopedPlanesTaskPanel import _TaskPanel_SlopedPlanes


__title__ = "SlopedPlanes Macro"
__author__ = "Damian Caceres Moreno"
__url__ = "http://www.freecadweb.org"


# rpdb2.start_embedded_debugger("test")


def makeSlopedPlanes(sketch):

    ''''''

    if sketch.TypeId != "Sketcher::SketchObject":
        return

    slopedPlanes =\
        FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "SlopedPlanes")
    _SlopedPlanes(slopedPlanes)
    _ViewProvider_SlopedPlanes(slopedPlanes.ViewObject)
    slopedPlanes.Base = sketch

    return slopedPlanes


class _SlopedPlanes():

    ''''''

    def __init__(self, slopedPlanes):

        ''''''

        slopedPlanes.addProperty("App::PropertyLink", "Base",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyBool", "Complement",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyBool", "Reverse",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyBool", "Simmetry",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyBool", "Solid",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyBool", "Down",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyFloat", "Up",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyFloat", "SlopeGlobal",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyFloat", "FactorLength",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyFloat", "FactorWidth",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyPrecision", "Tolerance",
                                 "SlopedPlanes")
        slopedPlanes.addProperty("App::PropertyEnumeration", "FaceMaker",
                                 "SlopedPlanes")

        self.State = False

        slopedPlanes.SlopeGlobal = 45.0
        slopedPlanes.FactorWidth = 1
        slopedPlanes.FactorLength = 2
        slopedPlanes.Up = 0
        slopedPlanes.FaceMaker = ["Part::FaceMakerBullseye",
                                  "Part::FaceMakerSimple",
                                  "Part::FaceMakerCheese"]
        slopedPlanes.Tolerance = (1e-7, 1e-7, 1, 1e-7)

        slopedPlanes.Proxy = self
        self.Type = "SlopedPlanes"
        self.Pyth = []

    def execute(self, slopedPlanes):

        ''''''

        sketch = slopedPlanes.Base
        shape = sketch.Shape.copy()
        sketchBase = sketch.Placement.Base
        sketchAxis = sketch.Placement.Rotation.Axis
        sketchAngle = sketch.Placement.Rotation.Angle
        shape.Placement = FreeCAD.Placement()

        tolerance = slopedPlanes.Tolerance
        _Py.tolerance = slopedPlanes.Tolerance
        _Py.reverse = slopedPlanes.Reverse
        slope = slopedPlanes.SlopeGlobal
        width = slopedPlanes.FactorWidth
        length = slopedPlanes.FactorLength
        faceMaker = slopedPlanes.FaceMaker

        face = Part.makeFace(shape, faceMaker)

        fList = face.Faces
        normal = utils.faceNormal(fList[0])
        _Py.normal = normal

        fFaceOuter = []
        coordinatesOuter = []
        for face in fList:
            outerWire = face.OuterWire
            falseFace = Part.makeFace(outerWire, "Part::FaceMakerSimple")
            fFaceOuter.append(falseFace)
            coordinates = utils.faceDatas(falseFace)[1]
            coordinates.extend(coordinates[0:2])
            coordinatesOuter.append(coordinates)

        lowerLeftFaces = [cc[0] for cc in coordinatesOuter]
        faceList = []
        falseFaceOuter = []
        coordinatesOuterOrdered = []
        while lowerLeftFaces:
            index = utils.lowerLeftPoint(lowerLeftFaces)
            lowerLeftFaces.pop(index)
            pop = coordinatesOuter.pop(index)
            coordinatesOuterOrdered.append(pop)
            pop = fList.pop(index)
            faceList.append(pop)
            pop = fFaceOuter.pop(index)
            falseFaceOuter.append(pop)

        pyFaceListOld = self.Pyth
        pyFaceListNew = []
        numFace = -1
        for face in faceList:
            numFace += 1
            size = face.BoundBox.DiagonalLength
            _Py.size = size
            _Py.face = face
            coordinatesOuter = coordinatesOuterOrdered[numFace]
            for pyFace in pyFaceListOld:
                oldCoord = pyFace.wires[0].coordinates
                if oldCoord[0] == coordinatesOuter[0]:
                    pyFaceListNew.append(pyFace)
                    pyFace.numFace = numFace
                    break
            else:
                pyFace = _PyFace(numFace)
                pyFaceListNew.append(pyFace)

            _Py.pyFace = pyFace

            wList = face.Wires[1:]
            coordinatesInner = []
            fFaceList = []
            for wire in wList:
                falseFace = Part.makeFace(wire, "Part::FaceMakerSimple")
                fFaceList.append(falseFace)
                coord = utils.faceDatas(falseFace)[1]
                coord.extend(coord[0:2])
                coordinatesInner.append(coord)

            lowerLeftInner = [cc[0] for cc in coordinatesInner]
            wireList = []
            falseFaceList = []
            coordinatesInnerOrdered = []
            while lowerLeftInner:
                index = utils.lowerLeftPoint(lowerLeftInner)
                lowerLeftInner.pop(index)
                pop = coordinatesInner.pop(index)
                coordinatesInnerOrdered.append(pop)
                wireList.append(wList[index])
                pop = fFaceList.pop(index)
                falseFaceList.append(pop)

            wireList.insert(0, face.OuterWire)
            falseFaceList.insert(0, falseFaceOuter[numFace])

            coordinates = [coordinatesOuter]
            if coordinatesInnerOrdered:
                coordinates.extend(coordinatesInnerOrdered)

            pyWireListOld = pyFace.wires
            pyWireListNew = []

            numWire = -1
            for wire in wireList:
                numWire += 1
                coo = coordinates[numWire]
                brea = False
                for pyWire in pyWireListOld:
                    oldCoo = pyWire.coordinates
                    if oldCoo[0] == coo[0]:
                        brea = True
                        if oldCoo != coo:
                            pyFace.reset = True
                            if len(oldCoo) != len(coo):
                                pyWire.reset = True
                        if brea:
                            pyWireListNew.append(pyWire)
                            pyWire.numWire = numWire
                            break
                else:
                    pyWire = _PyWire(numWire)
                    pyWireListNew.append(pyWire)
                    pyWire.reset = True
                    pyFace.reset = True

                pyWire.coordinates = coo

                falseFace = falseFaceList[numWire]
                geomWire = utils.arcGeometries(falseFace, coo[:-2])

                pyPlaneListOld = pyWire.planes
                pyPlaneListNew = []
                geomShapeWire = []
                numGeom = -1
                for geom in geomWire:
                    numGeom += 1
                    try:
                        pyPlane = pyPlaneListOld[numGeom]
                        pyPlaneListNew.append(pyPlane)
                        pyPlane.numGeom = numGeom
                        if pyWire.reset:
                            pyPlane.angle = slope
                            pyPlane.width = [width, width]
                            pyPlane.length = length
                    except IndexError:
                        pyPlane = _PyPlane(numWire, numGeom)
                        pyPlaneListNew.append(pyPlane)

                    pyPlane.geom = geom
                    pyPlane.geomAligned = geom
                    geomShapeWire.append(geom.toShape())

                pyWire.planes = pyPlaneListNew
                pyWire.shapeGeom = geomShapeWire

            pyFace.wires = pyWireListNew

            pyFace.parsing()

            pyFace.planning()

            if slopedPlanes.Up:
                pass

            pyFace.trimming()

            pyFace.priorLater()

            pyFace.simulating()

            pyFace.reflexing()

            pyFace.reviewing()

            pyFace.rearing()

            pyFace.ordinaries()

            pyFace.between()

            pyFace.aligning()

            pyFace.ending()

        self.Pyth = pyFaceListNew

        shellList = []
        for pyFace in pyFaceListNew:
            planeList, secondaries = [], []
            originList = []
            pyWireList = pyFace.wires
            for pyWire in pyWireList:
                numWire = pyWire.numWire
                # print 'numWire ', numWire
                for pyPlane in pyWire.planes:
                    numAngle = pyPlane.numGeom
                    angle = pyPlane.angle
                    # print '(numAngle, angle) ', (numAngle, angle)
                    # print pyPlane.shape
                    if [numWire, numAngle] not in originList:

                        if isinstance(angle, float):
                            # print 'a'

                            plane = pyPlane.shape
                            if isinstance(plane, Part.Compound):
                                # print 'a1'
                                planeList.append(plane.Faces[0])
                                secondaries.extend(plane.Faces[1:])
                            else:
                                # print 'a2'
                                planeList.append(plane)

                        else:
                            # print 'b'
                            alfa, beta = angle[0], angle[1]

                            if [alfa, beta] not in originList:
                                # print 'bb'
                                originList.append([alfa, beta])
                                # print[alfa, beta]

                                if alfa == numWire:
                                    # print 'bb1'

                                    if beta > numAngle:
                                        # print 'bb11'

                                        pyPl = pyFace.selectPlane(alfa, beta)
                                        pl = pyPl.shape
                                        planeList.append(pl)

                                elif alfa > numWire:
                                    # print 'bb2'

                                    pyPl = pyFace.selectPlane(alfa, beta)
                                    pl = pyPl.shape
                                    planeList.append(pl)

                                elif alfa < numWire:
                                    # print 'bb3'
                                    pass

            planeList.extend(secondaries)
            for plane in planeList:
                plane.rotate(FreeCAD.Vector(0, 0, 0), sketchAxis,
                             math.degrees(sketchAngle))
                plane.translate(sketchBase)
            shell = Part.makeShell(planeList)
            shellList.append(shell)

        endShape = Part.makeCompound(shellList)

        if slopedPlanes.Down:
            pass

        if slopedPlanes.Up:
            pass

        if slopedPlanes.Complement:
            endShape.complement()

        if slopedPlanes.Simmetry:
            pass

        if slopedPlanes.Solid:
            endShape = Part.makeSolid(endShape)

        # endShape.removeInternalWires(True)

        slopedPlanes.Shape = endShape

    def onChanged(self, slopedPlanes, prop):

        ''''''

        if self.State:
            return

        if prop == "SlopeGlobal":

            slope = slopedPlanes.SlopeGlobal
            value = slope
            prop = "angle"
            self.overWritePyProp(prop, value)

        elif prop == "FactorLength":

            length = slopedPlanes.FactorLength
            value = length
            prop = "length"
            self.overWritePyProp(prop, value)

        elif prop == "FactorWidth":

            width = slopedPlanes.FactorWidth
            value = (width, width)
            prop = "width"
            self.overWritePyProp(prop, value)

    def overWritePyProp(self, prop, value):

        ''''''

        for pyFace in self.Pyth:
            for pyWire in pyFace.wires:
                for pyPlane in pyWire.planes:
                    setattr(pyPlane, prop, value)

    def __getstate__(self):

        ''''''

        state = dict()

        state['Type'] = self.Type

        pyth = []
        for pyFace in self.Pyth:
            dct = pyFace.__dict__.copy()
            wires, alignaments = pyFace.__getstate__()
            dct['_wires'], dct['_alignaments'] = wires, alignaments
            pyth.append(dct)
        state['Pyth'] = pyth

        return state

    def __setstate__(self, state):

        ''''''

        self.Type = state['Type']

        pyth = []
        numFace = -1
        for dct in state['Pyth']:
            numFace += 1
            pyFace = _PyFace(numFace)
            wires, alignaments = dct['_wires'], dct['_alignaments']
            wires, alignaments = pyFace.__setstate__(wires, alignaments)
            dct['_wires'], dct['_alignaments'] = wires, alignaments
            pyFace.__dict__ = dct
            pyth.append(pyFace)
        self.Pyth = pyth

        self.State = True


class _ViewProvider_SlopedPlanes():

    ''''''

    def __init__(self, vobj):

        ''''''

        vobj.Proxy = self

    def getIcon(self):

        ''''''

        path = os.path.dirname(__file__)
        return path + "/SlopedPlanes_Tree.svg"

    def getDefaultDisplayMode(self):

        ''''''

        return "FlatLines"

    def __getstate__(self):

        ''''''

        return None

    def __setstate__(self, state):

        ''''''

        return None

    def attach(self, vobj):

        ''''''

        self.Object = vobj.Object

        obj = self.Object
        obj.Proxy.State = False

    def claimChildren(self):

        ''''''

        obj = self.Object
        base = obj.Base
        return [base]

    def unsetEdit(self, vobj, mode):

        ''''''

        FreeCADGui.Control.closeDialog()
        return

    def setEdit(self, vobj, mode=0):

        ''''''

        taskd = _TaskPanel_SlopedPlanes()
        taskd.obj = self.Object
        taskd.update()
        FreeCADGui.Control.showDialog(taskd)
        return True
