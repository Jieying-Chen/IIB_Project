NotePath = "C:\Users\96326\Desktop\IIBproject\VoiceSource\PianoNotes\";

for i = 1:39
    cur_note_path = NotePath + num2str(i) + '.aiff';
    [cur_audio, Fs] = audioread(cur_note_path);
    cur_note = cur_audio(:,1);
end
    