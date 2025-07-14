import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.optimize import root_scalar

import numpy as np

def intersection_and_position(x1, y1, x2, y2, x3, y3, x4, y4, tol=1e-9):
    """
    Compute the intersection point of two lines:
    Line 1: (x1, y1) to (x2, y2)
    Line 2: (x3, y3) to (x4, y4)

    Also determine whether the intersection point lies on the segment (x1, y1)-(x2, y2)
    (i.e., whether it is an internal division point or external).
    Returns:
        intersection: (x, y) coordinates of the intersection point
        is_internal: bool, True if the point lies on segment (x1, y1)-(x2, y2), otherwise False
    """
    # Represent both lines in matrix form
    A = np.array([[x2 - x1, x3 - x4],[y2 - y1, y3 - y4]])
    b = np.array([x3 - x1,y3 - y1])

    # Check determinant (to detect if lines are parallel)
    det = np.linalg.det(A)
    if abs(det) < tol:
        raise ValueError("Lines are parallel; no intersection point")

    # Solve the linear system to get scalar parameters
    t, s = np.linalg.solve(A, b)

    # Compute intersection coordinates
    inter_x = x1 + t * (x2 - x1)
    inter_y = y1 + t * (y2 - y1)

    is_internal = (0 - tol <= t <= 1 + tol)

    return (inter_x, inter_y), is_internal

def intersection_with_slope(x1, y1, x2, y2, x3, y3, m2, tol=1e-9):
    """
    Compute the intersection point between:
    - Line segment from (x1, y1) to (x2, y2)
    - Line with slope m2 passing through (x3, y3)

    Also determine whether the intersection lies on segment (x1, y1)-(x2, y2)

    Returns:
        intersection: (x, y) coordinates of the intersection
        is_internal: bool, True if intersection lies on segment (x1, y1)-(x2, y2)
    """
    # Direction vector of line 1
    dx1 = x2 - x1
    dy1 = y2 - y1

    # Direction vector of line 2 (slope form)
    dx2 = 1.0
    dy2 = m2

    # Matrix form: A * [t, s] = b
    A = np.array([
        [dx1, -dx2],
        [dy1, -dy2]
    ])
    b = np.array([
        x3 - x1,
        y3 - y1
    ])

    # Check for parallel lines
    det = np.linalg.det(A)
    if abs(det) < tol:
        raise ValueError("Lines are parallel; no intersection")

    # Solve for parameters t and s
    t, s = np.linalg.solve(A, b)

    # Compute intersection point on line 1
    inter_x = x1 + t * dx1
    inter_y = y1 + t * dy1

    # Check if intersection lies within segment (x1, y1)-(x2, y2)
    is_internal = (0 - tol <= t <= 1 + tol)

    return (inter_x, inter_y), is_internal



def calc_tangent(M_prev, beta_deg, gamma):
    """
    Calculate the expression:
    2 * cot(beta) * ((M_prev2 * sin^2(beta)) - 1) / (M_prev^2 * (gamma + cos(2*beta)) + 2)
    
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
    sin_beta  = np.sin(beta)
    cos_2beta = np.cos(2 * beta)
    cot_beta  = 1 / np.tan(beta)
    
    # Compute numerator and denominator
    numerator = M_prev**2 * sin_beta**2 - 1
    denominator = M_prev**2 * (gamma + cos_2beta) + 2

    # Final expression
    val = 2 * cot_beta * (numerator / denominator)
    
    return val

def calc_P2P1(beta,gamma,M_prev): 
  val = 1+2*gamma/(gamma+1)*((M_prev*np.sin(beta))**2-1)
  return val

def calc_P1(P0,gamma,M_prev):
  val=P0/(1+(gamma-1)/2*M_prev**2)**(gamma/(gamma-1))
  return val

def calc_Mach(beta,theta1,M_prev,gamma):
  sin_beta = np.sin(beta)
  sin_beta_theta = np.sin(beta - theta1)

  numerator = 1 + (gamma - 1) / 2 * (M_prev * sin_beta) ** 2
  denominator = gamma * (M_prev * sin_beta) ** 2 - (gamma - 1) / 2

  val = 1 / sin_beta_theta * np.sqrt(numerator / denominator)
  return val
  #val=1/np.sin(beta-theta1)*np.sqrt((1+(gamma-1)/2*(M_prev*np.sin(beta))**2)/(gamma*(M_prev*np.sin(beta))**2-(gamma-1)/2))

def find_beta(M_prev, gamma, tanTheta, beta_range=(1.0, 89.9), num_points=1000):
    beta_vals = np.linspace(*beta_range, num_points)
    f_vals = [calc_tangent(M_prev, beta, gamma) - tanTheta for beta in beta_vals]

    for i in range(len(f_vals) - 1):
        if np.sign(f_vals[i]) != np.sign(f_vals[i+1]):
            a = beta_vals[i]
            b = beta_vals[i+1]
            result = root_scalar(
                lambda beta: calc_tangent(M_prev, beta, gamma) - tanTheta,
                bracket=[a, b],
                method='brentq'
            )
            if result.converged:
                return result.root

    raise ValueError("No root found in the specified beta range.")

def find_beta_old(M_prev, gamma, tanTheta, beta_range=(1.0, 89.9)):
    """
    Find beta_deg that makes calc_tangent(...) = tanTheta.
    
    Parameters:
        M_prev (float): upstream Mach number
        gamma (float): specific heat ratio
        tanTheta (float): target value to match
        beta_range (tuple): search interval for beta_deg (in degrees)
    
    Returns:
        float: beta_deg such that calc_tangent(...) ~ tanTheta
    """
    def objective(beta_deg):
        return calc_tangent(M_prev, beta_deg, gamma) - tanTheta

    result = root_scalar(objective, bracket=beta_range, method='brentq')
    
    if result.converged:
        return result.root
    else:
        raise ValueError("No solution found in the specified range.")

def plot_nozzle(M_in,xi,yi,xf,yf,theta_deg=7):
  # Units: mm
  L_total = 110         # Total length of the nozzle
  L_converge = 81       # Length of the converging section
  D_in = 24             # Inlet diameter
  D_out = 4             # Outlet diameter
  #theta_deg = 7         # Wall angle in degrees
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
  x_coords = [x1, x2, x3, x3, x1]
  y_coords = [y1, y2, y2, y4, y4]

  fig, ax = plt.subplots(figsize=(12, 4))
  
  ax.fill(x_coords, y_coords, color='royalblue')              # Draw top half of nozzle
  ax.fill(x_coords, [-y for y in y_coords], color='royalblue')# Draw bottom half of nozzle (mirrored in Y)

  
  # Beam path (reflection points)
  num_reflections = 5
  x_points = np.linspace(x1, x2, num_reflections + 1)
  y_points = [y1 if i % 2 == 0 else -y1 for i in range(num_reflections + 1)]
  
  # Plot reflection points and vertical dashed lines
  #for x, y in zip(x_points, y_points):
  #    ax.plot(x, y, 'ro')             # Red dot at reflection point
  #    ax.plot([x, x], [y, 0], 'r--')  # Vertical dashed line to centerline
  
  # Text annotations
  ax.text(10, y1 + 2, r'$\theta=7^\circ$', fontsize=12)
  ax.text(40, -D_in/2 - 3, 'M={}'.format(M_in), fontsize=12)
  ax.text(30, -D_in/2 - 7, '81', fontsize=10)
  ax.text(45, -D_in/2 - 11, '110', fontsize=10)

  ax.axhline(y=0, color='gray',alpha=0.5,linestyle='--')
  
  # Double-headed arrow for "81"
  arrow1 = FancyArrowPatch((0, -D_in/2 - 5), (81, -D_in/2 - 5),
                           arrowstyle='<->', color='black', mutation_scale=10)
  ax.add_patch(arrow1)
  
  # Double-headed arrow for "110"
  arrow2 = FancyArrowPatch((0, -D_in/2 - 9), (110, -D_in/2 - 9),
                           arrowstyle='<->', color='black', mutation_scale=10)
  ax.add_patch(arrow2)

  for x0,y0,x1,y1 in zip(xi,yi,xf,yf):
    ax.plot([x0,x1],[y0,y1],color='r')
    ax.plot([x0,x1],[-y0,-y1],color='r')

  
  # Plot settings
  ax.set_aspect('equal')
  ax.axis('off')
  plt.tight_layout()
  plt.show()

def calc_shockwave_He():
  M1=4
  theta1_deg=7
  theta1_rad=np.radians(theta1_deg)
  gamma=1.66
  P0=1734582
  T0=319
  m=4.0026
  R0=8.31446
  R=2077.265
  
  tan_Goal=np.tan(theta1_rad)
  #beta0_deg=find_beta(M1, gamma, tan_Goal, beta_range=(1.0, 89.9))
  #beta_rad=np.radians(beta0_deg)
  #print('beta0_deg',beta0_deg)
  M_prev=M1
  P1=calc_P1(P0,gamma,M1)

  x3=0
  y3=12

  x3_list=list()
  x4_list=list()
  y3_list=list()
  y4_list=list()

  print('i,Mach,beta_deg,beta_rad,P2/P1,P1,P2')
  for i in range(7):
    beta_deg=find_beta(M_prev, gamma, tan_Goal, beta_range=(1.0, 89.9))
    beta_rad=np.radians(beta_deg)
    P2P1=calc_P2P1(beta_rad,gamma,M_prev)
    Mach=calc_Mach(beta_rad,theta1_rad,M_prev,gamma)
    P2=P2P1*P1
    print('{},{},{},{},{},{},{}'.format(i+1,Mach,beta_deg,beta_rad,P2P1,P1,P2))


    if i%2==0:
      #print('even')
      x1=0
      y1=0
      x2=81
      y2=0
      (x4,y4),flag=intersection_with_slope(x1,y1,x2,y2,x3,y3,-np.tan(beta_rad))
      #plt.plot([x3,x4],[y3,y4],color='r')
      x3_list.append(x3)
      y3_list.append(y3)
      x4_list.append(x4)
      y4_list.append(y4)
      x3=x4
      y3=y4
    else:
      #print('odd')
      x1=0
      y1=12
      x2=81
      y2=2
      (x4,y4),flag=intersection_with_slope(x1,y1,x2,y2,x3,y3,np.tan(beta_rad))
      #plt.plot([x3,x4],[y3,y4],color='r')
      x3_list.append(x3)
      y3_list.append(y3)
      x4_list.append(x4)
      y4_list.append(y4)
      x3=x4
      y3=y4

    #for next calc
    M_prev=Mach
    P1=P2

  plot_nozzle(M1,x3_list,y3_list,x4_list,y4_list,theta_deg=theta1_deg)
  #plt.show()
  

if __name__=="__main__":
  #plot_nozzle()
  calc_shockwave_He()
