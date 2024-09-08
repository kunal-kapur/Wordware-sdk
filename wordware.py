from typing import Dict, Union
import os
import requests
import json

from helpers import InputParam
class Wordware:

    def __init__(self, prompt_id: str, api_key: Union[str, None]=None, publish_id: Union[str, None]=None) -> None:
        if api_key is None:
            api_key = os.getenv("WORDWARE_API_KEY")
            if api_key is None:
                raise ValueError("Add WORDWARE_API_KEY")
        # when endpoint for publish_id/describe is added, prompt_id can be replaced with publish_id    
        r1 = requests.get(f"https://app.wordware.ai/api/prompt/{prompt_id}/describe",
                      headers={"Authorization": f"Bearer {api_key}"})
        response = r1.json()
        if response.get('ok', True) is False:
            raise ValueError("No such prompt exists")
        
        self.describe_info  = response

        self.api_key = api_key
        self.prompt_id = prompt_id

        self.publish_id = publish_id
        # this will grab from the official published version
        if self.publish_id is None:
            self.publish_id = prompt_id


        self.inputs = {}
        for i in response['inputs']:
            if i['label'] in self.inputs:
                raise ValueError(f"Same input name {i['label']}")
            new_input = InputParam(i)
            self.inputs[new_input.label] = new_input


    def describe(self,):
        return self.describe_info

    def run(self, inputs: Dict={}, **kwargs):
        for key, value in kwargs.items():
            inputs[key] = value
        input_keys = set(inputs.keys())
        excluded = set(self.inputs.keys()).difference(input_keys)
        extra = input_keys.difference(set(self.inputs.keys()))
        try:
            if len(excluded) > 0  or len(extra) > 0:
                raise ValueError("Invalid inputs")
        except ValueError as e:
            print(repr(e))
            print(f"Excluded arugments", excluded)
            print(f"Extra arguments", extra)
        
        r = requests.post(f"https://app.wordware.ai/api/prompt/{self.prompt_id}/run",
                                        json={
                        "inputs": inputs
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    stream=True
                    )
    
    





        