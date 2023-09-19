#import matplotlib
#matplotlib.use("Agg")
import numpy as n
import matplotlib.pyplot as plt
import digital_rf as drf
import scipy.signal as s
import pyfftw
import traceback
import h5py
import time

d=drf.DigitalRFReader("/dev/shm/hf25")
ch="cha"
b=d.get_bounds(ch)
i1=b[0]+4*25000000

# this is the fft length
w=512*2*2*2
step=w
sr=25000000
dt=0.1
n_samples=int(dt*sr)
n_spectra = int((n_samples-w)/step)

# "ionogram"
S=n.zeros([n_spectra,w],dtype=n.float32)

wf=s.hann(w)

detection_threshold=20.0
peak_mf=0.0
while True:
    b=d.get_bounds(ch)
    n_sec_behind=(b[1]-i1)/sr
    print("peak mf %1.0f %1.0f s behind buffer head"%(peak_mf,n_sec_behind))
    head=b[1]
    # if we are late, don't worry, step onto what is in the ring buffer
    if i1 < b[0]:
        i1=b[0]+25000000*10
        print("we couldn't keep up. skipping some data to catch up")
        
    if (i1+n_samples) < head:
        try:
            z=d.read_vector_c81d(i1,n_samples,ch)

            idx=n.arange(w,dtype=int)
            for i in range(n_spectra):
                Z=n.fft.fftshift(pyfftw.interfaces.numpy_fft.fft(z[i*step+idx]*wf))
                P=n.real(Z)**2.0 + n.imag(Z)**2.0
                S[i,:]=P


            spike_mf=n.mean(S,axis=1)
            spike_mf=spike_mf-n.median(spike_mf)
            sigma=n.std(spike_mf)

            peak_mf=n.max(spike_mf)/sigma
            
            if peak_mf > detection_threshold:
                # read a little bit more data to make sure we catch enough of the event
                z=d.read_vector_c81d(i1-n_samples,2*n_samples,ch)
                print("detection %1.2f"%(peak_mf))
                h=h5py.File("event-%1.1f.h5"%(i1-n_samples),"w")
                h["z"]=z
                h["i0"]=i1-n_samples
                h.close()
                
        except:
            print("couldn't keep up. skipping to catch up")
            traceback.print_exc()
            pass
        i1+=n_samples
    else:
        print("waiting for more data")
        time.sleep(1)
    

        
    
