from os import getcwd

def moveDirUp(fileName, levels=1):
    baseDir = getcwd()
    for _ in range(levels):
        if '/' in baseDir:
            baseDir = baseDir[:baseDir.rfind('/')]
            slash = '/'
        else:
            baseDir = baseDir[:baseDir.rfind('\\')]
            slash = '\\'
    
    return baseDir + slash + fileName