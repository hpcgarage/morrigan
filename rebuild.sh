# Uninstall and delete object files forcing them to be rebuilt


cd sst-core
make uninstall
make clean

cd sst-elements
make uninstall
make clean

cd DRAMsim3
make clean
