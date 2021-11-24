from flask import request, redirect, jsonify
from flask_restx import Api, Resource, fields, Namespace

from model import recruit_post_model as model

from service import recruit_service

# 팀 구인과 관련된 모델 선언
Recruit = model.RecruitPostModel()
recruit_ns = Recruit.recruit_ns
recruit_post_model = Recruit.recruit_post_model
recruit_update_post_model = Recruit.recruit_update_post_model

# 특정 게시글을 검색하기 위한 조건, Query Param 활용
search_parse = Recruit.search_parse

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
        return recruit_service.search_post(request, search_parse)
        

# 게시글 수정
@recruit_ns.route('/update', methods=['PUT'])
class RecruitPostUpdate(Resource):
    @recruit_ns.expect(recruit_update_post_model)
    def put(self):
        return recruit_service.update_post(request)
        

# 게시글 삭제
@recruit_ns.route('/delete', methods=['DELETE'])
class RecruitPostDelete(Resource):
    @recruit_ns.expect(recruit_post_model)
    def delete(self, post_id):
        db_connector.mongo.db.recruit_post.delete_one({"recruit_state": "구인중"})
        return "is RecruitPostDelete"
