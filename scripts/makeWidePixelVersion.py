import os
import shutil

# how much wider
multiplier = 1.2

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
        f.save()
        f.close()