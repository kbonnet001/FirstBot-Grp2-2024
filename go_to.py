import math

# C'est le chantier ahhhhhhhhhhhhhh

def go_to_xya(x_n, y_n, theta_n, x_n_1 = 0.0, y_n_1 = 0.0, theta_n_1 = 0.0) : 
  """
  Args 
  x_n_1 : current position x (default 0)
  y_n_1 : current position y (default 0)
  theta_n_1 : current orientation (default 0)
  x_n : target position x
  y_n : target position y 
  theta_n : target orientation
   
  
  """
  while (x_n_1 != x_n or y_n_1!= y_n or theta_n_1!=theta_n) : 
    
    # Compute distance to target
    distance = math.sqrt((x_n - x_n_1)**2 + (y_n - y_n_1)**2)

    # Compute angle to target
    theta_target_angle = math.atan2(y_n - y_n_1, x_n - x_n_1)
    
    epsilon_theta = theta_target_angle - theta_n_1 # if we have already a theta
    epsilon_theta = (epsilon_theta + math.pi) % (2 * math.pi) - math.pi # normalisation
    
    # 
    
    return v_gauche, v_droit


import math

def go_to_position(x_current, y_current, theta_current, x_target, y_target, theta_target, L, r, dt):
    # 1. Calculer la distance vers la cible
    distance_to_target = math.sqrt((x_target - x_current)**2 + (y_target - y_current)**2)
    
    # 2. Calculer l'angle vers la cible
    angle_to_target = math.atan2(y_target - y_current, x_target - x_current)
    
    # 3. Calculer la différence d'angle nécessaire pour tourner vers la cible
    angle_error = angle_to_target - theta_current
    
    # 4. Calculer la différence d'orientation pour atteindre theta_target
    theta_error = theta_target - theta_current
    
    # 5. Définir les vitesses linéaire et angulaire (simple contrôle proportionnel)
    # Ajuster ces gains (K_lin et K_ang) selon les besoins du robot
    K_lin = 1.0  # Gain pour la vitesse linéaire
    K_ang = 1.0  # Gain pour la vitesse angulaire
    
    x_dot = K_lin * distance_to_target  # Vitesse linéaire proportionnelle à la distance
    theta_dot = K_ang * (angle_error + theta_error)  # Vitesse angulaire pour corriger l'orientation

    # 6. Calculer les vitesses des roues à partir des vitesses linéaire et angulaire
    v_gauche, v_droit = compute_wheel_speeds(x_dot, theta_dot, L, r)
    
    # 7. Utiliser la fonction pour calculer la variation de position et orientation
    dx, dy, d_theta = calculate_position_variation(x_dot, theta_dot, theta_current, dt)
    
    # 8. Mettre à jour la position et orientation actuelles
    x_new = x_current + dx
    y_new = y_current + dy
    theta_new = theta_current + d_theta
    
    return x_new, y_new, theta_new, v_gauche, v_droit




