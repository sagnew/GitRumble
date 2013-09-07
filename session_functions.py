import random

def create_session_id():
    # TODO(Sam): Make sure that no duplicate IDs can be created
    random.seed()
    return random.randint(0, 9999)
