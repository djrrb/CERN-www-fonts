import os
from fontmake.font_project import FontProject

makeTTF = True
makeWOFF = True

baseDir = os.path.split(__file__)[0]


if makeTTF:

    # gather UFOs from build script parent folder
    paths = []
    for filename in os.listdir(os.path.abspath(baseDir)):
        if filename.endswith('.ufo'):
            paths.append(filename)

    # make fontmake project
    project = FontProject()
    project.run_from_ufos(
        paths, 
        output=("ttf"),
        remove_overlaps=False, 
        reverse_direction=False, 
        use_production_names=False)

if makeWOFF:

    #define woff and woff2 tools
    sfnt2woffPath = 'sfnt2woff-zopfli'
    sfnt2woff2Path = 'woff2_compress'
    returnedInfo = os.system(sfnt2woffPath)
    returnedInfo2 = os.system(sfnt2woff2Path)
    # hack for hardcoded absolute paths as fallback, sorry!
    if returnedInfo == 32512:
        sfnt2woffPath = u"~/Documents/Tools/fontGenerate/sfnt2woff-zopfli/sfnt2woff-zopfli"
        sfnt2woff2Path = u"~/Documents/Tools/fontGenerate/woff2/woff2_compress"

    # generate woff and woff2
    masterTTFPath = os.path.join(os.path.abspath(baseDir), 'master_ttf')
    masterWebPath = os.path.join(os.path.abspath(baseDir), 'master_web')
    
    # make separate folder for webfonts
    if not os.path.exists(masterWebPath):
        os.mkdir(masterWebPath)
    
    for filename in os.listdir(masterTTFPath):
        if filename.endswith('.ttf') or filename.endswith('.otf'):
            # get absolute path
            filePath = os.path.join(masterTTFPath, filename)

            # WOFF
            woffCommand = "{sfnt2woffPath} {path}".format(sfnt2woffPath=sfnt2woffPath, path=filePath)
            os.system(woffCommand)
            woffFilename = filename.replace('.ttf', '.woff').replace('.otf', '.woff')
            if os.path.exists( os.path.join(masterTTFPath, woffFilename) ):
                os.rename( os.path.join(masterTTFPath, woffFilename) , os.path.join(masterWebPath, woffFilename) )

            # WOFF2
            woff2Command = "{woff2Path} {path}".format(woff2Path=sfnt2woff2Path, path=filePath)
            os.system(woff2Command)
            woff2Filename = filename.replace('.ttf', '.woff2').replace('.otf', '.woff2')
            if os.path.exists( os.path.join(masterTTFPath, woff2Filename) ):
                os.rename( os.path.join(masterTTFPath, woff2Filename) , os.path.join(masterWebPath, woff2Filename) )


print ("DONE!")

