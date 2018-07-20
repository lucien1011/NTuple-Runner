import subprocess,os

def isRootFile(fileName):
    return fileName.endswith(".root")

def skipTrivial(line):
    return bool(line) and line.split()[-1] != "." and line.split()[-1] != ".." and not "GridFTP Server" in line and 'logged in' not in line

def listdir_uberftp(path,selection=isRootFile):
    if not "ufhpc" in os.environ["HOSTNAME"]:
        cmd = ["uberftp", "cmsio.rc.ufl.edu", "ls %s"%path]
        output = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0]
        return [l.split()[-1] for l in output.split('\r\n') if skipTrivial(l) and selection(l)]
    else:
        return [l for l in os.listdir(path) if selection(l)]


