"""

module for making rig structure and rig module

"""

import maya.cmds as mc

from . import control

sceneObjectType= 'rig'

class Base():
    """
    class for building top rig base structure
    """
    
    def __init__(self,
                 characterName = 'new',
                 sceneSetup = 1.00,
                 mainCtrlAttachObj = ''
                 ):
        
        """
        @param charaterName: str, name of the character rig 
        @param sceneSetup: float, scale of scene
        
        @return: Nothing
        
        
        
        """
        
        
        # creation du groupe general du rig
        self.topGrp = mc.group(n='%s_character_grp' % characterName, em = True)
        self.rigGrp = mc.group(n='%s_rig_grp' % characterName, em = True, p = self.topGrp)
        self.modelGrp = mc.group(n='%s_geometry_grp' % characterName, em = True, p =  self.topGrp)
        
        characterNameAt = 'characterName'
        sceneObjectTypeAt = 'sceneObjectType'
        
        for at in [characterNameAt, sceneObjectTypeAt]:
            mc.addAttr(self.topGrp, ln = at, dt = 'string')
    
        mc.setAttr(self.topGrp + '.' + characterNameAt, characterName, l = 1, type = 'string')
        mc.setAttr(self.topGrp + '.' + sceneObjectTypeAt, sceneObjectType, l = 1, type = 'string')
        
        # creation of global ctrl
        masterCtrl = control.Control(side ='C', name ='Master', radius =sceneSetup * 20, parent = self.rigGrp, lockChannels = ['v'], normal = [0, 1, 0])
        globCtrl = control.Control(side ='C', name ='global', radius =sceneSetup * 15, parent = masterCtrl.ctrl, lockChannels = ['v', 's'], normal = [0, 1, 0])
        
        for axis in ['y','z']:
            mc.connectAttr('%s.sx'% masterCtrl.ctrl, '%s.s%s' % (masterCtrl.ctrl, axis))
            mc.setAttr('%s.s' % masterCtrl.ctrl, k = False)
            
        
        # make skeleton group
        self.skeletonGrp = mc.group(n='%s_skeleton_grp' % characterName, em = True, p = globCtrl.ctrl)
        self.modulesGrp = mc.group(n='%s_modules_grp' % characterName, em = True, p = globCtrl.ctrl)
        self.partGrp = mc.group(n='%s_parts_grp' % characterName, em = True, p = self.rigGrp)
        # remove inherit transform for part Grp.
        mc.setAttr(self.partGrp + '.it', 0 , l = 1)
        
        # make main control
        mainCtrl = control.Control(side ='C', name ='main', radius =sceneSetup * 1, parent = self.rigGrp, lockChannels = ['v', 't', 'r', 's'], normal = [1, 0, 0], translateTo= mainCtrlAttachObj)
        
        self._adjustMainCtrlShape(mainCtrl, sceneSetup)
        
        if mc.objExists(mainCtrlAttachObj):
            mc.parentConstraint(mainCtrlAttachObj, mainCtrl.ctrlOff, mo = True)
            
        mainVisAts = ['modelVis', 'jointVis']
        mainDispAts= ['modelDisp','jointDisp']
        mainObjList = [self.modelGrp, self.skeletonGrp]
        mainObjVisDvList = [1,0]
        for at, obj, dfVal in zip(mainVisAts, mainObjList, mainObjVisDvList):
            mc.addAttr(mainCtrl.ctrl, ln = at, at = 'enum', enumName = 'off:on', k = True, dv = dfVal )
            mc.setAttr('%s.%s' % (mainCtrl.ctrl,at), cb = True)
            mc.connectAttr('%s.%s' % (mainCtrl.ctrl,at), obj + '.v')
            
        for at, obj in zip(mainDispAts, mainObjList):
            mc.addAttr(mainCtrl.ctrl, ln = at, at = 'enum', enumName = 'normal:template:reference', k = True, dv = 2 )
            mc.setAttr('%s.%s' % (mainCtrl.ctrl,at), cb = True)
            mc.setAttr('%s.ove' % obj, 1)
            mc.connectAttr('%s.%s' % (mainCtrl.ctrl,at), obj + '.ovdt')    
            
             
    def _adjustMainCtrlShape(self, ctrlObj, scale):
        
        # adjust shape of the main control
        ctrlShapes = mc.listRelatives(ctrlObj.ctrl, s = 1, type = 'nurbsCurve')
        cls = mc.cluster(ctrlShapes)[1]
        mc.setAttr('%s.ry' % cls, 90)
        mc.move(8* scale, ctrlObj.ctrlOff, moveY = True, relative = True)
        mc.delete(cls)
        
            
class Module():
    """
    class for building module rig structure (cloth, belt, etc...)
    """
    def __init__(self,
                 name = 'new',
                 side = 'L',
                 baseObj = None
                 ):     
        """
        @param name: str, name of the module
        @param side: L R C, define the module side
        @param baseObj: str, define the parent of the module
        
        
        """
        self.topGrp = mc.group(n= '%s_%s_Module_grp' % (side, name), em = True)
        self.controlGrp = mc.group(n= '%s_%s_Controls_grp' % (side, name), em = True, p = self.topGrp)
        self.joints = mc.group(n= '%s_%s_Joints_grp' % (side, name), em = True, p = self.topGrp)
        self.partsGrp = mc.group(n='%s_%s_Parts_grp' % (side, name), em = True, p = self.topGrp)
        self.partsNoTransGrp = mc.group(n='%s_%s_PartsNoTrans_grp' % (side, name), em = True, p = self.topGrp)
        
        mc.setAttr(self.partsNoTransGrp + '.it', 0, l= 1)
            
        # parent module 
        if baseObj:
            mc.parent(self.topGrp, baseObj.modulesGrp)
            
            
            
            
            