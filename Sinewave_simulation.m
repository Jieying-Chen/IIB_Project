freq_pick

key_time = win_time*(1 - overlap/N);
subwin = 0:1/Fs:key_time;
%subwin = 0:1/Fs:2;

signal = zeros(1,length(subwin)*length(key(1,:)));

for i = 1:length(filtered_freq(1,:))
    buffer = zeros(1,length(subwin));
    cur = filtered_freq(:,i);
    %cur_key = unique(nonzeros(cur)); %the same key only be played once
    ori_freq = nonzeros(cur); %add up
    if ~isempty(ori_freq)
        for j = 1:length(ori_freq)
            [c cur_key] = min(abs(notes-ori_freq(j)));
            [cur_f cur_int] = key2freq(cur_key,notes,ori_freq(j));
            if cur_f ~= 0
                buffer = buffer + 1 * sinewave(cur_f,subwin);
            end
        end
    end
    signal((i-1)*length(buffer)+1:i*length(buffer)) = buffer;
end

%plot(signal)
spectrogram(signal,win,overlap,DFT_points,Fs,'yaxis');
sound(signal,Fs)