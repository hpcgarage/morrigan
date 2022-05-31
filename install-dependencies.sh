# File: install-dependencies.sh

# This file downloads and installs dependencies of the Morrigan project.
# It is designed to be run from the top directory of the project.

set -euo pipefail

MORRIGAN_HOME=$(pwd)

# Tools will be installed at $PREFIX/
PREFIX=$MORRIGAN_HOME/install

# The following file will contain necessary environment variables
# after this script has run.
MORRIGAN_ENV_FILE=$MORRIGAN_HOME/morrigan-env.sh
rm -f $MORRIGAN_ENV_FILE

# Create a file for logging installation progress.
MORRIGAN_LOGS=$MORRIGAN_HOME/logs
LOGFILE=$MORRIGAN_LOGS/install-dependencies.out
mkdir -p $MORRIGAN_HOME/logs
rm -f $LOGFILE

# These versions are known to work with our project. Change them at your
# own risk.
M4_VERSION=1.4.18
AUTOCONF_VERSION=2.69
AUTOMAKE_VERSION=1.16.2
LIBTOOL_VERSION=2.4.6

CMAKEURL='https://github.com/Kitware/CMake/releases/download/v3.21.1/cmake-3.21.1-linux-x86_64.tar.gz'
PINURL='https://software.intel.com/sites/landingpage/pintool/downloads/pin-3.20-98437-gf02b61307-gcc-linux.tar.gz'


#########################################################
# You should not need to edit anything below this line! #
#########################################################

# Make necessesary directories
mkdir -p $MORRIGAN_HOME/deps
mkdir -p $MORRIGAN_HOME/install

#####################
# Install Autotools #
#####################

cd deps

wget http://ftp.gnu.org/gnu/m4/m4-${M4_VERSION}.tar.gz
wget http://ftp.gnu.org/gnu/autoconf/autoconf-${AUTOCONF_VERSION}.tar.gz
wget http://ftp.gnu.org/gnu/automake/automake-${AUTOMAKE_VERSION}.tar.gz
wget http://ftp.gnu.org/gnu/libtool/libtool-${LIBTOOL_VERSION}.tar.gz

# Decompress
gzip -dc m4-${M4_VERSION}.tar.gz | tar xvf -
gzip -dc autoconf-${AUTOCONF_VERSION}.tar.gz | tar xvf -
gzip -dc automake-${AUTOMAKE_VERSION}.tar.gz | tar xvf -
gzip -dc libtool-${LIBTOOL_VERSION}.tar.gz | tar xvf -

# Build and install
cd m4-${M4_VERSION}
./configure -C --prefix=$PREFIX && make && make install
cd ../autoconf-${AUTOCONF_VERSION}
./configure -C --prefix=$PREFIX && make && make install
cd ../automake-${AUTOMAKE_VERSION}
./configure -C --prefix=$PREFIX && make && make install
cd ../libtool-${LIBTOOL_VERSION}
./configure -C --prefix=$PREFIX && make && make install

cd $MORRIGAN_HOME

echo
echo "MORRIGAN: Autotools successfully installed." | tee -a $LOGFILE
echo
sleep 1

#################
# Install Cmake #
#################

mkdir -p deps/cmake
mkdir -p $PREFIX/bin
mkdir -p $PREFIX/share

cd deps/cmake
wget $CMAKEURL
tar xzf *.tar.gz
cd $(ls -d */)
cp bin/* $PREFIX/bin/
cp -r share/* $PREFIX/share/

cd $MORRIGAN_HOME
echo
echo "MORRIGAN: Cmake successfully installed." | tee -a $LOGFILE
echo
sleep 1

# Install Pin3
mkdir -p $MORRIGAN_HOME/install/packages/pin
cd $MORRIGAN_HOME/install/packages/pin
wget $PINURL
tar xvzf *.tar.gz
MORRIGAN_PIN_HOME=$PWD/$(ls -d */)

echo export PATH=$MORRIGAN_HOME/install/bin:'$PATH' >> $MORRIGAN_ENV_FILE
echo export MORRIGAN_PIN_HOME=$MORRIGAN_PIN_HOME >> $MORRIGAN_ENV_FILE
echo export MORRIGAN_HOME=$MORRIGAN_HOME >> $MORRIGAN_ENV_FILE
echo export MORRIGAN_LOGS=$MORRIGAN_LOGS >> $MORRIGAN_ENV_FILE

echo "MORRIGAN: Pin 3 successfully installed." >> $LOGFILE

echo
echo "MORRIGAN: Autotools, Cmake, and Pin3 have been installed."
echo "MORRIGAN: Update your path by running \"source $MORRIGAN_ENV_FILE\"" | tee -a $LOGFILE

