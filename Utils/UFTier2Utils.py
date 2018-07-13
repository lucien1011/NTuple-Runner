import subprocess

def isRootFile(fileName):
    return fileName.endswith(".root")

def skipTrivial(line):
    return bool(line) and line.split()[-1] != "." and line.split()[-1] != ".."

def listdir_uberftp(path,selection=isRootFile):
    cmd = ["uberftp", "cmsio.rc.ufl.edu", "ls %s"%path]
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0]
    return [l.split()[-1] for l in output.split('\r\n') if skipTrivial(l) and selection(l)]


