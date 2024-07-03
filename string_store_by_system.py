import os

class StoreBySystem:
    def store_by_system(self, person, system_response):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        store_path1 = os.path.join(script_directory, "string_store.txt")
        store_path2 = os.path.join(script_directory, "string_store_person.txt")
        stored_string_person = person + ":" + system_response
        with open(store_path1, 'a', encoding="utf-8") as file:
            file.write("\n"+system_response)
        with open(store_path2, 'a', encoding="utf-8") as file:
            file.write("\n"+stored_string_person)