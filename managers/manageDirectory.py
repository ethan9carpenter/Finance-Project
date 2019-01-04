from os import getcwd, chdir

def moveDirUp(fileName=None, levels=1, inplace=False, baseDir=getcwd()):
    for _ in range(levels):
        if '/' in baseDir:
            baseDir = baseDir[:baseDir.rfind('/')]
            slash = '/'
        else:
            baseDir = baseDir[:baseDir.rfind('\\')]
            slash = '\\'
    if inplace:
        chdir(baseDir)
    
    if fileName is not None:
        return baseDir + slash + fileName