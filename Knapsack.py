import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

def knapsack(weights, values, capacity):
    n = len(weights)
    dp = np.zeros((n + 1, capacity + 1), dtype=int)
    updates = []
    derivations = []

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                if dp[i - 1][w - weights[i - 1]] + values[i - 1] > dp[i - 1][w]:
                    dp[i][w] = dp[i - 1][w - weights[i - 1]] + values[i - 1]
                    derivations.append(((i, w), [(i-1, w), (i-1, w - weights[i-1])]))
                else:
                    dp[i][w] = dp[i - 1][w]
                    derivations.append(((i, w), [(i-1, w)]))
            else:
                dp[i][w] = dp[i - 1][w]
                derivations.append(((i, w), [(i-1, w)]))
            updates.append(dp.copy())
    
    return updates, derivations

def visualize(updates, derivations):
    steps = len(updates)
    cols = 4
    rows = (steps + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 4))
    
    colors = ['#FF6B6B', '#4ECDC4','#45B7D1','#96CEB4','#FFEEAD']
    
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors)
    
    for step, (dp, derivation) in enumerate(zip(updates, derivations)):
        row, col = divmod(step, cols)
        ax = axes[row, col] if rows > 1 else axes[col]

        im = ax.imshow(dp, cmap=custom_cmap, aspect='auto')
        ax.set_title(f'Step {step + 1}', fontsize=12, pad=10)
        ax.set_xlabel('Capacity', fontsize=10)
        ax.set_ylabel('Items', fontsize=10)

        ax.set_yticks(range(dp.shape[0]))
        ax.set_xticks(range(dp.shape[1]))

        current_cell, source_cells = derivation
        ax.add_patch(plt.Rectangle((current_cell[1]-0.5, current_cell[0]-0.5), 1, 1, fill=False, edgecolor='#A44200', lw=2)) 
        
        for source_cell in source_cells:
            ax.add_patch(plt.Rectangle((source_cell[1]-0.5, source_cell[0]-0.5), 1, 1, fill=False, edgecolor='#3C1518', lw=2))

        for i in range(dp.shape[0]):
            for j in range(dp.shape[1]):
                ax.text(j, i, str(dp[i, j]),  ha='center', va='center', color='black', fontweight='bold')

        ax.grid(True, color='gray', linestyle='--', alpha=0.3)

    for step in range(len(updates), rows * cols):
        row, col = divmod(step, cols)
        ax = axes[row, col] if rows > 1 else axes[col]
        ax.axis('off')
    plt.tight_layout()
    plt.show()


weights = [4, 5, 1]
values = [1, 2, 3]
capacity = 4
updates, derivations = knapsack(weights, values, capacity)
visualize(updates, derivations)

