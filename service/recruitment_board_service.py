from flask import request

from config.connector import Connector
from model.response_model import ResponseModel
from service.token_service import TokenService


class RecruitmentBoardService:

    # DB 연결에 필요한 설정
    def __init__(self) -> None:
        self.mongodb_connector = Connector.mongodb_connector()
        self.counter_db = self.mongodb_connector.counter
        self.post_db = self.mongodb_connector.recruitment_board

    # 게시글 저장
    def create_post(self, req_data: request) -> dict:
        # 전달 받은 토큰에서 유저 정보를 가져옴
        user_token = request.headers["Header"]
        user_info = TokenService.get_user(user_token)

        # 유저 권한이 사용자일 때만 글 작성이 가능
        # 예) 게스트(guest)는 글 작성 불가능
        if user_info["role"] == "user":
            # 게시글의 고유 아이디로 쓰일 아이디 정의 (게시글의 등록 순서대로 부여, auto_increment)
            # 현재 k번 게시글까지 있다고 가정 하였을 때 새롭게 등록될 게시글은 k+1번째 게시글임
            post_id = self.counter_db.find_one({"type": "recruitment_board"}, {"_id": 0})["counter"] + 1

            # 게시글 저장 전, 일부 데이터 추가
            post_data = req_data.json
            # 1. 앞에서 가져온 게시글 고유 아이디
            post_data["post_id"] = post_id
            # 2. 게시글 작성자를 구분 할 작성자의 github id
            user_github_id = user_info["github_id"]
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

    # 특정 게시글 조회
    def read_post(self, req_data, post_id):
        # 전달 받은 토큰에서 유저 정보를 가져옴
        user_token = req_data.headers["Header"]
        user_info = TokenService.get_user(user_token)

        # 특정 게시글 조회는 회원만 조회가 가능
        if user_info["role"] == "user":

            # 요청 받은 게시글 번호에 해당하는 게시글 조회
            data = self.post_db.find_one({"post_id": int(post_id)}, {"_id": 0})

            # 결과가 없다면 잘못된 번호를 전달 받은 케이스
            if data is not None:
                return ResponseModel.set_response(req_data.path, 200, "Done", data)
            else:
                return ResponseModel.set_response(req_data.path, 200, "Incorrect Post ID", None)
        else:
            return ResponseModel.set_response(req_data.path, 200, "Permission Denied", None)

    # 게시글 목록 조회
    # 게시글 목록 조회의 경우 회원 권한이 없어도 조회 가능
    def read_post_list(self, req_data):

        # 사용 가능한 검색 방식 리스트
        search_method_list = ("all", "title", "author", "contents", "tags")

        # DB 상에 조회한 데이터를 저장할 리스트
        data = []

        # 전달받은 Query String을 확인하며 조회 방법, 범위를 파악함

        # 1. 검색 방법 확인 (전체 검색, 제목 검색 등)
        try:
            search_method = req_data.args["search_method"]
        except:
            search_method = None

        # 2. 검색하고자 하는 단어 확인 (자바, 개발자 등)
        try:
            search_word = req_data.args['search_keyword']
        except:
            search_word = None

        # 3. 검색 하고자 하는 범위 확인
        #    기본적 10개(1~10번 게시글) 단위로 조회 가능 (1~10번 게시글, 11~20번 게시글 등)\
        #    사용자가 잘못된 값(0, 음수, 값이 없을 경우 등)을 전달 했을 때 1로 초기화
        try:
            search_page = int(req_data.args['page'])

            if search_page <= 0:
                search_page = 1
        except:
            search_page = 1

        # 전달받은 Query String 중 검색 방식에 따라 동작을 진행
        # 1. 검색 방식과 검색 단어가 모두 없다 -> 전체 게시글 조회 (find all)
        if (search_method is None) and (search_word is None):
            return self.for_unit_search(None, search_word, search_page)

        # 2. 검색 방식과 검색 단어 중 하나라도 없다 -> 검색 불가
        elif (search_method is None) or (search_word is None):
            return ResponseModel.set_response(req_data.path, 200, "Fail",
                                              "Missing search_method or search_word Parameter")

        # 3. 전달받은 검색 방법이 지원하는(유효한) 방식인지 확인
        elif search_method in search_method_list:
            search_word = '.*' + search_word + '.*'

        # 3-1. 전달받은 검색 방식이 지원하지 않는 경우("all", "author", "tags", "contents", "title" 이 외) Fail
        else:
            return ResponseModel.set_response(req_data.path, 200, "Fail", "Unknown search_method")

        # 이후 검색 시작
        # 1. 전체 범위 검색
        if search_method == "all":
            data = self.for_unit_search("all", search_word, search_page)

        # 2. 글쓴이로 검색
        elif search_method == 'author':
            data = self.for_unit_search("author", search_word, search_page)

        # 3. 태그로 검색
        elif search_method == 'tags':
            data = self.for_unit_search("tags", search_word, search_page)

        # 4. 글 내용으로 검색
        elif search_method == 'contents':
            data = self.for_unit_search("contents", search_word, search_page)

        # 5. 제목으로 검색
        elif search_method == 'title':
            data = self.for_unit_search("title", search_word, search_page)

        return ResponseModel.set_response(req_data.path, 200, "Done", data)

    # 게시글 조회 시 사용 되는 함수
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

    # 게시글 수정
    def update_post(self, req_data):
        # 전달 받은 토큰에서 유저 정보를 가져옴
        user_token = req_data.headers["Header"]
        user_info = TokenService.get_user(user_token)

        # 수정 될 새로운 데이터
        new_data = req_data.json

        # 수정 될 기존 데이터를 DB에서 가져옴
        data_before_update = self.post_db.find_one({"post_id": new_data["post_id"]}, {"_id": 0})

        # 데이터에 대해 수정 권한이 있는지 확인
        # 1. 기존 데이터에 저장되어 있는 github_id와 전달받은 토큰에서 github_id를 비교
        # 2. 동일하다면 게시글 수정(교체) 작업 진행
        if user_info["github_id"] == data_before_update["github_id"]:
            new_data["github_id"] = user_info["github_id"]
            self.post_db.replace_one({"post_id": new_data["post_id"]}, new_data, upsert=True)
            return ResponseModel.set_response(req_data.path, 200, "Done", new_data["post_id"])
        else:
            return ResponseModel.set_response(req_data.path, 200, "Permission Denied", None)

    # 게시글 삭제
    def delete_post(self, req_data):
        # 전달 받은 토큰에서 유저 정보를 가져옴
        user_token = req_data.headers["Header"]
        user_info = TokenService.get_user(user_token)

        # 삭제하고자 하는 데이터
        delete_data = req_data.json

        # 삭제하고자 하는 게시글을 DB에서 가져옴
        data_delete_request = self.post_db.find_one({"post_id": delete_data["post_id"]}, {"_id": 0})

        # 데이터 삭제 권한이 있는지 확인
        # 1. 삭제하고자 하는 데이터가 있는지(유효한지) 확인
        # 2. 기존 데이터에 저장되어 있는 github_id와 전달받은 토큰에서 github_id를 비교
        # 3. 동일하다면 게시글 삭제
        if data_delete_request is not None:
            if user_info["github_id"] == data_delete_request["github_id"]:
                delete_result = self.post_db.delete_one({"post_id": delete_data["post_id"]})
                return ResponseModel.set_response(req_data.path, 200, "Done", f"{delete_data['post_id']}")
            else:
                return ResponseModel.set_response(req_data.path, 200, "Fail", f"Permission Error")
        else:
            return ResponseModel.set_response(req_data.path, 200, "Fail", f"Incorrect Post ID: {delete_data['post_id']}")