def zero_pad_nr(frame_nr, len_number=6):
	len_frame_nr = len(str(frame_nr))
	len_padding = len_number - len_frame_nr
	new_nr = ('0'*len_padding) + frame_nr
	return new_nr
