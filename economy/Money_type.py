from enum import Enum
class MoneyType(Enum):
    RS3 = 1
    R07 = 2
    TOKENS = 3

    def formatString(self):
    	if self == MoneyType.R07:
    		return "07"
    	else:
    		return self.name