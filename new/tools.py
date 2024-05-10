class Tools:
    def __init__(self, code_interpreter: bool = False, retrieval: bool = False):
        self.code_interpreter = code_interpreter
        self.retrieval = retrieval
        self.tools = list()
        self.functions: dict = dict()

    def __repr__(self):
        return f"<Functions {list(self.functions.keys())}>"

    def __str__(self):
        return f"<Functions {list(self.functions.keys())}>"

    def add_function(self, function: any, description: dict) -> bool:
        """
        add a function to the tools
        :param function: function: function to add
        :param description: dict: description of the function
        :return: bool: True if added
        """

        self.functions[function.__name__] = {"function": function, "description": description}
        return True

    def remove_function(self, function_name: str) -> bool:
        """
        remove a function from the tools
        :param function_name: str: name of the function to remove
        :return: bool: True if removed
        """

        del self.functions[function_name]
        return True

    def list_functions(self) -> list:
        """
        list all functions
        :return: list: list of functions
        """

        return list(self.functions.keys())

    def get_tools(self) -> list:
        """
        get the tools
        :return: list: list of tools
        """

        tools = list()
        if self.code_interpreter:
            tools.append({"type": "code_interpreter"})
        if self.retrieval:
            tools.append({"type": "retrieval"})
        if self.functions:
            for func in self.functions.keys():
                tools.append(self.functions[func]["description"])
        return tools
