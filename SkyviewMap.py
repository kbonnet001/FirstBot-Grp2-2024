import cv2
import numpy as np
import matplotlib.pyplot as plt

class SkyviewMap() : 
  def __init__(self, width, height, scale, name, background_color=(255, 255, 255), color = (0,0,0), thickness=2):
    self.width = width # pixel
    self.height = height # pixel
    self.scale = scale # scale pixels/m
    self.name = name
    self.color = color # color of drawing
    self.thickness = thickness # thickness of drawing
    self.map_image = np.ones((height, width, 3), dtype=np.uint8) * np.array(background_color, dtype=np.uint8)
    
  # Fonction pour tracer le chemin du robot
  def trace_position_on_map(self, positions_n_1, positions_n) :
    """ Add a new short line between point n-1 and n
    Args : 
    - positions_n_1 (m) : positions (x, y) at n-1
    - positions_n (m) : positions (x, y) at n
    """
    # Convert pos real (m) to pos pixels
    pos_px_n_1 = self.real_to_pixel(positions_n_1)
    pos_px_n = self.real_to_pixel(positions_n)
    
    # Add new short line
    cv2.line(self.map_image, pos_px_n_1, pos_px_n, self.color, self.thickness)
  
  def display_and_save_map(self):
    """Save and show the final map"""
    map_image_rgb = cv2.cvtColor(self.map_image, cv2.COLOR_BGR2RGB)
    plt.imshow(map_image_rgb)
    plt.axis('off')
    cv2.imwrite(f'./{self.name}.jpg', self.map_image) # save
    plt.show()

  def real_to_pixel(self, position):
    """Convert real position xy to position int pixels
    Arg : 
    - position (m) : position real (x,y)
    """
    # Get position
    x, y = position
    x_px = int(self.width/2 + x * self.scale)  # Convertir x en pixels et centrer
    y_px = int(self.height/2 - y * self.scale)  # Convertir y en pixels (attention à l'inversion Y)
    return (x_px, y_px)

# Exemple 
if __name__ == "__main__":
    map_image_test = SkyviewMap(600, 600, 300, "test")
    
    # Exemples
    position_0 = (0.0, 0.0)
    position_1 = (0.05, 0.0)
    position_2 = (0.1, 0.1)
    position_3 = (0.1, 0.1)
    
    # en vrai, à faire à la fin de chaque boucle while pour odom
    map_image_test.trace_position_on_map(position_0, position_1)
    map_image_test.trace_position_on_map(position_1, position_2)
    map_image_test.trace_position_on_map(position_2, position_3)

    map_image_test.display_and_save_map()
