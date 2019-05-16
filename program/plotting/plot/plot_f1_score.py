


f1_score = calc_f1(y_true, y_pred, labels=None, pos_label=1, average='binary', sample_weight=None)




def plot_thresholds(title, ax, thresholds, distances, annotations):
    min_distances = list(np.amin(distances, axis=1))



    f1_scores = []
    recalls = []
    precisions = []
    y_true = np.array(annotations)
    for threshold in thresholds:
        predictions = threshold_predictions(min_distances, threshold)
        recall = recall_score(y_true, predictions)
        precision = precision_score(y_true, predictions)
        f1_score = calc_f1(y_true, predictions)
        recalls.append(recall)
        precisions.append(precision)
        f1_scores.append(f1_score)
    ax.plot(thresholds, f1_scores)
    ax.plot(thresholds, recalls)
    ax.plot(thresholds, precisions)
    ax.legend(['f1_score', 'recall', 'precision'], loc='lower left')
    ax.set_title(title)

    results = [f1_scores, precisions, recalls]
    return results
    # ax.xlabel('threshold')
    # plt.show()


def plot_distances(title, ax, distances):
    ax.imshow(distances)
    ax.set_title(title)


def observe_optimal_threshold(results, thresholds):
    list_f1_scores = []
    for result in results:
        f1_scores = result[0]
        list_f1_scores.append(f1_scores)
    all_f1_scores = np.array(list_f1_scores)
    list_f1_scores = list(all_f1_scores.T)
    means = np.mean(all_f1_scores, axis=0)
    stds = np.round(np.std(all_f1_scores, axis=0), 2)
    df_data = {
        'threshold': thresholds,
        'f1_score_mean': means,
        'f1_score_std': stds,
        'f1_scores': list_f1_scores
    }

    df = pd.DataFrame.from_dict(df_data)
    df = df.sort_values(['f1_score_mean', 'f1_score_std'], ascending=[False, True])
    return df


def plot_(N):

    distances = cdist(np.array(list(dataset_augmented['hash_add'])), trailer_hashes, metric='hamming')
    # %%
    min_distances = list(np.amin(distances, axis=1))
    predictions = [1 if distance < 0.07 else 0 for distance in min_distances]
    dataset['predictions'] = predictions
    # %%
    dataset
    # %%
    thresholds = [0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(4, 2, sharex=True, sharey=True)
    results1 = plot_thresholds('no augmentation', ax1, thresholds,
                               cdist(np.array(list(dataset.hash)), trailer_hashes, metric='hamming'), dataset.annotation)
    results2 = plot_thresholds('colorspace change', ax2, thresholds,
                               cdist(np.array(list(dataset_augmented['hash_add'])), trailer_hashes, metric='hamming'),
                               dataset.annotation)
    results3 = plot_thresholds('gaussian noise', ax3, thresholds,
                               cdist(np.array(list(dataset_augmented['hash_gauss'])), trailer_hashes, metric='hamming'),
                               dataset.annotation)
    results4 = plot_thresholds('compression', ax4, thresholds,
                               cdist(np.array(list(dataset_augmented['hash_compress'])), trailer_hashes, metric='hamming'),
                               dataset.annotation)
    results5 = plot_thresholds('hue and saturation change', ax5, thresholds,
                               cdist(np.array(list(dataset_augmented['hash_add_hsv'])), trailer_hashes, metric='hamming'),
                               dataset.annotation)
    results6 = plot_thresholds('contrast', ax6, thresholds,
                               cdist(np.array(list(dataset_augmented['hash_contrast'])), trailer_hashes, metric='hamming'),
                               dataset.annotation)
    results7 = plot_thresholds('aspect ratio', ax7, thresholds,
                               cdist(np.array(list(dataset_augmented['hash_resize'])), trailer_hashes, metric='hamming'),
                               dataset.annotation)

    fig.set_size_inches(18.5, 10.5)
    fig.savefig('thresholds_{}'.format(film))

    # %%
    results = [results1, results2, results3, results4, results5, results6, results7]
    df = get_optimal_threshold(results, thresholds)



def plot_many():
    plt.rcParams['figure.figsize'] = [10, 20]

    fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4, sharex=True, sharey=True)

    plot_distances('no augmentation', ax1, distances)
    plot_distances('colorspace change', ax2, distances_add)
    plot_distances('gaussian noise', ax3, distances_gauss)
    plot_distances('compression', ax4, distances_compress)
    plot_distances('hue and saturation change', ax5, distances_add_csv)
    plot_distances('contrast', ax6, distances_constrast)
    plot_distances('aspect ratio', ax7, distances_resize)

    fig.savefig('distances')