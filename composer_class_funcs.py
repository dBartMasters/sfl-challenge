# Functions to support classifier notebook

## Libraries
import os
import numpy as np
import pandas as pd
# midi files
import mido

# extract features from midi file using mido library
def extract_features_from_midi(file_path, second_interval=30):
    ## Input: file path of midi file
    ## Output: list [ticks per beat, key, average_velocity, note counts for 128 notes]

    # import file
    midi = mido.MidiFile(file_path)

    # initialize values
    note_counts = [0] * 128  # MIDI notes range from 0 to 127
    total_velocity = 0
    note_on_count = 0
    elapsed_time = 0
    key = '' # each file should have only 1 key. Investigate if this assumption is correct.
    tpb = midi.ticks_per_beat

    # get ticks
    for msg in midi:
        # get the key
        if msg.is_meta and msg.type == 'key_signature':
            key = msg.key
        
        # just the first n seconds
        elapsed_time += msg.time
        if elapsed_time<=second_interval:
            if msg.type == 'note_on' and msg.velocity > 0:
                note_counts[msg.note] += 1
                total_velocity += msg.velocity
                note_on_count += 1
        else:
            break
            
    # Calculate average velocity
    if note_on_count > 0:
        average_velocity = total_velocity / note_on_count
    else:
        average_velocity = 0
    
    # Normalize the note counts to be between 0 and 1
    normalized_note_counts = (note_counts - np.min(note_counts)) / (np.max(note_counts) - np.min(note_counts))
    
    # combine into 1 list
    combined_features = [tpb, key, average_velocity] + list(normalized_note_counts)

    return combined_features

# create dataset from all midi files in a directory
def load_dataset(directory, labeled=True):
    features = []
    labels = []
    if labeled:
        for composer_dir in os.listdir(directory):
            composer_path = os.path.join(directory, composer_dir)
            if os.path.isdir(composer_path):
                for file_name in os.listdir(composer_path):
                    if file_name.endswith('.mid'):
                        file_path = os.path.join(composer_path, file_name)
                        features.append(extract_features_from_midi(file_path))
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
    feature_columns = ['tpb', 'key', 'average_velocity']+[f'Note_{i}' for i in range(128)]
    df = pd.DataFrame(features, columns=feature_columns)
    if len(labels)>0:
        df['composer'] = labels
    return df