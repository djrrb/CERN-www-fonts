import os
from fontmake.font_project import FontProject
from fontTools.designspaceLib import DesignSpaceDocument, SourceDescriptor, InstanceDescriptor, AxisDescriptor
from fontParts.world import OpenFont


def buildDesignSpace(sources, instances, axes):
    # use DesignSpaceDocument because it supports axis labelNames
    doc = DesignSpaceDocument()
    
    for source in sources:
        s = SourceDescriptor()
        s.path = source["path"]
        s.name = source["name"]
        s.copyInfo = source["copyInfo"]
        s.location = source["location"]
        s.familyName = source["familyName"]
        s.styleName = source["styleName"]
        doc.addSource(s)
    
    for instance in instances:
        i = InstanceDescriptor()
        i.location = instance["location"]
        i.familyName = instance["familyName"]
        i.styleName = instance["styleName"]
        doc.addInstance(i)
    
    for axis in axes:
        a = AxisDescriptor()
        a.minimum = axis["minimum"]
        a.maximum = axis["maximum"]
        a.default = axis["default"]
        a.name = axis["name"]
        a.tag = axis["tag"]
        for languageCode, labelName in axis["labelNames"].items():
            a.labelNames[languageCode] = labelName
        a.map = axis["map"]
        doc.addAxis(a)
        
    return doc
    

makeTTF = True
makeWOFF = True

baseDir = os.path.split(__file__)[0]

sourcesPath = os.path.join(baseDir)
sourcesWidePath = '../sources-wide'

axes = [
    dict(minimum=100,  maximum=120, default=100, name="wdth", tag="wdth", labelNames={"en": "Width"}, map=[]),
]

if makeTTF:

    for filename in os.listdir(os.path.abspath(sourcesPath)):
        if filename.endswith('.ufo'):
            path = os.path.join(sourcesPath, filename)
            wideFilename = filename.replace('.ufo', '-wide.ufo')
            f = OpenFont(os.path.abspath(path))
            widePath = os.path.join(sourcesWidePath, wideFilename)
            familyName = filename.replace('.ufo', '')
            psName = f.info.familyName.replace(' ', '')+'-'+f.info.styleName.replace(' ', '')
            psNameWide = psName + ' Wide'
            smFn = f.info.familyName + ' ' + f.info.styleName
            smFnWide = f.info.familyName + f.info.styleName + 'Wide'
        
            sources = [
                dict(path=path, name=path, location=dict(wdth=100), styleName=f.info.styleName, familyName=f.info.familyName, copyInfo=True),    
                dict(path=widePath, name=widePath, location=dict(wdth=120), styleName=f.info.styleName+" Wide", familyName=f.info.familyName, copyInfo=False),  
                ]
            instances = [
        dict(filename=path, location=dict(wdth=100), styleName=f.info.styleName, familyName=f.info.familyName, postScriptFontName=psName,             styleMapFamilyName=smFn, styleMapStyleName=f.info.styleMapStyleName),

        dict(filename=widePath, location=dict(wdth=120), styleName=f.info.styleName+' Wide', familyName=f.info.familyName, postScriptFontName=psNameWide,             styleMapFamilyName=smFnWide, styleMapStyleName=f.info.styleMapStyleName)

                ]        
            ds = buildDesignSpace(sources, instances, axes)
            dsFilename = filename.replace('.ufo', '.designspace')
            ds.write(dsFilename)
        
            project = FontProject()
            project.run_from_designspace(
                dsFilename, 
                output=("variable"),
                remove_overlaps=False, 
                reverse_direction=False, 
                use_production_names=False,
                )
            
            os.remove(os.path.abspath(dsFilename))


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
    masterTTFPath = os.path.join(os.path.abspath(baseDir), 'variable_ttf')
    masterWebPath = os.path.join(os.path.abspath(baseDir), 'variable_web')
    
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

