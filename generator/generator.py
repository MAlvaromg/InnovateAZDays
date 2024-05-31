import os
import json
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version = "2024-02-01",
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    )

def call_openai_and_write_file(messages, file_name=""):
    response = client.chat.completions.create(
        model = os.getenv("CHAT_COMPLETIONS_DEPLOYMENT_NAME"),
        messages = messages,
        temperature = 0.1,
        max_tokens = 4000
    )

    file_json = json.loads(response.choices[0].message.content, strict=False)
    print(file_json['filecontent'])

    if not file_name:
        file_name = "temp/" + file_json['filename']
    with open(file_name, 'w') as f:
        f.write(file_json['filecontent'])

    return response.choices[0].message

def get_url(file):
    with open(file) as f:
        issue_body = f.read()
        return issue_body.split("](")[1].split(")")[0]

def get_appname(file):
    appname = ""
    with open(file) as f:
        appname = f.read().split("App:")[1].strip().replace(" ", "").lower()
    with open("temp/appname.txt", 'w') as f:
        f.write(appname)
    return appname

appname = get_appname('temp/title.txt')
url = get_url('temp/body.txt')

messages=[
    { "role": "system", "content": "You are an assistant for web developers. You provide working source code based on image sketches." },
    { "role": "user", "content": [  
        { 
            "type": "text", 
            "text": f"Based on this image, generate a markdown file describing the files that would be generated for a new standalone angular component named '{appname}' for this app. These include: model, service, component logic, html and css. Do not include source code, just a summary of the component and the files. Include in the summary an OpenAPI specification in YAML that describes the necessary API for this component. Reply with the markdown file contents formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." 
        },
        { 
            "type": "image_url",
            "image_url": { "url": url }
        }
    ] }
]
print("🚀🚀🚀 GENERATING SUMMARY 🚀🚀🚀")
response = call_openai_and_write_file(messages, 'temp/summary.md')

messages.append(response)
messages.append({ "role": "user", "content": "Generate the component model implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })

print("🚀🚀🚀 GENERATING MODEL 🚀🚀🚀")
response = call_openai_and_write_file(messages)

messages.append(response)
messages.append({ "role": "user", "content": "Generate the component service implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })

print("🚀🚀🚀 GENERATING SERVICE 🚀🚀🚀")
response = call_openai_and_write_file(messages)

messages.append(response)
messages.append({ "role": "user", "content": "Generate the component logic implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })

print("🚀🚀🚀 GENERATING LOGIC 🚀🚀🚀")
response = call_openai_and_write_file(messages)

messages.append(response)
messages.append({ "role": "user", "content": "Generate the component html implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })

print("🚀🚀🚀 GENERATING HTML 🚀🚀🚀")
response = call_openai_and_write_file(messages)

messages.append(response)
messages.append({ "role": "user", "content": "Generate the component css implementation file. Reply with the source code formatted inside a json with two keys: 'filename' and 'filecontent'. Don't wrap this json in markdown." })

print("🚀🚀🚀 GENERATING CSS 🚀🚀🚀")
response = call_openai_and_write_file(messages)