import math
import cmath
import random

#Utils funcions for Measurement Device Independent QKD protocol. Based on NetSquid library
# Utils functions used by MDI nodes

def polarization_angle(qubit):
    # It takes in input a qubit object from netsquid library, work with the ket representation
    # and return the polarization angle of the photon with this.qubit state
    # WARNING: this function works pretty well if qubit state has rational coefficients
    #   in the ket representation. For complex coefficient may return a wrong result 
    q = qubit.qstate.qrepr.ket
    theta = math.acos(abs(q[0]))
    try:
        if abs(q[0]) != 0 and abs(q[1]) != 0:
            phi = cmath.phase((q[1]*(q[0].real-q[0].imag*1j))/(abs(q[0])*abs(q[1])))
        else:
            #print("[!] phi angle could be not available")
            phi = cmath.nan
    except:
        print("phi angle could be not available")
    if not cmath.isnan(phi):
        polarization_angle = math.atan(math.sin(theta)/(math.cos(theta)*math.cos(phi)))
    else:
        polarization_angle = theta

    return polarization_angle
     
def detection_probabilities(theta_a, theta_b, J_square=1, T_square=0.5, R_square=0.5):
    # It takes in input the polarization angle of the two photons entering the 50:50 beam splitter of the measurement device
    # and return a dict of probabilities of which detectors could clicked with the given photons
    # R_square and T_square are respectevly reflection and transmission square amplitudes of the beam splitter
    # J_square is the integral of the waves function. In the ideal scenario is equal to 1 but if a realistic behavior is desiderable
    #   it may useful to change this value with a proper one
    # See doi:10.3390/electronics7040049 for reference 
    same_double_vertical = (math.sin(theta_a) ** 2)*(math.sin(theta_b) ** 2)*(T_square)*(R_square)*(1+J_square)
    same_double_horizontal = (math.cos(theta_a) ** 2)*(math.cos(theta_b) ** 2)*(T_square)*(R_square)*(1+J_square)
    same_vertical_horizontal = (T_square)*(R_square)*((math.sin(theta_a) ** 2)*(math.cos(theta_b) ** 2) + (math.sin(theta_b) ** 2)*(math.cos(theta_a) ** 2) + 2*(math.sin(theta_a))*(math.cos(theta_a))*(math.sin(theta_b))*(math.cos(theta_b))*J_square)
    formula_prob_cvdh = (math.sin(theta_a) ** 2)*(math.cos(theta_b) **  2)*(T_square ** 2) + (math.sin(theta_b) ** 2)*(math.cos(theta_a) ** 2)*(R_square ** 2) - 2*(math.sin(theta_a))*(math.cos(theta_a))*(math.sin(theta_b))*(math.cos(theta_b))*(T_square)*(R_square)*J_square
    formula_prob_chdv = (math.sin(theta_a) ** 2)*(math.cos(theta_b) **  2)*(R_square ** 2) + (math.sin(theta_b) ** 2)*(math.cos(theta_a) ** 2)*(T_square ** 2) - 2*(math.sin(theta_a))*(math.cos(theta_a))*(math.sin(theta_b))*(math.cos(theta_b))*(T_square)*(R_square)*J_square
    formula_prob_cvdv = (math.sin(theta_a) ** 2)*(math.sin(theta_b) **  2)*(1-2*(T_square)*(R_square)*(1+J_square))
    formula_prob_chdh = (math.cos(theta_a) ** 2)*(math.cos(theta_b) **  2)*(1-2*(T_square)*(R_square)*(1+J_square))
    probs = {
        "cvcv": same_double_vertical,
        "dvdv": same_double_vertical,
        "chch": same_double_horizontal,
        "dhdh": same_double_horizontal,
        "cvch": same_vertical_horizontal,
        "dvdh": same_vertical_horizontal,
        "cvdh": formula_prob_cvdh,
        "chdv": formula_prob_chdv,
        "cvdv": formula_prob_cvdv,
        "chdh": formula_prob_chdh,
    }
    return probs

def di_measurement(qubit_a, qubit_b):
    # It returns a possible measurement result for mdi-qkd protocol with two polarized photon in input
    theta_a = polarization_angle(qubit_a)
    theta_b = polarization_angle(qubit_b)
    probs = detection_probabilities(theta_a, theta_b)
    return random.choices(list(probs.keys()), weights=list(probs.values()), k=1)

def extract_qubit(message):
    # Extract the qubit from message received from CombinedChannel
    quantum_message = message[1]
    if len(quantum_message) > 0:
        return quantum_message[0]
    else:
        return None