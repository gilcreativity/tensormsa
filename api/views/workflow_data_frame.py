import json
from rest_framework.response import Response
from rest_framework.views import APIView
from master.workflow.data.workflow_data_frame import WorkFlowDataFrame as data_frm
from common.utils import *

class WorkFlowDataFrame(APIView):
    """
    """
    def post(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : insert cnn configuration data
          completed
        """
        try:
            # save uploaded file on source folder
            file_cnt = save_upload_file(request, nnid, ver, node)
            return Response(json.dumps(["{0} file upload success".format(file_cnt)]))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def get(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : get cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def put(self, request, src, form, prg, nnid, ver, node):
        """
        - desc ; update cnn configuration data
        """
        try:
            # set parms for data_node
            if (prg == 'source'):
                return_data = data_frm().put_step_source(src, form, prg, nnid, ver, node, request.data)
            elif (prg == 'pre'):
                return_data = data_frm().put_step_preprocess(src, form, prg, nnid, ver, node, request.data)
            elif (prg == 'store'):
                return_data = data_frm().put_step_store(src, form, prg, nnid, ver, node, request.data)
            else:
                return_data = {'result': 'no type'}
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))

    def delete(self, request, src, form, prg, nnid, ver, node):
        """
        - desc : delete cnn configuration data
        """
        try:
            return_data = ""
            return Response(json.dumps(return_data))
        except Exception as e:
            return_data = {"status": "404", "result": str(e)}
            return Response(json.dumps(return_data))
