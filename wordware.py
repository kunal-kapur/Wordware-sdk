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
        # additionally some information on the version would allow the user to pass it as a default arugment as use the most 
        # updated one to date as the default
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

    def run(self, inputs: Dict={}, version: Union[str, None]=None,  **kwargs):
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
        print("Inputs: ", inputs)
        r = requests.post(f"https://app.wordware.ai/api/released-app/{self.publish_id}/run",
                                        json={
                        "inputs": inputs,
                        "version": version,
                    },
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    stream=True
                    )
        if r.status_code != 200:
            print("Request failed with status code", r.status_code)
            print(json.dumps(r.json(), indent=4))
        else:
            for line in r.iter_lines():
                if line:
                    content = json.loads(line.decode('utf-8'))
                    print(content)
                    value = content['value']
                    # We can print values as they're generated
                    if value['type'] == 'generation':
                        if value['state'] == "start":
                            print("\nNEW GENERATION -", value['label'])
                        else:
                            print("\nEND GENERATION -", value['label'])
                    elif value['type'] == "chunk":
                        print(value['value'], end="")
                    elif value['type'] == "outputs":
                        # Or we can read from the outputs at the end
                        # Currently we include everything by ID and by label - this will likely change in future in a breaking
                        # change but with ample warning
                        print("\nFINAL OUTPUTS:")
                        return (json.dumps(value, indent=4))
        
        





        