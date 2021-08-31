# File: install-dependencies.sh

# This file downloads and installs dependencies of the Morrigan project.
# It is designed to be run from the top directory of the project.
MORRIGAN_HOME=$(pwd)

# Tools will be installed at $PREFIX/
PREFIX=$MORRIGAN_HOME/install

# The following file will contain necessary environment variables
# after this script has run.
OUTFILE=$MORRIGAN_HOME/morrigan-deps.sh

# These versions are known to work with our project. Change them at your
# own risk.
M4_VERSION=1.4.18
AUTOCONF_VERSION=2.69
AUTOMAKE_VERSION=1.16.2
LIBTOOL_VERSION=2.4.6

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

#################
# Install Cmake #
#################

# Install Pin3

# Install 

