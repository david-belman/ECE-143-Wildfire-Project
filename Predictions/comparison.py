import matplotlib.pyplot as plt
import numpy as np

# Example metrics collected from model outputs
models = ['SVM', 'Gradient Boosting', 'Random Forest']
train_mse = [2337.6735092895883, 478.6357903091953, 595.4732815815545]  # Replace with your actual Train MSE values
test_mse = [5825.792125092726, 2425.6344208155047, 2366.122516513344]  # Replace with your actual Test MSE values
train_r2 = [0.009885986284143167, 0.8544053002103986, 0.8188648750888664]  # Replace with your actual Train R² values
test_r2 = [0.0022354269163704643, 0.13452805150782465, 0.10669289042582175]  # Replace with your actual Test R² values

x = np.arange(len(models))  # the label locations
width = 0.20  # the width of the bars

fig, ax = plt.subplots(figsize=(14, 8))
rects1 = ax.bar(x - width/2, train_mse, width, label='Train MSE')
rects2 = ax.bar(x + width/2, test_mse, width, label='Test MSE')
rects3 = ax.bar(x - width*1.5, train_r2, width, label='Train R²', color='green')
rects4 = ax.bar(x + width*1.5, test_r2, width, label='Test R²',color='red')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by model and dataset')
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
ax.bar_label(rects4, padding=3)

fig.tight_layout()

plt.show()
