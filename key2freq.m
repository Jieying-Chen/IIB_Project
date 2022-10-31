function [freq intensity]= key2freq(key,notes,ori_freq)
    freq = notes(key);
    if key == 1
        sig = (notes(2)-notes(1));
    else
        sig = (notes(key)-notes(key-1));
    end
    sig = sig/2;
    intensity = exp(-0.5 .*((ori_freq-freq)/sig).^2);
end


%freq_A4 = 440;
%freq = freq_A4 * 2^((key-49)/12);
%freq = zeros(1,numel(key));
%for i = 1:numel(key)
%    if key(i) ~= 0
%        freq(i)=notes(key(i));
%    end
%end
%    freq = reshape(freq, size(key));