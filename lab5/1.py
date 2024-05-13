from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, CheckButtons

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    np.random.seed(0)
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.multivariate_normal([noise_mean], [[noise_covariance]], len(t)).flatten()
        signal += noise
    return signal


    
def plot_function(slider_am, slider_fr, slider_ph, slider_n, show_noise, N, Wn):
    noise_mean = 0.0
    t = np.linspace(0, 10, 1000)
    ax.clear()
    ax.set_ylim(-11, 11)
    if show_noise:
        y = harmonic_with_noise(t, slider_am, slider_fr, slider_ph, noise_mean, slider_n, show_noise)
        ax.plot(t, y, color='green', label='Шум')  

        b, a = signal.iirfilter(N, Wn, output='ba', btype='low')
        filtered_noise = signal.filtfilt(b, a, y)
        ax.plot(t, filtered_noise, color='blue', label='Відфільтрований шум')  
    y = harmonic_with_noise(t, slider_am, slider_fr, slider_ph, noise_mean, slider_n, False)
 
    ax.plot(t, y, color='red', label='Гармоніка')  
    ax.set_title('Гармоніка зі шумом')
    ax.set_xlabel('Час')
    ax.set_ylabel('Амплітуда')
    ax.grid(True)
    ax.legend(loc="lower right",fontsize="small") 
    plt.draw()

def update(val):
    plot_function(slider_am.val, slider_fr.val, slider_ph.val,slider_n.val, check.get_status()[0], int(slider_N.val),float(slider_Wn.val))

def reset(val):
    slider_am.set_val(4)
    slider_fr.set_val(1)
    slider_ph.set_val(np.pi)
    slider_n.set_val(3)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.5)  
slider_am = Slider(fig.add_axes([0.15, 0.4, 0.4, 0.05]),
    label="Амплітуда",
    valmin=0,
    valmax=8,
    valinit=4)
slider_fr = Slider(fig.add_axes([0.15, 0.35, 0.4, 0.05]),
    label="частота",
    valmin=0,
    valmax=2,
    valinit=1)
slider_ph = Slider(fig.add_axes([0.15, 0.3, 0.4, 0.05]),
    label="фаза",
    valmin=0,
    valmax=2*np.pi,
    valinit=np.pi)
slider_n = Slider(fig.add_axes([0.15, 0.25, 0.4, 0.05]),
    label="шум",
    valmin=0,
    valmax=6,
    valinit=3)
slider_N = Slider(fig.add_axes([0.15, 0.05, 0.4, 0.05]),
    label="N",
    valmin=1,
    valmax=10,
    valinit=5)
slider_Wn = Slider(fig.add_axes([0.15, 0.0, 0.4, 0.05]),
    label="Wn",
    valmin=0.01,
    valmax=0.99,
    valinit=0.1)

slider_am.on_changed(update)
slider_fr.on_changed(update)
slider_ph.on_changed(update)
slider_n.on_changed(update)
slider_N.on_changed(update)
slider_Wn.on_changed(update)

check = CheckButtons(
    ax= fig.add_axes([0.15, 0.20, 0.25, 0.05]),
    labels=['показати шум'],
    actives=[True],
)
check.on_clicked(update)
button = Button(fig.add_axes([0.15, 0.14, 0.2, 0.05]), "reset")
button.on_clicked(reset)

plot_function(slider_am.val, slider_fr.val, slider_ph.val, slider_n.val, check.get_status()[0], float(slider_N.val),float(slider_Wn.val))

plt.show()

