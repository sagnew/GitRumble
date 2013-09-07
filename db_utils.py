import pymongo

connection = pymongo.Connection('mongodb://<user>:<password>@paulo.mongohq.com:10050/GitRumble')
db = connection.git_rumble
collection = db.sessions

def insert_into_db(session_id, user_dict, payment):
	"""
    Inserts a session's information into the collection

    Args:
        session_id: The id of the session
        user_dict: a dictionary associating Github usernames to their original number of commits
    returns:
        The session id, just in case it was changed.
    """
	#Only insert if the session is not already in the collection
	while not collection.find({"session_id": session_id}).count() == 0:
        session_id = create_session_id()

	session = {"session_id": session_id,
				"user_dict": user_dict,
                "payment": payment
				}
	collection.insert(session)
    return session_id

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
