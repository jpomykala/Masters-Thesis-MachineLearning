import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from sklearn.utils.multiclass import unique_labels

from src.consts import plotFormat, dpi, plot_save_path


def start_test(iterations, y_test, clf_function, args):
    fit_time_acc = 0
    predict_time_acc = 0
    accuracy_acc = 0

    for iter_index in range(0, iterations):
        y_pred, fit_time, predict_time = clf_function(*args)
        fit_time_acc += fit_time
        predict_time_acc += predict_time
        accuracy_acc += accuracy_score(y_test, y_pred)

    mean_fit_time = fit_time_acc / iterations
    mean_predict_time = predict_time_acc / iterations
    mean_accuracy = accuracy_acc / iterations

    return mean_accuracy, mean_fit_time, mean_predict_time


def report_data(title, iterations, y_test, labels, clf_function, args):
    precision_acc = 0
    recall_acc = 0
    f1_acc = 0
    support_acc = 0

    for iter_index in range(0, iterations):
        y_pred, fit_time, predict_time = clf_function(*args)
        clf_report_plot(title, y_test, y_pred, target_names=labels)
        print(classification_report(y_test, y_pred, target_names=labels))

    mean_precision_acc = precision_acc / iterations
    mean_recall_acc = recall_acc / iterations
    mean_f1_acc = f1_acc / iterations
    mean_support_acc = support_acc
    return mean_precision_acc, mean_recall_acc, mean_f1_acc, mean_support_acc


def clf_report_plot(title, y_true, y_pred, target_names=None, sample_weight=None):
    labels = unique_labels(y_true, y_pred)
    p, r, f1, s = precision_recall_fscore_support(y_true, y_pred,
                                                  labels=labels,
                                                  average=None,
                                                  sample_weight=sample_weight)

    p = np.append(p, np.average(p, weights=s))
    r = np.append(r, np.average(r, weights=s))
    f1 = np.append(f1, np.average(f1, weights=s))

    rows = zip(target_names, p, r, f1, s)

    classes = [x[0] for x in rows]
    classes.append('średnia')
    data = np.array([p, r, f1])
    data = np.transpose(data)

    shape = (len(classes), 3)
    matrix_data = data.reshape(shape)

    categories = ['precyzja', 'czułość', 'miara f1']

    fig, ax = plt.subplots()
    im = ax.imshow(matrix_data, interpolation='nearest', cmap=plt.cm.coolwarm_r, vmin=0, vmax=1)

    ax.set_xticks(np.arange(len(categories)))
    ax.set_yticks(np.arange(len(classes)))

    ax.set_xticklabels(categories)
    ax.set_yticklabels(classes)

    ax.set_aspect('auto')

    fmt = '.2f'
    tresh_low = 0.4
    tresh_high = 0.6

    for i in range(len(classes)):
        for j in range(len(categories)):
            text = ax.text(j, i, format(matrix_data[i, j], fmt),
                           ha="center", va="center",
                           color="black" if tresh_low < matrix_data[i, j] < tresh_high else "white")

    ax.set_title(title)
    fig.tight_layout()
    plt.savefig(plot_save_path + 'report-' +
                title.lower().replace(' ', '-').encode("ascii", errors="ignore").decode() +
                "." + plotFormat, dpi=dpi,
                format=plotFormat)
    plt.show()
