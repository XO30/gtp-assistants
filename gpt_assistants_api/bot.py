import time
import json

from gpt_assistants_api.assistant import Assistant
from gpt_assistants_api.thread import create_thread
from gpt_assistants_api.run import Run
from gpt_assistants_api.tools import Tools


class Bot:
    def __init__(self, assistant: Assistant, tools: Tools = None):
        self.assistant = assistant
        self.tools = tools
        self.threads = dict()

    def _create_thread(self, conversation_id: str or int):
        if conversation_id not in self.threads:
            self.threads[conversation_id] = create_thread()
        return self.threads[conversation_id]

    def _poll_status(self, run: Run):
        while True:
            run.retrieve()
            if run.status in ['completed', 'failed', 'cancelled']:
                break
            elif run.status == 'requires_action':
                run = self._handle_required_actions(run)
            else:
                time.sleep(0.1)
        return run

    def _handle_required_actions(self, run: Run):
        required_actions = run.required_action['submit_tool_outputs']['tool_calls']
        tool_outputs = []

        for required_action in required_actions:
            func_name = required_action['function']['name']
            arguments = json.loads(required_action['function']['arguments'])
            action_id = required_action['id']

            if func_name in self.tools.functions.keys():
                output = self.tools.functions[func_name]['function'](**arguments)
            else:
                raise ValueError(f'function {func_name} not found')

            print(f'function {func_name} called with arguments {arguments} and output {output}')

            tool_outputs.append({
                'tool_call_id': action_id,
                'output': output
            })
        return run.submit_tool_outputs(tool_outputs)

    def create_message(
            self,
            conversation_id: str or int,
            text: str,
            role: str = 'user',
            files: list or None = None,
            metadata: dict or None = None
    ):
        thread = self._create_thread(conversation_id)
        thread.create_message(text, role, files, metadata)

    def create_response(self, conversation_id: str or int):
        thread = self._create_thread(conversation_id)
        run = thread.create_run(self.assistant.id)
        _ = self._poll_status(run)
        answer = thread.list_messages()[0]
        text = answer.content[0]['text']['value']
        annotations = answer.content[0]['text']['annotations']
        return text, annotations
