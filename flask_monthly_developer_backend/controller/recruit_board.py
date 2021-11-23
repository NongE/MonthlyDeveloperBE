import json

from flask import request, redirect, jsonify
from flask_restx import Api, Resource, fields, Namespace

from model import recruit_post_model as model

from service import recruit_service

# 팀 구인과 관련된 모델 선언
Recruit = model.RecruitPostModel()
recruit_ns = Recruit.recruit_ns
recruit_post_model = Recruit.recruit_post_model

<<<<<<< HEAD
# 특정 게시글을 검색하기 위한 조건, Query Param 활용
search_parse = Recruit.search_parse
=======
# 특정 게시글을 검색하기 위한 조건
search_parse = reqparse.RequestParser()
search_parse.add_argument("recruit_search_method", type=str, help="게시글 찾는 방법")
search_parse.add_argument("recruit_search_word", type=str, help="게시글 단어")

>>>>>>> upstream/main

# 새로운 게시글 등록 (작성)
@recruit_ns.route('/new_post', methods=['POST'])
class RecruitPostCreate(Resource):
    @recruit_ns.expect(recruit_post_model)
    def post(self):
        return recruit_service.save_post(request)


# 게시글 검색
@recruit_ns.route('/search', methods = ['GET'])
class RecruitPostSearch(Resource):
    @recruit_ns.expect(search_parse)
    def get(self):

        search_method = request.args.get('recruit_search_method')

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
                    "req_path": request.path,
                    "req_result": "Fail",
                    "result": json.loads(json_util.dumps(data_all))
                }
                return new_post_res

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
                    "req_path": request.path,
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

# 게시글 수정
@recruit_ns.route('/update/<int:recruit_post_id>', methods=['PUT'])
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
@recruit_ns.route('/delete', methods=['DELETE'])
class RecruitPostDelete(Resource):
    @recruit_ns.expect(recruit_post_model)
    def delete(self, post_id):
        db_connector.mongo.db.recruit_post.delete_one({"recruit_state": "구인중"})
        return "is RecruitPostDelete"
