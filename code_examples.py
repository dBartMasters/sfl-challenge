# extra code snippets for later

# example file
train_midi_path+"Bach/Cello Suite 3_BWV1009_2217_cs3-1pre.mid"

# def extract_features_from_midi(file_path):
#     midi = mido.MidiFile(file_path)
#     note_counts = [0] * 128  # MIDI notes range from 0 to 127
#     # get ticks
#     for track in midi.tracks:
#         for msg in track:
#             if msg.type == 'note_on' and msg.velocity > 0:
#                 note_counts[msg.note] += 1
    
#     return note_counts

# test extract features function
file_path = train_midi_path+"Bach/Cello Suite 3_BWV1009_2217_cs3-1pre.mid"
# note_counts, ticks_per_beat, key, average_velocity = extract_features_from_midi(file_path)
features = extract_features_from_midi(file_path)
print(features)
# print("Note Counts:", note_counts)
# print("Ticks per Beat:", ticks_per_beat)
# print("Key:", key)
# print("Average Velocity:", average_velocity)

features=extract_features_from_midi(train_midi_path+"Bach/Cello Suite 3_BWV1009_2217_cs3-1pre.mid")

# simple midi functions
midi = mido.MidiFile(train_midi_path+"Bach/Cello Suite 3_BWV1009_2217_cs3-1pre.mid")

print(midi.type)
print(midi.length)
print(midi.ticks_per_beat)

for i, track in enumerate(midi.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        if msg.is_meta : #and msg.type == 'key_signature':
            # print(msg.key)
            print(msg)

for track in midi.tracks:
    for msg in track:
        # print(track)
        print(msg)            

# Plot ROC curves for each class
plt.figure(figsize=(14, 10))
for i in range(num_classes):
    fpr, tpr, thresholds = roc_curve(y_test == i, y_proba_lr[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'Class {class_labels[i]} (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], 'k--', lw=2)  # Diagonal line for random guess
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curves')
plt.legend(loc='best')
plt.show()

# Plot precision-recall curves for each class
plt.figure(figsize=(14, 10))
for i in range(num_classes):
    precision, recall, thresholds = precision_recall_curve(y_test == i, y_proba_lr[:, i])
    plt.plot(thresholds, precision[:-1], label=f'Class {class_labels[i]} Precision')
    plt.plot(thresholds, recall[:-1], label=f'Class {class_labels[i]} Recall')
    plt.xlabel('Threshold')
    plt.ylabel('Precision/Recall')
    plt.title(f'Precision-Recall Curve for Class {class_labels[i]}')
    plt.legend(loc='best')
    plt.show()


# # Transform the DataFrame into a long format
# df_long = pd.melt(composer_avg.reset_index(), id_vars=['Composer'], var_name='Note', value_name='Value')

# # Plot the bar chart
# plt.figure(figsize=(15, 8))
# sns.barplot(x='Note', y='Value', hue='Composer', data=df_long)

# # Customize the plot
# plt.title('Composer Note Values Bar Chart')
# plt.xlabel('Notes')
# plt.ylabel('Values')
# plt.legend(title='Composer')
# plt.xticks(rotation=90)  # Rotate x-axis labels if needed for better readability

# # Display the plot
# plt.show()

# # Generate the heatmap
# plt.figure(figsize=(12, 8))
# sns.heatmap(composer_avg, cmap='viridis', cbar=True)

# # Display the plot
# plt.title('Composer Note Values Heatmap')
# plt.xlabel('Notes')
# plt.ylabel('Composers')
# plt.show()

def exp_mido(file_path):
    midi = mido.MidiFile(file_path)
    print('Midi file type', midi.type)
    print('Length',midi.length)
    print('Ticks per beat',midi.ticks_per_beat)

    elapsed_time = 0
    ticks_per_beat = midi.ticks_per_beat
    tempo = 500000

    for msg in midi:
        if msg.type == 'set_tempo':
            tempo = msg.tempo

        elapsed_time += mido.tick2second(msg.time, ticks_per_beat, tempo)
        # print(elapsed_time)
        if elapsed_time <= 30:
            print(msg)

exp_mido(file_path_ps1)

tempo=5000
elapsed_time=0

for track in midi.tracks:
    # print(track)
    for msg in track:        
        if msg.type == 'set_tempo':
            tempo = msg.tempo
            print('Tempo:\t',tempo)

        calc_time = mido.tick2second(msg.time, ticks_per_beat, tempo)
        elapsed_time += calc_time
        print('msg.time\t',msg.time)
        print('calc time:\t', calc_time)
        print('Elapsed Time:\t',elapsed_time)        
        # if elapsed_time <= 30:
        #     print(msg.time)

# Load the MIDI file
midi_file = mido.MidiFile(file_path_ps1)

# Initialize a variable to keep track of elapsed time
# elapsed_time = 0

# Define the duration in seconds for which we want to collect messages
target_duration = 30

# List to store the messages within the first 30 seconds
messages_within_duration = []

# Iterate through the messages in the MIDI file
for track in midi_file.tracks:
    elapsed_time = 0
    for message in track:
        elapsed_time += message.time
        if elapsed_time <= target_duration:
            print(elapsed_time)
            print(message)


# Display the collected messages
# for msg in messages_within_duration:
#     print(msg)

midi = mido.MidiFile(file_path_ps1)
print('Midi file type', midi.type)
print('Length',midi.length)
print('Ticks per beat',midi.ticks_per_beat)

ticks_per_beat = midi.ticks_per_beat

midi = mido.MidiFile(file_path_ps1)

# initialize values
note_counts = [0] * 128  # MIDI notes range from 0 to 127
total_velocity = 0
note_on_count = 0
elapsed_time = 0
key = '' # each file should have only 1 key. Investigate if this assumption is correct.
tpb = midi.ticks_per_beat

# get ticks
# for track in midi.tracks:
for msg in midi:
    # get the key
    if msg.is_meta and msg.type == 'key_signature':
        key = msg.key
    
    # just the first n seconds
    elapsed_time += msg.time
    if elapsed_time<=30:
        if msg.type == 'note_on' and msg.velocity > 0:
            note_counts[msg.note] += 1
            total_velocity += msg.velocity
            note_on_count += 1
    else:
        break

print(note_counts)
print(elapsed_time)