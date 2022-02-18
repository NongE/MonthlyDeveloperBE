from flask import request

from config.connector import Connector
from model.response_model import ResponseModel
from service.token_service import TokenService


class RecruitmentBoardService:

    def __init__(self) -> None:
        self.mongodb_connector = Connector.mongodb_connector()
        self.counter_db = self.mongodb_connector.counter
        self.post_db = self.mongodb_connector.recruitment_board

    def create_post(self, req_data: request) -> dict:

        user_token = request.headers["Header"]
        user_info = TokenService.get_user(user_token)

        if user_info["role"] == "user":
            # DB 연결

            # 게시글의 고유 아이디로 쓰일 아이디 선언 (게시글의 등록 순서대로 부여, auto_increment)
            # 현재 k번 게시글까지 있다고 가정하였을 때 새롭게 등록될 게시글은 k+1번째 게시글임
            post_id = self.counter_db.find_one({"type": "recruitment_board"}, {"_id": 0})["counter"] + 1

            # 전달받은 데이터에 게시글 아이디를 추가
            user_github_id = user_info["github_id"]

            post_data = req_data.json
            post_data["post_id"] = post_id
            post_data["github_id"] = user_github_id

            try:
                # 데이터를 DB에 저장
                self.post_db.insert_one(post_data)

                # 현재 게시물 번호 업데이트
                self.counter_db.update_one({"type": "recruitment_board"}, {"$set": {"counter": post_id}})

                return ResponseModel.set_response(req_data.path, 200, "Done", post_id)

            # DB 저장 중 오류 발생 시 Exception
            except:
                return ResponseModel.set_response(req_data.path, 200, "DB save Failed", None)
        else:
            return ResponseModel.set_response(req_data.path, 200, "Permission Denied", None)

    def read_post(self, req_data, post_id):
        user_token = req_data.headers["Header"]
        user_info = TokenService.get_user(user_token)

        if user_info["role"] == "user":
            data = self.post_db.find_one({"post_id": int(post_id)}, {"_id": 0})

            if data is not None:
                return ResponseModel.set_response(req_data.path, 200, "Done", data)
            else:
                return ResponseModel.set_response(req_data.path, 200, "Incorrect Post ID", None)
        else:
            return ResponseModel.set_response(req_data.path, 200, "Permission Denied", None)

    def read_post_list(self, req_data):
        # 검색 범위, 검색 단어를 전달 받음
        # 이후 범위에 해당 하는 단어를 포함하는 게시물 출력

        # 사용 가능한 검색 방식 리스트
        search_method_list = ("all", "title", "author", "contents", "tags")
        # DB 상에 조회한 데이터를 저장할 리스트
        data = []

        # Query String 전달 받은 검색 방법 확인
        try:
            search_method = req_data.args["search_method"]
        except:
            search_method = None

        # Query String 전달 받은 검색 단어 확인
        try:
            search_word = req_data.args['search_keyword']
        except:
            search_word = None

        # Query String 전달 받은 검색 페이지(페이지 당 10개의 데이터)
        try:
            search_page = int(req_data.args['page'])
        except:
            search_page = None

        # 사용자가 page 단위에 0 혹은 음수를 집어 넣는 경우
        # 강제로 1로 초기화
        if search_page <= 0:
            search_page = 1

        # 검색 방식과 검색 단어가 모두 없다 -> 전체 게시글 조회 (find all)
        if (search_method is None) and (search_word is None):
            return self.for_unit_search(None, search_word, search_page)

        # 검색 방식과 검색 단어 중 하나라도 없다 -> 검색 불가
        elif (search_method is None) or (search_word is None):
            return ResponseModel.set_response(req_data.path, 200, "Fail",
                                              "Missing search_method or search_word Parameter")

        # 이 외에는 지원하는 검색 방식인지 검증
        elif search_method in search_method_list:
            search_word = '.*' + search_word + '.*'

        # 전달받은 검색 방식이 "all", "author", "tags", "contents", "title"
        # 중 해당하는 내용이 없다면 Fail
        else:
            return ResponseModel.set_response(req_data.path, 200, "Fail", "Unknown search_method")

        # 전체 범위 검색
        if search_method == "all":
            data = self.for_unit_search("all", search_word, search_page)

        # 글쓴이로 검색
        elif search_method == 'author':
            data = self.for_unit_search("author", search_word, search_page)

        # 태그로 검색
        elif search_method == 'tags':
            data = self.for_unit_search("tags", search_word, search_page)

        # 글 내용으로 검색
        elif search_method == 'contents':
            data = self.for_unit_search("contents", search_word, search_page)

        # 제목으로 검색
        elif search_method == 'title':
            data = self.for_unit_search("title", search_word, search_page)

        return ResponseModel.set_response(req_data.path, 200, "Done", data)

    def for_unit_search(self, search_method, search_word, search_page):
        # 전체 조회
        if search_method is None:
            data = self.post_db.find({}, {"_id": 0}).skip((search_page - 1) * 10).limit(
                10)
            data = [doc for doc in data]

        # 전체 범위에 대해 검색 (제목 ~ 태그)
        elif search_method == 'all':
            data = self.post_db.find({"$or": [{"title": {'$regex': search_word}},
                                              {"author": {'$regex': search_word}},
                                              {"contents": {'$regex': search_word}},
                                              {"tags": {'$regex': search_word}}]},
                                              {"_id": 0}).skip((search_page - 1) * 10).limit(10)
            data = [doc for doc in data]
        # 특정 범위에 대해 검색(제목, 작성자 등)
        else:
            data = self.post_db.find({search_method: {'$regex': search_word}}, {"_id": 0})\
                                .skip((search_page - 1) * 10)\
                                .limit(10)
            data = [doc for doc in data]
        return data

    def update_post(self, req_data):
        user_token = req_data.headers["Header"]
        user_info = TokenService.get_user(user_token)

        new_data = req_data.json

        data_before_update = self.post_db.find_one({"post_id": new_data["post_id"]}, {"_id": 0})

        if user_info["github_id"] == data_before_update["github_id"]:
            new_data["github_id"] = user_info["github_id"]
            self.post_db.replace_one({"post_id": new_data["post_id"]}, new_data, upsert=True)
            return ResponseModel.set_response(req_data.path, 200, "Done", new_data["post_id"])
        else:
            return ResponseModel.set_response(req_data.path, 200, "Permission Denied", None)

    def delete_post(self, req_data):
        # 기존 게시글 삭제
        # 삭제하고자 하는 게시글의 번호를 전달 받아 삭제
        try:
            delete_data = req_data.json

            delete_result = self.post_db.delete_one({"post_id": delete_data["post_id"]})

            if delete_result.deleted_count == 0:
                return ResponseModel.set_response(req_data.path, 200, "Fail", f"Incorrect Post ID: {delete_data['post_id']}")
            else:
                return ResponseModel.set_response(req_data.path, 200, "Done", delete_data["post_id"])
        except Exception as e:
            return ResponseModel.set_response(req_data.path, 200, "Fail", None)
