clear
VoicePath = "C:\Users\96326\Desktop\IIBproject\VoiceSource\";
%filename = "JLspeech1.mp3";
filename = "test-human.m4a";
[audio, Fs] = audioread(VoicePath+filename);


duration = length(audio)/Fs;

%win_time = 20e-3; %sec
win_time = 20e-3;
win_length = round(win_time*Fs); %sample per window
%win = hamming(win_length);

N=round(win_length/2)*2;%frame length
overlap = 0;
disp(['OVERLAP = ' num2str(overlap)]);
DFT_points = 22050;
freq_bin = Fs / DFT_points;%range of each frequency bin

%x=buffer(audio,N,overlap);%slice signal

%[N_samps,N_frames]=size(x);

%x_w=repmat(hann(N),1,N_frames).*x;%window function

notes = 440 * 2.^(((1:88)-49)./12); %key = round(49+12*log2(freq/440))
upper_freq = (440 * 2.^((89-49)./12) + 440 * 2.^((88-49)./12))/2; %freq of the 89th key

[s,f,t] = spectrogram(audio,win_length,overlap,DFT_points,Fs,'yaxis');

s_cropped = s(1:floor(upper_freq/freq_bin)+1,:);
f_cropped = f(1:floor(upper_freq/freq_bin)+1);
intensity = abs(s_cropped).^2;

thres = 500;

filtered_intensity = (intensity > thres); %intensity .* (intensity > 20) to preserve the intensity
filtered_freq = filtered_intensity.*f_cropped;

key = round(49+12*log2(filtered_freq./440))+20; %20 to transform from midi (128 keys, middle C the 60th one) to 88-keys piano
key(key < 21)=0;

%mesh(t,f_t,10*log(abs(s_t).^2))