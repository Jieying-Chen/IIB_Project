function freq = key2freq(key,quarter,notes)
    if quarter == 0
        %freq_A4 = 440;
        %freq = freq_A4 * 2^((key-49)/12);
        freq = zeros(1,numel(key));
        for i = 1:numel(key)
            if key(i) ~= 0
                freq(i)=notes(key(i));
            end
        end
        freq = reshape(freq, size(key));
    elseif quarter == 1
        freq = zeros(1,numel(key));
        for i = 1:numel(key)
            if key(i) ~= 0
                freq(i)=notes(key(i));
            end
        end
        freq = reshape(freq, size(key));
    end
end