from tkinter import *
from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.prism_nets import prism_nets

from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.archimedean_tilings import archimedean_tilings
from tiling_dicts.isogonal_tilings import isogonal_tilings


nets = list(plato_archi_nets.keys()) + list(prism_nets.keys())
nets += list(johnson_nets.keys())

tiles = list(platonic_tilings)+list(archimedean_tilings)+list(isogonal_tilings)


master = Tk()
all_buttons = []
for net in nets:
    all_buttons.append(Button(master,text=net))

for tile in tiles:
    all_buttons.append(Button(master,text=tile))

def smart_grid(parent, *args, **kwargs): # *args are the widgets!
    divisions   = kwargs.pop('divisions', 100)
    force_f     = kwargs.pop('force', False)
    if 'sticky' not in kwargs:
        kwargs.update(sticky='w')
    try:
        parent.win_width
    except:
        parent.win_width = -1
    winfo_width = parent.winfo_width()
    if 1 < winfo_width != parent.win_width or force_f:
        parent.win_width = winfo_width
        row = col = width = 0
        argc = len(args)
        for i in range(argc):
            widget_width = args[i].winfo_width()
            columns = max(1, int(widget_width * float(divisions) / winfo_width))
            width += widget_width
            if width > winfo_width:
                width = widget_width
                row += 1
                col = 0
            args[i].grid(row=row, column=col, columnspan=columns, **kwargs)
            col += columns
        parent.update_idletasks() # update() #
        return row + 1
master.geometry("600x600")
smart_grid(master,all_buttons)
# for elem in all_buttons:
#     elem.pack()
variable = StringVar(master)
##variable.set(OPTIONS[0]) # default value

#w = OptionMenu(master, variable, *OPTIONS)
#w.pack()

mainloop()