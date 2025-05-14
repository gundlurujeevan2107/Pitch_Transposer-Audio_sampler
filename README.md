# Pitch_Transposer-Audio_sampler
Pitch-shifting is a technique used to modify the perceived pitch of an audio signal without 
altering its tempo. Applications range from music production and instrument synthesis i.e 
creating an instrument of anything. Traditional pitch shifting uses frequency-domain methods 
like phase vocoders but can introduce artifacts and require complex computation. This project 
explores a time-domain alternative using resampling, interpolation, and overlap-add to shift 
pitch while maintaining natural audio quality. 
By integrating pitch detection, MIDI mapping and playback, the project’s core operations 
involved in pitch shifting and creating an interface for instrument for easy access. 
The primary objectives of this project are: 
• To detect the fundamental frequency of an audio signal using the YIN algorithm. 
• To convert the detected pitch into its corresponding MIDI value. 
• To shift the pitch of the audio signal using time-domain interpolation and overlap-add. 
• To implement an interactive Gradio interface for uploading audio, triggering note 
playback via keyboard, and visualizing pitch changes. 
By achieving these goals, the system serves as both a learning tool and a foundation for 
advanced development in audio signal processing. It gives the user the first step towards music 
production and creation
