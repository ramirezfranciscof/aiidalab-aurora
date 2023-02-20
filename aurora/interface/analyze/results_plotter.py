# -*- coding: utf-8 -*-

import pandas as pd
import ipywidgets as ipw
import aiida_aurora.utils
import matplotlib.pyplot as plt

from aurora.engine.results import query_jobs, cycling_analysis
from aurora import __version__


class ResultsPlotterComponent(ipw.VBox):
    """Description pending"""

    BOX_LAYOUT_1 = {'width': '40%'}
    BUTTON_STYLE = {'description_width': '30%'}
    BUTTON_LAYOUT = {'margin': '5px'}
    PLOT_TYPES = [('', ''), ('Voltage & current vs time', 'voltagecurrent_time'), ('Voltage vs time', 'voltage_time'), ('Current vs time', 'current_time'), ('Capacity vs cycle', 'capacity_cycle')]

    def __init__(self, plotmaker_model=None):
        """Description pending"""
        self.CURRENT_JOBID = None

        if plotmaker_model is None:
            raise ValueError('An plot maker model must be provided.')
        self.plotmaker_model = plotmaker_model

        # initialize widgets
        self.w_results_header = ipw.HTML(value="<h2>Plot Results</h2>")
        self.w_choose_process = ipw.Text(
            description='Experiment PK:',
            placeholder='PK',
            layout={'width': '30%'},
        )
        self.w_plot_type = ipw.Dropdown(
            description="Select plot type:", value=None,
            options=self.PLOT_TYPES,
            layout=self.BOX_LAYOUT_1, style={'description_width': 'initial'})
        self.w_plot_draw = ipw.Button(
            description="Draw plot",
            button_style='info', tooltip="Draw plot", icon='line-chart',
            disabled=False,
            style=self.BUTTON_STYLE, layout=self.BUTTON_LAYOUT)
        self.w_log_output = ipw.Output()
        self.w_plot_output = ipw.Output(layout={'height': '500px', 'width': '90%', 'overflow': 'scroll', 'border': 'solid 2px', 'margin': '5px', 'padding': '5px'})

        super().__init__()
        self.children = [
            self.w_results_header,
            ipw.HBox([self.w_choose_process, self.w_plot_type, self.w_plot_draw]),
            self.w_log_output,
            self.w_plot_output
        ]
                
        # setup automations
        self.w_plot_draw.on_click(self.draw_plot)
        self.draw_blank_plot()

    @property
    def selected_plot_type(self):
        return self.w_plot_type.value

    @property
    def selected_process_pk(self):
        if self.w_choose_process.value == '':
            return None
        try:
            return int(self.w_choose_process.value)
        except ValueError:
            raise ValueError('PK must be a number!')

    def _cycling_analysis(self):
        return cycling_analysis(self.output_explorer.selected_job_id)
    
    def _load_data(self, dummy=None):
        "Load data, store it, and print some output info."
        self.w_log_output.clear_output()
        if self.selected_job_id:
            self.w_plot_draw.disabled = False
            with self.w_log_output:
                # NOTE TODO: maybe we do not always want to perform a cycling analysis, loading the data would be enough
                self.data = self._cycling_analysis()
        else:
            self.w_plot_draw.disabled = True

        # reset plot
        self.w_plot_type.value = None
        self.w_plot_output.clear_output()

    def draw_plot(self, dummy=None):
        #--- temp for testing
        #self.w_choose_process.value = '192'
        #self.w_plot_type.value = 'voltagecurrent_time'
        #self.w_plot_type.value = 'voltage_time'
        #self.w_plot_type.value = 'current_time'
        #self.w_plot_type.value = 'capacity_cycle'
        #--- temp for testing

        if self.selected_process_pk is None:
            raise ValueError('Select job id!')
            return

        if self.selected_plot_type is None:
            raise ValueError('Select plot type!')
            return

        chosen_data = cycling_analysis(self.selected_process_pk)
        self.w_plot_output.clear_output()
        with self.w_plot_output:
            # NOTE: this is a very rudimental way of creating plots
            # --> check the internet for the best way to work with matplotlib plots in ipywidgets
            # e.g. https://swdevnotes.com/python/2021/interactive-charts-with-ipywidgets-matplotlib/
            # CURRENT BUG: once created, plots cannot be deleted
            # I think we need to implement a way to update a figure/axes
            if not chosen_data:
                print("ERROR: No data loaded!")
            elif self.selected_plot_type == 'voltagecurrent_time':
                aiida_aurora.utils.plot.plot_Ewe_I(chosen_data)
            elif self.selected_plot_type == 'voltage_time':
                aiida_aurora.utils.plot.plot_Ewe(chosen_data)
            elif self.selected_plot_type == 'current_time':
                aiida_aurora.utils.plot.plot_I(chosen_data)
            elif self.selected_plot_type == 'capacity_cycle':
                aiida_aurora.utils.plot.plot_Qd(chosen_data)

        #matplotlib_plot = self.plotmaker_model.make_plot(self.selected_process_pk)
        return

        title = None
        self.w_plot_output.clear_output()
        if self.selected_job_id and self.selected_plot_type:
            self.w_plot_output.clear_output()
            with self.w_plot_output:
                # NOTE: this is a very rudimental way of creating plots
                # --> check the internet for the best way to work with matplotlib plots in ipywidgets
                # e.g. https://swdevnotes.com/python/2021/interactive-charts-with-ipywidgets-matplotlib/
                # CURRENT BUG: once created, plots cannot be deleted
                # I think we need to implement a way to update a figure/axes
                if not self.data:
                    print("ERROR: No data loaded!")
                elif self.selected_plot_type == 'voltagecurrent_time':
                    aiida_aurora.utils.plot.plot_Ewe_I(self.data)
                elif self.selected_plot_type == 'voltage_time':
                    aiida_aurora.utils.plot.plot_Ewe(self.data)
                elif self.selected_plot_type == 'current_time':
                    aiida_aurora.utils.plot.plot_I(self.data)
                elif self.selected_plot_type == 'capacity_cycle':
                    aiida_aurora.utils.plot.plot_Qd(self.data)

    def draw_blank_plot(self):
        """Draws the default blank plot"""
        self.w_plot_output.clear_output()
        with self.w_plot_output:
            #plt.close() # unnecessary with the clear_output?
            fig, axx = plt.subplots(1, figsize=(9, 4))
            plt.subplots_adjust(left=0.1, right=0.95, bottom=0.15, top=0.9)
            fig.suptitle('title1')
            plt.show()
            #return fig, axx
