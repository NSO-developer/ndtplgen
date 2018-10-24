#DEVTPLBUILD
#Maxwell Schmitt (maxwschm@cisco.com)


## Provided as-is -- allows you to build an xml file to import multiple devices in NSO


### Prerequisites:
Python 3


### Using:
Edit the python file's infile and outfile variable to what you'd prefer

The infile's structure should look like:

r1,127.0.0.1,10025,default,cisco-ios-xr
r2,127.0.0.1,10026,default,cisco-ios-xr
r3,127.0.0.1,10027,default,cisco-ios-xr
r4,127.0.0.1,10028,default,cisco-ios-xr
r5,127.0.0.1,10029,default,cisco-ios-xr
r6,127.0.0.1,10030,default,cisco-ios-xr

name (displayed in nso), device address, ssh port, authgroup (should already be setup in NSO), ned id.

Then call like:
python3 devtplbuild.py
and import into NSO like:
ncs_load -lm outfile (requires NSO to be sourced)


Sample infile and outfile are included in the repo for you to analyze.