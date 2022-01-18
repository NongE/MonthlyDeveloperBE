from flask import request, redirect, jsonify
from flask_restx import Api, Resource, fields, Namespace

from model.board import recruit_model as model

from service.board import recruit_service

from decorator.token_validator import token_validator


# 팀 구인과 관련된 모델 선언
Recruit = model.RecruitModel()
recruit_ns = Recruit.recruit_ns

# 사용자의 토큰을 확인하기 위한 Parser
token_parse = Recruit.token_parse

# 특정 게시글을 검색하기 위한 Parser, Query Param 활용
search_parse = Recruit.search_parse

# 게시글 등록, 업데이트, 삭제를 위한 Model
recruit_post_model = Recruit.recruit_model
recruit_update_model = Recruit.recruit_update_model
recruit_delete_model = Recruit.recruit_delete_model


# 새로운 게시글 등록 (작성)
@recruit_ns.route('/new_post', methods=['POST'])
class RecruitCreate(Resource):
    @recruit_ns.expect(recruit_post_model)
    def post(self):
        return recruit_service.save_post(request)


# 게시글 검색
@recruit_ns.route('/search', methods=['GET'])
class RecruitSearch(Resource):
    @recruit_ns.expect(search_parse)
    def get(self):
        return recruit_service.search_post(request)
        

# 게시글 수정
@recruit_ns.route('/update', methods=['PUT'])
class RecruitUpdate(Resource):
    @recruit_ns.expect(recruit_update_model)
    def put(self):
        return recruit_service.update_post(request)
        

# 게시글 삭제
@recruit_ns.route('/delete', methods=['DELETE'])
class RecruitDelete(Resource):
    @token_validator
    @recruit_ns.expect(token_parse, recruit_delete_model)
    def delete(self):
        return recruit_service.delete_post(request)
