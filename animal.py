# cretea class object, call it animal
class Animal:
  # initiate animal object, while requesting 4 arguements 
  def __init__(self, name, scientific_name, rank):
    # self refers to this unique instance of animal being created, self allows all following methods to be able to reference all parameters
    self.name = name
    self.scientific_name = scientific_name
    self.rank = rank
  
  def get_info(self):
    return f"{self.name}, {self.scientific_name}, {self.rank}"
  
