import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import json
import numpy as np
from landmark_reader import LandMarkReader

# with open("landmarks_v4/00666.json") as f:
#     data = json.load(f)
lmr = LandMarkReader('landmarks_v5/00666.bin')
with open("meshes_v2.json") as f:
    mesh_data = json.load(f)

class AnimationViewer:
    def __init__(self, master):
        self.master = master
        master.title("Animation Viewer")

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection="3d")
        self.ax.view_init(elev=0, azim=-90)
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.frame_index = 0
        self.animation_running = False

        self.replay_button = tk.Button(master, text="Replay", command=self.replay_animation)
        self.replay_button.pack(side=tk.BOTTOM)

    def draw_meshes(self, part, color, dsize, esize, draw_edges=True):
        mpart = part[-4:]
        # points = np.array(data[part][self.frame_index])
        points = np.array([lmr.get(part, self.frame_index, pi) for pi in range(lmr.get_numpoints(part))])
        x_vals = points[:, 0]
        y_vals = np.zeros(len(points))
        z_vals = 256 - points[:, 1]

        if part == 'pose':
            y_vals = y_vals / 10 + 0.1

        # self.ax.scatter(x_vals, y_vals, z_vals, s=dsize, c=color)
        if draw_edges:
            for edge in mesh_data[mpart]:
                self.ax.plot(
                    [x_vals[edge[0]], x_vals[edge[1]]],
                    [y_vals[edge[0]], y_vals[edge[1]]],
                    [z_vals[edge[0]], z_vals[edge[1]]],
                    linewidth=esize,
                    color=color,
                )

    def update_plot(self):
        self.ax.clear()
        self.ax.set_xlim(0, 256)
        self.ax.set_ylim(-128, 128)
        self.ax.set_zlim(0, 256)

        self.draw_meshes("face", "blue", 0.05, 1)
        self.draw_meshes("pose", "green", 2, 1)
        self.draw_meshes("rhand", "red", 2, 1)
        self.draw_meshes("lhand", "orange", 2, 1)

        self.canvas.draw()

    def replay_animation(self):
        if not self.animation_running:
            self.animation_running = True
            self.replay_button.config(state=tk.DISABLED)
            while self.frame_index < lmr.num_frames:
                self.update_plot()
                self.frame_index += 1
                self.master.update_idletasks()
                time.sleep(0.01)  # Adjust pause time as needed
            self.frame_index = 0
            self.animation_running = False
            self.replay_button.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    AnimationViewer(root)
    root.mainloop()


if __name__ == "__main__":
    main()
