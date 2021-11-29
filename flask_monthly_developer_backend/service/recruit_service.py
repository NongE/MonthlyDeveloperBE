import json
from bson import json_util

from config import db_connector
from model import response_model

response_model = response_model.ResponseModel()

def save_post(req_data):
    # 응답을 위한 Dict
    new_post_res = {}

    # 게시글의 고유 아이디 정보
    # 게시글 고유 아이디는 게시글의 등록 순서를 의미
    # 현재 k번 게시글까지 있다고 가정하였을 때 새롭게 등록될 게시글은 k+1번째 게시글임
    counter_db = db_connector.mongo.db.counter
    recruit_post_id = counter_db.find_one({"type": "recruit_post"}, {"_id":0})["counter"] + 1
    post_db = db_connector.mongo.db.recruit_post
    try:
        # 새 글 생성
        recruit_title = req_data.json.get("recruit_title")  # 제목
        recruit_author = req_data.json.get("recruit_author")  # 글쓴이
        recruit_contents = req_data.json.get('recruit_contents')  # 내용
        recruit_tags = req_data.json.get('recruit_tags')  # tags
        recruit_state = req_data.json.get('recruit_state')  # 상태

        newpost_recruit = {'recruit_post_id': recruit_post_id, 'recruit_title': recruit_title,
                        'recruit_author': recruit_author, 'recruit_contents': recruit_contents,
                        'recruit_tags': recruit_tags, 'recruit_state': recruit_state}
        
        for k, v in newpost_recruit.items():
            if k != "recruit_tags" and v == None:
                raise Exception("Missing Parameter")
    # 전달받은 Body 중에 누락된 내용이 있다면 Exception 발생
    # 제목, 글쓸이, 내용, 상태는 누락될 수 없음
    except:
        return response_model.set_response(req_data.path, 200, "Missing Parameter", None)
    
    try:
        # mongoDB에 추가
        # post = db.[colletion_name] # Collection에 접근 후
        # post.insert_one(newpost_recruit).inserted_id  #한 개 저장
        post_db.insert(newpost_recruit)
        # 현재 게시물 번호 업데이트
        counter_db.update_one({"type": "recruit_post"}, {"$set": {"counter": recruit_post_id}})

        return response_model.set_response(req_data.path, 200, "Done", recruit_post_id)

    # DB 저장 중 오류 발생 시 Exception
    except:

        return response_model.set_response(req_data.path, 200, "DB save Failed", None)


def search_post(req_data, search_parse):

    def for_unit_search(search_method):
        try:
            # [전체] 에서 특정 단어가 들어간 경우를 찾는 경우
            # 특정 단어가 포함된 글을 찾기 위해서 .*[특정단어].* 형태로 만듬

            recruit_all = '.*' + search_parse.parse_args()['recruit_search_word'] + '.*'
            data = [doc for doc in
                            db_connector.mongo.db.recruit_post.find({search_method: {'$regex': recruit_all}})]
            return json.loads(json_util.dumps(data))

        except:
            # 아무것도 쓰지 않고 넘긴 경우
            data_all = [doc for doc in db_connector.mongo.db.recruit_post.find()]

            new_post_res = {
                "req_path": req_data.path,
                "req_result": "Fail",
                "result": json.loads(json_util.dumps(data_all))
            }
            return new_post_res

    search_method = req_data.args.get('recruit_search_method')

    # 게시물 전체 검색
    if search_method == 'all':
        try:
            # [전체] 에서 특정 단어가 들어간 경우를 찾는 경우
            # 특정 단어가 포함된 글을 찾기 위해서 .*[특정단어].* 형태로 만듬

            recruit_all = '.*' + search_parse.parse_args()['recruit_search_word'] + '.*'
            data = [doc for doc in
                        db_connector.mongo.db.recruit_post.find({"$or": [{"recruit_title": {'$regex': recruit_all}},
                                                                         {"recruit_author": {'$regex': recruit_all}},
                                                                         {"recruit_contents": {'$regex': recruit_all}},
                                                                         {"recruit_tags": {'$regex': recruit_all}},
                                                                         ]})]
            return json.loads(json_util.dumps(data))

        except:
            # 아무것도 쓰지 않고 넘긴 경우
            data_all = [doc for doc in db_connector.mongo.db.recruit_post.find()]

            new_post_res = {
                    "req_path": req_data.path,
                    "req_result": "Fail",
                    "result": json.loads(json_util.dumps(data_all))
            }
            return new_post_res

    # 글쓴이로 검색
    elif search_method == 'author':
        return for_unit_search("recruit_author")

    # 태그로 검색
    elif search_method == 'tags':
        return for_unit_search("recruit_tags")

    # 글 내용으로 검색
    elif search_method == 'contents':
        return for_unit_search("recruit_contents")

    # 제목으로 검색
    elif search_method == 'title':
        return for_unit_search("recruit_title")


def update_post(req_data):
    # 응답을 위한 Dict
    update_post_res = {}
    try:
        update_data = req_data.json  
        db_connector.mongo.db.recruit_post.update({"recruit_post_id": update_data["recruit_post_id"]}, update_data)
            
        update_post_res = {
            "req_path": req_data.path,
            "req_result": "Done"
        }

        return update_post_res

    except:
        update_post_res = {
            "req_path": req_data.path,
            "req_result": "Fail"
        } 
        return update_post_res