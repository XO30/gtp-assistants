from .utils import send_get_request, send_post_request, send_delete_request
from .constants import HEADERS
from .tools import Tools
from .file import (
    upload_file,
    create_assistant_file,
    list_assistant_files,
    delete_assistant_file,
    retrieve_assistant_file,
    delete_file
)


def list_assistants() -> list:
    """
    list all assistants
    :return: list: list of all assistants
    """

    url = "https://api.openai.com/v1/assistants?order=desc&limit=20"
    response = send_get_request(url, HEADERS)
    return [Assistant(**assistant) for assistant in response["data"]]


def retrieve_assistant(assistant_id: str) -> object:
    """
    retrieve an assistant
    :param assistant_id: str: id of the assistant
    :return: object: assistant object
    """

    url = f"https://api.openai.com/v1/assistants/{assistant_id}"
    response = send_get_request(url, HEADERS)
    return Assistant(**response)


def delete_assistant(assistant_id: str) -> bool:
    """
    delete an assistant
    :param assistant_id: str: id of the assistant
    :return: bool: True if deleted
    """

    url = f"https://api.openai.com/v1/assistants/{assistant_id}"
    send_delete_request(url, HEADERS)
    return True


def create_assistant(
        model: str,
        name: str or None = None,
        description: str or None = None,
        instructions: str or None = None,
        tools: Tools or None = None,
        file_ids: list or None = None,
        metadata: dict or None = None
) -> object:
    """
    create a new assistant
    :param model: str: id of the model
    :param name: str or None: name of the assistant
    :param description: str or None: description of the assistant
    :param instructions: str or None: instructions for the assistant
    :param tools: Tools or None: tools for the assistant
    :param file_ids: list or None: list of file ids
    :param metadata: dict or None: metadata for the assistant
    :return: object: assistant object
    """

    data = dict()
    data["model"] = model
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    if instructions:
        data["instructions"] = instructions
    if file_ids:
        data["file_ids"] = file_ids
    if metadata:
        data["metadata"] = metadata
    if tools:
        data["tools"] = tools.get_tools()

    url = "https://api.openai.com/v1/assistants"
    response = send_post_request(url, HEADERS, data)
    return Assistant(**response)


def modify_assistant(
        assistant_id: str,
        model: str or None = None,
        name: str or None = None,
        description: str or None = None,
        instructions: str or None = None,
        tools: Tools or None = None,
        file_ids: list or None = None,
        metadata: dict or None = None
) -> object:
    """
    modify an assistant
    :param assistant_id: str: id of the assistant
    :param model: str or None: id of the model
    :param name: str or None: name of the assistant
    :param description: str or None: description of the assistant
    :param instructions: str or None: instructions for the assistant
    :param tools: Tools or None: tools for the assistant
    :param file_ids: list or None: list of file ids
    :param metadata: dict or None: metadata for the assistant
    :return: object: assistant object
    """

    data = dict()
    if model:
        data["model"] = model
    if name:
        data["name"] = name
    if description:
        data["description"] = description
    if instructions:
        data["instructions"] = instructions
    if file_ids:
        data["file_ids"] = file_ids
    if metadata:
        data["metadata"] = metadata
    if tools:
        data["tools"] = tools.get_tools()

    url = f"https://api.openai.com/v1/assistants/{assistant_id}"
    response = send_post_request(url, HEADERS, data)
    return Assistant(**response)


class Assistant:
    def __init__(self,
                 id: str,
                 object: str,
                 created_at: int,
                 name: str,
                 description: str,
                 model: str,
                 instructions: str,
                 tools: list,
                 file_ids: list,
                 metadata: dict,
                 top_p: any,
                 ):
        self.id = id
        self.object = object
        self.created_at = created_at
        self.name = name
        self.description = description
        self.model = model
        self.instructions = instructions
        self.tools = tools
        self.file_ids = file_ids
        self.metadata = metadata

    def __repr__(self):
        return f"<Assistant {self.name}, id: {self.id}>"

    def __str__(self):
        return f"<Assistant {self.name}, id: {self.id}>"

    def info(self) -> None:
        """
        print assistant info
        :return: None
        """

        self.retrieve()
        print(f"Name: {self.name}")
        print(f"ID: {self.id}")
        print(f"Object: {self.object}")
        print(f"Created at: {self.created_at}")
        print(f"Description: {self.description}")
        print(f"Model: {self.model}")
        print(f"Instructions: {self.instructions}")
        print(f"Tools: {self.tools}")
        print(f"File IDs: {self.file_ids}")
        print(f"Metadata: {self.metadata}")
        return None

    def retrieve(self) -> object:
        """
        retrieve assistant
        :return: object: assistant object
        """

        assistant = retrieve_assistant(self.id)
        self.__dict__.update(**assistant.__dict__)
        return assistant

    def delete(self) -> bool:
        """
        delete assistant
        :return: bool: True if deleted
        """

        delete_assistant(self.id)
        self.__dict__.clear()
        del self
        return True

    def modify(
            self,
            model: str or None = None,
            name: str or None = None,
            description: str or None = None,
            instructions: str or None = None,
            tools: Tools or None = None,
            file_ids: list or None = None,
            metadata: dict or None = None
    ) -> object:
        """
        modify assistant
        :param model: str or None: id of the model
        :param name: str or None: name of the assistant
        :param description: str or None: description of the assistant
        :param instructions: str or None: instructions for the assistant
        :param tools: Tools or None: tools for the assistant
        :param file_ids: list or None: list of file ids
        :param metadata: dict or None: metadata for the assistant
        :return: object: assistant object
        """

        assistant = modify_assistant(
            self.id,
            model,
            name,
            description,
            instructions,
            tools,
            file_ids,
            metadata
        )
        self.__dict__.update(**assistant.__dict__)
        return assistant

    def add_assistant_files(self, file: list) -> bool:
        """
        add assistant file
        :param file: list: list of files to add
        :return: True if successful
        """

        self.retrieve()
        file_ids = self.file_ids
        for file in file:
            file = upload_file(file)
            assistant_file = create_assistant_file(self.id, file.id)
            file_ids.append(assistant_file.id)
        self.modify(file_ids=file_ids)
        return True

    def list_assistant_files(self) -> list:
        """
        list assistant files
        :return: list: list of assistant files
        """

        return list_assistant_files(self.id)

    def delete_assistant_file(self, file_id: str) -> bool:
        """
        delete assistant file
        :param file_id: str: id of the file
        :return: bool: True if successful
        """

        delete_assistant_file(self.id, file_id)
        delete_file(file_id)
        return True

    def retrieve_assistant_file(self, file_id: str) -> object:
        """
        retrieve assistant file
        :param file_id: str: id of the file
        :return: object: assistant file object
        """

        return retrieve_assistant_file(self.id, file_id)
