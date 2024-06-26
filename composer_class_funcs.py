# Functions to support classifier notebook explore_nb_mido.ipynb

## Libraries
import os
import numpy as np
import pandas as pd
# midi files
import mido
# sklearn 
from sklearn.metrics import accuracy_score, classification_report, precision_recall_curve, roc_curve, auc, roc_auc_score
# viz
import matplotlib.pyplot as plt
import seaborn as sns

# extract features from midi file using mido library
def extract_features_from_midi(file_path, second_interval=[1,30]):
    ## Input: file path of midi file
    ## Output: list [ticks per beat, key, average_velocity, note counts for 128 notes]

    # import file
    midi = mido.MidiFile(file_path)

    # initialize values
    note_counts = [0] * 128  # MIDI notes range from 0 to 127
    # total_velocity = 0
    velocities = []
    note_on_count = 0
    elapsed_time = 0
    key = '' # each file should have only 1 key. Investigate if this assumption is correct.
    tpb = midi.ticks_per_beat
    type = midi.type
    filename = os.path.basename(midi.filename)


    # get ticks
    for msg in midi:
        # get the key
        if msg.is_meta and msg.type == 'key_signature':
            key = msg.key
        
        # extract messages for the time window specified
        elapsed_time += msg.time
        if (elapsed_time>=second_interval[0] and elapsed_time<=second_interval[1]):
            if msg.type == 'note_on' and msg.velocity > 0:
                note_counts[msg.note] += 1
                # total_velocity += msg.velocity
                velocities.append(msg.velocity)
                note_on_count += 1
            
    # Calculate velocity statistics
    if velocities:
        average_velocity = np.mean(velocities)
        variance_velocity = np.var(velocities)
    else:
        average_velocity = 0
        variance_velocity = 0
    
    # Normalize the note counts to be between 0 and 1
    normalized_note_counts = (note_counts - np.min(note_counts)) / (np.max(note_counts) - np.min(note_counts))
    
    # combine into 1 list
    combined_features = [filename, type, tpb, key, average_velocity, variance_velocity] + list(normalized_note_counts)

    return combined_features

# sample implementation for testing
# file_path_ps2 = test_midi_path+"0.981087291054314_adj.mid"
# file_path_ps1 = train_midi_path+"Bach/Cello Suite 3_BWV1009_2217_cs3-1pre.mid"
# x = extract_features_from_midi(file_path_ps1, second_interval=[210,240])

# create dataset from all midi files in a directory
def load_dataset(directory, labeled=True, segments=2):
    features = []
    labels = []
    if labeled:
        for composer_dir in os.listdir(directory):
            composer_path = os.path.join(directory, composer_dir)
            if os.path.isdir(composer_path):
                for file_name in os.listdir(composer_path):
                    if file_name.endswith('.mid'):
                        file_path = os.path.join(composer_path, file_name)
                        for i in range(1,segments+1): # this segments out the files to get more records by the time specified
                            features.append(extract_features_from_midi(file_path, second_interval=[(i-1)*30+1,i*30]))
                            labels.append(composer_dir)
        return features, labels
    else:
        for file_name in os.listdir(directory):
            if file_name.endswith('.mid'):
                file_path = os.path.join(directory, file_name)
                features.append(extract_features_from_midi(file_path))
        return features
    
# create a pandas dataframe from lists
def create_dataframe(features, labels=[]):
    # Convert to pandas DataFrame
    feature_columns = ['filename','type', 'tpb', 'key', 'average_velocity', 'variance_velocity']+[f'Note_{i}' for i in range(128)]
    df = pd.DataFrame(features, columns=feature_columns)
    if len(labels)>0:
        df['composer'] = labels
    return df

# model evaluation stats and visualizations
def model_eval(classifier_name, y_train, y_pred_train, y_proba_train, y_test, y_pred_test, y_proba_test,  label_encoder):
    print(classifier_name,':')

    # Calculate AUC for the training set
    auc_train_lr = roc_auc_score(y_train, y_proba_train, multi_class='ovr', average='macro')
    # Calculate AUC for the test set
    auc_test_lr = roc_auc_score(y_test, y_proba_test, multi_class='ovr', average='macro')

    print(f"AUC for Training Set: {auc_train_lr:.4f}")
    print(f"AUC for Test Set: {auc_test_lr:.4f}")

    # Calcuate an accuracy score
    print("Accuracy Score (Test):", accuracy_score(y_test, y_pred_test))
    print("\nClassification Report (Test):")
    print(classification_report(y_test, y_pred_test,))  

    # Visualize the classification probabilities for each class
    class_labels = label_encoder.classes_
    num_classes = len(class_labels)

    plt.figure(figsize=(12, 8))
    for i in range(num_classes):
        plt.subplot(num_classes, 1, i+1)
        sns.histplot(y_proba_test[:, i], kde=True, bins=20)
        plt.title(f'Class {class_labels[i]}: Probability Distribution (Test)')
        plt.xlabel('Predicted Probability')
        plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()

    # Plot ROC curves for each class
    plt.figure(figsize=(7, 5))
    for i in range(num_classes):
        fpr, tpr, thresholds = roc_curve(y_test == i, y_proba_test[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'Class {class_labels[i]} (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], 'k--', lw=2)  # Diagonal line for random guess
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(classifier_name+' ROC Curves (Test)')
    plt.legend(loc='best')
    plt.show()

# print out top features
def top_feat(classifier, classifier_name, x_train, n=5):
    # Get feature importances
    importances = classifier.feature_importances_

    # Get feature names
    feature_names = x_train.columns

    # Number of top features to display
    n_top_features = 10

    # Sort feature importances in descending order and get the top n features
    indices = np.argsort(importances)[::-1][:n_top_features]
    top_feature_names = feature_names[indices]
    top_importances = importances[indices]

    # Print top n feature importances with names
    print(f"Top {n_top_features} feature importances:")
    for feature_name, importance in zip(top_feature_names, top_importances):
        print(f"{feature_name}: {importance}")


    # Plot the top n feature importances
    plt.figure(figsize=(10, 6))
    plt.title(f"Top {n_top_features} Feature Importances: {classifier_name}")
    plt.bar(range(n_top_features), top_importances, align="center")
    plt.xticks(range(n_top_features), top_feature_names, rotation=90)
    plt.xlabel("Feature")
    plt.ylabel("Importance")
    plt.show()

    return top_importances