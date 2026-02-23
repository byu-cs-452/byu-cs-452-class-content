import matplotlib.pyplot as plt
import numpy as np
import random

# Configuration
rows, cols = 15, 15  # Size of the matrix
fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
ax.set_facecolor('#fdfdfd')

# 1. Generate the Matrix of Weights
matrix = np.random.rand(rows, cols)

# 2. Display the weights as text and a background heatmap
for i in range(rows):
    for j in range(cols):
        val = matrix[i, j]
        ax.text(j, i, f"{val:.2f}", ha='center', va='center', 
                fontsize=8, color='black', fontweight='bold', zorder=5)
        # Optional: light colored squares behind numbers
        rect = plt.Rectangle((j-0.5, i-0.5), 1, 1, color='whitesmoke', alpha=0.5, zorder=1)
        ax.add_patch(rect)

# 3. Lines from the left (Input)
for i in range(rows):
    ax.annotate('', xy=(-0.5, i), xytext=(-3, i),
                arrowprops=dict(arrowstyle="-", color='royalblue', lw=1.2, alpha=0.6))

# 4. Lines to the right (Output)
for i in range(rows):
    ax.annotate('', xy=(cols-0.5, i), xytext=(cols+2, i),
                arrowprops=dict(arrowstyle="-", color='crimson', lw=1.2, alpha=0.6))

# 5. Internal connections (Weight to Weight)
# Connecting a subset to avoid a total "blackout" of lines
for _ in range(100):
    r1, c1 = random.randint(0, rows-1), random.randint(0, cols-1)
    r2, c2 = random.randint(0, rows-1), random.randint(0, cols-1)
    ax.plot([c1, c2], [r1, r2], color='gray', lw=0.5, alpha=0.2, zorder=2)

# 6. Random lines from Top-Left to "Hundreds of values" (The Flood - Green)
for _ in range(200):
    target_r = random.randint(0, rows-1)
    target_c = random.randint(0, cols-1)
    ax.plot([-3, target_c], [rows+2, target_r], color='#2ecc71', 
            lw=0.4, alpha=0.15, zorder=3)

# Formatting
ax.set_xlim(-4, cols + 3)
ax.set_ylim(-2, rows + 3)
plt.axis('off')
plt.tight_layout()
plt.savefig("c:/repos/ag/embeddings/neuralnetpicture/complex_matrix.png", bbox_inches='tight', dpi=300)
print("Image saved to c:/repos/ag/embeddings/neuralnetpicture/complex_matrix.png")
plt.show()
