import numpy as np
import matplotlib.pyplot as plt

class GetTrajectory:
    def __init__(self, qf, T_max, num_points=None, dt=None):
        """
        qf: List of final positions
        T_max: Maximum time to reach the final position
        num_points: Number of points to generate the trajectory
        dt: Time step to generate the trajectory
        """
        
        self.q0 = np.array([0, 0, 0])
        assert len(qf) == len(self.q0), f"q0 and qf must have the same length: {len(self.q0)}"
        self.qf = np.array(qf)
        self.T_max = int(T_max)
        self.num_points = num_points
        self.dt = dt
        self.dof = len(qf)

        if num_points is not None:
            self.trajectory, self.velocities = self._generate_trajectory_points(num_points)
        elif dt is not None:
            self.trajectory, self.velocities = self._generate_trajectory_dt(dt)
        else:
            raise ValueError("You must specify either num_points or dt.")

    def _generate_trajectory_points(self, num_points):
        t = np.linspace(0, self.T_max, num_points)
        trajectory = np.zeros((num_points, self.dof))
        velocities = np.zeros((num_points, self.dof))

        a0 = self.q0
        a1 = np.zeros(self.dof)
        a2 = np.zeros(self.dof)
        a3 = 10 * (self.qf - self.q0) / self.T_max**3
        a4 = -15 * (self.qf - self.q0) / self.T_max**4
        a5 = 6 * (self.qf - self.q0) / self.T_max**5

        for i in range(num_points):
            tau = t[i]
            trajectory[i] = (
                a0 +
                a1 * tau +
                a2 * tau**2 +
                a3 * tau**3 +
                a4 * tau**4 +
                a5 * tau**5
            )
            velocities[i] = (
                a1 +
                2 * a2 * tau +
                3 * a3 * tau**2 +
                4 * a4 * tau**3 +
                5 * a5 * tau**4
            )

        return trajectory, velocities

    def _generate_trajectory_dt(self, dt):
        t = np.arange(0, self.T_max + dt, dt)
        num_points = len(t)
        if num_points >100:
            raise ValueError("The number of points is too high, please use a lower dt or greater T_max.")
        trajectory = np.zeros((num_points, self.dof))
        velocities = np.zeros((num_points, self.dof))

        a0 = self.q0
        a1 = np.zeros(self.dof)
        a2 = np.zeros(self.dof)
        a3 = 10 * (self.qf - self.q0) / self.T_max**3
        a4 = -15 * (self.qf - self.q0) / self.T_max**4
        a5 = 6 * (self.qf - self.q0) / self.T_max**5

        for i in range(num_points):
            tau = t[i]
            trajectory[i] = (
                a0 +
                a1 * tau +
                a2 * tau**2 +
                a3 * tau**3 +
                a4 * tau**4 +
                a5 * tau**5
            )
            velocities[i] = (
                a1 +
                2 * a2 * tau +
                3 * a3 * tau**2 +
                4 * a4 * tau**3 +
                5 * a5 * tau**4
            )

        return trajectory, velocities

    def plot_trajectory(self):
        if self.num_points is not None:
            t = np.linspace(0, self.T_max, self.num_points)
        else:
            t = np.arange(0, self.T_max + self.dt, self.dt)
        
        plt.figure()
        for i in range(self.dof):
            plt.plot(t, self.trajectory[:, i], label=f'x{i+1} position')
            plt.plot(t, self.velocities[:, i], label=f'v{i+1} velocity', linestyle='--')
        plt.title('Joint Trajectory and Velocities')
        plt.xlabel('Time [s]')
        plt.ylabel('Position / Velocity')
        plt.legend()
        plt.grid(True)
        plt.show()

    def get_trajectory(self):
        self.velocities = np.round(self.velocities, 3)
        self.trajectory = np.round(self.trajectory, 3)
        return self.trajectory, self.velocities

def format_vel(vels):
    # solo 3 decimales
    vx = "{:.4f}".format(vels[0])
    vy = "{:.4f}".format(vels[1])
    w = "{:.4f}".format(vels[2])
    return f"{vx},{vy},{w};"

def send_velocities(velocities: list):
    assert velocities.shape[1] == 3, "Path must have 3 columns"

    msg = ''
    for vels in velocities:
        msg += format_vel(vels)
    print(msg)
        
# Ejemplo de uso
if __name__ == "__main__":
    qf = [0.3, 1, 0.1]  # [Vx, Vy, w]
    T_max = 2.0  # Tiempo máximo

    # Opción 1: Generar trayectoria en base a número de puntos
    num_points = 50
    jtraj_points = GetTrajectory(qf, T_max, num_points=num_points)
    _, velocities_points = jtraj_points.get_trajectory()
    print("Velocidades (num_points):\n", velocities_points)
    # jtraj_points.plot_trajectory()

    # Opción 2: Generar trayectoria en base a dt
    dt = 0.2
    jtraj_dt = GetTrajectory(qf, T_max, dt=dt)
    _, velocities_dt = jtraj_dt.get_trajectory()
    print("Velocidades (dt):\n", velocities_dt)
    send_velocities(velocities_dt)
    distx = 0
    disty = 0
    for vx, vy, w in velocities_dt:
        distx += vx * dt
        disty += vy * dt
    print("Distancia recorrida en x:", distx)
    print("Distancia recorrida en y:", disty)
    # jtraj_dt.plot_trajectory()
