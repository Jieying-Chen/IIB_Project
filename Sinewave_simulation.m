freq_pick

subwin = 0:1/Fs:win_time;
%subwin = 0:1/Fs:2;

signal = zeros(1,length(subwin)*length(key(1,:)));

for i = 1:length(key(1,:))
    buffer = zeros(1,length(subwin));
    cur = key(:,i);
    cur_key = unique(nonzeros(cur));
    if ~isempty(cur_key)
        for j = 1:length(cur_key)
            cur_f = key2freq(cur_key(j),quarter,notes);
            if cur_f ~= 0
                buffer = buffer + sinewave(cur_f,subwin);
            end
        end
    end
    signal((i-1)*length(buffer)+1:i*length(buffer)) = buffer;
end

plot(signal)
sound(signal,Fs)