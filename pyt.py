import requests
import pandas as pd 

headers = {"Authorization": "Bearer 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"}

def run_query(query, variables): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
    print(request.text)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

        
# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
query = """
query($owner: String!, $name: String!)
{   repository(owner: $owner, name: $name)
    {   
        name
        object(expression: "main:src/file")
        {
            ... on Tree
            {
                entries 
                {
                    # name
                    # type
                    object 
                    {
                        ... on Blob 
                        {
                        # byteSize
                        text
                        }
                    }
                }
            }
        }
    }
}"""
variables = {
    "owner" : "edinburgh-teaching", 
    "name" : "INF2-CS-CW0-test"
}
result = run_query(query, variables) # Execute the query
s_no = result["data"]["repository"]["object"]['entries'][0]['object']['text'] 
repo_name = result["data"]["repository"]["name"]
### 0 before object needed as [ is before object
### expected output from result.text {"data":{"repository":{"object":{"entries":[{"object":{"text":"s2032563\n"}}]}}}} 
# print(s_no)
# print(repo_name)
data = {'Student Number' : [s_no],
        'Repo Name' : [repo_name]
        }
st_num = pd.DataFrame(data, columns=['Student Number', 'Repository Name'])
st_num.to_csv('log.csv', index = False)


