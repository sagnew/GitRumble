import pymongo

connection = pymongo.Connection('mongodb://<user>:<password>@paulo.mongohq.com:10050/GitRumble')
db = connection.git_rumble
collection = db.sessions

def insert_into_db(session_id, user_dict):
	"""
    Inserts a session's information into the collection

    Args:
        session_id: The id of the session
        user_dict: a dictionary associating Github usernames to their original number of commits
    """
	session = {"session_id": session_id,
				"user_dict": user_dict
				}
	#Only insert if the session is not already in the collection
	if collection.find({"session_id": session_id}).count() == 0:
		collection.insert(session)
    else:
        #TODO(Sam): Generate a new session here

def get_user_dict_by_session_id(session_id):
    """
    Retrieves the user dict associated with the given session id.
    """

    return db.find_one({'session_id': session_id})['user_dict']

def update_user_dict(session_id, user_dict):
    """Updates the user_dict associated with the given session_id"""

    new_object = db.find_one({'session_id': userid})
    new_object['user_dict'] = user_dict
    db.update({'session_id': session_id}, new_object)
