from datetime import datetime

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()
    
    def get_fields(self):
        return 

comment = Comment(email='leila@example.com', content='foo bar')


from rest_framework import serializers
class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

ser = CommentSerializer(data=comment.__dict__)
print(type(ser))
print(ser)  
ser.is_valid()
print(ser.data)


from rest_framework.renderers import JSONRenderer # render - to change obj into form - as view or as data?

json_data = JSONRenderer().render(ser.data)
print("json rendered ocb: " + str(json_data))

import json
# print("json dumped ocj: " + str(json.dumps(comment.__dict__))) # nie zadziała. no bo datetine to nie obiekt promityw
#becouse serialization = convertion into Python native datatypes. then u write as json


import io
from rest_framework.parsers import JSONParser

ser.is_valid()
stream = io.BytesIO(json_data)       # u read json as bytes stream
print(type(stream)) 
print(stream)
data = JSONParser().parse(stream)
print(data)
print(type(data))


class CommntModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['email', 'content', 'created'] # like in form, fields to use. List them explisitly so u dont show excesive data when model changes // fields = '__all__' // exclude

print(repr(CommentSerializer))
model_serialized = CommntModelSerializer(comment)