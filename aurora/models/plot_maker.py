# -*- coding: utf-8 -*-
import json
import logging
import pandas as pd

from pydantic import BaseModel
from typing import Dict, Generic, Sequence, TypeVar, Literal, Union

from aurora.schemas.cycling import ElectroChemSequence, OpenCircuitVoltage
from aurora.schemas.battery import BatterySample, BatterySpecsJsonTypes, BatterySampleJsonTypes
from aurora.engine.results import cycling_analysis


class PlotMakerModel():
    """The model that controls the submission of a process for a set of batteries."""
    
    def __init__(self):
        self.list_of_observers = []
        self.list_of_observations = []

    #----------------------------------------------------------------------#
    # METHODS RELATED TO OBSERVABLES
    #----------------------------------------------------------------------#
    def suscribe_observer(self, observer):
        if observer not in self.list_of_observers:
            self.list_of_observers.append(observer)

    def unsuscribe_observer(self, observer):
        if observer in self.list_of_observers:
            self.list_of_observers.remove(observer)

    def update_observers(self, observators_chain=None):
        if observators_chain is not None:
            self.list_of_observations.append(observators_chain)
        for observer in self.list_of_observers:
            observer.update()

    #----------------------------------------------------------------------#
    # METHODS RELATED TO PLOTTING
    #----------------------------------------------------------------------#
    def make_plot(self, process_pk):
        """Makes the plot for process node with given pk."""
        data = cycling_analysis(process_pk)
        raise ValueError(f'data = \n{data}')


