import requests
import json, os
from common.utils import *

# [TEST - Celery]
# apt-get install rabbitmq-server
# service rabbitmq-server start
# rabbitmqctl add_user tensormsa tensormsa
# rabbitmqctl set_user_tags tensormsa administrator
# rabbitmqctl set_permissions -p / tensormsa '.*' '.*' '.*'
# celery -A hoyai worker -l info
# ./manage.py runserver 2fb1ece74beb:8000 --noreload

println("S")
url = "{0}:{1}".format(os.environ['HOSTNAME'] , "8000")
nn_id = "mro001"
net_type = "cnn" # cnn, resnet
wf_ver_id = 0

# get workflow version
if wf_ver_id == 0:
    resp = requests.get('http://' + url + '/api/v1/type/common/target/nninfo/nnid/'+nn_id+'/version/')
    data = json.loads(resp.json())

    # get Max workflow version
    for config in data:
        if config["fields"]["nn_wf_ver_id"] > wf_ver_id:
            wf_ver_id = config["fields"]["nn_wf_ver_id"]

wf_ver_id = str(wf_ver_id)
# CNN Network WorkFlow Node : Network Config Setup
# (CNN Network WorkFlow Node의 Network Config를 Setup 해준다.)
node = "netconf_node"

if net_type == "cnn":
    resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                         "param":{"traincnt": 1
                                  ,"epoch": 2
                                  ,"batch_size":1000000
                                  ,"predictcnt": 3
                         },
                         "config": {"num_classes":10,
                                    "learnrate": 0.001,
                                    "layeroutputs":32,
                                    "net_type":"cnn",
                                    "eval_type":"category",
                                    "optimizer":"AdamOptimizer" #RMSPropOptimizer
                                     }
                         ,"layer1": {"active": "relu",
                                     "cnnfilter": [3, 3],
                                     "cnnstride": [1, 1],
                                     "maxpoolmatrix": [2, 2],
                                     "maxpoolstride": [2, 2],
                                     "padding": "SAME",
                                     "droprate": "0.8",
                                     "layercnt":4
                                    }
                         ,"layer2": {"active": "relu",
                                     "cnnfilter": [3, 3],
                                     "cnnstride": [1, 1],
                                     "maxpoolmatrix": [1, 1],
                                     "maxpoolstride": [2, 2],
                                     "padding": "SAME",
                                     "droprate": "0.8",
                                     "layercnt":1
                                    }
                         ,"out": {"active": "softmax",
                                   "node_out": 625,
                                   "padding": "SAME"
                                }
                         ,"labels":[]
                        })
elif net_type == "resnet":
    resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                         "param":{"traincnt": 3
                                  ,"epoch": 2
                                  ,"batch_size":25000
                                  ,"predictcnt": 10
                         },
                         "config": {"num_classes":10,
                                    "learnrate": 0.001,
                                    "layeroutputs":18, #18, 34, 50, 101, 152, 200
                                    "net_type":"resnet",
                                    "eval_type":"category",
                                    "optimizer":"AdamOptimizer" #RMSPropOptimizer
                                     }
                         ,"labels":[]
                        })
netconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(netconf))

# CNN Network WorkFlow Node :  Data Config Setup
# yolo min image size 385 and %7 = 0
node = "datasrc"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',
                     json={
                            "preprocess": {"x_size": 32,
                                           "y_size": 32,
                                           "channel":3,
                                           "filesize": 1000000,
                                           "yolo": "n",
                                           "augmentation":"N"}
                     })
dataconf = json.loads(resp.json())
# print("insert workflow node conf info evaluation result : {0}".format(dataconf))

# CNN Network WorkFlow Node :  Eval Config Setup
node = "eval_node"
resp = requests.put('http://' + url + '/api/v1/type/wf/state/netconf/detail/cnn/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',json={})
evalconf = json.loads(resp.json())

# CNN Network WorkFlow Node :  Eval Data Config Setup
# (CNN Network WorkFlow Node의 Data Config를 Setup 해준다.)
node = 'evaldata'
resp = requests.put('http://' + url + '/api/v1/type/wf/state/imgdata/src/local/form/file/prg/source/nnid/'+nn_id+'/ver/'+wf_ver_id+'/node/'+node+'/',json={
                            "preprocess": {"x_size": 32,
                                           "y_size": 32,
                                           "channel":3,
                                           "filesize": 1000000,
                                           "yolo": "n",
                                           "augmentation":"N"}
                     })
edataconf = json.loads(resp.json())

# CNN Network Training
# (CNN Network Training을 실행한다 .)
resp = requests.post('http://' + url + '/api/v1/type/runmanager/state/train/nnid/'+nn_id+'/ver/'+wf_ver_id+'/')
data = json.loads(resp.json())
print(data)

def spaceprint(val, cnt):
    leng = len(str(val))
    cnt = cnt - leng
    restr = ""
    for i in range(cnt):
        restr += " "
    restr = restr+str(val)
    return restr

if data == None:
    print(data)
else:
    try:
        if data["status"] == "404":
            print(data["result"])
    except:
        for train in data:
            if train != None and train != "" and train != {} and train != "status" and train != "result":
                try:
                    for tr in train["TrainResult"]:
                        print(tr)
                except:
                    maxcnt = 0
                    line = ""
                    for label in train["labels"]:
                        if maxcnt<len(label)+2:
                            maxcnt = len(label)+2

                    for i in range(len(train["labels"])):
                        for j in range(maxcnt+4):
                            line += "="

                    label_sub = []
                    for label in train["labels"]:
                        label = spaceprint(label,maxcnt)
                        label_sub.append(label)

                    space = ""
                    for s in range(maxcnt):
                        space +=" "

                    print(space, label_sub)
                    print(space, line)
                    for i in range(len(train["labels"])):
                        truecnt = 0
                        totcnt = 0
                        predict_sub = []
                        for j in range(len(train["predicts"][i])):
                            pred = spaceprint(train["predicts"][i][j],maxcnt)

                            predict_sub.append(pred)
                            totcnt += int(pred)
                            # print(train["labels"].index(train["labels"][i]))
                            if train["labels"].index(train["labels"][i]) == j:
                                truecnt = int(pred)
                        if totcnt == 0:
                            percent = 0
                        else:
                            percent = round(truecnt/totcnt*100,2)
                        print(spaceprint(train["labels"][i],maxcnt), predict_sub, str(percent)+"%")


println("E")





