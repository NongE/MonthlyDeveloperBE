import json
from bson import json_util
from flask import jsonify

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

    # 검색 범위, 검색 단어를 전달받음
    # 이후 범위에 해당 하는 단어를 포함하는 게시물 출력
    def for_unit_search(search_method, search_word):

        # 전체 조회
        if search_method == None:
            data = [doc for doc in db_connector.mongo.db.recruit_post.find({}, {"_id":0})]

        # 전체 범위에 대해 검색 (제목 ~ 태그)
        elif search_method == 'all':
            data = [doc for doc in
                    db_connector.mongo.db.recruit_post.find({"$or": [{"recruit_title": {'$regex': search_word}},
                                                                     {"recruit_author": {'$regex': search_word}},
                                                                     {"recruit_contents": {'$regex': search_word}},
                                                                     {"recruit_tags": {'$regex': search_word}},
                                                                     ]}, {"_id":0})]
        # 특정 범위에 대해 (제목, 작성자 등)
        else:
            data = [doc for doc in
                            db_connector.mongo.db.recruit_post.find({search_method: {'$regex': search_word}}, {"_id":0})]
        
        return response_model.set_response(req_data.path, 200, "Done", data)

    # 사용 가능한 검색 방식 리스트
    search_method_list = ["all", "author", "tags", "contents", "title"]

    # Query String으로 검색하고자 하는 범위와 단어를 전달 받음
    search_method = req_data.args.get('recruit_search_method')
    search_word = search_parse.parse_args()['recruit_search_word']

    # 검색 방식과 검색 단어가 모두 없다 -> 전체 게시글 조회 (find all)
    if (search_method == None) and (search_parse.parse_args()['recruit_search_word'] == None):
        return for_unit_search(None, search_word)

    # 검색 방식과 검색 단어 중 하나라도 없다 -> 검색 불가
    elif (search_method == None) or (search_parse.parse_args()['recruit_search_word'] == None):
        return response_model.set_response(req_data.path, 200, "Fail", "Missing search_method or search_word Parameter")
    
    # 검색 방식 검증
    elif search_method in search_method_list:
        search_word = '.*' + search_word + '.*'
    # 
    else:
        return response_model.set_response(req_data.path, 200, "Fail", "Unknown search_method")
    
    # 전체 범위 검색
    if search_method == "all":
        return for_unit_search("all", search_word)

    # 글쓴이로 검색
    elif search_method == 'author':
        return for_unit_search("recruit_author", search_word)

    # 태그로 검색
    elif search_method == 'tags':
        return for_unit_search("recruit_tags", search_word)

    # 글 내용으로 검색
    elif search_method == 'contents':
        return for_unit_search("recruit_contents", search_word)

    # 제목으로 검색
    elif search_method == 'title':
        return for_unit_search("recruit_title", search_word)

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