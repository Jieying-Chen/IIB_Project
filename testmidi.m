midilength = length(find(key));

msgArray = midimsg([midilength*2,1]);
idx = 1:2;


gap = t(2)-t(1);

for i = 1:length(key(1,:))
    cur = key(:,i);
    cur_key = unique(nonzeros(cur));
    if ~isempty(cur_key)
        for j = 1:length(cur_key)
            msgArray(idx) = midimsg('Note',j,cur_key(j),64,gap,t(i));
            idx = idx+2;
        end
    end
end

osc = audioOscillator();
deviceWriter = audioDeviceWriter('SampleRate',osc.SampleRate);
msgs = msgArray;
eventTimes = [msgs.Timestamp];
i = 1;
tic
while toc < max(eventTimes)
    if toc > eventTimes(i)
        msg = msgs(i);
        i = i+1;
        
        if msg.Velocity~= 0
            osc.Frequency = 440 * 2^((msg.Note-69)/12);
            osc.Amplitude = msg.Velocity/127;
        else
            osc.Amplitude = 0; 
        end
    end
    deviceWriter(osc());
end
release(deviceWriter)

testmsgs = [midimsg('Note',1,60,64,5,0), ...
        midimsg('Note',2,64,64,3,0), ...
        midimsg('Note',3,67,64,2,0), ...
        midimsg('Note',4,72,64,2,0)]; %c major chord