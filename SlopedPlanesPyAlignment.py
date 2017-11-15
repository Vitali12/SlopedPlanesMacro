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


from SlopedPlanesPy import _Py


__title__ = "SlopedPlanes Macro"
__author__ = "Damian Caceres Moreno"
__url__ = "http://www.freecadweb.org"


class _PyAlignment(_Py):

    ''''''

    def __init__(self):

        ''''''

        self.base = None
        self.aligns = []
        self.chops = []
        self.rango = []
        self.falsify = False
        self.simulatedShape = None
        self.prior = None
        self.later = None

    @property
    def base(self):

        ''''''

        return self._base

    @base.setter
    def base(self, base):

        ''''''

        self._base = base

    @property
    def aligns(self):

        ''''''

        return self._aligns

    @aligns.setter
    def aligns(self, aligns):

        ''''''

        self._aligns = aligns

    @property
    def chops(self):

        ''''''

        return self._chops

    @chops.setter
    def chops(self, chops):

        ''''''

        self._chops = chops

    @property
    def rango(self):

        ''''''

        return self._rango

    @rango.setter
    def rango(self, rango):

        ''''''

        self._rango = rango

    @property
    def falsify(self):

        ''''''

        return self._falsify

    @falsify.setter
    def falsify(self, falsify):

        ''''''

        self._falsify = falsify

    @property
    def simulatedShape(self):

        ''''''

        return self._simulatedShape

    @simulatedShape.setter
    def simulatedShape(self, simulatedShape):

        ''''''

        self._simulatedShape = simulatedShape

    @property
    def prior(self):

        ''''''

        return self._prior

    @prior.setter
    def prior(self, prior):

        ''''''

        self._prior = prior

    @property
    def later(self):

        ''''''

        return self._later

    @later.setter
    def later(self, later):

        ''''''

        self._later = later

    def trimming(self):

        ''''''

        pyWireList = _Py.pyFace.wires
        enormousShape = self.base.enormousShape
        numWire = self.base.numWire
        pyWire = pyWireList[numWire]

        rango = self.rango
        pyPlaneList = pyWire.planes

        for ran in rango:
            for nG in ran:
                pyPl = pyPlaneList[nG]
                if not pyPl.aligned:

                    pyPl.trimming(enormousShape)

        for chop in self.chops:

            for pyPlane in chop:

                enormousShape = pyPlane.enormousShape
                if enormousShape:
                    numWire = pyPlane.numWire
                    pyWire = pyWireList[numWire]
                    pyPlaneList = pyWire.planes

                    for rango in pyPlane.rango:
                        for nG in rango:
                            pyPl = pyPlaneList[nG]
                            if not pyPl.aligned:

                                pyPl.trimming(enormousShape)

    def priorLater(self):

        ''''''

        pyBase = self.base
        # print 'base ', pyBase.numGeom
        base = pyBase.shape
        bigBase = pyBase.bigShape
        pyCont = self.aligns[0]
        cont = pyCont.shape
        bigCont = pyCont.bigShape

        pyPrior = self.prior
        pyLater = self.later
        prior = pyPrior.shape
        later = pyLater.shape
        bigPrior = pyPrior.bigShape
        bigLater = pyLater.bigShape

        cutterList = []

        if ((not pyPrior.reflexed) or
           (pyPrior.choped and not pyPrior.aligned)):
            # print '1'
            cutterList.append(bigPrior)

        if ((not pyLater.reflexed) or
           (pyLater.choped and not pyLater.aligned)):
            # print '2'
            cutterList.append(bigLater)

        if not pyPrior.aligned:

            gS = pyPrior.geomShape
            prior = self.cutting(prior, [bigBase], gS)
            pyPrior.shape = prior

        if not pyLater.aligned:

            if not self.falsify:

                gS = pyLater.geomShape
                later = self.cutting(later, [bigBase], gS)

            else:

                gS = pyLater.geomShape
                later = self.cutting(later, [bigCont], gS)

            pyLater.shape = later

        if not self.falsify:
            # print 'A'

            if cutterList:
                # print '3'
                gS = pyBase.geomShape
                base = self.cutting(base, cutterList, gS)
                pyBase.shape = base

        else:
            # print 'B'

            [pyOne, pyTwo] = self.chops[0]

            cList = [pyOne.bigShape] + cutterList

            gS = pyBase.geomShape
            base = self.cutting(base, cList, gS)
            pyBase.shape = base

            cList = [pyTwo.bigShape] + cutterList

            gS = pyCont.geomShape
            cont = self.cutting(cont, cList, gS)
            pyCont.shape = cont

    def simulatingAlignment(self):

        ''''''

        pyBase = self.base
        base = pyBase.shape.copy()
        enormousBase = pyBase.enormousShape
        # print(pyBase.numWire, pyBase.numGeom)

        chops = self.chops
        rango = self.rango
        pyWireList = _Py.pyFace.wires

        if not self.falsify:

            chopList = []
            numChop = -1
            for [pyOne, pyTwo] in chops:
                numChop += 1

                numWire = pyOne.numWire
                pyWire = pyWireList[numWire]
                pyPlaneList = pyWire.planes

                rChop = rango[numChop]
                # print 'rChop ', rChop
                cList = []
                for nn in rChop:
                    pyPl = pyPlaneList[nn]
                    if not pyPl.choped:
                        pl = pyPl.shape
                        if pl:
                            cList.append(pl)

                enormousChopTwo = pyTwo.enormousShape
                chopOneCopy = pyOne.shape.copy()

                cutList = [enormousBase, enormousChopTwo] + cList

                gS = pyOne.geomShape
                chopOneCopy = self.cutting(chopOneCopy, cutList, gS)

                enormousChopOne = pyOne.enormousShape
                chopTwoCopy = pyTwo.shape.copy()

                cutList = [enormousBase, enormousChopOne] + cList

                gS = pyTwo.geomShape
                chopTwoCopy = self.cutting(chopTwoCopy, cutList, gS)

                chopList.extend([chopOneCopy, chopTwoCopy])

            lenChops = len(chops)
            num = lenChops / 2
            rest = lenChops % 2

            if rest == 0:
                numLeft = num - 1
                numRight = num

            else:
                numLeft = num
                numRight = num

            pyLeft = chops[numLeft][0]
            pyRight = chops[numRight][-1]

            rangoLeft = pyLeft.rango
            rangoRight = pyRight.rango
            rango = rangoLeft + rangoRight

            cutList = []
            for ran in rango:
                for nn in ran:
                    pyPl = pyPlaneList[nn]
                    if not pyPl.choped:
                        if pyPl != pyBase:
                            if pyPl.reflexed:
                                pl = pyPl.simulatedShape
                            else:
                                pl = pyPl.shape
                            if pl:
                                cutList.append(pl)
                                # print 'rango nn ', nn

            rearLeft = pyLeft.rear
            rearRight = pyRight.rear
            rear = rearLeft + rearRight

            for nn in rear:
                pyPl = pyPlaneList[nn]
                if not pyPl.choped:
                    pl = pyPl.shape
                    if pl:
                        cutList.append(pl)
                        # print 'rear nn ', nn

            cutterList = chopList + cutList

            limitList = []
            pyPrior = self.prior
            pyLater = self.later
            bigPrior = pyPrior.bigShape
            bigLater = pyLater.bigShape
            limitList.extend([bigPrior, bigLater])
            cutterList.extend(limitList)

            geomList = [py.geomShape for py in self.aligns]
            geomList.insert(0, pyBase.geomShape)

            base = base.cut(cutterList, _Py.tolerance)
            shapeList = []
            for ff in base.Faces:
                section = ff.section(geomList, _Py.tolerance)
                if section.Edges:
                    # print 'a'
                    shapeList.append(ff)

        else:

            pyCont = self.aligns[0]
            cont = pyCont.shape.copy()
            pyLater = self.later
            bigLater = pyLater.bigShape
            gS = pyCont.geomShape
            cont = self.cutting(cont, [bigLater], gS)

            shapeList = [base, cont]

        # print shapeList
        self.simulatedShape = shapeList

    def virtualizing(self):

        ''''''

        virtualizedChops = []
        for [pyChopOne, pyChopTwo] in self.chops:

            pyOne = pyChopOne.virtualizing()
            pyOne.choped = True
            pyTwo = pyChopTwo.virtualizing()
            pyTwo.choped = True

            virtualizedChops.append([pyOne, pyTwo])

        self.chops = virtualizedChops

    def simulating(self):

        ''''''

        enormousShape = self.base.enormousShape

        for chop in self.chops:
            for pyPlane in chop:
                pyPlane.simulating(enormousShape)

    def aligning(self):

        ''''''

        # print(self.base.numWire, self.base.numGeom)
        # print[(x.numWire, x.numGeom) for x in self.aligns]
        # print[[(x.numWire, x.numGeom), (y.numWire, y.numGeom)]
        # for [x, y] in self.chops]

        pyBase = self.base

        enormousBase = pyBase.enormousShape
        aligns = self.aligns
        chops = self.chops

        rangoChopList = self.rango
        pyWireList = _Py.pyFace.wires

        pyCont = aligns[0]
        cont = pyCont.shape
        enormousCont = pyCont.enormousShape

        chopList = []

        numChop = -1
        for [pyOne, pyTwo] in self.chops:
            numChop += 1

            rangoChop = rangoChopList[numChop]

            nW = pyOne.numWire
            pyW = pyWireList[nW]
            pyPlaneList = pyW.planes

            cutList = []
            for nn in rangoChop:
                pyPl = pyPlaneList[nn]
                if not pyPl.choped:
                    if not pyPl.aligned:
                        pl = pyPl.shape
                        cutList.append(pl)
                        # print 'rangoChop ', nn
                    else:
                        pass  # ???
                else:
                    pass  # ???

            num = -1
            for pyPlane in [pyOne, pyTwo]:
                num += 1

                # print '# chop ', pyPlane.numGeom

                cutterList = []

                nW = pyPlane.numWire
                pyW = pyWireList[nW]
                pyPlaneList = pyW.planes

                rear = pyPlane.rear
                for nG in rear:
                    pyPl = pyPlaneList[nG]
                    if not pyPl.choped:
                        if not pyPl.aligned:
                            rearPlane = pyPl.shape
                            cutterList.append(rearPlane)
                            # print 'rearPlane ', nG

                rango = pyPlane.rango
                for ran in rango:
                    for nn in ran:
                        pyPl = pyPlaneList[nn]
                        if not pyPl.choped:
                            if not pyPl.aligned:
                                rangoPlane = pyPl.shape
                                cutterList.append(rangoPlane)
                                # print 'rango ', nn

                cutterList.extend(cutList)

                if cutterList:
                    plane = pyPlane.shape
                    gS = [pyOne, pyTwo][num].geomShape
                    plane = self.cutting(plane, cutterList, gS)
                    pyPlane.shape = plane

            num = -1
            for pyPlane in [pyOne, pyTwo]:
                num += 1

                plane = pyPlane.shape
                planeCopy = plane.copy()

                if not self.falsify:
                    cList = [enormousBase]
                else:
                    if num == 0:
                        cList = [enormousBase]
                    else:
                        cList = [enormousCont]

                gS = [pyOne, pyTwo][num].geomShape
                planeCopy = planeCopy.cut(cList, _Py.tolerance)

                for ff in planeCopy.Faces:
                    section = ff.section([gS], _Py.tolerance)
                    if not section.Edges:
                        sect = ff.section([_Py.face], _Py.tolerance)
                        if sect.Edges:
                            planeCopy = ff
                            plane = self.cutting(plane, [planeCopy], gS)
                            pyPlane.shape = plane
                            break

            shapeOne = pyOne.shape
            shapeTwo = pyTwo.shape

            cutterList = [shapeTwo]
            gS = pyOne.geomShape
            ff = self.cutting(shapeOne, cutterList, gS)
            pyOne.shape = ff

            cutterList = [shapeOne]
            gS = pyTwo.geomShape
            ff = self.cutting(shapeTwo, cutterList, gS)
            pyTwo.shape = ff

            chopList.append([pyOne, pyTwo])

        if not self.falsify:

            numChop = -1
            for pyCont in aligns:
                numChop += 1

                [pyOne, pyTwo] = chopList[numChop]
                rangoChop = rangoChopList[numChop]

                nW = pyOne.numWire
                pyW = pyWireList[nW]
                pyPlaneList = pyW.planes

                shapeOne = pyOne.shape
                shapeTwo = pyTwo.shape

                cutterList = [shapeOne, shapeTwo]

                for nn in rangoChop:
                    pl = pyPlaneList[nn].shape
                    if pl:
                        cutterList.append(pl)
                        # print 'rangoChop ', nn

                base = pyBase.shape
                base = base.cut(cutterList, _Py.tolerance)

                if len(base.Faces) == 2:
                    # print 'a'

                    gS = pyBase.geomShape
                    base = self.selectFace(base.Faces, gS)
                    pyBase.shape = base

                else:
                    # print 'b'

                    gS = pyBase.geomShape
                    ff = self.selectFace(base.Faces, gS)
                    pyBase.shape = ff

                    gS = pyTwo.geomShape
                    shapeTwo = self.cutting(shapeTwo, [ff], gS)
                    pyTwo.shape = shapeTwo

                    gS = pyCont.geomShape
                    ff = self.selectFace(base.Faces, gS)
                    pyCont.shape = ff

                    try:
                        for pyP in aligns[numChop+1:]:
                            pyP.angle = [pyCont.numWire, pyCont.numGeom]
                    except IndexError:
                        pass

                    pyCont.angle = pyBase.angle

                    gS = pyOne.geomShape
                    shapeOne = self.cutting(shapeOne, [ff], gS)
                    pyOne.shape = shapeOne

                    pyBase = aligns[numChop]

        else:

            base = pyBase.shape

            rangoChop = rangoChopList[0]
            pyCont = aligns[0]

            [pyChopOne, pyChopTwo] = chops[0]
            [pyOne, pyTwo] = chopList[0]

            cutterList = [shapeOne, shapeTwo]

            for nn in rangoChop:
                pl = pyPlaneList[nn].shape
                if pl:
                    cutterList.append(pl)
                    # print 'rangoChop ', nn

            gS = pyBase.geomShape
            base = self.cutting(base, cutterList, gS)
            pyBase.shape = base

            gS = pyCont.geomShape
            cont = self.cutting(cont, cutterList, gS)
            pyCont.shape = cont

    def rangging(self):

        ''''''

        pyWireList = _Py.pyFace.wires

        for [pyPlane, pyPl] in self.chops:

            pyWire = pyWireList[pyPlane.numWire]
            pyW = pyWireList[pyPl.numWire]

            pyPlane.rangging(pyWire, 'backward')
            pyPl.rangging(pyW, 'forward')

    def ranggingChop(self):

        ''''''

        pyWireList = _Py.pyFace.wires

        for [pyPlane, pyPl] in self.chops:
            [(w1, g1), (w2, g2)] =\
                [(pyPlane.numWire, pyPlane.numGeom),
                 (pyPl.numWire, pyPl.numGeom)]

            if w1 == w2:
                pyWire = pyWireList[w1]
                lenWire = len(pyWire.planes)
                if g1 > g2:
                    ranA = range(g1+1, lenWire)
                    ranB = range(0, g2)
                    ran = ranA + ranB
                else:
                    ran = range(g1+1, g2)
                rangoChop = ran

            else:
                rangoChop = []

            self.addValue('rango', rangoChop, 'backward')