import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# завдання 3: початкові параметри 
DEFAULTS = {
    "amplitude":        1.0,
    "frequency":        1.0,
    "phase":            0.0,
    "noise_mean":       0.0,
    "noise_covariance": 0.1,
    "cutoff":           5.0,
}

t = np.linspace(0, 4 * np.pi, 1000)

# стан: шум та останні параметри шуму
state = {
    "noise": None,
    "last_nmean": None,
    "last_ncov": None
}

# генеруємо початковий шум (зберігаємо для Reset)
initial_noise = np.random.normal(
    DEFAULTS["noise_mean"],
    np.sqrt(max(DEFAULTS["noise_covariance"], 1e-9)),
    size=t.shape
)

# завдання 1: функція гармоніки (повертає лише чисту гармоніку, оновлює шум при зміні параметрів шуму)
def harmonic_with_noise(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    global state
    harmonic = amplitude * np.sin(frequency * t + phase)
    
# генеруємо новий шум тільки якщо змінили параметри шуму або шуму ще немає
    if (state["noise"] is None or 
        state["last_nmean"] != noise_mean or 
        state["last_ncov"] != noise_covariance):
        state["noise"] = np.random.normal(noise_mean, np.sqrt(max(noise_covariance, 1e-9)), size=t.shape)
        state["last_nmean"] = noise_mean
        state["last_ncov"] = noise_covariance
        
    return harmonic # тепер повертаємо тільки гармоніку

# завдання 7: фільтр
def apply_filter(signal, cutoff, fs=1000, order=4):
    nyq = fs / 2
    norm_cutoff = cutoff / nyq
    norm_cutoff = np.clip(norm_cutoff, 0.001, 0.999)
    b, a = butter(order, norm_cutoff, btype="low", analog=False)
    return filtfilt(b, a, signal)

# завдання 2: налаштовуємо макет з двома графіками
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))
plt.subplots_adjust(left=0.08, right=0.95, top=0.90, bottom=0.52, wspace=0.2)
fig.suptitle("Порівняння початкової та відфільтрованої гармонік", fontsize=14, fontweight='bold')

# ініціалізуємо стан шуму початковим значенням
state["noise"] = initial_noise.copy()
state["last_nmean"] = DEFAULTS["noise_mean"]
state["last_ncov"] = DEFAULTS["noise_covariance"]

# початкові сигнали
h_init = harmonic_with_noise(t, DEFAULTS["amplitude"], DEFAULTS["frequency"], DEFAULTS["phase"],
                             DEFAULTS["noise_mean"], DEFAULTS["noise_covariance"], True)
noisy_init = h_init + state["noise"]
filt_init = apply_filter(noisy_init, DEFAULTS["cutoff"])

# лівий графік
line_noisy, = ax1.plot(t, noisy_init, color="orange", lw=1.0, label="Зашумлена")
line_clean1, = ax1.plot(t, h_init, color="crimson", lw=1.5, label="Чиста гармоніка")
ax1.set_title("Початковий сигнал")
ax1.legend(loc="upper right", fontsize=9)
ax1.grid(True, alpha=0.3)

# правий графік
line_filtered, = ax2.plot(t, filt_init, color="blue", lw=2, label="Відфільтрована")
line_clean2, = ax2.plot(t, h_init, color="crimson", lw=1.5, ls="--", alpha=0.7, label="Чиста (еталон)")
ax2.set_title("Результат фільтрації")
ax2.legend(loc="upper right", fontsize=9)
ax2.grid(True, alpha=0.3)

# інтерактивні 
def make_slider(bottom, label, valmin, valmax, valinit, valstep=0.001):
    ax_s = fig.add_axes([0.15, bottom, 0.60, 0.03])
    return Slider(ax_s, label, valmin, valmax, valinit=valinit, valstep=valstep)
    
# слайдери
s_amp    = make_slider(0.42, "Amplitude",        0.1,  3.0,   DEFAULTS["amplitude"])
s_freq   = make_slider(0.36, "Frequency",        0.1,  5.0,   DEFAULTS["frequency"])
s_phase  = make_slider(0.30, "Phase",            0.0,  6.28,  DEFAULTS["phase"])
s_nmean  = make_slider(0.24, "Noise Mean",       -1.0, 1.0,   DEFAULTS["noise_mean"])
s_ncov   = make_slider(0.18, "Noise Covariance", 0.0,  2.0,   DEFAULTS["noise_covariance"])
s_cutoff = make_slider(0.12, "Cutoff Freq",      1.0, 100.0,  DEFAULTS["cutoff"], valstep=0.5)

# завдання 4: чекбокс
ax_check = fig.add_axes([0.80, 0.32, 0.12, 0.08])
check = CheckButtons(ax_check, ["Show Noise"], [True])

ax_btn = fig.add_axes([0.80, 0.17, 0.10, 0.05])
btn_reset = Button(ax_btn, "Reset")

# завдання 10: інструкції для користувача
instructions = (
    "Інструкція:\n"
    "• Амплітуда / Частота / Фаза — параметри чистої гармоніки.\n"
    "• Шум Mean / Covariance — параметри шуму (генерується новий лише при зміні).\n"
    "• Cutoff Freq — частота зрізу фільтра (що менше значення, то сильніша фільтрація).\n"
    "• 'Show Noise' — відображає/ховає зашумлений сигнал на лівому графіку.\n"
    "• 'Reset' — відновлює початкові параметри та початкову реалізацію шуму."
)
fig.text(0.08, 0.02, instructions, fontsize=9, color='black',
         bbox=dict(facecolor='white', alpha=0.9, edgecolor='lightgray', boxstyle="round,pad=0.5"))

# 5. логіка оновлення
def update(val=None):
    show_noise = check.get_status()[0]
    
    h = harmonic_with_noise(t, s_amp.val, s_freq.val, s_phase.val,
                            s_nmean.val, s_ncov.val, show_noise)
    
# для відображення на лівому графіку
    if show_noise:
        noisy = h + state["noise"]
    else:
        noisy = h
    
# для фільтра завжди використовую зашумлений сигнал (навіть якщо чекбокс вимкнений)
    real_noisy = h + state["noise"]
    filt = apply_filter(real_noisy, s_cutoff.val)
    
    line_clean1.set_ydata(h)
    line_noisy.set_ydata(noisy)
    line_noisy.set_visible(show_noise)
    
    line_clean2.set_ydata(h)
    line_filtered.set_ydata(filt)
    
    ax1.relim()
    ax1.autoscale_view()
    ax2.relim()
    ax2.autoscale_view()
    fig.canvas.draw_idle()

# завдання 6: кнопка reset
def reset(event):
# скидаємо слайдери
    for s in [s_amp, s_freq, s_phase, s_nmean, s_ncov, s_cutoff]:
        s.eventson = False
        s.reset()
        s.eventson = True
    
# вмикаємо чекбокс
    if not check.get_status()[0]:
        check.set_active(0)
    
# відновлюю початковий шум (той самий масив, що при запуску)
    global initial_noise
    state["noise"] = initial_noise.copy()
    state["last_nmean"] = DEFAULTS["noise_mean"]
    state["last_ncov"] = DEFAULTS["noise_covariance"]
    
    update()

# прив'язка подій
for s in [s_amp, s_freq, s_phase, s_nmean, s_ncov, s_cutoff]:
    s.on_changed(update)

check.on_clicked(update)
btn_reset.on_clicked(reset)

plt.show()