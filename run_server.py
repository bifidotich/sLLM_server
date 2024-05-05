from flask import Flask, request, jsonify
import aimodel
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

path_model = config.get('MODEL', 'PATH_MODEL')
max_length = int(config.get('DEVICE', 'MAX_LENGTH'))
max_memory_mapping = eval(config.get('DEVICE', 'MEMORY_MAP'))
port = int(config.get('SERVER', 'PORT'))

app = Flask(__name__)

device = f'cuda:{list(max_memory_mapping.keys())[0]}'
model, tokenizer = aimodel.get_model(model_name=path_model, max_memory_mapping=max_memory_mapping)


def sample_response():
    return {
        "id": None,
        "object": None,
        "created": None,
        "model": None,
        "system_fingerprint": None,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "",
            },
            "logprobs": None,
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": None,
            "completion_tokens": None,
            "total_tokens": None
        }
    }


def generate_response_from_messages(messages, condition='GPT4 Correct'):
    start_prompt = f"{condition} Assistant:"
    prompt = start_prompt
    messages = list(reversed(messages))
    for msg in messages:
        role = msg['role'].strip().capitalize()
        text = msg['content']
        local_prompt = f'{condition} {role}: {text}<|end_of_turn|>{prompt}'
        if len(local_prompt) < max_length:
            prompt = local_prompt
        else:
            break
    print(prompt)
    response = aimodel.generate_response(model=model, tokenizer=tokenizer, prompt=prompt, max_length=max_length)
    return response.split(start_prompt)[-1]


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    model = data.get('model', None)
    condition = data.get('condition', None)
    messages = data.get('messages', [])

    if not model or not messages:
        return jsonify({"error": "Model and messages are required"}), 400
    if condition is None:
        condition = ''
    response_text = generate_response_from_messages(messages, condition=condition)

    response = sample_response()
    response["model"] = str(model)
    response["choices"][0]["message"]["content"] = response_text

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
