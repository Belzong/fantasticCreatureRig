"""

control module for making rig controls


"""

import maya.cmds as mc
import maya.mel as mel


class Control():
    
    """
    
    class for building rig & basic control
    
    """
    def __init__(self,
                 scale = 1.00, 
                 side = 'C',
                 name = 'new',
                 shape = 'circle', 
                 translateTo = '',
                 rotateTo = '',
                 parent = '',
                 lockChannels = ['s','v'],
                 radius = 1.00,
                 normal = [1,0,0]
                 ):
        
        """
        @param scale: flaot, scale scen
        @param side: L R C, define the side of the controller (define the color at the same time
        @param name: str, module name
        @param shape: circle, triangle, cross, star, square
        @param translateTo: str, go to the specified object
        @param rotateTo: str, take the orientation of the specified object
        @param parent: str, parent the controller to the specified object
        @param lockChannels: list, list of attribute to lock
        @param radius: float, define the radius size of the controller
        @param normal: list like [1,1,1], define the normal orientation of the controller.
        

        
        
        """    
        ctrlObject = ''
            
        if shape == 'triangle':
            ctrlObject = mel.eval('curve -d 1 -p 0 0 2 -p -2 0 -2 -p 2 0 -2 -p 0 0 2 -k 0 -k 1 -k 2 -k 3 ;')[0]
            ctrlObject = mc.rename(ctrlObject, '%s_%s_ctrl'% (side, name))
        elif shape == 'cross':
            ctrlObject = mel.eval('curve -d 1 -p -1 0 1 -p -1 0 4 -p -3 0 4 -p 0 0 8 -p 3 0 4 -p 1 0 4 -p 1 0 1 -p 4 0 1 -p 4 0 3 -p 8 0 0 -p 4 0 -3 -p 4 0 -1 -p 1 0 -1 -p 1 0 -4 -p 3 0 -4 -p 0 0 -8 -p -3 0 -4 -p -1 0 -4 -p -1 0 -1 -p -4 0 -1 -p -4 0 -3 -p -8 0 0 -p -4 0 3 -p -4 0 1 -p -1 0 1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 ;')[0]
            ctrlObject = mc.rename(ctrlObject, '%s_%s_ctrl'% (side, name))
        elif shape == 'star':
            ctrlObject = mel.eval('curve -d 1 -p -2 0 -2 -p 0 0 -6 -p 2 0 -2 -p 6 0 0 -p 2 0 2 -p 0 0 6 -p -2 0 2 -p -6 0 0 -p -2 0 -2 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 ;')[0]
            ctrlObject = mc.rename(ctrlObject, '%s_%s_ctrl'% (side, name))
        elif shape == 'square':
            ctrlObject = mel.eval('curve -d 1 -p -3 0 -3 -p -3 0 3 -p 3 0 3 -p 3 0 -3 -p -3 0 -3 -k 0 -k 1 -k 2 -k 3 -k 4 ;')[0]
            ctrlObject = mc.rename(ctrlObject, '%s_%s_ctrl'% (side, name))
            
        elif shape == 'sphere':
            ctrlObject = mc.circle(n = '%s_%s_ctrl'% (side, name), ch = False, normal = [1,0,0], radius =radius )[0]
            addShape = mc.circle(n = '%s_%s_ctrl'% (side, name), ch = False, normal = [0,0,1], radius = radius)[0]
            mc.parent(mc.listRelatives(addShape, s = 1), ctrlObject, r = True, s = True)
            mc.delete(addShape)
            
        if not ctrlObject:
            ctrlObject = mc.circle(n = '%s_%s_ctrl'% (side, name), ch = False, normal = normal, radius = radius)[0]
                
            
        # define color of the controller
        ctrlShapes = mc.listRelatives(ctrlObject, s = 1)  
        [mc.setAttr('%s.ove' % s, 1) for s in ctrlShapes]
        if side == 'L' or side == 'l':
            [mc.setAttr('%s.ovc' % s, 13) for s in ctrlShapes]
        elif side == 'R'or side == 'r':
            [mc.setAttr('%s.ovc' % s, 6)  for s in ctrlShapes]
        elif side == 'C'or side == 'c':
            [mc.setAttr('%s.ovc' % s, 17) for s in ctrlShapes]
        else:
            [mc.setAttr('%s.ovc' % s, 22) for s in ctrlShapes]
    
        ctrlOffset = mc.group(n = '%s_%s_ctrlOff'% (side, name), em = True)
        
        # parent le ctrl au groupe
        mc.parent(ctrlObject, ctrlOffset)
        
        # translate ctrl
        if mc.objExists(translateTo):
            mc.delete(mc.pointConstraint(translateTo, ctrlOffset, mo = False))
            
        # rotation ctrl
        if mc.objExists(rotateTo):
            mc.delete(mc.orientConstraint(rotateTo, ctrlOffset, mo= False))
            
        # parent ctrl
        if mc.objExists(parent):
            mc.parent(ctrlOffset, parent)
            
        lockList = []    
        # lock ctrl channels and visibility
        for lockChannel in lockChannels:
            if lockChannel in ['t','r','s']:
                for axis in ['x','y','z']:
                    at  = lockChannel + axis
                    lockList.append(at)
                    
            else:
                lockList.append(lockChannel)
                
        for at in lockList:
            mc.setAttr('%s.%s' % (ctrlObject, at), lock = True, k = 0)
        

            
            
        
            
        # add public members
        self.ctrl = ctrlObject
        self.ctrlOff = ctrlOffset
        
        
            
        
        