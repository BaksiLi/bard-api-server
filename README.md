# Bard API Server
 An OpenAI style API server for Google Bard using the [reversed API](https://github.com/dsdanielpark/Bard-API).

<img width="550" alt="Screenshot 2023-11-01 at 01 00 29" src="https://github.com/BaksiLi/bard-api-server/assets/26314680/107b28dc-856a-4168-a9ab-ddd40c945e17">


## Future Plan
- [ ] CLI
- [ ] Support for longer chat messages (`[{'role': 'user', 'content': 'xxxx'}, ...]`)
- [ ] Dockerize

## Usage

```
import openai

openai.api_base = "http://localhost:8000/v1"
openai.api_key = '****'

completion = openai.Completion.create(model="bard", 
                                      messages=[{'role': 'user', 'content': 'Hello'}])
print(completion)
```

This would give you:
```
{
  "id": "3260b2ec-52b1-4a10-84c4-cdbaa31dd3f2",
  "object": "chat.completion",
  "created": 1698771134,
  "model": "bard",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Hello! How may I help you today?\r\n\r\nI am excited to be able to help you with your tasks and answer your questions. I am still under development, but I am learning new things every day. I am always happy to receive feedback, so please let me know if there is anything I can do to improve."
      },
      "finish_reason": "stop",
      "index": 0
    }
  ]
}
```

Which is equivalent to 
```
import openai

openai.api_base = "https://api.openai.com/v1"
openai.api_key = '****'

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion)
```
