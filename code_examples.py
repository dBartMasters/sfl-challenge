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