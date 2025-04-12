class ProviderError(Exception):
    pass

class MappingWrongArgumentsError(ProviderError):
    pass

class ParserError(Exception):
    pass

class MissingTestError(ParserError):
    pass

class TestWithoutMappingError(ParserError):
    pass

class DuplicatedMappingDecoratorError(ParserError):
    pass


class MissingMappingError(Exception):
    pass

class MissingRequiredMappingError(MissingMappingError):
    pass