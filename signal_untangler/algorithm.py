def is_interweaving(aOriginalString, aStringX, aStringY):
    if not aStringX or not aStringY:
        return False
    
    len_s = len(aOriginalString)
    len_x = len(aStringX)
    len_y = len(aStringY)
    
    # Need minimum length to contain both patterns
    min_length = len_x + len_y
    if len_s < min_length:
        return False
    
    # Try each possible starting position
    for start in range(len_s - min_length + 1):
        # For each starting position, create a single state rather than a set of states
        x_pos = 0
        y_pos = 0
        x_completed = False
        y_completed = False
        
        # Process characters from this starting position
        i = start
        while i < len_s:
            char = aOriginalString[i]
            matched = False
            
            # Try to match with X first (prioritize X over Y)
            if char == aStringX[x_pos]:
                x_pos = (x_pos + 1) % len_x
                if x_pos == 0:
                    x_completed = True
                matched = True
                i += 1
            # If X didn't match, try Y
            elif char == aStringY[y_pos]:
                y_pos = (y_pos + 1) % len_y
                if y_pos == 0:
                    y_completed = True
                matched = True
                i += 1
            
            # If neither pattern matched, this starting position doesn't work
            if not matched:
                break
            
            # Check if we've completed both patterns
            if x_completed and y_completed:
                return True
        
    return False
