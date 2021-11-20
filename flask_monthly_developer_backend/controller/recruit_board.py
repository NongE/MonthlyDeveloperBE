import json
from bson import json_util
from flask import request, redirect, jsonify
from flask_restx import Api, Resource, fields, Namespace

from config import db_connector
from model import recruit_post_model as model

# 팀 구인과 관련된 모델 선언
Recruit = model.RecruitPostModel()
recruit_ns = Recruit.recruit_ns
recruit_post_model = Recruit.recruit_post_model

# 특정 게시글을 검색하기 위한 조건, Query Param 활용
search_parse = Recruit.search_parse

# 새로운 게시글 등록 (작성)
@recruit_ns.route('/new_post', methods=['POST'])
class RecruitPostCreate(Resource):
    @recruit_ns.expect(recruit_post_model)
    def post(self):

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
            recruit_title = request.json.get("recruit_title")  # 제목
            recruit_author = request.json.get("recruit_author")  # 글쓴이
            recruit_contents = request.json.get('recruit_contents')  # 내용
            recruit_tags = request.json.get('recruit_tags')  # tags
            recruit_state = request.json.get('recruit_state')  # 상태

            newpost_recruit = {'recruit_post_id': recruit_post_id, 'recruit_title': recruit_title,
                            'recruit_author': recruit_author, 'recruit_contents': recruit_contents,
                            'recruit_tags': recruit_tags, 'recruit_state': recruit_state}
            
            for k, v in newpost_recruit.items():
                if k != "recruit_tags" and v == None:
                    raise Exception("Missing Parameter")

        # 전달받은 Body 중에 누락된 내용이 있다면 Exception 발생
        # 제목, 글쓸이, 내용, 상태는 누락될 수 없음
        except:
            new_post_res = {
                "req_path": request.path,
                "req_result": "Missing Parameter"
            }
            return new_post_res

        try:
            # mongoDB에 추가
            # post = db.[colletion_name] # Collection에 접근 후
            # post.insert_one(newpost_recruit).inserted_id  #한 개 저장
            post_db.insert(newpost_recruit)

            # 현재 게시물 번호 업데이트
            counter_db.update_one({"type": "recruit_post"}, {"$set": {"counter": recruit_post_id}})

            new_post_res = {
                "req_path": request.path,
                "req_result": "Done"
            }

            return new_post_res
        # DB 저장 중 오류 발생 시 Exception
        except:
            new_post_res = {
                "req_path": request.path,
                "req_result": "Fail"
            }
            return new_post_res


# 게시글 검색
@recruit_ns.route('/search', methods = ['GET'])
class RecruitPostSearch(Resource):
    @recruit_ns.expect(search_parse)
    def get(self):

        try:
            # [전체] 에서 특정 단어가 들어간 경우를 찾는 경우
            # 특정 단어가 포함된 글을 찾기 위해서 .*[특정단어].* 형태로 만듬

            recruit_all = '.*' + search_parse.parse_args()['recruit_all'] + '.*'
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
                "req_path": request.path,
                "req_result": "No word",
                "result": json.loads(json_util.dumps(data_all))
            }
            return new_post_res

        # 글쓴이로 글 찾기

        # tags로 글 찾기

        # contents 글 찾기

        # state로 글 찾기

        # title로 글 찾기


# 게시글 수정
@recruit_ns.route('/update/<int:recruit_post_id>')
class RecruitPostUpdate(Resource):
    @recruit_ns.expect(recruit_post_model)
    def put(self, recruit_post_id):

        # 응답을 위한 Dict
        update_post_res = {}
        try:
            update_data = request.json
            update_data["recruit_post_id"] = recruit_post_id
            
            db_connector.mongo.db.recruit_post.update({"recruit_post_id": recruit_post_id}, update_data)

            update_post_res = {
                "req_path": request.path,
                "req_result": "Done"
            }

            return update_post_res
        except:
            update_post_res = {
                "req_path": request.path,
                "req_result": "Fail"
            } 
            return update_post_res


# 게시글 삭제
@recruit_ns.route('/delete')
class RecruitPostDelete(Resource):
    @recruit_ns.expect(recruit_post_model)
    def delete(self, post_id):
        db_connector.mongo.db.recruit_post.delete_one({"recruit_state": "구인중"})
        return "is RecruitPostDelete"
