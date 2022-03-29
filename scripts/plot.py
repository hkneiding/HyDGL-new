import numpy as np
import matplotlib.pyplot as plt
import wandb

from tools import calculate_r_squared


# def plot_metal_center_group_histogram(dataset, meta_data_dict: dict):

#     group_counts = np.zeros(10)
#     for graph in dataset:
#         group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1

#     group_counts = group_counts / len(dataset)

#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.bar(np.arange(3, 13), group_counts)
#     ax.set_xlabel('Metal center group')
#     ax.set_ylabel('Relative size')

#     return fig

def wandb_plot_metal_center_group_histogram(train_dataset, val_dataset, test_dataset, meta_data_dict: dict):

    train_group_counts = np.zeros(10)
    for graph in train_dataset:
        train_group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1
    train_group_counts = train_group_counts / len(train_dataset)

    val_group_counts = np.zeros(10)
    for graph in val_dataset:
        val_group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1
    val_group_counts = val_group_counts / len(val_dataset)

    test_group_counts = np.zeros(10)
    for graph in test_dataset:
        test_group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1
    test_group_counts = test_group_counts / len(test_dataset)

    data = [[name, a, b, c] for (name, a, b, c) in zip(np.arange(3, 13), train_group_counts, val_group_counts, test_group_counts)]
    table = wandb.Table(data=data, columns=['Metal center group', 'Train set ratio', 'Val set ratio', 'Test set ratio'])

    return wandb.plot.bar(table, 'Metal center group', 'Train set ratio', title='by metal center group')


def plot_metal_center_group_histogram(train_dataset, val_dataset, test_dataset, meta_data_dict: dict, file_path='./image.png'):

    train_group_counts = np.zeros(10)
    for graph in train_dataset:
        train_group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1
    train_group_counts = train_group_counts / len(train_dataset)

    val_group_counts = np.zeros(10)
    for graph in val_dataset:
        val_group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1
    val_group_counts = val_group_counts / len(val_dataset)

    test_group_counts = np.zeros(10)
    for graph in test_dataset:
        test_group_counts[meta_data_dict[graph.id]['metal_center_group'] - 3] += 1
    test_group_counts = test_group_counts / len(test_dataset)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(np.arange(3, 13) - 0.25, train_group_counts, width=0.35, label='Train')
    ax.bar(np.arange(3, 13), val_group_counts, width=0.35, label='Val')
    ax.bar(np.arange(3, 13) + 0.25, test_group_counts, width=0.35, label='Test')
    ax.set_xlabel('Metal center group')
    ax.set_ylabel('Relative size')
    ax.set_xticks([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    ax.legend()

    fig.savefig(file_path, format='png', dpi=300)


def plot_correlation(predicted_values: list, true_values: list, file_path='./image.png'):

    # set up canvas
    fig, ax = plt.subplots(figsize=(8, 4))
    # base points
    ax.plot(predicted_values, true_values, 'bo')
    # regression line
    z = np.polyfit(predicted_values, true_values, 1)
    p = np.poly1d(z)
    ax.plot(predicted_values, p(predicted_values), "r--")

    # formatting
    ax.text(0.3, 0.9, 'R² = ' + str(calculate_r_squared(np.array(predicted_values), np.array(true_values))), size=15, color='blue', ha='center', va='center', transform=ax.transAxes)
    ax.set_xlabel('Predicted values')
    ax.set_ylabel('True values')

    fig.savefig(file_path, format='png', dpi=300)


def plot_error_by_metal_center_group(predicted_values: list, true_values: list, metal_center_groups: list):

    group_counts = np.zeros(10)
    group_accumulated_errors = np.zeros(10)
    for i in range(len(predicted_values)):
        group_accumulated_errors[metal_center_groups[i] - 3] += np.abs(predicted_values[i] - true_values[i])
        group_counts[metal_center_groups[i] - 3] += 1

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(np.arange(3, 13), group_accumulated_errors / group_counts)
    ax.set_xlabel('Metal center group')
    ax.set_ylabel('Mean average deviation')

    return fig


def wandb_plot_error_by_metal_center_group(predicted_values: list, true_values: list, metal_center_groups: list):

    group_counts = np.zeros(10)
    group_accumulated_errors = np.zeros(10)
    for i in range(len(predicted_values)):
        group_accumulated_errors[metal_center_groups[i] - 3] += np.abs(predicted_values[i] - true_values[i])
        group_counts[metal_center_groups[i] - 3] += 1

    data = [[name, prec] for (name, prec) in zip(np.arange(3, 13), group_accumulated_errors / group_counts)]
    table = wandb.Table(data=data, columns=['Metal center group', 'Average error'])

    return wandb.plot.bar(table, 'Metal center group', 'Average error', title='Error by metal center group')
