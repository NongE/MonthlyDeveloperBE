from flask import request, redirect, jsonify
from flask_restx import Api, Resource, fields, Namespace

from model import recruit_post_model as model

from service import recruit_service

from controller.token_require import token_require


# 팀 구인과 관련된 모델 선언
Recruit = model.RecruitPostModel()
recruit_ns = Recruit.recruit_ns
user_token = Recruit.user_token
recruit_post_model = Recruit.recruit_post_model
recruit_update_post_model = Recruit.recruit_update_post_model
recruit_delete_post_model = Recruit.recruit_delete_post_model

# 특정 게시글을 검색하기 위한 조건, Query Param 활용
search_parse = Recruit.search_parse


# 새로운 게시글 등록 (작성)
@recruit_ns.route('/new_post', methods=['POST'])
class RecruitPostCreate(Resource):
    @recruit_ns.expect(recruit_post_model)
    def post(self):
        return recruit_service.save_post(request)


# 게시글 검색
@recruit_ns.route('/search', methods=['GET'])
class RecruitPostSearch(Resource):
    @recruit_ns.expect(search_parse)
    def get(self):
        return recruit_service.search_post(request)
        

# 게시글 수정
@recruit_ns.route('/update', methods=['PUT'])
class RecruitPostUpdate(Resource):
    @recruit_ns.expect(recruit_update_post_model)
    def put(self):
        return recruit_service.update_post(request)
        

# 게시글 삭제
@recruit_ns.route('/delete', methods=['DELETE'])
class RecruitPostDelete(Resource):
    @token_require
    @recruit_ns.doc(body = recruit_delete_post_model, parser=user_token)
    def delete(self):
        return recruit_service.delete_post(request)
