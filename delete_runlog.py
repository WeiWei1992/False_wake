import os

res=os.getcwd()
result_tmp_1_path = os.path.join(res, 'runlog.log')
# result_tmp_path_1
# print("res: ",res)
# print("result_tmp_path_1:",result_tmp_path_1)
# print("result_tmp_1_path",result_tmp_1_path)
if os.path.isfile(result_tmp_1_path):
    print("删除runlog.log")
    os.remove(result_tmp_1_path)