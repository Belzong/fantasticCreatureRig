"""
modularSkeleton @ base

Create the proxy skeleton to place element

"""

import maya.cmds as mc
import maya.mel as mel


class genModularSpline():
    
    def __init__(self, side = 'C', name = 'qSpine', parent = None, keepOffset = True):  
        """
        creation of spline for vertabrae spine / neck / tail with locator 
        
        @param name: str, qSpine / hSpine / neck / tail
        @param parent: str, parent la spline par rapport a l element 
        
        """
        
        self.curve = ''
        # creation des differentes forme de spine
        if name == 'qSpine':
            self.curve = mel.eval('curve -d 3 -p 0 0 0 -p 0 -0.182686 2.554175 -p 0 -0.548058 7.662525 -p 0 -0.296248 11.239302 -p 0 0.0740619 14.430958 -p 0 -0.343976 15.701256 -p 0 -0.552995 16.336406 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 4 -k 4 ;')
    
        elif name == 'hSpine':
            self.curve = mel.eval('curve -d 3 -p 0 0 0 -p 0 1.289913 0.54511 -p 0 3.869739 1.63533 -p 0 8.521045 -0.541321 -p 0 9.537737 0.172862 -p 0 10.046083 0.529954 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 3 -k 3 ;')

        elif name == 'neck':
            self.curve = mel.eval('curve -d 3 -p 0 0 0 -p -0.58145 0.751154 0 -p -1.74435 2.253462 0 -p -4.259692 2.4056 0 -p -5.517363 2.481668 0 -k 0 -k 0 -k 0 -k 1 -k 2 -k 2 -k 2 ;')
        
        elif name == 'tail':
            self.curve = mel.eval('curve -d 3 -p 0 0 0 -p 0 0 -1.875 -p 0 0 -5.625 -p 0 0 -7.5 -p 0 0 -12.375 -p 0 0 -14.125 -p 0 0 -15 -k 0 -k 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 4 -k 4 ;')
        
        else:
            pass
        
        # security line for name
        if mc.objExists('%s_%s1' % (side, name)):
            for i in range(9999):
                print 'i = %s' % i
                if not mc.objExists('%s_%s%s' % (side, name, i+1)):
                    name = '%s%d'  % (name, i+1)
                    break
        else:
            name =  '%s1' % name
        print name     
        self.curve = mc.rename(self.curve, '%s_%s'% (side, name))
        mel.eval('rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 2 -d 3 -tol 0.01 "%s";' % self.curve)
        
        # set inherit transform curve to 0
        mc.setAttr('%s.inheritsTransform' % self.curve, 0)
        
        # cluster on curve creation
        clusterList = []
        curveCVs = mc.ls('%s.cv[:]' %(self.curve), fl = True)
        
        if curveCVs: # Check if we found any cvs
            for i, cv in enumerate(curveCVs):
                cls = mc.cluster(cv)[1] # Create cluster on a cv
                cls = mc.rename(cls, '%s%dHandle_cls' % (self.curve, i+1)) 
                clusterList.append(cls)
        
        # cluster group creation
        clsGrp = mc.group(n = '%s_clsGrp' % self.curve, em = True)
        mc.hide(clsGrp)
        for cls in clusterList:
            mc.parent(cls, clsGrp)
      
      
        # creation des locators start / mid / end
        locSpine = []
        locSide = ['Start', 'Mid', 'End']
        locPos =  [0,2,4]
        locGrp = mc.group(n='%s_locController_grp' % self.curve, em = True)
        for i, pos in enumerate(locSide):
            loc = mc.spaceLocator(n='%s%s_loc' % (self.curve,pos))[0]
            mc.delete(mc.parentConstraint(clusterList[locPos[i]],loc , mo = False))
            mc.parent(loc, locGrp)
            locSpine.append(loc)
            
        mc.parentConstraint(locSpine[0], clusterList[0], mo = True)
        mc.parentConstraint(locSpine[0], clusterList[2], clusterList[1],mo = True)
        mc.parentConstraint(locSpine[1], clusterList[2], mo = True)
        mc.parentConstraint(locSpine[2], clusterList[2], clusterList[3],mo = True)
        mc.parentConstraint(locSpine[2], clusterList[4], mo = True)

        # group de rangement
        masterGrp = mc.group(n= '%s_setupGrp' % self.curve, em = True)
        
        # replace pivot to loc start position
        mc.delete(mc.parentConstraint(locSpine[0], masterGrp, mo = False))
        mc.makeIdentity(masterGrp, a = True)
        
        # parent each group to master grp
        mc.parent(self.curve,masterGrp)
        mc.parent(clsGrp, masterGrp)
        mc.parent(locGrp, masterGrp)
        
        if parent:
            mc.parentConstraint(parent, masterGrp, mo = keepOffset)
  

            
        
def rebuildCurveToJointChain(nb = 5, name = '', curveSel = None, parent = None, keepOffset = False):
    if curveSel:
        # rebuild de la curve suivant le nombre de cv
        mc.rebuildCurve(curveSel, d = 3, rt = 0, s= nb)
        
        if curveSel.endswith('_crv'):
            name = curveSel.split('_crv')[0]
        else:
            name = curveSel
        # list each cv on the curve
        cvs = mc.ls(curveSel + '.cv[:]', fl = True)
        
        # remove to the list the cv[1] and the second lastest cv
        del cvs[-2], cvs[1]
        mc.select(cl=1)
        
        # creation of joint per cv with the cvs list
        jntList = []
        i = 1
        for cv in cvs:
            # get the position of cv in the world space
            pos = mc.xform(cv, q = True, ws = True, t = True)
            jnt = mc.joint(n = '%s_%d_jnt' % (name, i), p = pos)
            jntList.append(jnt)
            i = i +1 
    
        if parent:
            mc.delete(mc.pointConstraint( parent, jntList[0], mo = keepOffset))
            
            mc.parent(jntList[0], parent)
    else:
        mc.error('No curve was specified, the joint creation on curve has been aborted')
  
class genModularLeg():
    
    def __init__(self, name = 'qLeg', parent = None):
        """
        creation of leg system
        
        @param name: str, qLeg / qInvLeg / qHuman / iLeg  
        @param parent: str, parent le systeme par rapport a l element designe 
        
        """
        pass
        
        