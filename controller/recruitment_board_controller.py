from flask import request, redirect, jsonify
from flask_restx import Api, Resource, fields, Namespace

from model.recruitment_borad_model import RecruitmentBoardModel

from service.recruitment_board_service import RecruitmentBoardService

from decorator.token_validator import token_validator


# 팀 구인과 관련된 모델 선언
RecruitmentBoardModel = RecruitmentBoardModel()
recruitment_ns = RecruitmentBoardModel.recruitment_borad_ns

# 사용자의 토큰을 확인하기 위한 Parser
token_parse = RecruitmentBoardModel.token_parse

# 게시글 등록을 위한 Model
recruit_post_model = RecruitmentBoardModel.create_post_model

# # 특정 게시글을 검색하기 위한 Parser, Query Param 활용
# search_parse = RecruitmentBoardModel.search_parse
#
# # 게시글 등록, 업데이트, 삭제를 위한 Model
# recruit_post_model = RecruitmentBoardModel.recruit_model
# recruit_update_model = RecruitmentBoardModel.recruit_update_model
# recruit_delete_model = RecruitmentBoardModel.recruit_delete_model

recruitment_board_service = RecruitmentBoardService()


# 새로운 게시글 등록 (작성)
@recruitment_ns.route('/create_post', methods=['POST'])
class CreatePost(Resource):
    @recruitment_ns.expect(token_parse, recruit_post_model)
    def post(self):
        return recruitment_board_service.create_post(request)

#
# # 게시글 검색
# @recruitment_ns.route('/search', methods=['GET'])
# class RecruitmentSearch(Resource):
#     @recruitment_ns.expect(search_parse)
#     def get(self):
#         return recruitment_service.search_post(request)
#
#
# # 게시글 수정
# @recruitment_ns.route('/update', methods=['PUT'])
# class RecruitmentUpdate(Resource):
#     @recruitment_ns.expect(recruit_update_model)
#     def put(self):
#         return recruitment_service.update_post(request)
#
#
# # 게시글 삭제
# @recruitment_ns.route('/delete', methods=['DELETE'])
# class RecruitmentDelete(Resource):
#     @recruitment_ns.expect(token_parse, recruit_delete_model)
#     def delete(self):
#         return recruitment_service.delete_post(request)
