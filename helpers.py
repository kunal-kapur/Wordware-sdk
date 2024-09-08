from typing import Dict, Literal


Input_Type = Literal["text", "long text ", "image"]

class InputParam:
    def __init__(self, input: dict) -> None:
        self.id = input['id']
        self.label = input['label']
        self.type: Input_Type = input['type']
    
        
