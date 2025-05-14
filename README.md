# Pitch Transposer & Audio Sampler  

## Overview  
Pitch-shifting is a technique used to modify the perceived pitch of an audio signal **without altering its tempo**. Applications range from **music production** to **instrument synthesis**, allowing users to create an instrument from any sound.  

Traditional pitch shifting relies on **frequency-domain methods** like **phase vocoders**, but these can introduce artifacts and require complex computation. This project explores a **time-domain alternative** using **resampling, interpolation, and overlap-add** to shift pitch while maintaining natural audio quality.  

## **Project Goals**  
This project integrates **pitch detection, MIDI mapping, and playback**, along with an interactive interface for easy access to pitch-shifting functionalities.  

### **Primary Objectives**  
- **Detect the fundamental frequency** of an audio signal using the **YIN algorithm**.  
- **Convert the detected pitch** into its corresponding **MIDI value**.  
- **Shift the pitch** of the audio signal using **time-domain interpolation and overlap-add**.  
- **Implement an interactive Gradio interface** for:  
  - Uploading audio files  
  - Triggering note playback via keyboard  
  - Visualizing pitch changes  

## **Implementation Details**  
By achieving these goals, the system serves as both a **learning tool** and a **foundation for advanced development** in audio signal processing. It provides users with an **entry point into music production and creation**.  

## **Installation**  
Clone the repository:  
```bash
git clone github.com/gundlurujeevan2107/Pitch_Transposer-Audio_sampler
cd Pitch_Transposer-Audio_sampler
