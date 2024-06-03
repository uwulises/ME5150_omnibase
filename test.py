import numpy as np
PI = 3.14159265359;  # pi
QUARTER_PI = PI / 4;  # pi/4
max_v = 0.25;  # m/s
r = 0.025;  # m
max_w_rads = max_v / r;  # rad/s
print(max_w_rads)
max_pwm = 255;  # PWM

encoder_resolution = 2500;                  
rad2enc = encoder_resolution / (2 * PI); 

max_w_encoder = max_w_rads * rad2enc;  
min_w_encoder = - max_w_encoder
enc2pwm = max_pwm / max_w_encoder; 
print(max_w_encoder)


Vx = 0.5
Vy = 0
w = 0
# r = 27
# lxy = 0.1
# w1 = -(Vx + Vy + lxy * w)* 1 / r
# w2 = (Vx - Vy - lxy * w)* 1 / r
# w3 = -(Vx - Vy + lxy * w)* 1 / r
# w4 = (Vx + Vy - lxy * w)* 1 / r

# print(w1, w2, w3, w4)
# l=75
# print(np.sqrt(2)*l)

R = 75
r = 25
w1 = (-np.sin(QUARTER_PI) * Vx + np.cos(QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000);          
w2 = (-np.sin(3 * QUARTER_PI) * Vx + np.cos(3 * QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000);  
w3 = (-np.sin(5 * QUARTER_PI) * Vx + np.cos(5 * QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000);  
w4 = (-np.sin(7 * QUARTER_PI) * Vx + np.cos(7 * QUARTER_PI) * Vy + (R/1000) * w) * 1 / (r/1000);  
w =[w1, w2, w3, w4]

print(w)
if np.max(np.abs(w)) > max_w_rads: #mantener en el rango -max_w_rads, max_w_rads
    w = w / np.max(np.abs(w)) * max_w_rads
print(w)

m_enc = [i*rad2enc for i in [w1, w2, w3, w4]]
print(m_enc)

m_pwm = [i*enc2pwm for i in m_enc]
print(m_pwm)