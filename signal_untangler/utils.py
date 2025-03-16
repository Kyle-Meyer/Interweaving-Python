def validate_binary_string(s):
    return all(char in '01' for char in s)

def find_pattern_period(s):
    n = len(s)
    for i in range(1, n // 2 + 1):
        if n % i == 0:
            is_periodic = True
            for j in range(i, n):
                if s[j] != s[j % i]:
                    is_periodic = False
                    break
            if is_periodic:
                return i
    return n
