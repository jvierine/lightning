
# stop all processes doing realtime chirp analysis
kill `ps ax |grep thor.py|grep python |awk '{print $1}' |xargs`
kill `ps ax |grep drf|grep python |awk '{print $1}' |xargs`
kill `ps ax |grep rx_uhd |awk '{print $1}' |xargs`
# remove remaining data in ringbuffer
rm -Rf /dev/shm/hf25

