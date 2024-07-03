from search import SearchFromIndex
from calculation import Calculation
from conversation_history import CreateHistory
from adding_process import AddingIndex
from string_store_by_system import StoreBySystem
import settings
import json

class SudyIndex():
    def __init__(self):
        self.index = SearchFromIndex()
        self.calculation = Calculation()
        self.history = CreateHistory()
        self.adding_index = AddingIndex()
        self.store_by_system = StoreBySystem()
    def system_running(self, userComment):
        try:
            index_result = self.index.query(userComment, top_k=settings.retrieve_number_rate * 2, cutoff=settings.remember_rate)
             #print("index_result")
            self.history.make_history(settings.listener_name_set, userComment)
            # print("history_make_listener")
            calculation_result = self.calculation.processing_info(index_result)
            # print("calculation")
            self.adding_index.process_string(settings.listener_name_set, userComment)
            # print("adding_index")

            return calculation_result
            
        except (AttributeError, KeyError):
            self.history.make_history(settings.listener_name_set, userComment)
            # print("except history_make")
            self.adding_index.process_string(settings.listener_name_set, userComment)
            # print("except adding_index")

            return ""
    def system_running2(self, aituber_response):
        self.history.make_history(settings.character_name_set, aituber_response)
        # print("2 history_make")
        self.store_by_system.store_by_system(settings.character_name_set, aituber_response)
        # print("store_system")