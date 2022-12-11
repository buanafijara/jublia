# importing the requests library
import requests

# defining the api-endpoint 
API_ENDPOINT = "http://127.0.0.1:5000/save_emails"
  
# data to be sent to api
content = """Lorem ipsum dolor sit amet consectetur adipisicing elit. 
    Ratione iste aliquid ea animi magni maiores aperiam quo, veritatis 
    beatae quam? Amet iusto dolorem repudiandae asperiores nobis magni 
    veniam veritatis praesentium?"""
data = {'event_id': 1,
        'email_subject': 'Subject for Event 1',
        'email_content': content,
        'timestamp': '2022-12-13 17:00'}
  
# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = data)
  
# extracting response text 
result = r.text
print(result)