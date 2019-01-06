from os import getcwd, chdir

def moveDirUp(fileName=None, levels=1, inplace=False, baseDir=getcwd()):
    """
    Allows for access to resource files outside of the working directory.
    
    @param fileName: The name of the file to return the file path of.
    @param levels: How many folders up to move the directory.
    @param inplace: If True, move the current working directory up
                    'levels' number of folders, otherwise only
                    return the moved 'fileName' as a full filepath.
    @param baseDir: The base directory that is being worked with currently.
                    Default is the current working directory.
    
    @return: If 'inplace', the full moved up file path
    """
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