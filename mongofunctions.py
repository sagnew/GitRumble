import pymongo

connection = pymongo.Connection('mongodb://name:password@linus.mongohq.com:10040/gitrumble')
db = connection.git_rumble
collection = db.sessions

def insert_into_db(session_id, user_dict):
	"""
    Inserts a session's information into the collection

    Args:
        session_id: The id of the session
        user_dict: a dictionary associating Github usernames to their original number of commits
    """
	session = {"id": session_id,
				"user_dict": user_dict
				}
	#Only insert if the session is not already in the collection
	if collection.find({"id": session_id}).count() == 0 and collection.find({"email": email}).count() == 0:
		collection.insert(session)
    else:
        #TODO(Sam): Generate a new session here
