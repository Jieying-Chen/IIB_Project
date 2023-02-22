##ARCHIVED FUNCTIONS

def separate_majors(notes):
    major1 = [1,3,4,6,8,9,11]
    major2 = [0,2,3,5,7,9,10]

    C_notes = []
    Gb_notes = []

    len_all = len(notes)

    i = 0
    while i < len(notes):
        note = notes[i]
        seq = note.pitch % 12
        if (seq in major1) and (seq not in major2):
            C_notes.append(notes.pop(i))
            i -= 1
        elif (seq in major1) and (seq not in major2):
            Gb_notes.append(notes.pop(i))
            i -= 1
        i += 1

    j = len(notes)
    while j > 0:
        #print(notes[0].pitch % 12)
        if j % 2 == 0:
            C_notes.append(notes.pop(0))
        else:
            Gb_notes.append(notes.pop(0))
        j -= 1
    return C_notes, Gb_notes
    

def separate_majors(notes):
    C_major = [1,3,4,6,8,9,11]
    Gb_major = [0,2,3,5,7,9,10]

    C_notes = []
    Gb_notes = []

    len_all = len(notes)

    # for i,note in enumerate(notes):
    #     seq = note.pitch % 12
    #     if (seq in C_major) and (seq not in Gb_major):
    #         C_notes.append(notes.pop(i))
    #     elif (seq in Gb_major) and (seq not in C_major):
    #         Gb_notes.append(notes.pop(i))
    i = 0
    while i < len(notes):
        note = notes[i]
        seq = note.pitch % 12
        if (seq in C_major) and (seq not in Gb_major):
            C_notes.append(notes.pop(i))
            i -= 1
        elif (seq in Gb_major) and (seq not in C_major):
            Gb_notes.append(notes.pop(i))
            i -= 1
        i += 1


    j = len(notes)
    while j > 0:
        #print(notes[0].pitch % 12)
        if j % 2 == 0:
            C_notes.append(notes.pop(0))
        else:
            Gb_notes.append(notes.pop(0))
        j -= 1
    if len_all!= len(C_notes) + len(Gb_notes):
        print('False')
    return [C_notes, Gb_notes]  

# candidate = []
# for i,note in enumerate(notes_group):
#     if (note['note'] not in pitch_group) and (note['note']-pitch_group[0] <= 12):
#         if overlapped and note['note'] > (high + 1):
#             candidate.append(note)
#         elif not overlapped:
#             candidate.append(note)
# for c in candidate:
#     print(c)
# for j,note in enumerate(candidate):
#     if len(current_group) == 5:
#         break
#     for current_allocated_note in current_group:
#         if note['start'] == current_allocated_note['start'] and note['end'] == current_allocated_note['end']:
#             current_group.append(candidate.pop(j))
#             notes_group.remove(note)
    
# for j,note in enumerate(candidate):
#     if len(current_group) == 5:
#         break
#     for current_allocated_note in current_group:
#         if note['start'] == current_allocated_note['start']:
#             current_group.append(candidate.pop(j))
#             notes_group.remove(note)
    
# for j,note in enumerate(candidate):
#     if len(current_group) == 5:
#         break
#     for current_allocated_note in current_group:
#         if note['end'] == current_allocated_note['end']:
#             current_group.append(candidate.pop(j))
#             notes_group.remove(note)

# if len(current_group) != 5:
#     for k in range(5-len(current_group)):
#         current_group.append(candidate.pop(k))
#         notes_group.remove(candidate[k])



# f1 = False
# f2 = False
# for note in candidate:
#     if thesame(note[1],thenote):
#         print('exist in can')
#         f1 = True
#         for note in notes_group:
#             if thesame(note,thenote):
#                 print('exist')
#                 f2 = True
# if f1 and not f2:
#     print(pitch_group)
#     print(current_group)