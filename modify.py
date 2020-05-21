import requests, json, time

session = requests.session()

timeStamp = int(time.time())


def login():
    # 登录
    url = 'http://test-api-passport.kaikeba.com/login'
    data = {"mobile": "18510780788", "verify_code": "111111", "remember": 1}
    res = session.post(url=url, data=data)
    # print(res.text)
    dict_response = json.loads(res.text)
    s_t = dict_response['data']['sso_token']

    #
    url1 = 'http://test-weblearn.kaikeba.com/token'
    data1 = {"sso_token": "{}".format(s_t)}
    res_ponse = session.post(url=url1, data=data1)
    # c=requests.utils.dict_from_cookiejar(res_ponse.cookies)
    # print(c)
    # print(res_ponse.text)


def ex_user():
    # 提取userid accesstoken
    url3 = 'https://xiaoke-test.kaikeba.com/api/v1.0/small-course/passport/learn-center/token?app_id='
    res1 = session.get(url=url3, verify=False)

    cookie_dict = requests.utils.dict_from_cookiejar(res1.cookies)
    dict_data = json.loads(res1.text)
    extract_userid = dict_data['data']['userId']
    extract_accessToken = dict_data['data']['accessToken']
    return extract_userid, extract_accessToken


def ex_jupyterCourseId():
    # 提取jupyter_courseid
    url4 = 'http://test-weblearn.kaikeba.com/student/small_course/list'
    res_ponse = session.get(url=url4)

    dict_data = json.loads(res_ponse.text)
    extract_jupyter_courseid = dict_data['data']['list'][-1]['id']
    return extract_jupyter_courseid


def ex_jupyterClassId():
    userData = ex_user()
    extract_jupyter_courseid = ex_jupyterCourseId()
    # 提取jupyter_id
    url10 = 'https://xiaoke-test.kaikeba.com/api/v1.0/small-course/user/{}/purchased-course/{}?token={}&app_data=&scope=1'.format(
        userData[0], extract_jupyter_courseid, userData[1])
    res_ponse = session.get(url10, verify=False)
    # print(res_ponse.text)
    dict_data = json.loads(res_ponse.text)
    extract_jupyter_class_id = dict_data['data']['smallClassList'][0]['id']
    extract_jupyter_task_id = dict_data['data']['smallClassList'][0]['firstTaskId']
    return extract_jupyter_class_id, extract_jupyter_task_id


def ex_userNameData(userData,extract_jupyter_courseid):
    jupyterData = ex_jupyterClassId()
    # 提取username-xiaoke
    url17 = 'https://xiaoke-test.kaikeba.com/smallcourse-jupyter/notebooks/{}/{}/{}/{}/python-excel/python_excel.ipynb?kkb_course_type=spbl&t={}&token=157ea116ef293d4dd74ca37f4c7f40360906f7a8d7f3c643'.format(
        userData[0], extract_jupyter_courseid, jupyterData[0], jupyterData[1], timeStamp)
    cookie = 'userId={}'.format(userData[0]), 'accessToken={}'.format(userData[1])
    header = {"cookie": cookie}
    tunple_cookie = header['cookie']
    str_cookie = ";".join(tunple_cookie)
    new_header = {"cookie": str_cookie}
    res_ponse = session.get(url17, headers=new_header, verify=False)
    print(url17)
    print(cookie)
    # print(new_header)
    print(res_ponse.status_code)
    # print(res_ponse.text)
    # dict_cookie=requests.utils.dict_from_cookiejar(res_ponse.cookies)
    # extract_username_xiaoke_test_kaikeba_com=dict_cookie['username-xiaoke-test-kaikeba-com']
    # print(extract_username_xiaoke_test_kaikeba_com)


login()
userData = ex_user()
extract_jupyter_courseid = ex_jupyterCourseId()
ex_userNameData(userData,extract_jupyter_courseid)




#
# #提取
# url16 = 'https://xiaoke-test.kaikeba.com/smallcourse-jupyter/api/contents/{}/{}/{}/{}/python-excel/python_excel.ipynb?type=notebook&_={}'.format(
# extract_userid, extract_jupyter_courseid, extract_jupyter_class_id, extract_jupyter_task_id,timeStamp)
# cookie='username-xiaoke-test-kaikeba-com={}'.format(extract_username_xiaoke_test_kaikeba_com)
# header={"cookie":cookie}
# print(header)
# res_ponse11 = session.get(url=url16,headers=header,verify=False)
# print(res_ponse11.text)
