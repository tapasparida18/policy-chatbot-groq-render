import json
import urllib.request
 
payload = {
    "model": "llama3",
    "prompt": "What are working hours?",
    "stream": False
}
 
try:
 
    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        }
    )
 
    with urllib.request.urlopen(request) as response:
 
        result = json.loads(
            response.read().decode()
        )
 
        print(result)
 
except Exception as e:
 
    print("ERROR:")
    print(e)