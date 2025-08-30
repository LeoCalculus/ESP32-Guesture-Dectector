import numpy as np
train_y_indices = np.repeat([0, 1, 2, 3], 100)  # [0...0, 1...1, 2...2, 3...3] 100 times each
train_y_onehot = np.eye(4)[train_y_indices]  # Convert to one-hot (400, 4)
print(train_y_onehot)