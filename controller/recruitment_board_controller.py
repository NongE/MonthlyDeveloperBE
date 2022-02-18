from flask import request
from flask_restx import Resource

from model.recruitment_borad_model import RecruitmentBoardModel

from service.recruitment_board_service import RecruitmentBoardService

from decorator.token_validator import token_validator


# 팀 구인과 관련된 모델 선언
RecruitmentBoardModel = RecruitmentBoardModel()
recruitment_ns = RecruitmentBoardModel.recruitment_board_ns

# 사용자 토큰을 확인 하기 위한 Parser
token_parse = RecruitmentBoardModel.token_parse

# 게시글 등록을 위한 Model
create_post_model = RecruitmentBoardModel.create_post_model

# 게시글 검색을 위한 Model
read_post_parser = RecruitmentBoardModel.read_post_parser

# 게시글 업데이트를 위한 Model
update_post_model = RecruitmentBoardModel.update_post_model

# 게시글 삭제를 위한 Model
delete_post_model = RecruitmentBoardModel.delete_post_model

# 게시글 CRUD와 관련된 서비스
recruitment_board_service = RecruitmentBoardService()


# 새로운 게시글 등록 (작성)
@recruitment_ns.route('/create_post', methods=['POST'])
class CreatePost(Resource):
    @token_validator
    @recruitment_ns.expect(token_parse, create_post_model)
    def post(self) -> dict:
        return recruitment_board_service.create_post(request)


# 게시글 목록 검색
@recruitment_ns.route('/search', methods=['GET'])
class ReadPostList(Resource):
    @recruitment_ns.expect(read_post_parser)
    def get(self):
        return recruitment_board_service.read_post_list(request)


# 특정 게시물(게시물 번호) 검색
@recruitment_ns.route('/search/<post_id>', methods=['GET'])
class ReadPost(Resource):
    @token_validator
    @recruitment_ns.expect(token_parse)
    def get(self, post_id=None):
        return recruitment_board_service.read_post(request, post_id)


# 게시글 수정
@recruitment_ns.route('/update', methods=['PUT'])
class RecruitmentUpdate(Resource):
    @token_validator
    @recruitment_ns.expect(token_parse, update_post_model)
    def put(self):
        return recruitment_board_service.update_post(request)


# 게시글 삭제
@recruitment_ns.route('/delete', methods=['DELETE'])
class RecruitmentDelete(Resource):
    @token_validator
    @recruitment_ns.expect(token_parse, delete_post_model)
    def delete(self):
        return recruitment_board_service.delete_post(request)
