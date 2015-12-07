import essentia as es
import matplotlib.pyplot as plt
import essentia.standard as estd
import essentia.streaming as estr
import pylab
from pylab import plot, show, figure



# audio_path = "../../weilun_thesis/die_another_day/welcome_to_sweden_1.wav"
# audio_path ="../../weilun_thesis/die_another_day/big_bang_1.wav"
audio_path = "call_me_maybe.mp3"

hopSize = 1024
frameSize = 2048
sampleRate = 44100
guessUnvoiced = True

loader = estd.MonoLoader(filename = audio_path, sampleRate=44100)
audio = loader()

w = estd.Windowing(type = 'hann')
spectrum = estd.Spectrum()
mfcc = estd.MFCC()
loudness = estd.Loudness()

# frame = audio[5*44100 : 5*44100 + 1024]
# spec = spectrum(w(frame))

# plot(spec)
# show()

# mfccs = []

# for frame in estd.FrameGenerator(audio, frameSize = 1024, hopSize = 512):
#     mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
#     mfccs.append(mfcc_coeffs)

# # transpose to have it in a better shape
# # we need to convert the list to an essentia.array first (== numpy.array of floats)
# mfccs = es.array(mfccs).T

# # and plot
# pylab.imshow(mfccs[1:,:], aspect = 'auto')
# show()


pool = es.Pool()


for frame in estd.FrameGenerator(audio, frameSize = 2048, hopSize = 1096):
    # mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
    # pool.add('lowlevel.mfcc', mfcc_coeffs)
    # pool.add('lowlevel.mfcc_bands', mfcc_bands)
    loud_result = loudness(spectrum(w(frame)))
    pool.add('loudness', loud_result)
    # print loud_result

# estd.YamlOutput(filename = 'temp.json', format = "json")(pool)

y_axis = range(0,len(pool["loudness"]))
time = map(lambda x:float(x)/(float(44100)/1024), y_axis)
# print time

plt.plot(time, pool["loudness"])
plt.show()


