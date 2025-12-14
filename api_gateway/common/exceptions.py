class ApiException(Exception):
    def __init__(self, title: str, description: str, status: int):
        self.title = title
        self.description = description
        self.status = status
