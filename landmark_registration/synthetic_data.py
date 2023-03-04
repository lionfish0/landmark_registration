data = {}
np.set_printoptions(precision=2,suppress=True)
simpos = {'a':[0,0],'b':[2,0],'c':[4,0],'cam1':[10,0],'cam2':[2,10],'cam3':[2,-10]}
camrot = {}
camrot['cam1'] = np.deg2rad(-90)
camrot['cam2'] = np.deg2rad(180)
camrot['cam3'] = np.deg2rad(0)
for item in ['a','b','c']:
    data[item] = {'imgcoords':{}}
for cam in ['cam1','cam2','cam3']:
    print(cam)
    rot = camrot[cam]
    for item in ['a','b','c']:
        newpos = np.array([[np.cos(rot),-np.sin(rot)],
        [np.sin(rot),np.cos(rot)]])@(np.array(simpos[item])-np.array(simpos[cam]))
        print(newpos)
        pix = 1024*(newpos[0]/(newpos[1]+0.0001))/np.tan((np.pi/3)/2)
        print(pix)
        if newpos[1]>0:
            #print(item,cam,newpos)
            if (pix>-1000) & (pix<1000):
                data[item]['imgcoords'][cam] = [pix+1024,768]
                
data['cam1'] = {'initpos':[0,5,0]}
data['cam2'] = {'initpos':[5,0,0]}
data['cam3'] = {'initpos':[-5,0,0]}
data['a']['constraintdistance'] = {'b':2.0}
data['b']['constraintdistance'] = {'c':2.0}                


for d,cont in data.items():
    if 'imgcoords' in cont:
        for cam,val in cont['imgcoords'].items():
            print("%s[%s] %9.1f %9.1f" % (d,cam,val[0],val[1]))
    else:
        print("%s -" % d)
