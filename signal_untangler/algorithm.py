def is_interweaving(aOriginalString, aStringX, aStringY):
    if not aStringX or not aStringY:
        return False
    
    len_s = len(aOriginalString)
    len_x = len(aStringX)
    len_y = len(aStringY)
    
    # We need at least one complete copy of x and y
    min_length = len_x + len_y
    if len_s < min_length:
        return False
    
    # Try each possible starting position
    for start in range(len_s - min_length + 1):
        # Initialize state tracking
        states = {(0, 0, False, False)}  # (x_pos, y_pos, completed_x, completed_y)
        
        # Process characters from this starting position
        for i in range(start, len_s):
            char = aOriginalString[i]
            new_states = set()
            
            for x_pos, y_pos, comp_x, comp_y in states:
                # Try to match with x
                if char == aStringX[x_pos]:
                    new_x_pos = (x_pos + 1) % len_x
                    new_comp_x = comp_x or new_x_pos == 0
                    new_states.add((new_x_pos, y_pos, new_comp_x, comp_y))
                
                # Try to match with y
                if char == aStringY[y_pos]:
                    new_y_pos = (y_pos + 1) % len_y
                    new_comp_y = comp_y or new_y_pos == 0
                    new_states.add((x_pos, new_y_pos, comp_x, new_comp_y))
            
            states = new_states
            
            # Check if we have a valid interweaving yet
            for state in states:
                if state[2] and state[3]:  # Both x and y completed
                    return True
            
            # If no valid states, try next starting position
            if not states:
                break
    
    return False
