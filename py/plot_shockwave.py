import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

def calculate_expression(M_prev, beta_deg, gamma):
    """
    Calculate the expression:
    2 * cot(beta) * ((M_prev^2 * sin^2(beta)) - 1) / (M_prev^2 * (gamma + cos(2*beta)) + 2)
    
    Parameters:
        M_prev (float): Mach number of the previous state (Mi-1)
        beta_deg (float): Shock angle beta in degrees
        gamma (float): Specific heat ratio (usually 1.4 for air)

    Returns:
        float: Value of the expression
    """
    # Convert beta from degrees to radians
    beta = np.radians(beta_deg)
    
    # Calculate trigonometric terms
    sin_beta = np.sin(beta)
    cos_2beta = np.cos(2 * beta)
    cot_beta = 1 / np.tan(beta)
    
    # Compute numerator and denominator
    numerator = M_prev**2 * sin_beta**2 - 1
    denominator = M_prev**2 * (gamma + cos_2beta) + 2

    # Final expression
    result = 2 * cot_beta * (numerator / denominator)
    
    return result


def plot_nozzle():
  # Units: mm
  L_total = 110         # Total length of the nozzle
  L_converge = 81       # Length of the converging section
  D_in = 24             # Inlet diameter
  D_out = 4             # Outlet diameter
  theta_deg = 7         # Wall angle in degrees
  theta_rad = np.deg2rad(theta_deg)  # Convert angle to radians
  
  # Nozzle profile (upper wall)
  x1 = 0
  x2 = L_converge
  x3 = L_total
  y1 = D_in / 2
  y2 = y1 - (x2 - x1) * np.tan(theta_rad)
  y3 = y2
  y4 = y1
  
  # Nozzle profile (lower wall) - symmetric about x-axis
  #x_coords = [x1, x2, x3, x3, x2, x1]
  #y_coords = [y1, y2, y2, -y2, -y2, -y1]
  x_coords = [x1, x2, x3, x3, x1]
  y_coords = [y1, y2, y2, y4, y4]

  fig, ax = plt.subplots(figsize=(12, 4))
  
  # Draw top half of nozzle
  ax.fill(x_coords, y_coords, color='royalblue')
  # Draw bottom half of nozzle (mirrored in Y)
  ax.fill(x_coords, [-y for y in y_coords], color='royalblue')
  
  # Beam path (reflection points)
  num_reflections = 5
  x_points = np.linspace(x1, x2, num_reflections + 1)
  y_points = [y1 if i % 2 == 0 else -y1 for i in range(num_reflections + 1)]
  
  # Plot reflection points and vertical dashed lines
  for x, y in zip(x_points, y_points):
      ax.plot(x, y, 'ro')             # Red dot at reflection point
      ax.plot([x, x], [y, 0], 'r--')  # Vertical dashed line to centerline
  
  # Text annotations
  ax.text(10, y1 + 2, r'$\theta=7^\circ$', fontsize=12)
  ax.text(40, -D_in/2 - 3, 'M=4', fontsize=12)
  ax.text(30, -D_in/2 - 7, '81', fontsize=10)
  ax.text(45, -D_in/2 - 11, '110', fontsize=10)
  
  # Double-headed arrow for "81"
  arrow1 = FancyArrowPatch((0, -D_in/2 - 5), (81, -D_in/2 - 5),
                           arrowstyle='<->', color='black', mutation_scale=10)
  ax.add_patch(arrow1)
  
  # Double-headed arrow for "110"
  arrow2 = FancyArrowPatch((0, -D_in/2 - 9), (110, -D_in/2 - 9),
                           arrowstyle='<->', color='black', mutation_scale=10)
  ax.add_patch(arrow2)
  
  # Plot settings
  ax.set_aspect('equal')
  ax.axis('off')
  plt.tight_layout()
  plt.show()
  
  #plt.figure(figsize=(12, 4))
  #plt.fill(x_coords, y_coords, color='royalblue')  # Draw nozzle shape (top)

  #y_coords=[-y for y in y_coords]
  #plt.fill(x_coords, y_coords, color='royalblue')  # Draw nozzle shape (bottom)
  #
  ## Beam path (reflections), assume 5 reflections
  #num_reflections = 5
  #x_points = np.linspace(x1, x2, num_reflections + 1)
  #y_points = [y1 if i % 2 == 0 else -y1 for i in range(num_reflections + 1)]
  ##plt.plot(x_points, y_points, color='skyblue')  # Beam reflection lines
  #
  ## Red particle tracks (dots + vertical dashed lines)
  #for x, y in zip(x_points, y_points):
  #    plt.plot(x, y, 'ro')              # Red dot at reflection point
  #    plt.plot([x, x], [y, 0], 'r--')   # Vertical dashed line to center axis
  #
  ## Simple annotations
  #plt.text(10, y1 + 2, r'$\theta=7^\circ$', fontsize=12)
  #plt.text(40, -D_in/2 - 3, 'M=4', fontsize=12)
  #plt.arrow(0, -D_in/2 - 5, 81, 0, length_includes_head=True,head_width=1, head_length=1, color='black')
  #plt.text(30, -D_in/2 - 7, '81', fontsize=10)
  #
  #plt.arrow(0, -D_in/2 - 9, 110, 0, head_width=1, head_length=3, color='black')
  #plt.text(45, -D_in/2 - 11, '110', fontsize=10)
  #
  ## Plot settings
  #plt.axis('equal')
  #plt.axis('off')
  #plt.tight_layout()
  #plt.show()

if __name__=="__main__":
  plot_nozzle()
