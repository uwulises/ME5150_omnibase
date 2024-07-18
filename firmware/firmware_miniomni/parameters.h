
#define QUARTER_PI 0.7853981633974483

#define M1_I1 5
#define M1_I2 6
#define M1_A 0
#define M1_B 1

#define M2_I1 4
#define M2_I2 3
#define M2_A 15
#define M2_B 14

#define M3_I1 10
#define M3_I2 9
#define M3_A 20
#define M3_B 21

#define M4_I1 11
#define M4_I2 12
#define M4_A 19
#define M4_B 18


int dt_vel = 100;      // Periodo de actualización velocidad, en milisegundos
// int dt_pid = 200;       // Periodo de actualización PID, en milisegundos
unsigned long t1_mot = 0;
unsigned long t1_pid = 0;

// /* Parametros omni */
// const int l = 75;  // Mitad de la distancia entre las ruedas delanteras y traseras, e izquierdas y derechas, en mm
// const int r = 30;  // Radio de las ruedas, en mm

/* Parametros miniomni*/
const int R = 75;  // Distancia desde el centro de robot al centro de las ruedas, en mm
const int r = 25;  // Radio de las ruedas, en mm
const int lxy = sqrt(2) * R;

const int encoder_resolution = 2500;                // encoder steps per revolution
const float rad2enc = encoder_resolution / (2 * PI);  // encoder steps per radian 397

const int max_pwm = 255;                         // PWM
const int max_w_rads = 20;                       // rads/s o 0.5 m/s
const int max_w_encoder = max_w_rads * rad2enc;  // encoder steps per second
const int min_w_encoder = -max_w_encoder;        // encoder steps per second