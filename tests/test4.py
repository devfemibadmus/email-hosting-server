import random
def random_selection():
    my_list = [True, "Hello", False]
    return random.choice(my_list)

def check_type():
    r = random_selection()
    if type(r) == bool:
        return f"is bool value is {r}"
    return f"is str value is {r}"
    
print(check_type())