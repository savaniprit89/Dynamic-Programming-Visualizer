import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def lcs(X, Y):
    m = len(X)
    n = len(Y)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    updates = []
    derivations = []

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                derivations.append(((i, j), [(i - 1, j - 1)]))
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                derivations.append(((i, j), [(i - 1, j), (i, j - 1)]))
            updates.append(dp.copy())

    return updates, derivations

def visualize(updates, derivations, X, Y):
    steps = len(updates)
    cols = 4
    rows = (steps + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 4))
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD']
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors)
    
    for step, (dp, derivation) in enumerate(zip(updates, derivations)):
        row, col = divmod(step, cols)
        ax = axes[row, col] if rows > 1 else axes[col]

        im = ax.imshow(dp, cmap=custom_cmap, aspect='auto')
        ax.set_title(f'Step {step + 1}', fontsize=12, pad=10)
        ax.set_xlabel('Y: ' + Y, fontsize=10)
        ax.set_ylabel('X: ' + X, fontsize=10)

        ax.set_xticks(range(dp.shape[1]))
        ax.set_yticks(range(dp.shape[0]))
        ax.set_xticklabels([''] + list(Y))
        ax.set_yticklabels([''] + list(X))

        current_cell, source_cells = derivation
        ax.add_patch(plt.Rectangle((current_cell[1]-0.5, current_cell[0]-0.5), 1, 1, fill=False, edgecolor='#A44200', lw=2)) 
        
        for source_cell in source_cells:
            ax.add_patch(plt.Rectangle((source_cell[1]-0.5, source_cell[0]-0.5), 1, 1, fill=False, edgecolor='#3C1518', lw=2))

        for i in range(dp.shape[0]):
            for j in range(dp.shape[1]):
                ax.text(j, i, str(dp[i, j]), 
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

X = "AGGTAB"
Y = "GXTXAYB"
updates, derivations = lcs(X, Y)
visualize(updates, derivations, X, Y)