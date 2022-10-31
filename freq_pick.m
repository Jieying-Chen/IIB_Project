clear
VoicePath = "C:\Users\96326\Desktop\IIBproject\VoiceSource\";
filename = "JLspeech1.mp3";
%filename = "TestNew.m4a";
%filename = "jw.m4a";
[audio, Fs] = audioread(VoicePath+filename);
audio = audio(:,1);

duration = length(audio)/Fs;

%%%%%%
win_time = 50e-3;
%%%%%%

win_length = round(win_time*Fs); %sample per window
win = hamming(win_length);

N=round(win_length/2)*2;%frame length
overlap = 0;
disp(['OVERLAP = ' num2str(overlap)]);

%%%%%%
DFT_points = 20000;
%%%%%%

disp(['frequency resolution = ' num2str(Fs/DFT_points)]);
freq_bin = Fs / DFT_points;%range of each frequency bin

notes = 440 * 2.^(((1:88)-49)./12); %key = round(49+12*log2(freq/440))

%%%%%%
quarter = 2;
%%%%%%
disp(['quarter = ' num2str(quarter)])
if quarter == 1
    quarter_notes = 427 * 2.^(((1:88)-49)./12);
    notes = sort([notes quarter_notes]);
elseif quarter == 2
    eighth = [434 * 2.^(((44:88)-49)./12) 428 * 2.^(((44:88)-49)./12) 422 * 2.^(((44:88)-49)./12)] ;
    notes = sort([notes eighth]);
end
lower_freq = (440 * 2.^((1-49)./12) + 440 * 2.^((0-49)./12))/2;
upper_freq = (440 * 2.^((89-49)./12) + 440 * 2.^((88-49)./12))/2; %freq of the 89th key

[s,f,t] = spectrogram(audio,win,overlap,DFT_points,Fs,'yaxis');

s_cropped = s(ceil(lower_freq/freq_bin)+1:floor(upper_freq/freq_bin),:);
f_cropped = f(ceil(lower_freq/freq_bin)+1:floor(upper_freq/freq_bin));
intensity = abs(s_cropped).^2;

%%%%%%
thres = 10;
%%%%%%

filtered_intensity = (intensity > thres); %intensity .* (intensity > 20) to preserve the intensity
filtered_freq = filtered_intensity.*f_cropped;

if quarter ~= 0
    key = zeros(1,numel(filtered_freq));
    for idx = 1:numel(filtered_freq)
        if filtered_freq(idx)~= 0
            [c index] = min(abs(notes-filtered_freq(idx)));
            key(idx) = index;
        end
    end
    key = reshape(key,size(filtered_freq));
    
elseif quarter == 0
    key = round(49+12*log2(filtered_freq./440)); %need an extra +20 to transform from midi!!! (128 keys, middle C the 60th one) to 88-keys piano
end

key(key < 0)=0;

%mesh(t,f,10*log(abs(s).^2))
%mesh(t,f,abs(s).^2)


%x=buffer(audio,N,overlap);%slice signal

%[N_samps,N_frames]=size(x);

%x_w=repmat(hann(N),1,N_frames).*x;%window function
%win = hamming(win_length);
