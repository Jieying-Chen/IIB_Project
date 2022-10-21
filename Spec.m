clear
VoicePath = "C:\Users\96326\Desktop\IIBproject\VoiceSource\";
filename = "JLSpeech1.mp3";
[audio, Fs] = audioread(VoicePath+filename);
%sound(audio,Fs)
%audio=y_out;
duration = length(audio)/Fs;


win_time = 20e-3; %sec
win_length = round(duration / win_time); %sample per window
win = hamming(win_length);

overlap = round(0.75*duration / win_time);

[s,f,t] = spectrogram(audio,win_length,overlap,100,Fs,'yaxis');
%spectrogram(audio,win_length,overlap,1000,Fs,'yaxis')
%set(gca, 'YDir','reverse')

[s2,f2,t2] = stft(audio,Fs,'Window',win,'OverlapLength',overlap,'FFTLength',500,'FrequencyRange','onesided');


s2(50:end,:)=0+0i;
iy = istft(s2,Fs,'Window',win,'OverlapLength',overlap,'FFTLength',500,'FrequencyRange','onesided');