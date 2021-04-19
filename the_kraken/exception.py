class KrakenError(Exception):
    def __init__(self, messages):
        self._messages = messages
    
    def __str__(self):
        output = ''
        if len(self._messages) == 1:
            output += self._messages[0]
        else:
            output += ', '.join(self._messages)
        return output