# app/routes.py
from flask import Blueprint, render_template, request, jsonify
from .utils import create_llm, execute_prompt
from .models import prompts
from .database import get_chat_history, save_chat_history

main = Blueprint('main', __name__)

llm = create_llm()

@main.route('/')
def index():
    return render_template('index.html', prompts=prompts)

@main.route('/execute', methods=['POST'])
def execute():
    print('request.json',request.json)
    prompt_id = request.json['promptId']
    user_input = request.json['userInput']
    prompt_text = prompts[prompt_id]["text"] + " " + user_input
    result = execute_prompt(llm, prompt_text)

    return jsonify({'result': result})


@main.route('/chat', methods=['GET'])
def chat_page():
    return render_template('chat.html')

@main.route('/chat', methods=['POST'])
def chat_execute():
    print('request.json', request.json)
    chat_id = request.json['chatId']
    prompt_id = request.json['promptId']
    user_input = request.json['userInput']

    history = get_chat_history(chat_id)

    prompt_text = prompts[prompt_id]["text"]
    context = history[-500:] if history else ''  # Use the last 500 characters as context
    full_prompt = f"{prompt_text}\nContext: {context}\nUser: {user_input}\nAssistant:"

    result = execute_prompt(llm, full_prompt)
    history += f"User: {user_input}\nAssistant: {result}\n"
    save_chat_history(chat_id, history)

    next_prompts = [prompt for prompt in prompts.values() if prompt["id"] != prompt_id]
    return jsonify({'result': result, 'nextPrompts': next_prompts})