'''
DEVTPLBUILD
Maxwell Schmitt
(maxwschm@cisco.com)

**THIS SCRIPT IS PROVIDED AS-IS**

'''

import subprocess

#Get the Fingerprint
def sshscan(addr, port):
  keydata = subprocess.getoutput(["ssh-keyscan -p " + port + " " + addr])
  keydata = keydata.split("ssh-rsa ")[1]
  return keydata

#Generate the individual device template
def tplgen(tpl, name, addr, port, keydata, authgroup, nedn):
    tpl = tpl.replace("\{name\}", name)
    tpl = tpl.replace("\{addr\}", addr)
    tpl = tpl.replace("\{port\}", port)
    tpl = tpl.replace("\{keydata\}", keydata)
    tpl = tpl.replace("\{authgroup\}", authgroup)
    tpl = tpl.replace("\{nedn\}", nedn.strip())
    return tpl

#Generate and concatenate the device templates
def grandtplgen(tpl, dlist):
    grandtpl = ''''''
    for entry in dlist:
        grandtpl += tplgen(tpl, entry["name"], entry["addr"], entry["port"], entry["keydata"], entry["authgroup"], entry["nedn"])
    return grandtpl

#Read in from file and output a list of dictionaries with all info needed to generate templates
def getdlist(ftr):
    infile = open(ftr, 'r')
    dlist = []
    for line in infile:
        values = line.split(',')
        idlist = {}
        idlist["name"] = values[0]
        idlist["addr"] = values[1]
        idlist["port"] = values[2]
        idlist["keydata"] = sshscan(values[1], values[2])
        idlist["authgroup"] = values[3]
        idlist["nedn"] = values[4]
        dlist.append(idlist)
    infile.close()
    return dlist

#MAIN CODE BELOW

enclosest = '<devices xmlns="http://tail-f.com/ns/ncs">\n'
tpl = '''  
  <device>

     <name>\{name\}</name>

     <address>\{addr\}</address>

     <port>\{port\}</port>

     <ssh>

       <host-key>

         <algorithm>ssh-rsa</algorithm>

         <key-data>\{keydata\}</key-data>

       </host-key>

     </ssh>

     <state>

       <admin-state>unlocked</admin-state>

     </state>

     <authgroup>\{authgroup\}</authgroup>

     <device-type>

       <cli>

         <ned-id xmlns:\{nedn\}-id="http://tail-f.com/ned/\{nedn\}-id">\{nedn\}-id:\{nedn\}</ned-id>

       </cli>

     </device-type>

   </device>\n'''
encloseend = "</devices>"

infile = "in.txt" #modify the string to change the infile destination
outfile = "out.xml"  #modify the string to change the outfile destination
grandtpl = grandtplgen(tpl, getdlist(infile))
grandout = enclosest + grandtpl + encloseend
xmlout = open(outfile, 'w')
xmlout.write(grandout)
xmlout.close()

print("Done!\nJust type ncs_load -lm " + outfile)
