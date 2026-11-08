# observation will need animal object
class Observation:
  def __init__(self, animal, observer, date, location, latitude, longitude):
    # animal should be an object I need it's name
    self.animal = animal
    self.observer = observer
    self.date = date
    self.location = location
    self.latitude = latitude
    self.longitude = longitude
    
  # give back above data
  def get_info(self):
    return f"{self.animal.name}, {self.observer}, {self.date}, {self.location}, {self.latitude}, {self.longitude}"
  