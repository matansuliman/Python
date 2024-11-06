

import numpy as np
import matplotlib.pyplot as plt


class PocketAlgorithm:
    def __init__(self, max_iter=1000):
        self.max_iter = max_iter
        self.best_weights = None
        self.best_score = float('inf')

    def h(self, x):
        return np.sign(np.dot(x, self.weights))
    
    def fit(self, X, y):
        # Add a bias term by appending a column of ones to X
        X = np.c_[np.ones(X.shape[0]), X]  # X with bias column

        # Initialize weights and bias term
        self.weights = np.zeros(X.shape[1])
        self.best_weights = self.weights.copy()

        for _ in range(self.max_iter):
            misclassified = []
            
            # Evaluate all points and store the misclassified ones
            for i, x in enumerate(X):
                # y[i] * dot(w,x[i]) <= 0
                if self.h(x) != y[i]:
                    misclassified.append(i)
            
            # Update the pocket if we find a better solution
            if len(misclassified) < self.best_score:
                self.best_score = len(misclassified)
                self.best_weights = self.weights.copy()

            # Stop if all points are correctly classified
            if self.best_score == 0:
                break
            
            # Randomly pick a misclassified point and update the weights
            if misclassified:
                i = np.random.choice(misclassified)
                self.weights += y[i] * X[i]
        
        # Set weights to the best found
        self.weights = self.best_weights
    
    def predict(self, X):
        # Add a bias term by appending a column of ones to X
        X = np.c_[np.ones(X.shape[0]), X]
        # Use the best weights for predictions
        return self.h(X)

    def plot_decision_boundary(self, X, y):
        # Add a bias term by appending a column of ones to X for prediction
        X_bias = np.c_[np.ones(X.shape[0]), X]

        # Create a mesh grid for plotting decision boundaries
        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
        
        # Flatten the grid points and predict their class labels
        grid = np.c_[xx.ravel(), yy.ravel()]
        Z = self.predict(grid)
        Z = Z.reshape(xx.shape)
        
        # Plot the decision boundary
        plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
        
        # Plot the data points
        for label, color, marker in zip(np.unique(y), ['blue', 'red'], ['o', 'x']):
            plt.scatter(X[y == label][:, 0], X[y == label][:, 1], color=color, label=f'Class {label}', marker=marker)
        
        # Labels and legend
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.legend()
        plt.title("Pocket Algorithm Decision Boundary")
        plt.show()

# Example data (2D points)
X = np.array([
    [2, 3],
    [3, 4],
    [4, 3.3],
    [1, 1],
    [5, 2],
    [3, 2]
])
y = np.array([1, 1, 1, -1, -1, -1])

# Initialize the Pocket Algorithm with Plot
pocket_algo = PocketAlgorithm()
pocket_algo.fit(X, y)
print(pocket_algo.predict(X))
pocket_algo.plot_decision_boundary(X, y)