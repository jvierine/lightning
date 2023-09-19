#!/usr/bin/bash
#
# start a ringbuffer
#
INSTALL_PATH=/home/j/src/lightning
cd $INSTALL_PATH
# stop all processes
./stop_ringbuffer.sh
# data dir
DDIR=/dev/shm/hf25
mkdir -p logs

# delete old data from ram disk
rm -Rf $DDIR
mkdir -p $DDIR

# sync to ntp time not needed, if you run ntpd
#echo "NTPDATE"
#sudo ntpdate ntp.uit.no

# setup ringbuffer
echo "Ringbuffer"
drf ringbuffer -z 30000MB $DDIR -p 2 >logs/ringbuffer.log 2>&1 &

while true;
do
    echo "Starting THOR"
    #
    ./rx_uhd --nolock >logs/thor.log 2>&1
    sleep 10
done
    
