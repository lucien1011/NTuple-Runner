import os

hostName = os.environ["HOSTNAME"]
if "ufhpc" in hostName:
    where = "hpg"
elif "ihepa" in hostName:
    where = "ihepa"
elif "lxplus" in hostName:
    where = "CERN"
else:
    raise RuntimeError,"Computing site not supported"
