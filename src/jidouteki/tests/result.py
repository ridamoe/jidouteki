from enum import Enum, auto
from typing import Self, List

class TestState(Enum):
    Unknown = auto()
    """The test could not run correctly"""

    Ok = auto()
    """The test executed successfully"""
    
    Error = auto()
    """The test failed with an error"""

class TestResult:
    def __init__(self, state: TestState, message=None, context = None):
        self.state = state
        self.message = message
        self.context = context
        
    def __bool__(self):
        return self.state == TestState.Ok
    
    def __repr__(self):
        msg =  f"- {self.message}" if self.message else ""
        
        return f"{self.state.name}{msg}"
    
class TestsOutcome:
    def __init__(self, result: List[TestResult] | TestResult = []):
        self.results: List[TestResult] = []
        if isinstance(result, list):
            self.results.extend(result)
        else:    
            self.results.append(result)

    def __repr__(self):
        return self.result.__repr__()
    
    def __bool__(self):
        return self.result
    
    def append(self, val: TestResult):
        self.results.append(val)
    
    @property
    def result(self):
        ret = TestResult(TestState.Unknown)
        for r in self.results:
            match r.state:
                case TestState.Unknown: pass
                case TestState.Error: 
                    ret = r
                    break
                case TestState.Ok: ret = r 
        return ret
    