# -*- coding: utf-8 -*-
"""The graphical part of a AMO Grid step"""

import molssi_workflow
from molssi_workflow import ureg, Q_, units_class  # noqa F401
import molssi_widgets as mw
import amo_grid_step  # noqa F401
import Pmw
import pprint  # noqa F401
import tkinter as tk
import tkinter.ttk as ttk


class TkAMOGrid(molssi_workflow.TkNode):
    """The graphical part of a AMO Grid step in a MolSSI flowchart.

    """

    def __init__(self, tk_workflow=None, node=None, canvas=None,
                 x=None, y=None, w=None, h=None):
        '''Initialize a node

        Keyword arguments:
        '''
        self.dialog = None

        super().__init__(tk_workflow=tk_workflow, node=node,
                         canvas=canvas, x=None, y=None, w=200, h=50)

    def create_dialog(self):
        """Create the dialog!"""
        self.dialog = Pmw.Dialog(
            self.toplevel,
            buttons=('OK', 'Help', 'Cancel'),
            defaultbutton='OK',
            master=self.toplevel,
            title='Edit AMO Grid step',
            command=self.handle_dialog)
        self.dialog.withdraw()

        # The information about widgets is held in self['xxxx'], i.e. this
        # class is in part a dictionary of widgets. This makes accessing
        # the widgets easier and allows loops, etc.


        # The tabbed notebook
        notebook = ttk.Notebook(self.dialog.interior())
        notebook.pack(side='top', fill=tk.BOTH, expand=tk.YES)
        self['notebook'] = notebook

        # Main frame holding the widgets
        frame = ttk.Frame(notebook)
        self['frame'] = frame
        notebook.add(frame, text='Parameters', sticky=tk.NW)

        # Shortcut for parameters
        P = self.node.parameters

        # The create the widgets. First two frames, one for central grid and
        # one for the atomic grids.
        central_grid = self['central_grid'] = ttk.LabelFrame(
            self['frame'], borderwidth=4, relief='sunken',
            text='Central Grid', labelanchor='n', padding=10)
        atomic_grids = self['atomic_grids'] = ttk.LabelFrame(
            self['frame'], borderwidth=4, relief='sunken',
            text='Atomic Grids', labelanchor='n', padding=10)

        central_grid.columnconfigure(0, minsize=50)
        central_grid.columnconfigure(1, minsize=50)
        central_grid.columnconfigure(2, minsize=50)
        atomic_grids.columnconfigure(0, minsize=50)
        atomic_grids.columnconfigure(1, minsize=50)
        atomic_grids.columnconfigure(2, minsize=50)
        
        for key in P:
            if key[0:7] == 'central':
                self[key] = P[key].widget(self['central_grid'])
            if key[0:6] == 'atomic':
                self[key] = P[key].widget(self['atomic_grids'])

        # Set up the callbacks to change the GUI
        for key in ('central grid angular quadrature',
                    'atomic grid angular quadrature'):
            self[key].combobox.bind(
                "<<ComboboxSelected>>", self.reset_dialog
            )

        # and lay them out
        central_grid.grid(row=0, column=0, sticky=tk.NSEW)
        atomic_grids.grid(row=0, column=1, sticky=tk.NSEW)
        self.reset_dialog()

        # Second tab for results
        rframe = self['results frame'] = ttk.Frame(notebook)
        notebook.add(rframe, text='Results', sticky=tk.NSEW)

        var = self.tk_var['create tables'] = tk.IntVar()
        if P['create tables'].value == 'yes':
            var.set(1)
        else:
            var.set(0)
        self['create tables'] = ttk.Checkbutton(
            rframe, text='Create tables if needed', variable=var
        )
        self['create tables'].grid(row=0, column=0, sticky=tk.W)

        self['results'] = mw.ScrolledColumns(
            rframe,
            columns=[
                'Result',
                'Save',
                'Variable name',
                'In table',
                'Column name',
            ]
        )
        self['results'].grid(row=1, column=0, sticky=tk.NSEW)
        rframe.columnconfigure(0, weight=1)
        rframe.rowconfigure(1, weight=1)

        self.setup_results()

        # And make the dialog wide enough
        frame.update_idletasks()
        width = frame.winfo_width() + 70  # extra space for frame, etc.
        height = frame.winfo_height()
        rwidth = rframe.winfo_width() + 70  # extra space for frame, etc.
        rheight = rframe.winfo_height()
        if rwidth > width:
            width = rwidth
        if rheight > height:
            height = rheight
        sw = frame.winfo_screenwidth()
        sh = frame.winfo_screenheight()

        if width > sw:
            width = int(0.9*sw)
        if height > sh:
            height = int(0.9*sh)
            
        self.dialog.geometry('{}x{}'.format(width, height))

    def reset_dialog(self, widget=None):
        """Layout the widgets in the dialog

        This initial function simply lays them out row by rows with
        aligned labels. You may wish a more complicated layout that
        is controlled by values of some of the control parameters.
        """

        # Setup the widgets for the central grid
        method = self['central grid angular quadrature'].get()

        # Remove any widgets previously packed for the central grid
        frame = self['central_grid']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # keep track of the row in a variable, so that the layout is flexible
        # if e.g. rows are skipped to control such as 'method' here
        row = 0
        widgets = []
        widgets1 = []
        widgets2 = []
        for key in ('central grid lmax', 'central grid angular quadrature'):
            self[key].grid(row=row, column=0, columnspan=3, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        if method == 'Lebedev':
            for key in ('central grid Lebedev rule',):
                self[key].grid(row=row, column=1, columnspan=2, sticky=tk.EW)
                widgets1.append(self[key])
                row += 1
        else:
            for key in ('central grid phi quadrature',):
                self[key].grid(row=row, column=1, columnspan=2, sticky=tk.EW)
                widgets1.append(self[key])
                row += 1
            for key in ('central grid phi n-points',):
                self[key].grid(row=row, column=2, columnspan=1, sticky=tk.EW)
                widgets2.append(self[key])
                row += 1
            for key in ('central grid theta quadrature',):
                self[key].grid(row=row, column=1, columnspan=2, sticky=tk.EW)
                widgets1.append(self[key])
                row += 1
            for key in ('central grid theta n-points',):
                self[key].grid(row=row, column=2, columnspan=1, sticky=tk.EW)
                widgets2.append(self[key])
                row += 1

        for key in ('central grid radial quadrature',
                    'central grid region n-points',
                    'central grid region outer limit'):
            self[key].grid(row=row, column=0, columnspan=3, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        # Align the labels
        mw.align_labels(widgets)
        mw.align_labels(widgets1)
        mw.align_labels(widgets2)

        # Setup the grids for the atomic centers
        method = self['atomic grid angular quadrature'].get()

        # Remove any widgets previously packed for the atomic grids
        frame = self['atomic_grids']
        for slave in frame.grid_slaves():
            slave.grid_forget()

        # keep track of the row in a variable, so that the layout is flexible
        # if e.g. rows are skipped to control such as 'method' here
        row = 0
        widgets = []
        widgets1 = []
        widgets2 = []

        for key in ('atomic grid lmax', 'atomic grid angular quadrature'):
            self[key].grid(row=row, column=0, columnspan=3, sticky=tk.EW)
            widgets.append(self[key])
            row += 1

        if method == 'Lebedev':
            for key in ('atomic grid Lebedev rule',):
                self[key].grid(row=row, column=1, columnspan=2, sticky=tk.EW)
                widgets1.append(self[key])
                row += 1
        else:
            for key in ('atomic grid phi quadrature',):
                self[key].grid(row=row, column=1, columnspan=2, sticky=tk.EW)
                widgets1.append(self[key])
                row += 1
            for key in ('atomic grid phi n-points',):
                self[key].grid(row=row, column=2, columnspan=1, sticky=tk.EW)
                widgets2.append(self[key])
                row += 1
            for key in ('atomic grid theta quadrature',):
                self[key].grid(row=row, column=1, columnspan=2, sticky=tk.EW)
                widgets1.append(self[key])
                row += 1
            for key in ('atomic grid theta n-points',):
                self[key].grid(row=row, column=2, columnspan=1, sticky=tk.EW)
                widgets2.append(self[key])
                row += 1

        for key in ('atomic grid radial quadrature',
                    'atomic grid region n-points',
                    'atomic grid region outer limit'):
            self[key].grid(row=row, column=0, columnspan=3, sticky=tk.EW)
            widgets.append(self[key])
            row += 1
            
        # Align the labels
        mw.align_labels(widgets)
        mw.align_labels(widgets1)
        mw.align_labels(widgets2)

    def right_click(self, event):
        """Probably need to add our dialog...
        """

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing the AMO Grid input
        """
        if self.dialog is None:
            self.create_dialog()

        self.dialog.activate(geometry='centerscreenfirst')

    def handle_dialog(self, result):
        """Handle the closing of the edit dialog

        What to do depends on the button used to close the dialog. If
        the user closes it by clicking the 'x' of the dialog window,
        None is returned, which we take as equivalent to cancel.
        """
        if result is None or result == 'Cancel':
            self.dialog.deactivate(result)
            return

        if result == 'Help':
            # display help!!!
            return

        if result != "OK":
            self.dialog.deactivate(result)
            raise RuntimeError(
                "Don't recognize dialog result '{}'".format(result))

        self.dialog.deactivate(result)
        # Shortcut for parameters
        P = self.node.parameters

        # Get the values for all the widgets. This may be overkill, but
        # it is easy! You can sort out what it all means later, or
        # be a bit more selective.
        for key in P:
            if key not in ('results', 'create tables'):
                P[key].set_from_widget()

        # and from the results tab...
        if self.tk_var['create tables'].get():
            P['create tables'].value = 'yes'
        else:
            P['create tables'].value = 'no'

        results = P['results'].value = {}
        for key, w_check, w_variable, w_table, w_column \
            in self.results_widgets:

            if self.tk_var[key].get():
                tmp = results[key] = dict()
                tmp['variable'] = w_variable.get()
            table = w_table.get()
            if table != '':
                if key not in results:
                    tmp = results[key] = dict()
                tmp['table'] = table
                tmp['column'] = w_column.get()

    def handle_help(self):
        """Not implemented yet ... you'll need to fill this out!"""
        print('Help not implemented yet for AMO Grid!')

    def setup_results(self, calculation=None):
        """Layout the results tab of the dialog"""
        results = self.node.parameters['results'].value

        self.results_widgets = []
        table = self['results']
        frame = table.interior()

        row = 0
        for key, entry in amo_grid_step.properties.items():
            if 'dimensionality' not in entry:
                continue
            if entry['dimensionality'] != 'scalar':
                continue

            widgets = []
            widgets.append(key)

            table.cell(row, 0, entry['description'])

            # variable
            var = self.tk_var[key] = tk.IntVar()
            var.set(0)
            w = ttk.Checkbutton(frame, variable=var)
            table.cell(row, 1, w)
            widgets.append(w)
            e = ttk.Entry(frame, width=15)
            e.insert(0, key.lower())
            table.cell(row, 2, e)
            widgets.append(e)

            if key in results:
                if 'variable' in results[key]:
                    var.set(1)
                    e.delete(0, tk.END)
                    e.insert(0, results[key]['variable'])

            # table
            w = ttk.Combobox(frame, width=10)
            table.cell(row, 3, w)
            widgets.append(w)
            e = ttk.Entry(frame, width=15)
            e.insert(0, key.lower())
            table.cell(row, 4, e)
            widgets.append(e)

            if key in results:
                if 'table' in results[key]:
                    w.set(results[key]['table'])
                    e.delete(0, tk.END)
                    e.insert(0, results[key]['column'])

            self.results_widgets.append(widgets)
            row += 1

        # And make the dialog wide enough
        frame.update_idletasks()
        width = frame.winfo_width() + 70  # extra space for frame, etc.
        height = frame.winfo_height()
        sw = frame.winfo_screenwidth()
        sh = frame.winfo_screenheight()

        if width > sw:
            width = int(0.9*sw)
        if height > sh:
            height = int(0.9*sh)
            
        self.dialog.geometry('{}x{}'.format(width, height))
