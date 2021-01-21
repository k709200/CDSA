import tkinter
from tkinter import ttk, filedialog, messagebox

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

var_padx = 2
DB = []
root = tkinter.Tk()
root.wm_title("CDSA")

fig = Figure(figsize=(5, 4), dpi=80)
canvas = FigureCanvasTkAgg(fig, master=root)
toolbar = NavigationToolbar2Tk(canvas, root)


def _plot():
    try:
        DB_X = list(np.linspace(0, 1/var_Fs.get()*len(DB), len(DB)))
        fft_DB = np.abs(np.fft.fft(DB)[0:len(DB) // 2 + 1])
        fft_DB[0] = 0

        plt1 = fig.add_subplot(311)
        plt1.set_xlabel('Time(s)')
        plt1.plot(DB_X, DB, lw=1)

        plt2 = fig.add_subplot(312).psd(DB, len(DB), Fs=var_Fs.get(), lw=1)

        plt3 = fig.add_subplot(313)
        plt3.set_xlabel('N')
        plt3.set_ylabel('Amplitude')
        plt3.plot(fft_DB, lw=1)
        # A tk.DrawingArea.
        canvas.draw()
        toolbar.update()

        # def on_key_press(event):
        #     print("you pressed {}".format(event.key))
        #     key_press_handler(event, canvas, toolbar)

        # canvas.mpl_connect("key_press_event", on_key_press)
    except Exception as plotMsg:
        messagebox.showinfo(title='Error Message', message=plotMsg)


def _open():
    global DB
    filePath = filedialog.askopenfilename(
        filetypes=[('Text Files', '.txt'), ('Text Files', '.csv')])
    if filePath:
        try:
            openFile = open(filePath, mode='r')
            fileRd = openFile.read().strip().split()

            DB.clear()
            for i in fileRd:
                DB.append(float(i))
            openFile.close()

            lbox.delete(0, 'end')
            for i in DB:
                lbox.insert('end', i)
            for i in range(0, len(DB), 2):
                lbox.itemconfigure(i, background='#f0f0ff')

            # --data filling--
            var_dbox.set(len(DB))
            var_avg.set(np.average(DB))
            var_2sig.set(np.std(DB)*2)
            var_p2p.set(np.max(DB)-np.min(DB))
            var_max.set(np.max(DB))
            var_min.set(np.min(DB))
            _plot()
            _calc()
        except Exception as errMsg:
            messagebox.showinfo(title='Error Message', message=errMsg)


def _calc(*arg):
    try:
        var_t.set(1/var_Fs.get()*var_dbox.get()/var_frq.get())
        var_d.set(var_spd.get() / 60 * 1/var_Fs.get() *
                  var_dbox.get() / var_frq.get() / np.pi * 1000)
        var_c.set(var_spd.get() / 60 * 1/var_Fs.get()
                  * var_dbox.get() / var_frq.get())
    except Exception as zeroMsg:
        messagebox.showinfo('Error', zeroMsg)
        var_Fs.set(25.0)
        var_spd.set(1600.0)
        var_frq.set(400)


def _wipe():
    fig.clear()
    canvas.draw()


def _help():
    messagebox.showinfo('Help', '......')


def _info():
    messagebox.showinfo(
        'About', 'Cold Data Spectrum Analysis\n\nBuild on 2018.4.27\n\nPowered by open-source software\nVersion: v4.2.0\n\nAuthor: zhang.yichuan@upm.com')


def _exit():
    if messagebox.askokcancel('Exit?', 'Do you want to close it?'):
        root.destroy()
        exit()


# --list box--
lbox = tkinter.Listbox(root)  # , width=14
lbox.pack(side=tkinter.LEFT, fill=tkinter.Y)
sbar = ttk.Scrollbar(root, orient=tkinter.VERTICAL, command=lbox.yview)
sbar.pack(side=tkinter.LEFT, fill=tkinter.Y)
lbox['yscrollcommand'] = sbar.set
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)


# --paned window--
pw_main = tkinter.PanedWindow(root)
lf_cmd = ttk.LabelFrame(pw_main, text='command')
lf_smy = ttk.LabelFrame(pw_main, text='results')
lf_ana = ttk.LabelFrame(pw_main, text='analysis')
lf_inf = ttk.LabelFrame(pw_main, text='i')
pw_main.add(lf_cmd)
pw_main.add(lf_smy)
pw_main.add(lf_ana)
pw_main.add(lf_inf)
pw_main.pack(side=tkinter.TOP, fill=tkinter.BOTH)

# --cmd--
ttk.Button(lf_cmd, text='OPEN', command=_open).grid(
    row=10, column=10, padx=var_padx)
ttk.Button(lf_cmd, text="PLOT", command=_plot).grid(
    row=20, column=10, padx=var_padx)
ttk.Button(lf_cmd, text="WIPE", command=_wipe).grid(
    row=30, column=10, padx=var_padx)

# --data--
ttk.Label(lf_smy, text='Databox:').grid(
    row=10, column=10, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_smy, text='Average:').grid(
    row=20, column=10, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_smy, text='2-sig:').grid(row=30,
                                      column=10, sticky='e', padx=var_padx, pady=2)

var_dbox = tkinter.IntVar()
ttk.Entry(lf_smy, textvariable=var_dbox, width=9, state='readonly').grid(
    row=10, column=20, sticky='w', padx=var_padx, pady=2)

var_avg = tkinter.DoubleVar()
ttk.Entry(lf_smy, textvariable=var_avg, width=9, state='readonly').grid(
    row=20, column=20, sticky='w', padx=var_padx, pady=2)

var_2sig = tkinter.DoubleVar()
ttk.Entry(lf_smy, textvariable=var_2sig, width=9, state='readonly').grid(
    row=30, column=20, sticky='w', padx=var_padx, pady=2)

ttk.Separator(lf_smy, orient=tkinter.VERTICAL).grid(
    row=10, column=25, rowspan=30, padx=2, sticky=('n', 's'))

ttk.Label(lf_smy, text='P-P:').grid(row=10,
                                    column=30, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_smy, text='Max:').grid(
    row=20, column=30, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_smy, text='Min:').grid(
    row=30, column=30, sticky='e', padx=var_padx, pady=2)

var_p2p = tkinter.DoubleVar()
ttk.Entry(lf_smy, textvariable=var_p2p, width=9, state='readonly').grid(
    row=10, column=40, sticky='w', padx=var_padx, pady=2)

var_max = tkinter.DoubleVar()
ttk.Entry(lf_smy, textvariable=var_max, width=9, state='readonly').grid(
    row=20, column=40, sticky='w', padx=var_padx, pady=2)

var_min = tkinter.DoubleVar()
ttk.Entry(lf_smy, textvariable=var_min, width=9, state='readonly').grid(
    row=30, column=40, sticky='w', padx=var_padx, pady=2)


# --analysis--
ttk.Label(lf_ana, text='Fs(Hz):').grid(
    row=10, column=10, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_ana, text='Speed(m/min):').grid(
    row=20, column=10, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_ana, text='Frequency(n):').grid(
    row=30, column=10, sticky='e', padx=var_padx, pady=2)

var_Fs = tkinter.DoubleVar()
var_Fs.set(25.0)
var_spd = tkinter.DoubleVar()
var_spd.set(1600.0)
var_frq = tkinter.IntVar()
var_frq.set(400)
sbox_lim = [(0, 10000, 0.1), (0, 10000, 0.1), (0, 10000, 1)]
sbox_tvar = [var_Fs, var_spd, var_frq]

for i in range(3):
    sbox = ttk.Spinbox(lf_ana, textvariable=sbox_tvar[i], command=_calc, width=7,
                       from_=sbox_lim[i][0], to=sbox_lim[i][1], increment=sbox_lim[i][2])
    sbox.bind('<KeyRelease>', _calc)
    sbox.grid(row=10+10*i, column=20, sticky='w', padx=var_padx, pady=2)

ttk.Separator(lf_ana, orient=tkinter.VERTICAL).grid(
    row=10, column=25, rowspan=30, padx=2, sticky=('n', 's'))

ttk.Label(lf_ana, text='T(s):').grid(
    row=10, column=30, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_ana, text='Ø(mm):').grid(
    row=20, column=30, sticky='e', padx=var_padx, pady=2)
ttk.Label(lf_ana, text='D(m):').grid(
    row=30, column=30, sticky='e', padx=var_padx, pady=2)


var_t = tkinter.DoubleVar()
ttk.Entry(lf_ana, textvariable=var_t, width=16, state='readonly').grid(
    row=10, column=40, sticky='w', padx=var_padx, pady=2)

var_d = tkinter.DoubleVar()
ttk.Entry(lf_ana, textvariable=var_d, width=16, state='readonly').grid(
    row=20, column=40, sticky='w', padx=var_padx, pady=2)

var_c = tkinter.DoubleVar()
ttk.Entry(lf_ana, textvariable=var_c, width=16, state='readonly').grid(
    row=30, column=40, sticky='w', padx=var_padx, pady=2)

# --info--
ttk.Button(lf_inf, text='?', command=_help, width=2).grid(
    row=10, column=10, padx=var_padx)
ttk.Button(lf_inf, text="!", command=_info, width=2).grid(
    row=20, column=10, padx=var_padx)
ttk.Button(lf_inf, text="E", command=_exit, width=2).grid(
    row=30, column=10, padx=var_padx)


# --matplot box--
canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.BOTH, expand=1)


tkinter.mainloop()
