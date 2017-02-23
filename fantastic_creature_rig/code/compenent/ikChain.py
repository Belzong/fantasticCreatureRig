import maya.cmds as mc


class ikChain():
    def __init__(self, name='test', startJoint=None, endEffector=None, solver='ikRPsolver',
                 sticky=False, createCurve=False):
        self.ikChain = mc.ikHandle(n=name, startJoint=startJoint, endEffector=endEffector, solver=solver,
                                   sticky=sticky, createCurve=createCurve)[0]
        self.name = name
        self.startJoint = startJoint
        self.effector = endEffector
        self.midChain = mc.listConnections(startJoint)[0]

    def _distTool(self, type='ik', makeConstraint=True):
        # mise en place de mesure tool pour calculer la distance des joints en prevision d'un pole vector ou stretch
        # calcul des position des joints
        sjPos = mc.xform(self.startJoint, q=True, ws=True, t=True)
        midPos = mc.xform(self.midChain, q=True, ws=True, t=True)
        eePos = mc.xform(self.effector, q=True, ws=True, t=True)

        # creation des distance tool
        distStart = mc.distanceDimension(sp=sjPos, ep=midPos)
        distStartName = mc.rename((mc.listRelatives(distStart, parent=True)[0]), '{}Start_{}_dist'.format(type, self.name))
        distStart = mc.listRelatives(distStartName)[0]

        distEnd = mc.distanceDimension(sp=midPos, ep=eePos)
        distEndName = mc.rename((mc.listRelatives(distEnd, parent=True)[0]), '{}End_{}_dist'.format(type, self.name))
        distEnd = mc.listRelatives(distEndName)[0]

        # rename locator
        locStart = mc.rename(mc.listConnections(distStart)[0], '{}Start_{}_loc'.format(type, self.name))
        locMid = mc.rename(mc.listConnections(distStart)[1], '{}Mid_{}_loc'.format(type, self.name))
        locEnd = mc.rename(mc.listConnections(distEnd)[1], '{}End_{}_loc'.format(type, self.name))

        # clean outliner
        ikDistGrp = mc.group(n='{}Dist_{}_grp'.format(type, self.name), em= True)
        ikMeasureGrp = mc.group(n='{}Dist_{}_measure_grp'.format(type, self.name), em=True, parent=ikDistGrp)
        ikDistLocGrp = mc.group(n='{}Dist_{}_loc_grp'.format(type, self.name), em=True, parent=ikDistGrp)

        [mc.parent(loc, ikDistLocGrp) for loc in (locStart,locMid,locEnd)]
        [mc.parent(dist, ikMeasureGrp) for dist in (distStartName, distEndName)]

        if makeConstraint and type == 'ik':
            for loc, joint in zip([locStart,locMid,locEnd],[self.startJoint, self.midChain, self.effector]):
                mc.pointConstraint(joint, loc, mo=False)

        return {'distanceSt': distStartName, 'distanceEnd': distEndName, 'locators': [locStart, locMid, locEnd]}


ik = ikChain(startJoint='joint1', endEffector='joint3')

test2 = ik._distTool()
print test2