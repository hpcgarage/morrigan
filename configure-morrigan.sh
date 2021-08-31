set -euo pipefail
. morrigan-env.sh

SST_CORE_HOME=$MORRIGAN_HOME/install

cd sst-core
./autogen.sh
./configure --prefix=$SST_CORE_HOME --disable-mpi
#make all -j8
#make install

cd $MORRIGAN_HOME

echo "export SST_CORE_HOME=$SST_CORE_HOME" >> $MORRIGAN_ENV_FILE
