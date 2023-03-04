import numpy as np
from scipy.spatial.transform import Rotation as R

class Object():
    def __init__(self, name, position=None, orientation=None, fov=None):
        """
            position = position in 3d.
            orientation = [yaw,pitch,roll]
        """
        #self.label = label
        if position is None:
            self.position = np.random.rand(3)*1.0
        else:
            self.position = np.array(position)                
        
        #These bits only relevant for cameras (could subclass)
        if orientation is None:
            self.orientation = np.zeros(3) #np.random.rand(3)*np.pi*2
        else:
            self.orientation = np.array(orientation)
                
        if fov is None:
            self.fov = 0.577*2 #60deg fov
        else:
            self.fov = fov
        self.vfov = np.tan(self.fov/2)*(3/4)
        self.hfov = np.tan(self.fov/2)
        self.observations = []
        self.camera = False
        self.constraints = []
        self.name = name
    def getnumparam(self):
        if self.camera:
            return 6
        else:
            return 3
        
    def getparams(self):
        if self.camera:
            return np.r_[self.position,self.orientation]
        else:
            return self.position
        
    def setparams(self,v):
        if self.camera:
            self.orientation = v[3:6]
            self.position = v[0:3]
        else:
            self.position = v[0:3]
        
    def addobservation(self, target, coords):
        self.observations.append({'target':target, 'coords':coords})
        
    def addconstraintdistance(self,target,dist):
        self.constraints.append({'target':target,'dist':dist})

    def getpixel(self, target):
        """
        If this is a camera, then for a target object, get the position of the object in the image
        """
        print(target.position, self.position)
        p = np.array(target.position - self.position)
        r1 = R.from_euler('z', self.orientation[0], degrees=False) #yaw
        r2 = R.from_euler('Y', self.orientation[1], degrees=False) #pitch (intrinsic rotation around y axis)    
        r3 = R.from_euler('X', self.orientation[2], degrees=False) #roll (intrinsic rotation around x axis)    

        pvec = r3.apply(r2.apply(r1.apply(p)))
        print(pvec)
        #print(p,pvec)
        if len(pvec.shape)==1:
            pvec = pvec[None,:]
        #1024 x 768 or in our case 2048 x 1536
        #if pvec[:,0]<10:
        #    z = np.log(1+np.exp(pvec[:,0]*2))/2
        #else:
        #    z = pvec[:,0]
        z = pvec[0,0]
        #print(z)
        if np.abs(z)<0.0001: z = 0.0001
        if z<0:
            loss = -z
        else:
            loss = 0
        res = np.array([1024+1024*(-pvec[0,1]/z)/self.hfov,(1024+1024*(pvec[0,2]/z/self.vfov))*0.75])
        print(res)
        print("---")
        return res, loss
        
        
import json
def loadobjects(jsonfilename):
    data = json.load(open(jsonfilename,'r'))['items']
    for i in range(1,7): 
        if 'cam%d'%i not in data: data['cam%d'%i]={}
    objects = {}
    cameras = {}
    Ncam = 6
    for c in range(1,Ncam+1):
        name = 'cam%d' % c
        if name not in data:
            data[name]={'imgcoords':{}}

    for item, contents in data.items():
        print("Adding %s" % item)
        if 'initpos' in contents:
            initpos = contents['initpos']
        else:
            initpos = None

        obj = Object(item,initpos)
        objects[item] = obj
        if item[:3] == 'cam':
            cameras[item] = obj
            obj.camera=True

    for item, contents in data.items():
        if 'imgcoords' in contents:
            for cam,coords in contents['imgcoords'].items():
                if item in objects:
                    cameras[cam].addobservation(objects[item],coords)
        if 'constraintdistance' in contents:
            for target,dist in contents['constraintdistance'].items():
                objects[item].addconstraintdistance(objects[target],dist)


    for postid in range(16):
        if 'post%dtop' % postid in objects:
            objects['post%dtop' % postid].addconstraintdistance(objects['post%dbottom' % postid],0.568)
    return objects, cameras

