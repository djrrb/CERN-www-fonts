import os
import shutil

# how much wider
multiplier = 1.1
# how much pixel overlap
blockMultiplier = 1.35

scriptsFolder = os.path.abspath(os.path.split(__file__)[0])
sourcesFolder = os.path.join(os.path.split(scriptsFolder)[0], 'sources')
sourcesWideFolder = os.path.join(os.path.split(scriptsFolder)[0], 'sources-wide')
if not os.path.exists(sourcesWideFolder):
    os.mkdir(sourcesWideFolder)
for filename in os.listdir(sourcesFolder):
    if filename.endswith('.ufo'):
        srcPath = os.path.join(sourcesFolder, filename)
        path = os.path.join(sourcesWideFolder, filename.replace('.ufo', '-wide.ufo'))
        shutil.copytree(srcPath, path)
        try:
            f = OpenFont(path, showInterface=False)
        except:
            f = OpenFont(path, showUI=False)
        
        f.info.familyName += ' Wide'
    
        for g in f:
            for c in g.components:
                c.offset = c.offset[0] * multiplier, c.offset[1]
            for c in g.contours:
                c.scale((multiplier, 1))
            g.width *= multiplier
        
        g = f['block']
        bxw = g.box[2]-g.box[0]
        g.scale((blockMultiplier, 1))
        bxw2 = g.box[2]-g.box[0]
        diff = bxw2 - bxw
        g.move((-diff/2, 0))
        
        f.save()
        f.close()