import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# Define parameters for the grid
N = 100  # Grid size (increased for more detail)
ON = 255  # ON cells (white)
OFF = 0  # OFF cells (black)
vals = [ON, OFF]

# Create a random grid
grid = np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def update(frameNum, img, grid, N):
    newGrid = grid.copy()
    for i in range(N):
        for j in range(N):
            # Compute 8-neighbor sum
            total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
                     grid[(i-1)%N, j] + grid[(i+1)%N, j] + 
                     grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + 
                     grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N]) // 255

            # Apply Conway's rules
            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    # Update data
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# Set up the figure
fig, ax = plt.subplots()
img = ax.imshow(grid, interpolation='nearest', cmap='viridis')
ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ), frames=1000, interval=50, save_count=50)

# Save the animation
ani.save('conways_game_of_life.gif', writer=PillowWriter(fps=15))

plt.close(fig)  # Closing the plot to prevent it from displaying in the notebook
