import time
import json
from openai import OpenAI
from tools import Tools


class Bot:
    def __init__(self, assistant_id: str, api_key: str, tools: Tools):
        self.assistant_id = assistant_id
        self.client = OpenAI(api_key=api_key)
        self.conversations = {}
        self.tools = tools

    def _create_thread(self, conversation_id: str or int):
        if conversation_id not in self.conversations:
            thread = self.client.beta.threads.create()
            self.conversations[conversation_id] = thread
        return self.conversations[conversation_id]

    def _poll_status(self, run):
        while True:
            run = self.client.beta.threads.runs.retrieve(
                run_id=run.id,
                thread_id=run.thread_id
            )
            if run.status in ['completed', 'failed', 'cancelled']:
                break
            elif run.status == 'requires_action':
                run = self._handle_required_actions(run)
            else:
                time.sleep(0.1)
        return run

    def _handle_required_actions(self, run):
        required_actions = run.required_action['submit_tool_outputs']['tool_calls']
        tool_outputs = []

        for required_action in required_actions:
            func_name = required_action['function']['name']
            arguments = json.loads(required_action['function']['arguments'])
            action_id = required_action['id']

            # Assuming a tool handler for each function name exists
            output = self.tools.functions[func_name]['function'](**arguments)

            tool_outputs.append({
                'tool_call_id': action_id,
                'output': output
            })

        run.submit_tool_outputs(tool_outputs)
        return run

    def create_message(self, conversation_id: str or int, text: str, role: str = 'user'):
        thread = self._create_thread(conversation_id)
        message = self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role=role,
            content=text
        )
        return message

    def create_response(self, conversation_id: str or int):
        thread = self._create_thread(conversation_id)
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant_id
        )
        run = self._poll_status(run)
        print(run)
        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        #text = messages[0].content[0]['text']['value']
        #annotations = messages[0].content[0]['text']['annotations']
        return messages
