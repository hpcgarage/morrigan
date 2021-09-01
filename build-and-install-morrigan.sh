cd DRAMsim3
make -j8

cd ../sst-core
make -j8
make install

cd ../sst-elements
make -j8
make install
