import numpy as np
import matplotlib.pyplot as plt

class GetTrajectory:
    def __init__(self, qf, num_points):
        self.q0 = np.array([0, 0, 0])
        assert len(qf) == len(self.q0), f"q0 and qf must have the same length: {len(self.q0)}"
        self.qf = np.array(qf)
        self.num_points = num_points
        self.dof = len(qf)
        self.trajectory, self.velocities = self._generate_trajectory()

    def _generate_trajectory(self):
        t = np.linspace(0, 1, self.num_points)
        trajectory = np.zeros((self.num_points, self.dof))
        velocities = np.zeros((self.num_points, self.dof))

        a0 = self.q0
        a1 = np.zeros(self.dof)
        a2 = np.zeros(self.dof)
        a3 = 10 * (self.qf - self.q0)
        a4 = -15 * (self.qf - self.q0)
        a5 = 6 * (self.qf - self.q0)

        for i in range(self.num_points):
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
        t = np.linspace(0, 1, self.num_points)
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
        return self.trajectory, self.velocities

# Ejemplo de uso
if __name__ == "__main__":
    qf = [0, 1, 0.1]  # [Vx, Vy, w]
    num_points = 50  # Número de puntos en la trayectoria

    jtraj = GetTrajectory(qf, num_points)
    _, velocities = jtraj.get_trajectory()
    # print("Posiciones:\n", trajectory)
    print("Velocidades:\n", velocities)
    jtraj.plot_trajectory()
    
