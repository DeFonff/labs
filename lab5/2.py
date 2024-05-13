from bokeh.layouts import column
from bokeh.models import Button, Slider, CheckboxGroup
from bokeh.plotting import figure, curdoc
from scipy import signal
import numpy as np

def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    np.random.seed(0)
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.multivariate_normal([noise_mean], [[noise_covariance]], len(t)).flatten()
        signal += noise
    return signal

def update(attr, old, new):
    update_plot(slider_amplitude.value, slider_frequency.value, slider_phase.value, slider_noise.value, checkbox_noise.active)

def reset():
    slider_amplitude.value = 4
    slider_frequency.value = 1
    slider_phase.value = np.pi
    slider_noise.value = 3
    checkbox_noise.active = [0]

def filter(signal):
    filtered_signal = np.zeros(len(signal))
    for i in range(4, len(signal)-4):
        filtered_signal[i] = np.mean(signal[i-4:i+5])
    filtered_signal[:4] = signal[:4]
    filtered_signal[-4:] = signal[-4:]
    return filtered_signal

def update_plot(amplitude, frequency, phase, noise, show_noise):
    noise_mean = 0.0
    t = np.linspace(0, 10, 1000)
    fig.renderers = []
    fig.line(t, harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise, False), color='red', legend_label='Гармоніка')
    if show_noise:
        fig.line(t, harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise, show_noise), color='green', legend_label='шум')
        y = harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise, show_noise)
        y = filter(y)
        fig.line(t, y, color='blue', legend_label='Відфільтрований шум')
    fig.legend.location = "bottom_right"
fig = figure(title='Гармоніка зі шумом', x_axis_label='Час', y_axis_label='Амплітуда', width=1500)

slider_amplitude = Slider(start=0, end=8, value=4, step=0.5, title="Амплітуда")
slider_amplitude.on_change('value', update)

slider_frequency = Slider(start=0, end=2, value=1, step=0.5, title="Частота")
slider_frequency.on_change('value', update)

slider_phase = Slider(start=0, end=2*np.pi, value=np.pi, step=np.pi/4, title="Фаза")
slider_phase.on_change('value', update)

slider_noise = Slider(start=0, end=6, value=3, step=0.5, title="Шум")
slider_noise.on_change('value', update)

checkbox_noise = CheckboxGroup(labels=['Показати шум'], active=[0])
checkbox_noise.on_change('active', update)

button_reset = Button(label="Скинути", button_type="success")
button_reset.on_click(reset)

update_plot(4, 1, np.pi, 3, True)

layout = column(fig, slider_amplitude, slider_frequency, slider_phase, slider_noise, checkbox_noise, button_reset)

curdoc().add_root(layout)
