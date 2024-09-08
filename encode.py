import json
import requests
from pathlib import Path


def main():
    prompt_id = "240c6457-02de-45a0-95dc-fa5540a49583"
    api_key = Path("api.txt").read_text()

    print(api_key)

    prompt_id = "b2f176c9-baa7-4db3-ac56-d6f641a05c53"

    # Describe the prompt (shows just the inputs for now)
    r1 = requests.get(f"https://app.wordware.ai/api/prompt/dwadwadada{prompt_id}/describe",
                      headers={"Authorization": f"Bearer {api_key}"})
    
    print(json.dumps(r1.json()))

    # r = requests.post(f"https://app.wordware.ai/api/prompt/{prompt_id}/run",
    #                                         json={
    #                       "inputs": {
    #                           "person": "Elon Musk"
    #                       }
    #                   },
    #                   headers={"Authorization": f"Bearer {api_key}"},
    #                   stream=True
    #                   )
    
    # if r.status_code != 200:
    #     print("Request failed with status code", r.status_code)
    #     print(json.dumps(r.json(), indent=4))
    # else:
    #     for line in r.iter_lines():
    #         if line:
    #             content = json.loads(line.decode('utf-8'))
    #             print(content)
                # value = content['value']
                # # We can print values as they're generated
                # if value['type'] == 'generation':
                #     if value['state'] == "start":
                #         print("\nNEW GENERATION -", value['label'])
                #     else:
                #         print("\nEND GENERATION -", value['label'])
                # elif value['type'] == "chunk":
                #     print("CHUNKING")
                #     print(value['value'], end="")
                # elif value['type'] == "outputs":
                #     # Or we can read from the outputs at the end
                #     # Currently we include everything by ID and by label - this will likely change in future in a breaking
                #     # change but with ample warning
                #     print("\nFINAL OUTPUTS:")
                #     print(json.dumps(value, indent=4))
  


if __name__ == '__main__':
    main()