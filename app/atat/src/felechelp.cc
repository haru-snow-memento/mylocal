const char *helpstring=""
"This code calculates the electronic free energy within the one-electron\n"
"and temperature-independent bands approximations.\n"
"\n"
"It needs an dos.out input file (whose name can be changed with -dos option) that\n"
"has the following format:\n"
" [number of electron in unitcell]\n"
" [energy width of each bins used to calculate the dos]\n"
" [a multiplicative scale factor to adjust units]\n"
" [the density in each bin, in states/unit cell/energy] <- repeated\n"
"\n"
"The code calculates the electronic free energy from temperature T0 to T1 in steps of dT.\n"
"  a) The defaults are T0=0 T1=2000 dT=100.\n"
"  b) If a file Trange.in exists in the upper directory, it is used to set T0,T1,dT:\n"
"     Trange.in must contain two numbers on one line separated by a space: T1 (T1/dT+1).\n"
"     Note that T0=0 always.\n"
"     For phase diagram calculations, you must use this method to specify the temperature range.\n"
"  c) These defaults can be overridden by the -T0, -T1 and -dT options.\n"
"\n"
"The output files contain the free energy per unit cell.\n"
"  felec.log contain temperature and corresponding free energy on each line.\n"
"  felec contains the free energies only.\n"
"  plotdos.out contains the dos (col 1: energy normalized so that Ef=0 , col 2: DOS)\n"
"\n"
"-> For including electronic entropy in phase diagram calculations\n"
"\n"
" You are likely to use this code as follow:\n"
"\n"
"  #first create the Trange.in file for up to 2000K in intervals of 100K:\n"
"  echo 2000 21 > Trange.in\n"
"\n"
"  #This executes the svsl code in each subdirectory containing dos.out but no error file.\n"
"  foreachfile -e dos.out pwd \\; felec [options if desired]\n"
"\n"
"  #constructs a cluster expansion of the electronic free energy (eci are in felec.eci)\n"
"  clusterexpand felec\n"
"\n"
"  #add the energetic eci from eci.out to the electronic eci from felec.eci and create the teci.out\n"
"  #file that will be read by the Monte Carlo code.\n"
"  mkteci felec.eci\n"
"\n"
"  #you can even combine vibrational and electronic eci:\n"
"  mkteci fvib.eci felec.eci\n"
"\n"
;
