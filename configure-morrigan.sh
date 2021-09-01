set -euo pipefail
MORRIGAN_ENV_FILE=morrigan-env.sh
. $MORRIGAN_ENV_FILE

if [ -z ${MORRIGAN_HOME+x} ];
then
    echo "ERROR: MORRIGAN_HOME is unset";
    exit
fi


LOGFILE=$MORRIGAN_LOGS/configure-morrigan.out
mkdir -p $MORRIGAN_LOGS
rm -f $LOGFILE
touch $LOGFILE

SST_CORE_HOME=$MORRIGAN_HOME/install

cd sst-core
./autogen.sh
./configure --prefix=$SST_CORE_HOME --disable-mpi
make all -j8
make install

cd $MORRIGAN_HOME

echo "export SST_CORE_HOME=$SST_CORE_HOME" >> $MORRIGAN_ENV_FILE

echo
echo "MORRIGAN: sst-core has been configured." | tee -a $LOGFILE
echo
wait


cd DRAMsim3
cmake .
make -j8
MORRIGAN_DRAMDIR=$PWD
cd $MORRIGAN_HOME

echo "export MORRIGAN_DRAMDIR=$MORRIGAN_DRAMDIR" >> $MORRIGAN_ENV_FILE

echo
echo "MORRIGAN: DRAMsim3 has been configured." | tee -a $LOGFILE
echo
wait


#TODO: Check the output of elements config to make sure it built ariel and detected dramsim3
SST_ELEMENTS_HOME=$MORRIGAN_HOME/install
SST_ELEMENTS_ROOT="sst-elements"

echo export SST_ELEMENTS_HOME=$SST_ELEMENTS_HOME >> $MORRIGAN_ENV_FILE
echo export SST_ELEMENTS_ROOT=$SST_ELEMENTS_ROOT >> $MORRIGAN_ENV_FILE

cd sst-elements
# Remove Werror lmao
find . -name Makefile.am -exec sed -i s'/-Werror//g' {} \;
./autogen.sh
./configure --prefix=$SST_ELEMENTS_HOME --with-sst-core=$SST_CORE_HOME --with-pin=$MORRIGAN_PIN_HOME --with-dramsim3=$MORRIGAN_DRAMDIR
#make all -j8
#make install

cd $MORRIGAN_HOME

echo "Done"

