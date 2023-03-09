disp(['quarter note not finished!!'])

VoicePath = "C:\Users\96326\Desktop\IIBproject\VoiceSource\";
fname = input("filename? (in string! remember quotes)");
% ftype = input("audio type? 1 = m4a, 2 = mp3");
% if ftype == 1
%     ftype = ".m4a";
% elseif ftype == 2
%     ftype = ".mp3";
% else
%     disp(['Wrong type! Terminate.']);
%     return
% end
ftype = ".m4a";
filename = fname + ftype;
%filename = "JLspeech1.mp3";
%filename = "jc.m4a";
%filename = "jw.m4a";
%filename = "jc_25Jan.m4a";
%filename = "31Jan_jc.m4a";
[audio, Fs] = audioread(VoicePath+filename);
audio = audio(:,1);


duration = length(audio)/Fs;

%%%%%%
win_time = 50e-3;
%%%%%%

win_length = round(win_time*Fs); %sample per window
%win = hamming(win_length);
win = kaiser(win_length,5);

N=round(win_length/2)*2;%frame length
overlap = N/2;
disp(['OVERLAP = ' num2str(overlap)]);

%%%%%%
DFT_points = 20000;
%%%%%%

disp(['frequency resolution = ' num2str(Fs/DFT_points)]);
freq_bin = Fs / DFT_points;%size of each frequency bin

octave_down = input("how many octaves down?");
notes = 440 * 2.^(((1:88+octave_down * 12)-49)./12); %key = round(49+12*log2(freq/440))

%%%%%%
quarter = 0;
%%%%%%

disp(['quarter = ' num2str(quarter)])
if quarter == 1
    quarter_notes = 427 * 2.^(((1:88)-49)./12);
    notes = sort([notes quarter_notes]);
elseif quarter == 2
    eighth = [434 * 2.^(((44:88)-49)./12) 428 * 2.^(((44:88)-49)./12) 422 * 2.^(((44:88)-49)./12)] ;
    notes = sort([notes eighth]);
end
lower_freq = 440 * 2.^((0.5-49)./12);
upper_freq = 440 * 2.^((88.5 + 12 * octave_down -49)./12); 

[s,f,t] = spectrogram(audio,win,overlap,DFT_points,Fs,'yaxis');


s_cropped = s(f > lower_freq & f < upper_freq,:);
f_cropped = f(f > lower_freq & f < upper_freq);
intensity = abs(s_cropped).^2;

%%%%%%
thres = 10;
thres_highfreq = 50;
%%%%%%

intensity_filter = (intensity > thres); %intensity .* (intensity > 20) to preserve the intensity
filtered_freq = intensity_filter.*f_cropped;

filtered_int = intensity_filter.*intensity;
filtered_int_nm = filtered_int / max(max(filtered_int));

filtered_int_db = 10*log10(filtered_int);
filtered_int_db(filtered_int_db < 0)=0;
filtered_int_db = filtered_int_db / max(max(filtered_int_db));




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


%x=buffer(audio,N,overlap);%slice signal

%[N_samps,N_frames]=size(x);   

%x_w=repmat(hann(N),1,N_frames).*x;%window function
%win = hamming(win_length);
save_key = input("save key? ('1' = yes)");
if save_key == 1
    name1 = input("Default doc name? (if deafult: 1)");
    if name1 == 1
        name1 = fname + "_key_" + int2str(octave_down) + "octave";
    else
        name1 = input("doc name?");
    end
    str = "C:\Users\96326\Desktop\IIBproject\IIB_Project\MATLAB_data\" + name1 + int2str(thres) + ".mat";
    save(str,"key");
end

save_int = input("save intensity? ('1' = yes)");
if save_int == 1
    name2 = input("Default doc name? (if deafult: 1)");
    if name2 == 1
        name2 = fname + "_int_" + int2str(octave_down) + "octave";
    else
        name2 = input("doc name?");
    end
    str2 = "C:\Users\96326\Desktop\IIBproject\IIB_Project\MATLAB_data\" + name2 + int2str(thres) + ".mat";
    save(str2,"filtered_int_db");
end

%spectrogram(audio,win,overlap,DFT_points,Fs,'yaxis');
