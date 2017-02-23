import maya.cmds as mc
import maya.mel as mel



class genModularTorso():
    def __init__(self, jointSpineList = [],name = 'torso', sides = ['L', 'R'], step = 1, parent= True, offset = False):
        """
        creation of torso extras joint generic chain
        
        @param name: str, by default name = torso
        @param jointSpineList: list(str), list of chain joints to apply the new chain
        @param sides: list(str), defines the side creation by default ['L','R'] for left and right
        @param step: int, possibility to apply the chain on each joint or to step choin of your joinSpineList
        @param parent: bool, by default on True, define if the new chain will be parented with your join specified into the jointSpineList
        @param offset: bool, by default on True, define if the new chain keep his offset or stuck on the position of your join specified into the jointSpineList
        
        @return dict, of all chains master joint created.
        
        """
        self.masterJointChain = {}
        
        jointNames = ['Start', 'MidUp', 'MidDown', 'End']
        defaultPosList = [[1,0,0],[2,-1,0],[2,-3,0],[1,-4,0]]
        
        
        for i in range(0, len(jointSpineList), step):
            fullNameJoint = jointSpineList[i].split('_jnt')[0]
            nameJoint = fullNameJoint
            
            
            if nameJoint.startswith('C_'):
                nameJoint = fullNameJoint.split('C_')[1]
            elif nameJoint.startswith('R_'):
                nameJoint = fullNameJoint.split('R_')[1]
            elif nameJoint.startswith('L_'):
                nameJoint = fullNameJoint.split('L_')[1]
            
            # creation d un groupe temporaire pour le bon placement de la chaine de joint
            tmpGrp = mc.group(n = 'TMP_placement', em = True)
            mc.select(cl=1)
            
            for side in sides:
                

                torsoJntList = []
                for torsoName, pos in zip(jointNames, defaultPosList):
                    completeTorsoJointName = '%s_%s_%s%s_jnt' % (side, nameJoint, name, torsoName)
                    jnt = mc.joint(n= completeTorsoJointName, p = pos)
                    torsoJntList.append(jnt)
                if side == 'R':
                    curPos = mc.getAttr('%s.tx' % torsoJntList[0])
                    mc.setAttr('%s.tx' % torsoJntList[0], -2)
                    mc.setAttr('%s.ry' % torsoJntList[0], -180)
                    
                
            
                mc.parent(torsoJntList[0], tmpGrp)
                
            test = mc.listRelatives(tmpGrp)   
            
            mc.delete(mc.pointConstraint( jointSpineList[i],tmpGrp, mo = False))
            
            for elt in test:
                mc.parent(elt, w = True)
                
                if offset == False:
                    mc.delete(mc.pointConstraint(elt,jointSpineList[i], mo = False))
                if parent == True:
                    mc.parent(elt, jointSpineList[i])
                    
            mc.delete(tmpGrp)
                
        
            mc.select(cl=1)
            
            
            self.masterJointChain[torsoJntList[0]] = jointSpineList[i]
            
        
               
        sorted(self.masterJointChain)
            
test = genModularTorso(jointSpineList = ['joint1_jnt','joint2_jnt','joint3_jnt','joint4_jnt','joint5_jnt','joint6_jnt'], step = 2, parent = True)
print test.masterJointChain