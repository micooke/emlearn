
import numpy
import numpy.fft

import pytest
import numpy.testing

import matplotlib
matplotlib.use('Agg')
import librosa
import librosa.display

import emlearn
import eml_audio

FFT_SIZES = [
    64,
    128,
    256,
    512,
    1024,
]
@pytest.mark.parametrize('n_fft', FFT_SIZES)
def test_rfft_simple(n_fft):
    signal = numpy.arange(0, n_fft)

    ref = numpy.fft.fft(signal, n=n_fft).real
    out = eml_audio.rfft(signal)
    diff = (out - ref)

    numpy.testing.assert_allclose(out, ref, rtol=1e-4)

def test_rfft_not_power2_length():
    with pytest.raises(Exception) as e:
        eml_audio.rfft(numpy.array([0,1,3,4,5]))


@pytest.mark.skip('broken')
def test_melfilter():
    filename = librosa.util.example_audio_file()
    y, sr = librosa.load(filename, offset=1.0, duration=0.3)
    n_fft = 1024
    hop_length = 256
    fmin = 500
    fmax = 5000
    n_mels = 32

    spec = numpy.abs(librosa.core.stft(y, n_fft=n_fft, hop_length=hop_length))**2
    spec1 = spec[:,0]

    ref = librosa.feature.melspectrogram(S=spec1, sr=sr, htk=True, n_fft=n_fft, n_mels=n_mels, fmin=fmin, fmax=fmax)
    out = eml_audio.melfilter(spec1, sr, n_fft, n_mels, fmin, fmax)

    assert ref.shape == out.shape
    numpy.testing.assert_array_almost_equal(ref, out)


@pytest.mark.skip('broken')
def test_melspectrogram():

    filename = librosa.util.example_audio_file()

    y, sr = librosa.load(filename, offset=1.0, duration=0.3)

    n_mels = 64
    n_fft = 1024
    fmin = 500
    fmax = 5000
    hop_size = n_fft

    # Only do one frame
    y = y[0:n_fft]
    ref = librosa.feature.melspectrogram(y, sr, norm=None, htk=True,
                                         fmin=fmin, fmax=fmax, n_fft=n_fft, n_mels=n_mels, hop_length=hop_size)
    out = eml_audio.melspectrogram(y, sr, n_fft, n_mels, fmin, fmax)
    ref = ref[:,0:1]
    out = out.reshape(-1,1)

    #out = melspec(y, sr, n_fft, n_mels, fmin, fmax, hop_length=hop_size)[:,:10]

    print('r', ref.shape)

    assert out.shape == ref.shape

    from matplotlib import pyplot as plt
    fig, (ref_ax, out_ax) = plt.subplots(2)
    def specshow(d, ax):
        s = librosa.amplitude_to_db(d, ref=numpy.max)
        librosa.display.specshow(s, ax=ax, x_axis='time')
        #librosa.display.specshow(s, ax=ax, x_axis='time', y_axis='mel', fmin=fmin, fmax=fmax)
    specshow(ref, ax=ref_ax)
    specshow(out, ax=out_ax)

    fig.savefig('melspec.png')

    print('mean', numpy.mean(ref), numpy.mean(out))
    print('std', numpy.std(ref), numpy.std(out))
    s = numpy.mean(ref) / numpy.mean(out)
    print('scale', s)
    out = out * s

    #print(out-ref)
    numpy.testing.assert_allclose(out, ref, rtol=1e-6);


