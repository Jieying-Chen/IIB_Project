freq_pick

key_time = win_time*(1 - overlap/N);
subwin = 0:1/Fs:key_time;
%subwin = 0:1/Fs:2;

signal = zeros(1,length(subwin)*length(key(1,:)));

for i = 1:length(filtered_freq(1,:))
    buffer = zeros(1,length(subwin));
    cur = key(:,i);
    %cur_key = unique(nonzeros(cur)); %the same key only be played once
    cur_key = nonzeros(cur); %add up
    if ~isempty(cur_key)
        for j = 1:length(cur_key)
            %[c cur_key] = min(abs(notes-ori_freq(j)));
            [cur_f cur_int] = key2freq(cur_key(j),notes,[]);
            if cur_f ~= 0
                buffer = buffer + 1 * sinewave(cur_f,subwin);
            end
        end
    end
    signal((i-1)*length(buffer)+1:i*length(buffer)) = buffer;
end

plot(signal)
sound(signal,Fs)