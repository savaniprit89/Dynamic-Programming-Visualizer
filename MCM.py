import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def matrix_chain(p):
    n = len(p) - 1 
    dp = np.full((n, n), float('inf'))
    s = [[None] * n for _ in range(n)]
    updates = []
    derivations = []

    for i in range(n):
        dp[i][i] = 0

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                q = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if q < dp[i][j]:
                    dp[i][j] = q
                    s[i][j] = k
                    derivations.append(((i, j), [(i, k), (k + 1, j)]))
            updates.append(dp.copy())

    return dp, s, updates, derivations

def visualize(updates, derivations):
    steps = len(updates)
    cols = 4
    rows = (steps + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 4))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD']
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors)
    
    for step, (dp, derivation) in enumerate(zip(updates, derivations)):
        row, col = divmod(step, cols)
        ax = axes[row, col] if rows > 1 else axes[col]

        im = ax.imshow(dp, cmap=custom_cmap, aspect='auto', interpolation='nearest')
        ax.set_title(f'Step {step + 1}', fontsize=12)
        ax.set_xlabel('Matrix End (j)', fontsize=10)
        ax.set_ylabel('Matrix Start (i)', fontsize=10)

        ax.set_xticks(range(dp.shape[0]))
        ax.set_yticks(range(dp.shape[0]))

        current_cell, source_cells = derivation
        ax.add_patch(plt.Rectangle((current_cell[1]-0.5, current_cell[0]-0.5), 1, 1, fill=False, edgecolor='#A44200', lw=2)) 
        
        for source_cell in source_cells:
            ax.add_patch(plt.Rectangle((source_cell[1]-0.5, source_cell[0]-0.5), 1, 1, fill=False, edgecolor='#3C1518', lw=2))

        for i in range(dp.shape[0]):
            for j in range(dp.shape[1]):
                if dp[i][j] != float('inf'):
                    ax.text(j, i, str(int(dp[i][j])), 
                           ha='center', va='center',
                           color='black', 
                           fontweight='bold')

        ax.grid(True, color='gray', linestyle='--', alpha=0.3)

    for step in range(len(updates), rows * cols):
        row, col = divmod(step, cols)
        ax = axes[row, col] if rows > 1 else axes[col]
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

p = [10, 20, 30, 40, 30]
dp_table, split_table, updates, derivations = matrix_chain(p)
visualize(updates, derivations)
