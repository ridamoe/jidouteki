class ProviderConfigError(Exception):
    pass

class TestWithoutMappingError(ProviderConfigError):
    pass

class DuplicatedMappingDecoratorError(ProviderConfigError):
    pass


class MissingMappingError(Exception):
    pass

class MissingRequiredMappingError(MissingMappingError):
    pass