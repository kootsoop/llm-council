import os
from elevenlabs import ElevenLabs
from ari import store_in_pickle, load_from_pickle

client = ElevenLabs(
	     base_url="https://api.elevenlabs.io"
)


def check_if_already_done(conversation_id, conversations):
	if not conversations:
		return False
	for one_conversation in conversations.conversations:
		if one_conversation.conversation_id == conversation_id:
			return True
	return False


previous_conversations = None
if os.path.exists("elevenlabs_conversations.pkl"):
	previous_conversations = load_from_pickle("elevenlabs_conversations.pkl")

all_conversations = client.conversational_ai.conversations.list()

for one_conversation in all_conversations.conversations:
	this_id = one_conversation.conversation_id	
	if check_if_already_done(this_id, previous_conversations):
		print(f"Skipping already done conversation {this_id}")
		continue
	print("-----------------------------")
	print(one_conversation.conversation_id)
	details = client.conversational_ai.conversations.get(
		one_conversation.conversation_id
	)
	this_conversation = ""
	for one_step in details.transcript:
		if one_step.message is None:
			continue		
		this_conversation += f"{one_step.role}: {one_step.message}\n"

	with open(
		f"{one_conversation.conversation_id}.txt",
		"w"
	) as f:
		f.write(this_conversation)

store_in_pickle("elevenlabs_conversations.pkl", all_conversations)