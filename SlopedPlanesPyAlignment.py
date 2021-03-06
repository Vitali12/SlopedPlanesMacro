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


import Part
from SlopedPlanesPy import _Py


__title__ = "SlopedPlanes Macro"
__author__ = "Damian Caceres Moreno"
__url__ = "https://gitlab.com/damianCaceres/slopedplanes"
__version__ = ""


class _PyAlignment(_Py):

    '''The complementary python object class for alignments. An alignment
    is formed by two or more edges of the SlopedPlanes base which have
    the same direction. The edges could belong to different wires.'''

    def __init__(self):

        '''__init__(self):'''

        self.base = None
        self.aligns = []
        self.chops = []

        self.geomAligned = None
        self.geomList = []

        self.rango = []
        self.rangoPy = []   # TODO podría unir rango y rangoPy en un sola propiedad como en rangoRear. No parece ofrecer mucha ventaja
        self.rangoRear = ()  # desunir numeros de objetos py en dos listas

        self.falsify = False

        self.simulatedAlignment = []
        self.simulatedChops = []

        self.prior = None
        self.later = None
        self.rear = [None, None]

        self.aliShape = []

    @property
    def base(self):

        '''base(self):
        The first plane of the alignment.'''

        return self._base

    @base.setter
    def base(self, base):

        '''base(self, base):'''

        self._base = base

    @property
    def aligns(self):

        '''aligns(self):
        The secondaries planes of the alignment.'''

        return self._aligns

    @aligns.setter
    def aligns(self, aligns):

        '''aligns(self, aligns)'''

        self._aligns = aligns

    @property
    def chops(self):

        '''chops(self):
        List of twin planes which chop the alignment'''

        return self._chops

    @chops.setter
    def chops(self, chops):

        '''chops(self, chops)'''

        self._chops = chops

    @property
    def geomAligned(self):

        '''geomAligned(self):
        Joins in one edge the base edges of aligned planes.
        Redundant with pyAlignment.base.geomAligned'''

        return self._geomAligned

    @geomAligned.setter
    def geomAligned(self, geomAligned):

        '''geomAligned(self, geomAligned)'''

        self._geomAligned = geomAligned

    @property
    def geomList(self):

        '''geomList(self):
        Lists the base edges of aligned planes.'''

        return self._geomList

    @geomList.setter
    def geomList(self, geomList):

        '''geomList(self, geomList)'''

        self._geomList = geomList

    @property
    def rango(self):

        '''rango(self):
        List of list of planes, by number, between every chop.'''

        return self._rango

    @rango.setter
    def rango(self, rango):

        '''rango(self, rango)'''

        self._rango = rango

    @property
    def rangoPy(self):

        '''rangoPy(self):
        By python planes'''

        return self._rangoPy

    @rangoPy.setter
    def rangoPy(self, rangoPy):

        '''rangoPy(self, rangoPy)'''

        self._rangoPy = rangoPy

    @property
    def rangoRear(self):

        '''rangoRear(self): todos los planos que no pertenecen al alineamiento'''

        return self._rangoRear

    @rangoRear.setter
    def rangoRear(self, rangoRear):

        '''rangoRear(self, rangoRear)'''

        self._rangoRear = rangoRear

    @property
    def falsify(self):

        '''falsify(self)'''

        return self._falsify

    @falsify.setter
    def falsify(self, falsify):

        '''falsify(self, falsify)'''

        self._falsify = falsify

    @property
    def simulatedAlignment(self):

        '''simulatedAlignment(self)'''

        return self._simulatedAlignment

    @simulatedAlignment.setter
    def simulatedAlignment(self, simulatedAlignment):

        '''simulatedAlignment(self, simulatedAlignment)'''

        self._simulatedAlignment = simulatedAlignment

    @property
    def simulatedChops(self):

        '''simulatedChops(self)'''

        return self._simulatedChops

    @simulatedChops.setter
    def simulatedChops(self, simulatedChops):

        '''simulatedChops(self, simulatedChops)'''

        self._simulatedChops = simulatedChops

    @property
    def prior(self):

        '''prior(self):
        Plane before the alignment'''

        return self._prior

    @prior.setter
    def prior(self, prior):

        '''prior(self, prior):'''

        self._prior = prior

    @property
    def later(self):

        '''later(self):
        Plane after the alignment'''

        return self._later

    @later.setter
    def later(self, later):

        '''later(self, later)'''

        self._later = later

    @property
    def rear(self):

        '''def rear(self):
        Redundant with chops planes or alignment base plane?'''

        return self._rear

    @rear.setter
    def rear(self, rear):

        self._rear = rear

    @property
    def aliShape(self):

        '''aliShape(self):
        usado en postprocess?
        incluye aligns shapes y posteriormente chops shapes'''

        return self._aliShape

    @aliShape.setter
    def aliShape(self, aliShape):

        '''aliShape(self, aliShape)'''

        self._aliShape = aliShape

    def rangging(self, reset):

        '''rangging(self)'''

        # print('### rangging ', self.base.numWire, self.base.numGeom)

        pyWireList = _Py.pyFace.wires

        for [pyPlane, pyPl] in self.chops:

            numWire = pyPlane.numWire
            nWire = pyPl.numWire
            pyWire = pyWireList[numWire]
            pyW = pyWireList[nWire]

            if reset:

                if not pyPlane.rango:
                    pyPlane.rangging(pyWire, 'backward')
                if not pyPl.rango:
                    pyPl.rangging(pyW, 'forward')

            cc = pyWire.num2py(pyPlane.rango)
            pyPlane.rangoPy = cc
            cc = pyW.num2py(pyPl.rango)
            pyPl.rangoPy = cc

            if numWire == nWire:
                numGeom = pyPlane.numGeom
                nGeom = pyPl.numGeom
                rangoChop = self.rang(pyWire, numGeom, nGeom, 'forward')
                planeList = pyWire.planes

                ran = []
                for nn in rangoChop:
                    pyP = planeList[nn]
                    if not pyP.alignedList:
                        pyP.frontedList.append(self)
                    ran.append(pyP)

            else:
                rangoChop = []
                ran = []

            self.addValue('rango', rangoChop, 'backward')
            self.addValue('rangoPy', ran, 'backward')

        # print 'rangoRear'

        pyPrior = self.prior
        if pyPrior.alignedList:
            ali = pyPrior.alignedList[0]
            pyPrior = ali.aligns[-1]
        pyLater = self.later

        w1 = pyPrior.numWire
        w2 = pyLater.numWire

        if w1 == 0 and w1 == w2:

            pr = pyPrior.numGeom
            lat = pyLater.numGeom

            # print('pr ', pr)
            # print('lat ', lat)

            pyW = pyWireList[w1]
            lenW = len(pyW.planes)

            # print('rear[1] ', self.rear[1])
            # print('rear[0] ', self.rear[0])

            if self.rear[1] is not None:
                pr = self.sliceIndex(self.rear[1] - 1, lenW)

            if self.rear[0] is not None:
                lat = self.sliceIndex(self.rear[0] + 1, lenW)

            # print('pr ', pr)
            # print('lat ', lat)

            pyWire = pyWireList[w1]
            rangoRear = self.rang(pyWire, lat, pr, 'forward')
            # print('rangoRear ', rangoRear)
            rangoRear = [lat] + list(rangoRear) + [pr]
            # print('rangoRear ', rangoRear)

            pyPlaneList = pyWire.planes
            ran = []
            for nn in rangoRear:
                pyP = pyPlaneList[nn]
                pyP.rearedList.append(self)
                ran.append(pyP)

            rangoRear = (rangoRear, ran)

        else:

            rangoRear = ([], [])

        self.rangoRear = rangoRear
        # print('rangoRear ', rangoRear)

    def virtualizing(self):

        '''virtualizing(self)
        Virtualizes the chops which are aligned too, alignments and false
        alignments.
        Virtualizes the base of falsify alignnments which belongs to
        other alignment.'''

        # print('###### virtualizing alignment', self.base.numWire, self.base.numGeom)

        virtualizedChops = []
        for [pyChopOne, pyChopTwo] in self.chops:

            pyOne = pyChopOne.virtualizing()
            pyTwo = pyChopTwo.virtualizing()

            virtualizedChops.append([pyOne, pyTwo])

        self.chops = virtualizedChops

        if self.falsify:
            if not self.base.shape:
                virtualBase = self.base.virtualizing()
                self.base = virtualBase

    def trimming(self):

        '''trimming(self)
        The alignment blocks the path to the planes
        in its front and laterals.'''

        # print('###### trimming base ', self.base.numWire, self.base.numGeom)

        # self.printControl(str(self.base.numGeom))

        pyWireList = _Py.pyFace.wires
        tolerance = _Py.tolerance

        pyFace = _Py.pyFace
        mono = pyFace.mono

        falsify = self.falsify
        geomAligned = self.geomAligned

        rear = self.rear

        pyBase = self.base
        base = pyBase.shape
        numWire = pyBase.numWire
        numGeom = pyBase.numGeom
        enormousBase = pyBase.enormousShape
        baseRear = pyBase.rear
        baseControl = pyBase.control

        aligns = self.aligns

        pyCont = aligns[-1]
        cont = pyCont.shape
        nGeom = pyCont.numGeom
        enormousCont = pyCont.enormousShape
        contRear = pyCont.rear

        totalRear = baseRear + contRear + rear

        pyPrior = self.prior
        pyLater = self.later
        pr = pyPrior.numGeom
        lat = pyLater.numGeom
        w1 = pyPrior.numWire

        rangoChop = self.rango
        rangoCopy = rangoChop[:]
        rangoChopPy = self.rangoPy
        chops = self.chops
        rangoRear = self.rangoRear

        numChop = -1
        for rChop, rChopPy, [pyOne, pyTwo] in\
                zip(rangoChop, rangoChopPy, chops):
            numChop += 1
            # print('### numChop ', numChop)

            rangoOne = pyOne.rango[-1][:]
            rangoOnePy = pyOne.rangoPy[-1][:]
            if pyOne.rear:
                rearOne = pyOne.rear[-1]
            else:
                rearOne = None

            rangoTwo = pyTwo.rango[0][:]
            rangoTwoPy = pyTwo.rangoPy[-1][:]
            if pyTwo.rear:
                rearTwo = pyTwo.rear[0]
            else:
                rearTwo = None

            # print('rangoOne ', rangoOne  # , rangoOnePy)
            # print('rangoTwo ', rangoTwo  # , rangoTwoPy)

            for nn, pyP in zip(rangoOne, rangoOnePy):
                if nn in rangoTwo:
                    rangoOne.remove(nn)
                    rangoTwo.remove(nn)
                    rangoOnePy.remove(pyP)
                    rangoTwoPy.remove(pyP)

            # print('rangoOne ', rangoOne  # , rangoOnePy)
            # print('rangoTwo ', rangoTwo  # , rangoTwoPy)

            nW = pyOne.numWire
            pyPlList = pyWireList[nW].planes
            rC = []

            # if mono utilizar control para hacer descartes. IMPORTANTE!!!

            if not mono and nW == pyTwo.numWire:
                # print('nW')

                # the two rangos don't cut between them, if not aligned

                for nG, pyPl in zip(rangoOne, rangoOnePy):
                    if nG is not rearTwo:
                        control = pyPl.control
                        for r, pyPr in zip(rangoTwo, rangoTwoPy):
                            if r not in control and r is not rearOne:
                                if not pyPr.alignedList:
                                    if pyPl.alignedList:
                                        pass
                                    else:
                                        control.append(r)
                        # and opp Chop
                        r = pyTwo.numGeom
                        if r not in control:
                            control.append(r)

                for nG, pyPl in zip(rangoTwo, rangoTwoPy):
                    if nG is not rearOne:
                        control = pyPl.control
                        for r, pyPr in zip(rangoOne, rangoOnePy):
                            if r not in control and r is not rearTwo:
                                if not pyPr.alignedList:
                                    if pyPl.alignedList:
                                        pass
                                    else:
                                        control.append(r)
                        # and opp chop
                        r = pyOne.numGeom
                        if r not in control:
                            control.append(r)

                # self.printControl(str(self.base.numGeom))

                # rChop: trimming bigShape

                if falsify:
                    cutList = [enormousBase, enormousCont]
                else:
                    cutList = [enormousBase]

                for nG, pyPl in zip(rChop, rChopPy):
                    if not pyPl.alignedList:
                        # print(nG, pyPl)

                        bPl = pyPl.bigShape
                        gS = pyPl.geomShape
                        bPl = self.cutting(bPl, cutList, gS)
                        pyPl.bigShape = bPl

                        rC.append(bPl)

                        control = pyPl.control

                        # rChop doesn't cut with rangoRear and viceversa, if not aligned
                        if w1 == nW:
                            for r, pyPlR in zip(rangoRear[0], rangoRear[1]):
                                if r not in control:
                                    control.append(r)

                                if not pyPlR.alignedList:
                                    if nG not in pyPlR.control:
                                        pyPlR.control.append(nG)

                        # rChop is not cutted by alignment
                        control.append(numGeom)
                        if falsify:
                            control.append(nGeom)

                        # the aligment is not cutted by rChop
                        if numWire == nW:
                            baseControl.append(nG)
                            if falsify:
                                pyCont.control.append(nG)

                        # pyOne and pyTwo don't cut rChop, if not reflexed
                        if not pyPl.reflexed:
                            pyOne.control.append(nG)
                            pyTwo.control.append(nG)

                        # rChop doesn't cut with other rChop
                        # chops doesn't cut with other rChop

                        num = -1
                        for rr in rangoCopy:
                            num += 1
                            if num != numChop:
                                [pyO, pyT] = chops[num]
                                if pyO.numWire == nW:
                                    for nn in rr:
                                        pyOne.control.append(nn)
                                        pyTwo.control.append(nn)
                                        control.append(nn)

                # self.printControl(str(self.base.numGeom))

            # the rango of the chop are cutted by the chop,
            # and perhaps by the base or the continuation
            num = -1
            for pyPlane in [pyOne, pyTwo]:
                num += 1
                # print('### chop ', pyPlane.numWire, pyPlane.numGeom)
                enormousShape = pyPlane.enormousShape

                if num == 0:
                    rango = rangoOne

                    if rear[1] is not None:
                        index = rango.index(rear[1])
                        rango = rango[index:]

                    secondRear = pyOne.secondRear
                    pyPlList = pyWireList[pyOne.numWire].planes
                else:
                    rango = rangoTwo

                    if rear[0] is not None:
                        index = rango.index(rear[0])
                        rango = rango[index:]

                    secondRear = pyTwo.secondRear
                    pyPlList = pyWireList[pyTwo.numWire].planes
                # print('rango ', rango)

                # the cross
                if pyPlane.virtualized:
                    # print('virtualized')
                    aliList = pyPlane.alignedList
                    pyA = aliList[0]
                    gA = pyA.geomAligned.copy()
                    gA = gA.cut([geomAligned], tolerance)
                    if len(gA.Edges) == 2:
                        pyPlane.cross = True
                # print('cross ', pyPlane.cross)

                # consecutives
                consecutive = False
                for nG in rango:
                    if nG in secondRear:
                        break

                    pyPl = pyPlList[nG]  # cambiar a zip?
                    if pyPl.alignedList or pyPl.chopedList:
                        consecutive = True
                    # print('consecutive ', consecutive)

                    #rearedList = pyPl.rearedList
                    # el rango se debe limpiar desde un principio. Luego lo utilizaré en aligning de nuevo ???
                    #if not rearedList or self in rearedList or nG in rear:

                    control = pyPl.control
                    if pyPlane.numGeom not in control:
                        # print('# nG ', nG)
                        if not (pyPl.alignedList or pyPl.chopedList):

                            if not pyPlane.cross:
                                # print('1')

                                if consecutive:
                                    # print('a')

                                    if pyPl.frontedList:
                                        # print('a1')

                                        control.append(numGeom)
                                        pyPlane.control.append(nG)

                                    else:
                                        # print('a2')

                                        pyPl.trimming(enormousShape)

                                else:
                                    # print('b')

                                    cList = [enormousShape]

                                    if nG not in totalRear:
                                        # print('b1')
                                        if nG not in [pr, lat]:
                                            # print('b11')

                                            if falsify:
                                                # print('b111')
                                                if num == 0:
                                                    # print('b1111')
                                                    cList.append(enormousBase)
                                                    control.append(numGeom)
                                                else:
                                                    # print('b1112')
                                                    cList.append(enormousCont)
                                                    control.append(nGeom)

                                            else:
                                                # print('b112')
                                                cList.append(enormousBase)
                                                control.append(numGeom)

                                    pyPl.trimming(enormousShape, cList)

                                control.append(pyPlane.numGeom)

                            else:
                                # print('2')

                                pyPl.trimmingTwo(enormousShape)
                                baseControl.append(nG)

        if falsify:
            # the base and cont are cutted by a chop

            rC = Part.makeCompound(rC)

            section = rC.section([base], tolerance)
            if section.Edges:
                pyBase.cuttingPyth([pyTwo.enormousShape])
            else:
                pyBase.cuttingPyth([pyOne.enormousShape])

            section = rC.section([cont], tolerance)
            if section.Edges:
                pyCont.cuttingPyth([pyOne.enormousShape])
            else:
                pyCont.cuttingPyth([pyTwo.enormousShape])

            pyPlList = pyWireList[pyTwo.numWire].planes
            for nn in rangoTwo:
                pyPl = pyPlList[nn]
                if not pyPl.alignedList:
                    baseControl.append(nn)
                    pyPl.control.append(numGeom)

            contControl = pyCont.control
            pyPlList = pyWireList[pyOne.numWire].planes
            for nn in rangoOne:
                pyPl = pyPlList[nn]
                if not pyPl.alignedList:
                    contControl.append(nn)
                    pyPl.control.append(nGeom)

    def priorLater(self):

        '''priorLater(self)'''

        # print('###### priorLater base ', self.base.numWire, self.base.numGeom)

        falsify = self.falsify

        pyFace = _Py.pyFace
        mono = pyFace.mono

        pyBase = self.base
        numWire = pyBase.numWire
        numGeom = pyBase.numGeom
        enormousBase = pyBase.enormousShape
        control = pyBase.control

        pyCont = self.aligns[-1]
        nWire = pyCont.numWire
        nGeom = pyCont.numGeom
        enormousCont = pyCont.enormousShape

        pyPrior = self.prior
        pyLater = self.later
        pr = pyPrior.numGeom
        # print('prior ', pyPrior.numWire, pr)
        lat = pyLater.numGeom
        # print('later ', pyLater.numWire, lat)
        bigPrior = pyPrior.bigShape
        bigLater = pyLater.bigShape

        if falsify:
            # print('A')

            [pyOne, pyTwo] = self.chops[0]

            if not pyPrior.reflexed or mono:
                # print('AP1')

                pyBase.cuttingPyth([bigPrior])
                control.append(pr)
                if numWire == pyLater.numWire:
                    control.append(lat)

            elif pyBase.virtualized:
                # print('AP2')

                pyBase.cuttingPyth([bigPrior])
                control.append(pr)
                if numWire == pyLater.numWire:
                    control.append(lat)

            elif pyPrior.chopedList and len(pyBase.alignedList) == 1:
                # print('AP3')

                pyBase.cuttingPyth([bigPrior])
                control.append(pr)
                if numWire == pyLater.numWire:
                    control.append(lat)

            if not pyLater.reflexed or mono:
                # print('AL1')

                pyCont.cuttingPyth([bigLater])
                pyCont.control.append(lat)
                if nWire == pyPrior.numWire:
                    pyCont.control.append(pr)

            elif pyLater.chopedList and len(pyCont.alignedList) == 1:
                # print('AL2')

                pyCont.cuttingPyth([bigLater])
                pyCont.control.append(lat)
                if nWire == pyPrior.numWire:
                    pyCont.control.append(pr)

        else:
            # print('B')

            cutterList = []

            if not pyPrior.reflexed or pyPrior.chopedList or mono:
                # print('1')

                cutterList.append(bigPrior)

                if not pyBase.chopedList:
                    if numWire == pyLater.numWire:
                        # print('11')
                        control.append(pr)

            if not pyLater.reflexed or pyLater.chopedList or mono:
                # print('2')

                cutterList.append(bigLater)

                if not pyBase.chopedList:
                    if numWire == pyLater.numWire:
                        # print('21')
                        control.append(lat)

            if cutterList:
                # print('BB')

                pyBase.cuttingPyth(cutterList)
                # print('pyBase.shape ', pyBase.shape)

        # cuts pyPrior and pyLater

        if not (pyPrior.reflexed or pyPrior.arrow):
            # print('a')

            pyPrior.trimming(enormousBase)
            pyPrior.control.append(numGeom)
            # print('pyPrior.shape ', pyPrior.shape)

            if falsify:
                # print('a1')
                pyPrior.control.append(nGeom)

        if not (pyLater.reflexed or pyLater.arrow):
            # print('b')

            if not falsify:
                # print('b1')

                pyLater.trimming(enormousBase)
                pyLater.control.append(numGeom)
                # print('pyLater.shape ', pyLater.shape)

            else:
                # print('b2')

                pyLater.trimming(enormousCont)
                pyLater.control.append(nGeom)
                pyLater.control.append(numGeom)
                # print('pyLater.shape ', pyLater.shape)

    def simulatingChops(self):

        '''simulatingChops(self)
        simulating the rango'''

        # print('###### simulatingChops ', self.base.numWire, self.base.numGeom, self.falsify)

        tolerance = _Py.tolerance
        pyFace = _Py.pyFace
        face = pyFace.face
        falsify = self.falsify

        rangoChopPy = self.rangoPy
        simulatedChops = []

        geomList = [pyP.geomShape for pyP in self.aligns]
        geomList.insert(0, self.base.geomShape)
        self.geomList = geomList

        enormousBase = self.base.enormousShape
        enormousCont = self.aligns[-1].enormousShape

        numChop = -1
        for [pyOne, pyTwo] in self.chops:
            numChop += 1
            # print('### chops ', pyOne.numGeom, pyTwo.numGeom)

            # choped with reflex corner

            rrOne = []
            if pyOne.rear:
                pyReflexListOne = pyOne.reflexedList
                if pyReflexListOne:
                    pyReflexOne = pyReflexListOne[0]
                    pyOppOne = pyReflexOne.planes[1]
                    oppEnormousOne = pyOppOne.enormousShape
                    rrOne = pyOne.rango[0]
            # print('rrOne ', rrOne)

            rrTwo = []
            if pyTwo.rear:
                pyReflexListTwo = pyTwo.reflexedList
                if pyReflexListTwo:
                    pyReflexTwo = pyReflexListTwo[0]
                    pyOppTwo = pyReflexTwo.planes[0]
                    oppEnormousTwo = pyOppTwo.enormousShape
                    rrTwo = pyTwo.rango[1]
            # print('rrTwo ', rrTwo)

            # simulating

            if falsify:

                pyOne.simulating([enormousBase])
                pyTwo.simulating([enormousCont])

            else:

                pyOne.simulating([enormousBase])
                pyTwo.simulating([enormousBase])

            if pyOne.virtualized:
                pyO = self.selectBasePlane(pyOne.numWire, pyOne.numGeom)
                # print('1')
                pyO.simulating([enormousBase])

            if pyTwo.virtualized:
                pyT = self.selectBasePlane(pyTwo.numWire, pyTwo.numGeom)
                # print('2')
                if falsify:
                    # print('21')
                    pyT.simulating([enormousCont])
                else:
                    # print('22')
                    pyT.simulating([enormousBase])

            rChopPy = rangoChopPy[numChop]
            # print('rChop ', self.rango, rChopPy)
            cutList = []
            for pyPl in rChopPy:

                if not (pyPl.alignedList or pyPl.chopedList):

                    if pyPl.reflexed:
                        # print('pyPl.numGeom reflexed ', pyPl.numGeom)
                        pl = pyPl.simulatedShape
                        cutList.append(pl)

                    else:
                        # print('pyPl.numGeom ', pyPl.numGeom)
                        pl = pyPl.bigShape.copy()
                        gS = pyPl.geomShape

                        rr = pyPl.numGeom

                        if rr in rrOne:
                            # print('rrOne')
                            pl = self.cutting(pl, [oppEnormousOne], gS)

                        if rr in rrTwo:
                            # print('rrTwo')
                            pl = self.cutting(pl, [oppEnormousTwo], gS)

                        cutList.append(pl)

            cList = []

            if cutList:
                # print('cutList ', cutList)

                bb = self.base.seedShape.copy()

                bb = bb.cut([pyOne.simulatedShape,
                             pyTwo.simulatedShape], tolerance)

                for ff in bb.Faces:
                    section = ff.section(geomList, tolerance)
                    if not section.Edges:
                        section = ff.section([face], tolerance)
                        if section.Edges:
                            bb = ff
                            break

                cL = Part.makeCompound(cutList)
                cL = cL.cut([pyOne.enormousShape,
                             pyTwo.enormousShape], tolerance)

                for ff in cL.Faces:
                    section = ff.section([bb], tolerance)
                    if section.Edges:
                        cList.append(ff)

                pyOne.simulating(cutList)
                pyTwo.simulating(cutList)

                pyOne.cuttingPyth(cutList)
                pyTwo.cuttingPyth(cutList)

                if pyOne.virtualized:
                    # print('pyO')
                    pyO.cuttingPyth(cutList)
                    pyO.simulating(cutList)

                if pyTwo.virtualized:
                    # print('pyT')
                    pyT.cuttingPyth(cutList)
                    pyT.simulating(cutList)

            simulatedChops.append(cList)
            # print('cList ', cList)

        self.simulatedChops = simulatedChops

    def simulatingAlignment(self):

        '''simulatingAlignment(self)'''

        # print('###### simulatingAlignment ', self.base.numWire, self.base.numGeom, self.falsify, self.base.virtualized)

        chops = self.chops
        simulatedChops = self.simulatedChops
        falsify = self.falsify

        pyBase = self.base
        base = pyBase.shape.copy()
        pyPrior = self.prior
        pyLater = self.later

        pr = pyPrior.numGeom
        lat = pyLater.numGeom

        baseControl = pyBase.control
        rear = self.rear

        shapeList = []
        cutterList = []

        numChop = -1
        for [pyOne, pyTwo] in chops:
            numChop += 1

            simulC = simulatedChops[numChop]
            cutterList.extend(simulC)
            shapeList.extend(simulC)

            one = pyOne.simulatedShape.copy()
            two = pyTwo.simulatedShape.copy()

            if not falsify:

                enormousTwo = pyTwo.enormousShape
                gS = pyOne.geomShape
                one = self.cutting(one, [enormousTwo], gS)

                enormousOne = pyOne.enormousShape
                gS = pyTwo.geomShape
                two = self.cutting(two, [enormousOne], gS)

            cutterList.extend([one, two])
            shapeList.extend([one, two])

        # print('cutterList ', cutterList)
        # print('shapeList ', shapeList)

        if falsify:

            pyCont = self.aligns[-1]
            cont = pyCont.shape.copy()

            # prior and later

            cList = cutterList[:]
            if pr not in baseControl and not (pyPrior.alignedList and rear[1] is None):
                cList.append(pyPrior.bigShape)
            gS = pyBase.geomShape
            base = self.cutting(base, cList, gS)

            cList = cutterList[:]
            if lat not in pyCont.control and not (pyLater.alignedList and rear[0] is None):
                cList.append(pyLater.bigShape)
            gS = pyCont.geomShape
            cont = self.cutting(cont, cList, gS)

            shapeList.extend([base, cont])

        else:

            # prior and later

            if pr not in baseControl and not (pyPrior.alignedList and rear[1] is None):
                cutterList.append(pyPrior.bigShape)

            if lat not in baseControl and not (pyLater.alignedList and rear[0] is None):
                cutterList.append(pyLater.bigShape)

            # print('cutterList ', cutterList)

            geomList = self.geomList

            base = base.cut(cutterList, _Py.tolerance)
            # print('base.Faces ', base.Faces, [f.Area for f in base.Faces])
            for ff in base.Faces:
                section = ff.section(geomList, _Py.tolerance)
                if section.Edges:
                    # print('section')
                    shapeList.append(ff)

            # print('shapeList ', shapeList)

        self.simulatedAlignment = shapeList

    def aligning(self):

        '''aligning(self)'''

        # print('###### base ', self.base.numWire, self.base.numGeom)

        pyFace = _Py.pyFace
        geomShapeFace = pyFace.shapeGeom

        tolerance = _Py.tolerance
        pyWireList = _Py.pyFace.wires

        falsify = self.falsify

        pyBase = self.base
        enormousBase = pyBase.enormousShape
        control = pyBase.control
        aligns = self.aligns
        rangoChop = self.rango
        rangoChopPy = self.rangoPy
        simulatedChops = self.simulatedChops

        pyCont = aligns[-1]
        cont = pyCont.shape
        enormousCont = pyCont.enormousShape

        rear = self.rear

        # the chops

        chopList = []
        numChop = -1
        for [pyOne, pyTwo] in self.chops:
            numChop += 1
            # print('### [pyOne, pyTwo]', [(pyOne.numWire, pyOne.numGeom), (pyTwo.numWire, pyTwo.numGeom)])

            simulatedC = simulatedChops[numChop]
            # print('simulatedC ', simulatedC)

            cutList = []

            rangoOne = pyOne.rango[-1]
            rangoOnePy = pyOne.rangoPy[-1]
            numOne = pyOne.numWire
            pyWireOne = pyWireList[numOne]
            pyPlaneListOne = pyWireOne.planes
            rearAlignOne = None
            if pyOne.rear:
                rearOne = pyOne.rear[-1]
                # print('rearOne ', rearOne)
                pyPlOne = pyPlaneListOne[rearOne]
                plOne = self.processRear(rearOne, pyPlOne, numOne)
                if plOne:
                    cutList.extend(plOne)
                    # print(plOne)
            if rear[1] is not None:
                # print('rearAlignOne ', rear[1])
                index = rangoOne.index(rear[1])
                rangoOne = rangoOne[index + 1:]
                rangoOnePy = rangoOnePy[index:]
                rearAlignOne = pyPlaneListOne[rear[1]]
                rearAlignOne =\
                    self.processAlignRear(rearAlignOne, pyWireOne,
                                          1, enormousBase)
                # print('rearAlignOne ', rearAlignOne.Faces)
            # print('rangoOne ', rangoOne)

            rangoTwo = pyTwo.rango[0]
            rangoTwoPy = pyTwo.rangoPy[0]
            numTwo = pyTwo.numWire
            pyWireTwo = pyWireList[numTwo]
            pyPlaneListTwo = pyWireTwo.planes
            rearAlignTwo = None
            if pyTwo.rear:
                rearTwo = pyTwo.rear[0]
                # print('rearTwo ', rearTwo)
                pyPlTwo = pyPlaneListTwo[rearTwo]
                plTwo = self.processRear(rearTwo, pyPlTwo, numTwo)
                if plTwo:
                    cutList.extend(plTwo)
                    # print(plTwo)
            if rear[0] is not None:
                # print('rearAlignTwo ', rear[0])
                index = rangoTwo.index(rear[0])
                rangoTwo = rangoTwo[index:]
                rangoTwoPy = rangoTwo[index:]
                rearAlignTwo = pyPlaneListTwo[rear[0]]
                if falsify:
                    enormous = enormousCont
                else:
                    enormous = enormousBase
                rearAlignTwo =\
                    self.processAlignRear(rearAlignTwo, pyWireTwo, 2, enormous)
                # print(',rearAlingTwo ', rearAlignTwo.Faces)
            # print('rangoTwo ', rangoTwo)

            rCOne, cListOne, oppCListOne =\
                self.processRango(rangoOne, rangoOnePy, pyOne,
                                  numOne, enormousBase)
            # print(rCOne, cListOne, oppCListOne)

            rCTwo, cListTwo, oppCListTwo =\
                self.processRango(rangoTwo, rangoTwoPy, pyTwo,
                                  numTwo, enormousBase)
            # print(rCTwo, cListTwo, oppCListTwo)

            if numTwo == numOne:
                if pyOne.rear and pyTwo.rear:
                    between = self.rang(pyWireOne, rearTwo, rearOne, 'forward')
                    # print('between ', between)
                    cList = self.processBetween(between, pyPlaneListOne)
                    cutList.extend(cList)
                    # print(cList)

            else:
                if pyTwo.rear:
                    pyPlaneListTwo = pyWireTwo.planes
                    mm = self.sliceIndex(pyTwo.numGeom - 1,
                                         len(pyPlaneListTwo))
                    rr = self.rang(pyWireTwo, mm, rearTwo, 'backward')
                    # print('rr ', rr)

                    for r in rr:
                        pyPl = pyPlaneListTwo[r]
                        if not pyPl.reflexed:
                            cListTwo.append(pyPl.shape)

                if pyOne.rear:
                    pyPlaneListOne = pyWireOne.planes
                    mm = self.sliceIndex(pyOne.numGeom + 1,
                                         len(pyPlaneListOne))
                    rr = self.rang(pyWireOne, mm, rearOne, 'forward')
                    # print('rr ', rr)

                    for r in rr:
                        pyPl = pyPlaneListOne[r]
                        if not pyPl.reflexed:
                            cListOne.append(pyPl.shape)

            # print('cutList ', cutList)

            num = -1
            for pyPlane in [pyOne, pyTwo]:
                num += 1
                # print('# pyPlane ', pyPlane.numWire, pyPlane.numGeom, pyPlane.virtualized, pyPlane.cross)
                gS = pyPlane.geomShape
                plane = pyPlane.shape

                ccList = cutList[:]

                if num == 0:
                    rC = rCOne
                    cList = [enormousBase]

                    ccList.extend(cListOne)
                    ccList.extend(oppCListTwo)

                    if rearAlignOne:
                        ccList.append(rearAlignOne)

                else:
                    rC = rCTwo
                    if falsify:
                        cList = [enormousCont]
                    else:
                        cList = [enormousBase]

                    ccList.extend(cListTwo)
                    ccList.extend(oppCListOne)

                    if rearAlignTwo:
                        ccList.append(rearAlignTwo)

                plane = pyPlane.shape
                planeCopy = plane.copy()

                if ccList:
                    # print('ccList ', ccList)
                    # print(planeCopy.Faces)
                    planeCopy = planeCopy.cut(ccList, tolerance)
                    # print('planeCopy.Faces ', planeCopy.Faces)

                # print('cList ', cList)
                pCopy = planeCopy.copy()
                # print(pCopy.Faces)
                pCopy = pCopy.cut(cList, tolerance)

                fList = []    # surplus under the figure
                hList = []
                for ff in pCopy.Faces:
                    section = ff.section([gS], tolerance)
                    if not section.Edges:
                        section = ff.section([pyFace.face], tolerance)
                        if section.Edges:
                            fList.append(ff)
                            section = ff.section(geomShapeFace, tolerance)
                            if not section.Edges:
                                hList.append(ff)

                if fList:
                    # print('fList ', fList)
                    ###pyPlane.under = fList
                    # print(planeCopy.Faces)
                    planeCopy = planeCopy.cut(fList, tolerance)
                    # print('planeCopy.Faces ', planeCopy.Faces)

                if hList:

                    if pyPlane.virtualized and not pyPlane.cross:
                        # print('virtualized plane ', pyPlane.numWire, pyPlane.numGeom)
                        pyP = self.selectPlane(pyPlane.numWire,
                                               pyPlane.numGeom)

                        if isinstance(pyP.angle, list):
                            # print('virt B')
                            angle = pyP.angle
                            pyp = self.selectPlane(angle[0], angle[1])
                            shape = pyp.shape
                            shape = shape.cut(hList, tolerance)
                            gList = []
                            for ff in shape.Faces:
                                section = ff.section(geomShapeFace, tolerance)
                                if section.Edges:
                                    gList.append(ff)
                            pyp.shape = Part.makeCompound(gList)

                        else:
                            # print('virt A')
                            shape = pyP.shape
                            shape = shape.cut(hList, tolerance)
                            gList = []
                            for ff in shape.Faces:
                                section = ff.section(geomShapeFace, tolerance)
                                if section.Edges:
                                    gList.append(ff)
                            pyP.shape = Part.makeCompound(gList)

                # main face
                aList = []
                for ff in planeCopy.Faces:
                    # print('1')
                    section = ff.section([gS], tolerance)
                    if section.Edges:
                        # print('11')
                        aList.append(ff)
                        planeCopy = planeCopy.removeShape([ff])
                        break
                # print('planeCopy.Faces ', planeCopy.Faces)
                # print('aList ', aList)

                # second face
                if pyPlane.rear:

                    if planeCopy.Faces:
                        planeCopy = planeCopy.cut(cList, tolerance)

                    forward = pyPlane.forward
                    backward = pyPlane.backward

                    ffList = []
                    for ff in planeCopy.Faces:
                        # print('2')
                        section = ff.section([forward, backward], tolerance)
                        if not section.Edges:
                            # print('21')
                            section = ff.section(aList, tolerance)
                            if not section.Vertexes:
                                # print('211')
                                section = ff.section([rC], tolerance)
                                if section.Edges:
                                    # print('2111')
                                    ffList.append(ff)
                                    break

                    aList.extend(ffList)
                    # print('aList ', aList)

                comp = Part.makeCompound(aList)
                pyPlane.shape = comp

            # twin

            shapeOne = pyOne.shape.copy()
            shapeTwo = pyTwo.shape.copy()

            # print('pyOne.chopedList ', pyOne.chopedList)
            # print('pyTwo.chopedList ', pyTwo.chopedList)

            if len(pyOne.chopedList) == 1:
                # print('a')
                sList = [shapeTwo]
            else:
                # print('b')
                if pyOne.rear:
                    # print('b1')
                    simulTwo = pyTwo.simulatedShape
                    for pyA in pyOne.chopedList:
                        if pyA is not self:
                            bb = pyA.base.shape
                            gS = pyA.base.geomShape
                            tt = pyTwo.enormousShape
                            bb = self.cutting(bb, [tt], gS)
                            sList = [simulTwo, bb]
                            break
                else:
                    # print('b2')
                    sList = [shapeTwo]
            # print('sList ', sList)

            fList = []
            gS = pyOne.geomShape
            # ff = self.cutting(shapeOne.Faces[0], [shapeTwo], gS)
            ff = self.cutting(shapeOne.Faces[0], sList, gS)         ###
            fList.append(ff)

            for ff in shapeOne.Faces[1:]:
                ff = ff.cut([shapeTwo], _Py.tolerance)
                for f in ff.Faces:
                    section = f.section([rCOne], tolerance)
                    if section.Edges:
                        fList.append(f)

            # print('fList ', fList)
            compound = Part.makeCompound(fList)
            pyOne.shape = compound

            if len(pyTwo.chopedList) == 1:
                # print('a')
                sList = [shapeOne]
            else:
                # print('b')
                if pyTwo.rear:
                    # print('b1')
                    simulOne = pyOne.simulatedShape

                    for pyA in pyOne.chopedList:
                        if pyA is not self:
                            bb = pyA.base.shape
                            gS = pyA.aligns[-1].geomShape
                            tt = pyOne.enormousShape
                            bb = self.cutting(bb, [tt], gS)
                            sList = [simulOne, bb]
                            break
                else:
                    # print('b2')
                    sList = [shapeOne]
            # print('sList ', sList)

            fList = []
            gS = pyTwo.geomShape
            # ff = self.cutting(shapeTwo.Faces[0], [shapeOne], gS)
            ff = self.cutting(shapeTwo.Faces[0], sList, gS)
            fList.append(ff)

            for ff in shapeTwo.Faces[1:]:
                ff = ff.cut([shapeOne], tolerance)
                for f in ff.Faces:
                    section = f.section([rCTwo])
                    if section.Edges:
                        fList.append(f)

            # print('fList ', fList)
            compound = Part.makeCompound(fList)
            pyTwo.shape = compound

            chopList.append([pyOne, pyTwo])
        # print('chopList ', chopList)

        # the alignments

        if self.falsify:
            # print('AA')

            base = pyBase.shape

            rChop = rangoChop[0]
            pyCont = aligns[0]

            [pyOne, pyTwo] = chopList[0]

            shapeOne = pyOne.shape
            shapeTwo = pyTwo.shape

            cutterList = [shapeOne, shapeTwo]

            simulatedC = simulatedChops[0]

            cutterList.extend(simulatedC)

            prior = self.prior
            later = self.later

            # print('prior ', prior.numWire, prior.numGeom)
            # print('later ', later.numWire, later.numGeom)

            if prior.numWire == pyBase.numWire:
                if prior.numGeom not in control:
                    if prior.chopedList or prior.frontedList:
                        pass
                    elif not prior.alignedList:
                        cutterList.append(prior.shape)
                    elif prior.alignedList and not pyBase.chopedList:
                        cutterList.append(prior.selectShape())

            if later.numWire == pyCont.numWire:
                if later.numGeom not in pyCont.control:
                    if later.chopedList or later.frontedList:
                        # print('lat a')
                        pass
                    elif not later.alignedList:
                        # print('lat b')
                        cutterList.append(later.shape)
                    elif later.alignedList and not pyCont.chopedList:
                        # print('lat c')
                        cutterList.append(later.selectShape())

            if cutterList:

                base = pyBase.cuttingPyth(cutterList)
                cont = pyCont.cuttingPyth(cutterList)

                if pyBase.virtualized:
                    pyB = self.selectPlane(pyBase.numWire, pyBase.numGeom)
                    angle = pyB.angle
                    pyb = self.selectPlane(angle[0], angle[1])
                    pyb.cuttingPyth(cutterList)

            pyTwo.cuttingPyth([base, cont, shapeOne])
            pyOne.cuttingPyth([cont, base, shapeTwo])

            cutList = [cont, base]

            nW = pyOne.numWire
            pyW = pyWireList[nW]
            pyPlList = pyW.planes

            if simulatedC:
                # rChop with base and cont
                for nn in rChop:
                    pyPl = pyPlList[nn]
                    if not pyPl.chopedList and not pyPl.alignedList:
                        pyPl.cuttingPyth(cutList)
                        # print('rangoChop ', nn)

        else:
            # print('BB')

            cutList = []

            cL = []
            if len(pyFace.wires) > 1:
                for ch in chopList:
                    for p in ch:
                        cL.append(p.shape)
            # print(cL)

            lastAling = aligns[-1]

            numChop = -1
            for pyCont in aligns:
                numChop += 1

                base = pyBase.shape

                [pyOne, pyTwo] = chopList[numChop]
                rChop = rangoChop[numChop]
                rChopPy = rangoChopPy[numChop]

                nW = pyOne.numWire
                pyW = pyWireList[nW]
                pyPlList = pyW.planes

                shapeOne = pyOne.shape
                shapeTwo = pyTwo.shape

                cutterList = [shapeOne, shapeTwo]

                if numChop == 0:
                    prior = self.prior
                    later = self.later

                    if prior.numWire == pyBase.numWire:
                        if prior.numGeom not in control:
                            if prior.chopedList or prior.frontedList:
                                pass
                            elif not prior.alignedList:
                                pp = prior.shape.copy()
                                if cL:
                                    gS = prior.geomShape
                                    pp = self.cutting(pp, cL, gS)
                                # print('prior')
                                cutterList.append(pp)
                            elif prior.alignedList and not pyBase.chopedList:
                                cutterList.append(prior.selectShape())

                    if later.numWire == lastAling.numWire:
                        # if later.numGeom not in lastAling.control:
                        # TODO
                        if later.chopedList or later.frontedList:
                            pass
                        elif not later.alignedList:
                            ll = later.shape.copy()
                            if cL:
                                gS = later.geomShape
                                ll = self.cutting(ll, cL, gS)
                            # print('later')
                            cutterList.append(ll)
                        elif later.alignedList and not pyBase.chopedList:
                            cutterList.append(later.selectShape())

                simulatedC = simulatedChops[numChop]

                cutterList.extend(simulatedC)

                base = base.cut(cutterList, _Py.tolerance)
                # print('base.Faces ', base.Faces, len(base.Faces))

                gA = self.geomAligned
                # print('geomAligned ', gA, gA.firstVertex(True).Point, gA.lastVertex(True).Point)
                number = 0
                for ff in base.Faces:
                    section = ff.section([gA], tolerance)
                    if section.Edges:
                        number += 1
                # print('number ', number)

                if number <= 2:
                    # print('a no divide')

                    gS = pyBase.geomShape
                    base = self.selectFace(base.Faces, gS)
                    pyBase.shape = base
                    cutList.append(base)

                    shapeOne = pyOne.shape
                    fList = shapeOne.Faces
                    if len(fList) > 1:
                        ff = fList[1]
                        section = ff.section([base], tolerance)
                        if not section.Edges:
                            shapeOne = Part.makeCompound(fList[:1])
                            pyOne.shape = shapeOne

                    shapeTwo = pyTwo.shape
                    fList = shapeTwo.Faces
                    if len(fList) > 1:
                        ff = fList[1]
                        section = ff.section([base], tolerance)
                        if not section.Edges:
                            shapeTwo = Part.makeCompound(fList[:1])
                            pyTwo.shape = shapeTwo

                else:
                    # print('b divide')

                    gS = pyBase.geomShape
                    ff = self.selectFace(base.Faces, gS)
                    pyBase.shape = ff
                    cutList.append(ff)

                    gS = pyTwo.geomShape
                    f = shapeTwo.Faces[0]
                    f = self.cutting(f, [ff], gS)
                    fList = [f]
                    shapeTwo = Part.makeCompound(fList)
                    pyTwo.shape = shapeTwo

                    gS = pyCont.geomShape
                    ff = self.selectFace(base.Faces, gS)
                    pyCont.shape = ff
                    cutList.append(ff)

                    try:
                        for pyP in aligns[numChop + 1:]:
                            pyP.angle = [pyCont.numWire, pyCont.numGeom]
                    except IndexError:
                        pass

                    pyCont.angle = pyBase.angle

                    gS = pyOne.geomShape
                    f = shapeOne.Faces[0]
                    f = self.cutting(f, [ff], gS)
                    fList = [f]
                    shapeOne = Part.makeCompound(fList)
                    pyOne.shape = shapeOne

                    pyBase = aligns[numChop]

                if simulatedC:
                    # rChop with base and cont
                    # for nn, pyPl in map(None, rChop, rChopPy):
                    for pyPl in rChopPy:
                        if not (pyPl.chopedList or pyPl.alignedList):
                            pyPl.cuttingPyth(cutList)
                            # print('rangoChop ', nn)'''

    def processRango(self, rango, rangoPy, pyPlane, numWire, enormousBase):

        '''processRango(self, rango, rangoPy, pyPlane, numWire, enormousBase)'''

        control = pyPlane.control
        rC, cutList, oppCutList = [], [], []
        for nn, pyPl in zip(rango, rangoPy):
            # print('nn ',nn)
            if nn not in control:

                if pyPl.alignedList:
                    # print('a')

                    if not pyPlane.virtualized:
                        pyAli = pyPl.selectAlignmentBase()
                        if pyAli and pyAli != self:
                            pl = pyAli.simulatedAlignment
                            cutList.extend(pl)
                            oppCutList.extend(pl)

                elif not pyPl.chopedList:
                    # print('b')

                    pl = pyPl.shape.copy()

                    if not pyPl.frontedList:
                        # print('b1')
                        oppCutList.append(pl)

                    if pyPl.arrow:
                        # print('b2')
                        gShape = pyPl.geomShape
                        pl = self.cutting(pl, [enormousBase], gShape)

                    cutList.append(pl)
                    rC.append(pl)

        # print('rC ', rC)
        rC = Part.makeCompound(rC)

        # print('cutList ', cutList)
        # print('oppCutList ', oppCutList)
        return rC, cutList, oppCutList

    def processRear(self, rear, pyPl, numWire):

        '''processRear(self, rear, pyPl, numWire)'''

        pl = None

        if pyPl.alignedList:
            # print('r1')

            pyAli = pyPl.selectAlignmentBase()
            if not pyAli:
                pyAliList = pyPl.alignedList
                try:
                    pyAli = pyAliList[0]
                except IndexError:
                    pass
            if pyAli and pyAli != self:
                # print('pyAli ', pyAli.base.numGeom)
                pl = pyAli.simulatedAlignment

        elif pyPl.frontedList:
            # print('r2')
            pl = [pyPl.bigShape]

        elif not pyPl.chopedList:
            # print('r3')
            pl = [pyPl.shape]

        return pl

    def processAlignRear(self, rearAlign, pyWire, num, enormous):

        ''''''

        numGeom = rearAlign.numGeom

        if num == 1:
            # print('1')
            point = pyWire.coordinates[numGeom]
        else:
            # print('2')
            point = pyWire.coordinates[numGeom + 1]

        # print('point ', point)
        rA = rearAlign.shape.copy()
        rA = rA.cut([enormous], _Py.tolerance)
        # print(rA.Faces)
        rA = self.selectFacePoint(rA, point)

        return rA

    def processBetween(self, rango, pyPlaneList):

        '''processBetween(self, rango, pyPlaneList)'''

        cutList = []
        for nn in rango:
            pyPl = pyPlaneList[nn]
            pl = None

            if pyPl.alignedList:

                pl = None

            elif not pyPl.chopedList and not pyPl.frontedList:

                pl = [pyPl.shape]

            if pl:
                cutList.extend(pl)
                # print('rangoBetween ', nn)

        return cutList

    def postProcess(self):

        '''postProcess(self)'''

        # print('# self.Base ', self.base.numGeom)

        '''pyFace = self.pyFace
        if pyFace.mono:
            return'''

        pyFace = self.pyFace
        mono = pyFace.mono

        # recollects

            # rearChop with chop and alignment. Rango and rear with opp chop

            if pyO.shape and pyO.rear:
                pyPlList = pyWireList[pyO.numWire].planes
                rOne = pyO.rear[-1]
                pyRearPl = pyPlList[rOne]
                if not pyRearPl.aligned and not pyRearPl.choped:
                    pyRearPl.cuttingPyth([pyO.shape] + bList)

                    two = pyT.shape
                    if two:
                        rango = pyO.rango[-1] + [rOne]
                        for nn in rango:
                            pyPl = pyPlList[nn]
                            if not pyPl.choped and not pyPl.aligned:
                                pyPl.cuttingPyth([two])

            if pyT.shape and pyT.rear:
                pyPlList = pyWireList[pyT.numWire].planes
                rTwo = pyT.rear[0]
                pyRearPl = pyPlList[rTwo]
                if not pyRearPl.aligned and not pyRearPl.choped:
                    pyRearPl.cuttingPyth([pyT.shape] + bList)

                    one = pyO.shape
                    if one:
                        rango = pyT.rango[0] + [rTwo]
                        for nn in rango:
                            pyPl = pyPlList[nn]
                            if not pyPl.choped and not pyPl.aligned:
                                pyPl.cuttingPyth([one])

            # between rears with chops

            if pyO.shape and pyO.rear and\
               pyT.shape and pyT.rear:
                pyWireOne = pyWireList[pyO.numWire]
                between = self.rang(pyWireOne, rTwo, rOne, 'forward')
                for nn in between:
                    pyPl = pyPlList[nn]
                    if not pyPl.choped and not pyPl.aligned:
                        pyPl.cuttingPyth(cutList)

        # rangoRear vs rangoChop

        chops = self.chops
        rangoChop = self.rango
        # print 'rangoChop ', rangoChop
        rangoRear = self.rangoRear
        # print 'rangoRear ', rangoRear
        w1 = self.prior.numWire
        pyPlaneList = _Py.pyFace.wires[w1].planes

        rearList = []

        for pyPl in rangoRear[1]:

            if not (pyPl.choped or pyPl.fronted) and pyPl.shape:

                pl = pyPl.shape
                rearList.append(pl)

        if rearList:
            # print 'rearList ', rearList

            numChop = -1
            for rC in rangoChop:
                numChop += 1
                [pyOne, pyTwo] = chops[numChop]
                if pyOne.numWire == w1:

                    chopList = []
                    for r in rC:
                        pyPl = pyPlaneList[r]
                        if not pyPl.choped and not pyPl.aligned:
                            pl = pyPl.cuttingPyth(rearList)
                            chopList.append(pl)

                    if chopList:
                        # print 'chopList ', chopList
                        for pyPl in rangoRear[1]:
                            if not (pyPl.choped or pyPl.fronted):
                                pl = pyPl.cuttingPyth(chopList)

        # into rangoChop

        for rC in rangoChop:
            if len(rC) > 2:
                chopList = []
                planeList = []
                for r in rC:
                    pyPl = pyPlaneList[r]
                    if pyPl.choped or pyPl.aligned:
                        break
                    pl = pyPl.shape
                    chopList.append(pl.copy())
                    planeList.append(pyPl)

                num = -1
                for pyPl in planeList:
                    num += 1
                    pop = chopList.pop(num)
                    if chopList:
                        pyPl.cuttingPyth(chopList)
                    chopList.insert(num, pop)

        # alignment with choped rangoRear

        rearList = []
        for pyPl in rangoRear[1]:
            if pyPl.choped:
                # print 'a'
                pl = pyPl.shape
                if pl:
                    rearList.append(pl)

        if rearList:
            # print 'rearList ', rearList
            pyBase.cuttingPyth(rearList)
            for pyPl in self.aligns:
                if pyPl.shape:
                    pyPl.cuttingPyth(rearList)

    def rangging(self, reset):

        '''rangging(self)'''

        # print '### rangging ', (self.base.numWire, self.base.numGeom)

        pyWireList = _Py.pyFace.wires
        pyBase = self.base
        base = pyBase.shape
        bList = [base]
        for pyPl in self.aligns:
            if pyPl.shape:
                bList.append(pyPl.shape)
        # print('bList ', bList)
        self.aliShape = bList

        w1 = self.prior.numWire
        pyPlaneList = _Py.pyFace.wires[w1].planes

        # chops

        rangoChop = self.rango
        rangoRear = self.rangoRear
        rangoChopPy = self.rangoPy
        numChop = -1
        for [pyOne, pyTwo] in self.chops:
            numChop += 1
            rChopPy = rangoChopPy[numChop]
            pyPlList = pyWireList[pyOne.numWire].planes

            cutList = []
            pyO = self.selectPlane(pyOne.numWire, pyOne.numGeom)
            if pyO.shape:
                cutList.append(pyO.shape)
            pyT = self.selectPlane(pyTwo.numWire, pyTwo.numGeom)
            if pyT.shape:
                cutList.append(pyT.shape)
            # print('cutList ', cutList)

            # rangoChop with real chops

            if cutList:
                for pyPl in rChopPy:
                    # pyPl = pyPlList[nn]
                    if not pyPl.chopedList and not pyPl.alignedList:
                        pyPl.cuttingPyth(cutList)
                        # print('rangoChop ', nn)

            # TODO if cross chop with rangoChop


            # rearChop with chop and alignment. Rango and rear with opp chop

            if pyO.shape and pyO.rear:
                pyPlList = pyWireList[pyO.numWire].planes
                rOne = pyO.rear[-1]
                pyRearPl = pyPlList[rOne]
                if not pyRearPl.alignedList and not pyRearPl.chopedList:
                    pyRearPl.cuttingPyth([pyO.shape] + bList)

                    two = pyT.shape
                    if two:
                        rango = pyO.rango[-1] + [rOne]
                        for nn in rango:
                            pyPl = pyPlList[nn]
                            if not pyPl.chopedList and not pyPl.alignedList:
                                pyPl.cuttingPyth([two])

            if pyT.shape and pyT.rear:
                pyPlList = pyWireList[pyT.numWire].planes
                rTwo = pyT.rear[0]
                pyRearPl = pyPlList[rTwo]
                if not pyRearPl.alignedList and not pyRearPl.chopedList:
                    pyRearPl.cuttingPyth([pyT.shape] + bList)

                    one = pyO.shape
                    if one:
                        rango = pyT.rango[0] + [rTwo]
                        for nn in rango:
                            pyPl = pyPlList[nn]
                            if not pyPl.chopedList and not pyPl.alignedList:
                                pyPl.cuttingPyth([one])

            # between rears with chops

            if not mono:

                if pyO.shape and pyO.rear and\
                   pyT.shape and pyT.rear:
                    pyWireOne = pyWireList[pyO.numWire]
                    between = self.rang(pyWireOne, rTwo, rOne, 'forward')
                    for nn in between:
                        pyPl = pyPlList[nn]
                        if not pyPl.chopedList and not pyPl.alignedList:
                            pyPl.cuttingPyth(cutList)

        # rangoRear vs rangoChop

        if not mono:

            chops = self.chops

            rearList = []

            for pyPl in rangoRear[1]:

                if not (pyPl.chopedList or pyPl.frontedList) and pyPl.shape:

                    pl = pyPl.shape
                    rearList.append(pl)

            if rearList:
                # print('rearList ', rearList)

                numChop = -1
                for rC in rangoChop:
                    numChop += 1
                    [pyOne, pyTwo] = chops[numChop]
                    if pyOne.numWire == w1:

                        chopList = []
                        for r in rC:
                            pyPl = pyPlaneList[r]
                            if not pyPl.chopedList and not pyPl.alignedList:
                                pl = pyPl.cuttingPyth(rearList)
                                chopList.append(pl)

                        if chopList:
                            # print('chopList ', chopList)
                            for pyPl in rangoRear[1]:
                                if not (pyPl.chopedList or pyPl.frontedList):
                                    pl = pyPl.cuttingPyth(chopList)

        # into rangoChop

        for rC in rangoChop:
            if len(rC) > 2:
                chopList = []
                planeList = []
                for r in rC:
                    pyPl = pyPlaneList[r]
                    if pyPl.chopedList or pyPl.alignedList:
                        break
                    pl = pyPl.shape
                    chopList.append(pl.copy())
                    planeList.append(pyPl)

                num = -1
                for pyPl in planeList:
                    num += 1
                    pop = chopList.pop(num)
                    if chopList:
                        pyPl.cuttingPyth(chopList)
                    chopList.insert(num, pop)

        # alignment with choped rangoRear

        rearList = []
        for pyPl in rangoRear[1]:
            if pyPl.chopedList:
                # print('a')
                pl = pyPl.shape
                if pl:
                    rearList.append(pl)

        if rearList:
            # print('rearList ', rearList)
            pyBase.cuttingPyth(rearList)
            for pyPl in self.aligns:
                if pyPl.shape:
                    pyPl.cuttingPyth(rearList)
