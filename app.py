import numpy as np
import librosa
import soundfile as sf
from pygame import mixer
import os
import gradio as gr

O1=[71,74,73]

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

keys = { 
    'q' : 40, 'w' : 41, '3' : 42, 'e' : 43, '4' : 44, 'r' : 45, '5' : 46, 't' : 47, 'y' : 48, '7' :49 , 'u' : 50, '8' : 51 ,
    'i' : 52, 'o' : 53, '0' : 54, 'p' : 55, '-' : 56, '[' : 57, '=' : 58, ']' : 59, "\\" : 60
}

notes=[]

mixer.init(frequency=44100)

def play_clip(path):
    mixer.music.load(path)
    mixer.music.play()

def frequency_finder(f0):
    # Get the most common frequency
    if f0 is not None:
        frequency = np.nanmean(f0)
        note = note_name(frequency)
        print(f"Frequency: {frequency:.2f} Hz")
        return frequency , note
    else:
        print("Could not detect a stable pitch in the audio file.")
        
def note_name(frequency):
    # Convert frequency to the nearest MIDI number
    midi_value = round(69 + 12*np.log2(frequency/440))
    note_number = midi_value
    note = librosa.midi_to_note(midi_value)
    
    print(f"midi: {midi_value}")
    print(f"Note: {note}")    

    return note

def pitch_shift(y, midi_shift):
# single channel
    og_len = len(y)
    # Parameters
    anls_win_len = 5000  # Analysis window length
    anls_hop_len = 2000 # Analysis hop length
    scaling_fac = 2 ** (-midi_shift/ 12)
    shifted_hop_len = int(anls_hop_len * scaling_fac)
    shifted_win_len = int(anls_win_len * scaling_fac)
    
    # Hanning window for smoothing
    win_f = np.hanning(shifted_win_len)
    
    # Compute new waveform length
    new_y_len = int(np.ceil(og_len / anls_hop_len) * shifted_hop_len) + shifted_win_len
    new_y = np.zeros(new_y_len)
    new_scales = np.zeros(new_y_len)
    
    # Loop through windows
    for i in range(0, og_len - anls_win_len, anls_hop_len):
        clipped_len = min(anls_win_len, og_len - i)
        
        # Stretch to synth_win_len using linear interpolation
        idxs = np.linspace( i, i + clipped_len, shifted_win_len )
        start = np.floor(idxs).astype(int)
        frac = idxs - start
        
        # Ensure indices stay in range
        start = np.clip( start, 0, og_len - 2)
        
        # Interpolate
        window = y[start] * (1 - frac) + y[start + 1] * frac
        
        # Overlap-add method
        new_y[i:i + shifted_win_len] += window * win_f
        new_scales[i:i + shifted_win_len] += win_f
    
    # Normalize to avoid amplitude artifacts
    new_y = new_y / np.where(new_scales == 0, 1, new_scales)
    
    return new_y

def play_note(key, folder_name):
    if key:
        last_char = key[-1]
        if last_char != 'x':
            midi_note = keys.get(last_char)
            
            if midi_note:
                note=librosa.midi_to_note(midi_note) 
                notes.append(note)
                print("note played: ", note)
                path = f'samples/{folder_name}/{midi_note}.wav'
                play_clip(path)
                return note
            else:
                return "unknown key"
        else:
            return notes
    else:
        return ""

def guitar():
    return "guitar"

def piano():
    return "Piano"

def your_sample():
    return "your_sample"

def save_uploaded_audio(sample):
    if sample is None:
        return "No file uploaded."
    
    try:
        # Get the file path from the Gradio upload object
        file_path = sample.name
        # Define the new path where we want to save it
        new_path = "your_sample.wav"
        y, sr = librosa.load(file_path, sr=None)
        sf.write(new_path, y, sr)
        _ , note = process_audio(sample)
        return f"Saved as {new_path} and \n note : {note}"
    except Exception as e:
        return f"Error processing audio: {e}"

def process_audio(audio_upload):
    file_path ="your_sample.wav"
    y, sr = librosa.load(file_path)
    og_len = len(y)
    f0, _, _ = librosa.pyin( y, fmin=librosa.note_to_hz('A0'), fmax=librosa.note_to_hz('C8'))
    frequency, note = frequency_finder(f0)
    og_midi = round(69 + 12*np.log2(frequency/440))
    folder_name=f'samples/{file_path.split(".")[0]}'
    os.makedirs(folder_name, exist_ok = True)
    #pitch_shift_octave(y)
    for i in range(40,61):
        midi_shift = i - og_midi +12*(1)# add or subtract multiples of 12 to change the octave 
        y_shift = pitch_shift(y, midi_shift)
        sf.write(f'{folder_name}/{i}.wav', y_shift, samplerate=sr)
        play_clip(f'{folder_name}/{i}.wav')
        #ime.sleep(0.3)
        print(midi_shift, end = "  ")
    return 'playing your sample', note

with gr.Blocks() as demo:
    gr.Markdown("## 🎶 Audio Sampler: Pitch Transposer")
    folder_state = gr.State("guitar")  # default

    gr.Image(value="notes.png", label="Keys Reference", height = 260, width = 730)
    
    with gr.Row():
        gr.Button("🎸 Guitar").click(fn=guitar, outputs=folder_state)
        gr.Button("🎹 Piano").click(fn=piano, outputs=folder_state)
        gr.Button("🕶️ your Sample").click(fn=your_sample, outputs=folder_state)

    with gr.Row():
        key_input = gr.Textbox(label="Press a Key ")
        output_text = gr.Textbox(label="Note :")
    with gr.Row():
        gr.Markdown("## Upload Audio to Save in Your Project Folder \n for effective output, please upload an audio of length less than 1 second")
        audio_input = gr.File(label="Upload .wav or .mp3", file_types=[".wav", ".mp3"])
        sample_status = gr.Textbox(label="Save Status")
    
        audio_input.change(fn=save_uploaded_audio, inputs=audio_input, outputs=sample_status)
    
    key_input.change(fn=play_note, inputs=[key_input, folder_state], outputs=output_text)

demo.launch()
print(notes)