from .utils import send_post_request, send_get_request
from .constants import HEADERS
from .tools import Tools


def create_run(
        thread_id: str,
        assistant_id: str,
        model: str or None = None,
        instructions: str or None = None,
        tools: Tools or None = None,
        metadata: dict or None = None
) -> object:
    """
    create a new run
    :param thread_id: str: id of the thread
    :param assistant_id: str: id of the assistant
    :param model: str or None: id of the model
    :param instructions: str or None: instructions for the run
    :param tools: Tools or None: tools for the run
    :param metadata: dict or None: metadata for the run
    :return: object: run object
    """

    data = dict()
    data["assistant_id"] = assistant_id
    if model is not None:
        data["model"] = model
    if instructions is not None:
        data["instructions"] = instructions
    if tools is not None:
        data["tools"] = tools.get_tools()
    if metadata is not None:
        data["metadata"] = metadata

    url = f"https://api.openai.com/v1/threads/{thread_id}/runs"
    response = send_post_request(url, data=data, headers=HEADERS)
    return Run(**response)


def retrieve_run(thread_id: str, run_id: str) -> object:
    """
    retrieve a run
    :param thread_id: str: id of the thread
    :param run_id: str: id of the run
    :return: object: run object
    """

    url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}"
    response = send_get_request(url, headers=HEADERS)
    return Run(**response)


def modify_run(thread_id: str, run_id: str, metadata: dict) -> object:
    """
    modify a run
    :param thread_id: str: id of the thread
    :param run_id: str: id of the run
    :param metadata: dict: metadata to update
    :return: object: run object
    """

    data = dict()
    data["metadata"] = metadata

    url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}"
    response = send_post_request(url, data=data, headers=HEADERS)
    return Run(**response)


def list_runs(thread_id: str) -> list:
    """
    list all runs in a thread
    :param thread_id: str: id of the thread
    :return: list: list of run objects
    """

    url = f"https://api.openai.com/v1/threads/{thread_id}/runs"
    response = send_get_request(url, headers=HEADERS)
    return [Run(**run) for run in response["data"]] if "data" in response else []


def cancel_run(thread_id: str, run_id: str) -> object:
    """
    cancel a run
    :param thread_id: str: id of the thread
    :param run_id: str: id of the run
    :return: object: run object
    """

    url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}/cancel"
    response = send_post_request(url, data={}, headers=HEADERS)
    return Run(**response)


def submit_tool_outputs(thread_id: str, run_id: str, tool_outputs: list) -> object:
    """
    submit tool outputs
    :param thread_id: str: id of the thread
    :param run_id: str: id of the run
    :param tool_outputs: list: list of dictionaries containing tool call id and output
    :return: object: run object
    """

    data = {
        "tool_outputs": tool_outputs
    }
    url = f"https://api.openai.com/v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs"
    response = send_post_request(url, data=data, headers=HEADERS)
    return Run(**response)


class Run:
    def __init__(
            self,
            id: str,
            object: str,
            created_at: int,
            thread_id: str,
            assistant_id: str,
            status: str,
            expires_at: int,
            model: str,
            instructions: str,
            tools: list,
            file_ids: list,
            metadata: dict,
            temperature: any,
            top_p: any,
            max_completion_tokens: any,
            max_prompt_tokens: any,
            truncation_strategy: any,
            started_at: int or None = None,
            cancelled_at: int or None = None,
            failed_at: int or None = None,
            completed_at: int or None = None,
            required_action: object or None = None,
            last_error: str or None = None,

    ):
        self.id = id
        self.object = object
        self.created_at = created_at
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.status = status
        self.required_action = required_action
        self.last_error = last_error
        self.expires_at = expires_at
        self.started_at = started_at
        self.cancelled_at = cancelled_at
        self.failed_at = failed_at
        self.completed_at = completed_at
        self.model = model
        self.instructions = instructions
        self.tools = tools
        self.file_ids = file_ids
        self.metadata = metadata

    def __str__(self):
        return f"Run: {self.id} ({self.status})"

    def __repr__(self):
        return f"Run: {self.id} ({self.status})"

    def info(self) -> None:
        """
        print run info
        :return: None
        """

        print(f"ID: {self.id}")
        print(f"Object: {self.object}")
        print(f"Created at: {self.created_at}")
        print(f"Thread ID: {self.thread_id}")
        print(f"Assistant ID: {self.assistant_id}")
        print(f"Status: {self.status}")
        print(f"Required actions: {self.required_action}")
        print(f"Last error: {self.last_error}")
        print(f"Expires at: {self.expires_at}")
        print(f"Started at: {self.started_at}")
        print(f"Cancelled at: {self.cancelled_at}")
        print(f"Failed at: {self.failed_at}")
        print(f"Completed at: {self.completed_at}")
        print(f"Model: {self.model}")
        print(f"Instructions: {self.instructions}")
        print(f"Tool: {self.tools}")
        print(f"File IDs: {self.file_ids}")
        print(f"Metadata: {self.metadata}")
        return None

    def retrieve(self) -> object:
        """
        retrieve run
        :return: object: run object
        """

        run = retrieve_run(self.thread_id, self.id)
        self.__dict__.update(**run.__dict__)
        return run

    def modify(self, metadata: dict) -> object:
        """
        modify run
        :param metadata: dict: metadata to update
        :return: object: run object
        """

        run = modify_run(self.thread_id, self.id, metadata)
        self.__dict__.update(**run.__dict__)
        return run

    def cancel(self) -> object:
        """
        cancel run
        :return: run object
        """

        run = cancel_run(self.thread_id, self.id)
        self.__dict__.update(**run.__dict__)
        return run

    def submit_tool_outputs(self, tool_outputs: list) -> object:
        """
        submit tool output
        :param tool_outputs: list: list of dictionaries of tool outputs
        :return: object: run object
        """

        run = submit_tool_outputs(self.thread_id, self.id, tool_outputs)
        self.__dict__.update(**run.__dict__)
        return run
