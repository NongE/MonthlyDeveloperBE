import json
from bson import json_util
from flask import request, redirect, jsonify
from flask_restx import Api, Resource, fields, Namespace, reqparse

from config import db_connector

Recruit = Namespace("Recruit post", description="for recruit")

introduce = Recruit.model('Introduce', {
    'recruit_title': fields.String(description='recruit title', required=True),
    'recruit_author': fields.String(description='recruit author', required=True),
    'recruit_contents': fields.String(description='recruit contents', required=True),
    'recruit_tags': fields.List(fields.String, description='recruit tags', required=False, default="asdf"),
    'recruit_state': fields.String(description='recruit state', required=True),
})

# 특정 게시글을 검색하기 위한 조건
search_parse = reqparse.RequestParser()
search_parse.add_argument("recruit_number", type=int, help="게시글 번호")
search_parse.add_argument("recruit_author", type=str, help="게시글 작성자")
search_parse.add_argument("recruit_tags", type=str, help="게시글 태그")
search_parse.add_argument("recruit_state", type=str, help="게시글 상태")


# 새로운 게시글 등록 (작성)
@Recruit.route('/new_post', methods=['POST'])
class RecruitPostCreate(Resource):
    @Recruit.expect(introduce)
    def post(self):

        # 응답을 위한 Dict
        new_post_res = {}

        # 게시글의 고유 아이디 정보
        # 게시글 고유 아이디는 게시글의 등록 순서를 의미
        # 현재 k번 게시글까지 있다고 가정하였을 때 새롭게 등록될 게시글은 k+1번째 게시글임
        counter_db = db_connector.mongo.db.counter
        recruit_post_number = counter_db.find_one({"type": "recruit_post"}, {"_id": 0})["counter"] + 1

        post_db = db_connector.mongo.db.recruit_post

        try:
            # 새 글 생성
            recruit_title = request.json.get("recruit_title")  # 제목
            recruit_author = request.json.get("recruit_author")  # 글쓴이
            recruit_contents = request.json.get('recruit_contents')  # 내용
            recruit_tags = request.json.get('recruit_tags')  # tags
            recruit_state = request.json.get('recruit_state')  # 상태

            newpost_recruit = {'recruit_post_number': recruit_post_number, 'recruit_title': recruit_title,
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
            counter_db.update_one({"type": "recruit_post"}, {"$set": {"counter": recruit_post_number}})

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
@Recruit.route('/search')
class RecruitPostSearch(Resource):
    @Recruit.expect(search_parse)
    def get(self):

        # 글쓴이로 글 찾기
        author = search_parse.parse_args()['recruit_author']
        if author is not None:
            data = [doc for doc in db_connector.mongo.db.recruit_post.find({'recruit_author': author})]
            return json.loads(json_util.dumps(data))

        # tags로 글 찾기

        # contents 들어가는 단어로 글 찾기

        # state로 글 찾기

        state = search_parse.parse_args()['recruit_state']
        if state is not None:
            data = [doc for doc in db_connector.mongo.db.recruit_post.find({'recruit_state': state})]
            return json.loads(json_util.dumps(data))
        # title로 글 찾기




# 게시글 수정
@Recruit.route('/update')
class RecruitPostUpdate(Resource):
    @Recruit.expect(introduce)
    def put(self, post_id):
        db_connector.mongo.db.recruit_post.update({"recruit_state": "구인중"}, {"$set": {"recruit_state": "구인완료"}})
        return "is RecruitPostRead"


# 게시글 삭제
@Recruit.route('/delete')
class RecruitPostDelete(Resource):
    @Recruit.expect(introduce)
    def delete(self, post_id):
        db_connector.mongo.db.recruit_post.delete_one({"recruit_state": "구인중"})
        return "is RecruitPostDelete"
