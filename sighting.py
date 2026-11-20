# sighting class for user observations
class Sighting:
  def __init__(self, sighting_id,  animal, image, date, latitude, longitude, notes=""):
    # animal object
    self.sighting_id = sighting_id
    self.animal = animal
    self.image = image
    self.date = date
    self.latitude = latitude
    self.longitude = longitude
    self.notes = notes
  
  def get_info(self):
    return f"{self.sighting_id}, {self.animal.name}, {self.image}, {self.date}, {self.latitude}, {self.longitude}, {self.notes}" 