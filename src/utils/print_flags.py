# Active for developer, turn it off for production
flag_on = True

def show_flag(string):
    
    separator = "\n---------------------------------------------\n"
    
    flag_format = f"{separator}\n{string}\n{separator}"
    
    if flag_on:
        print(flag_format)
    else:
        return None