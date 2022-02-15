class LabelError(Exception):
    def __init__(self, error_message: str):
        super().__init__(error_message)


class TransformError(Exception):
    def __init__(self, error_message: str):
        super().__init__(error_message)


class ClassificationError(Exception):
    def __init__(self, error_message: str):
        super().__init__(error_message)


class FeatureError(Exception):
    def __init__(self, error_message: str):
        super().__init__(error_message)
