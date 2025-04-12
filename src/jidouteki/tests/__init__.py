from enum import Enum, auto
from .result import *

class TestKind(Enum):
    """
    Specifies the type of test that will be performed
    """
    
    Match = auto()
    """
    The result passes if the output value 
    matches the expected value exactly. 
    """
    
    NoErrors = auto()
    """
    The test passes if any valid output value
    is generated without error. 
    """
    
    Fail = auto()
    """
    The test is expected to fail with an error.
    """

class Test:
    def __init__(self, input, expected_output, kind):
        if isinstance(input, tuple):
            if isinstance(input[-1], dict):
                self.input = (input[:-1], input[-1])
            else:
                self.input = (input, {})
        elif isinstance(input, dict):
            self.input = ((), input)
        else:
            self.input = ((input,), {})
        self.expected_output = expected_output
        if kind is None:
            kind = TestKind.NoErrors if expected_output is None else TestKind.Match
        self.kind = kind
    
    def run(self, function) -> TestResult:
        try:
            output = function(*self.input[0], **self.input[1])
        except Exception as e:
            if self.kind == TestKind.Fail:
                return TestResult(TestState.Ok, None, e)
            else: 
                return TestResult(TestState.Error, None, e)
        else:
            match self.kind:
                case TestKind.NoErrors:
                    return TestResult(TestState.Ok)
                case TestKind.Match:
                    if output == self.expected_output:
                        return TestResult(TestState.Ok)
                    else:
                        return TestResult(TestState.Error, f"Expected {self.expected_output} but got {output}")
                case TestKind.Fail:
                    return TestResult(TestState.Error, f"Test returned {output} when was expected to fail")