import  symbl
import json

from json import JSONEncoder
# Process audio file
def document(filename):
  conversation_object = symbl.Video.process_file(
  # credentials={app_id: <app_id>, app_secret: <app_secret>}, #Optional, Don't add this parameter if you have symbl.conf file in your home directory
     file_path=filename)

# Printing transcription messages
  answer=((conversation_object.get_messages()))
# print(answer)
# print(conversation_object.get_action_items()) 
# print(conversation_object.get_topics()) 
# print(conversation_object.get_questions())
# print(conversation_object.get_follow_ups()) 
# print(conversation_object.transcription()) 
# jsonstr1 = json.dumps(answer,indent=4,cls=JSONEncoder) 
# json2 = json.loads(jsonstr1)
# print(json2)
  li=[]
# print(answer.messages)
  ans=''
  for i in answer.messages:
        ans+=(i.text)
  return ans    
  