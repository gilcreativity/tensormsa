import requests
import json, os

url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8989")

nn_id = 'nn00009'
nn_ver = '1'
node_name = 'eval_node'
resp = requests.put('http://' + url + '/api/v1/type/wf/state/eval/nnid/'+nn_id+'/ver/'+nn_ver+'/node/'+node_name+'/',
                    json={
                        "type": "w2v",
                    })

data = json.loads(resp.json())
print("evaluation result : {0}".format(data))
