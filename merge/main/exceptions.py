class LabelError(Exception):
    def __init__(self, err):
        super().__init__(err)


class TransformError(Exception):
    def __init__(self, err):
        super().__init__(err)


class ClassificationError(Exception):
    """ Raised if a Classifier can't handle the given input """

    def __init__(self, err):
        super().__init__(err)


class FeatureError(Exception):

    def __init__(self, err):
        super().__init__(err)


class CorpusError(Exception):
    """ Raised if corpus has an invalid format, either when constructing/loading or when using at runtime"""

    def __init__(self, err):
        super().__init__(err)


class ResourceError(Exception):
    """ Raised if external resources could not be located when attempting to load content
        (for example audio files, annotation files, etc.) """

    def __init__(self, err):
        super().__init__(err)


class QueryError(Exception):
    """ Raised if a Query or Influence is invalid """

    def __init__(self, err):
        super().__init__(err)


class CandidatesError(Exception):
    """ Raised when an invalid `Candidates` class is used """

    def __init__(self, err):
        super().__init__(err)


class FilterError(Exception):
    """ Raised when an error occurs in a `Filter` """

    def __init__(self, err):
        super().__init__(err)


class ConfigurationError(Exception):
    """ Raised when a component of the architecture has an invalid configuration
        (for example using a DYCI2Prospector in a SomaxGenerator)
    """

    def __init__(self, err):
        super().__init__(err)


class ComponentAddressError(Exception):
    """ Raised when a component address is invalid
        (for example when an address is already taken or when addressing a non-existing component)
    """


class ParameterError(Exception):
    """ Raised when a Parameter receives a value of the wrong type or out of the for the Parameter specified range """

    def __init__(self, err):
        super().__init__(err)


class InputError(Exception):
    """ Generic error for external input (generally over OSC) that cannot be handled and is not covered by any of the
        other exceptions in this module """


class StateError(Exception):
    """ Raised when an invalid state occurs in the runtime domain of the system, for example when
        sending a `Query` before loading a corpus
    """

    def __init__(self, err):
        super().__init__(err)
