from flask import request

from config.connector import Connector
from model.response_model import ResponseModel


class RecruitmentBoardService:

    def __init__(self) -> None:
        self.mongodb_connector = Connector.mongodb_connector()
        pass

    def create_post(self, req_data: request) -> dict:
        # DB 연결
        counter_db = self.mongodb_connector.counter
        post_db = self.mongodb_connector.recruitment_board

        # 게시글의 고유 아이디로 쓰일 아이디 선언 (게시글의 등록 순서대로 부여, auto_increment)
        # 현재 k번 게시글까지 있다고 가정하였을 때 새롭게 등록될 게시글은 k+1번째 게시글임
        post_id = counter_db.find_one({"type": "recruitment_board"}, {"_id": 0})["counter"] + 1

        # 전달받은 데이터에 게시글 아이디를 추가
        post_data = req_data.json
        post_data["post_id"] = post_id

        try:
            # 데이터를 DB에 저장
            post_db.insert_one(post_data)

            # 현재 게시물 번호 업데이트
            counter_db.update_one({"type": "recruitment_board"}, {"$set": {"counter": post_id}})

            return ResponseModel.set_response(req_data.path, 200, "Done", post_id)

        # DB 저장 중 오류 발생 시 Exception
        except:
            return ResponseModel.set_response(req_data.path, 200, "DB save Failed", None)


    # def search_post(req_data):
    #     # 검색 범위, 검색 단어를 전달받음
    #     # 이후 범위에 해당 하는 단어를 포함하는 게시물 출력
    #     def for_unit_search(search_method, search_word, search_page):
    #
    #         # 전체 조회
    #         if search_method is None:
    #             data = Connector.mongodb_connector().recruit_post.find({}, {"_id": 0}).skip((search_page - 1) * 10).limit(10)
    #             data = [doc for doc in data]
    #
    #         # 전체 범위에 대해 검색 (제목 ~ 태그)
    #         elif search_method == 'all':
    #             data = Connector.mongodb_connector().recruit_post.find({"$or": [{"recruit_title": {'$regex': search_word}},
    #                                                                 {"recruit_author": {'$regex': search_word}},
    #                                                                 {"recruit_contents": {'$regex': search_word}},
    #                                                                 {"recruit_tags": {'$regex': search_word}},
    #                                                                 ]}, {"_id": 0}).skip((search_page - 1) * 10).limit(10)
    #             data = [doc for doc in data]
    #         # 특정 범위에 대해 검색(제목, 작성자 등)
    #         else:
    #             data = Connector.mongodb_connector().recruit_post.find({search_method: {'$regex': search_word}}, {"_id": 0}).skip(
    #                 (search_page - 1) * 10).limit(10)
    #             data = [doc for doc in data]
    #
    #         return ResponseModel.set_response(req_data.path, 200, "Done", data)
    #
    #     # 사용 가능한 검색 방식 리스트
    #     search_method_list = ["all", "title", "author", "contents", "tags"]
    #
    #     # Query String으로 검색하고자 하는 범위와 단어를 전달 받음
    #     try:
    #         search_method = req_data.args["search_method"]
    #     except:
    #         search_method = None
    #
    #     try:
    #         search_word = req_data.args['search_keyword']
    #     except:
    #         search_word = None
    #
    #     try:
    #         search_page = int(req_data.args['page'])
    #     except:
    #         search_page = None
    #
    #     # 사용자가 page 단위에 0 혹은 음수를 집어 넣는 경우
    #     # 강제로 1로 초기화
    #     if search_page <= 0:
    #         search_page = 1
    #
    #     # 검색 방식과 검색 단어가 모두 없다 -> 전체 게시글 조회 (find all)
    #     if (search_method is None) and (search_word is None):
    #         return for_unit_search(None, search_word, search_page)
    #
    #     # 검색 방식과 검색 단어 중 하나라도 없다 -> 검색 불가
    #     elif (search_method is None) or (search_word is None):
    #         return ResponseModel.set_response(req_data.path, 200, "Fail", "Missing search_method or search_word Parameter")
    #
    #     # 이 외에는 지원하는 검색 방식인지 검증
    #     elif search_method in search_method_list:
    #         search_word = '.*' + search_word + '.*'
    #
    #     # 전달받은 검색 방식이 "all", "author", "tags", "contents", "title"
    #     # 중 해당하는 내용이 없다면 Fail
    #     else:
    #         return ResponseModel.set_response(req_data.path, 200, "Fail", "Unknown search_method")
    #
    #     # 전체 범위 검색
    #     if search_method == "all":
    #         return for_unit_search("all", search_word, search_page)
    #
    #     # 글쓴이로 검색
    #     elif search_method == 'author':
    #         return for_unit_search("recruit_author", search_word, search_page)
    #
    #     # 태그로 검색
    #     elif search_method == 'tags':
    #         return for_unit_search("recruit_tags", search_word, search_page)
    #
    #     # 글 내용으로 검색
    #     elif search_method == 'contents':
    #         return for_unit_search("recruit_contents", search_word, search_page)
    #
    #     # 제목으로 검색
    #     elif search_method == 'title':
    #         return for_unit_search("recruit_title", search_word, search_page)
    #
    # def update_post(req_data):
    #     # 기존 게시글 수정
    #     # 수정하려는 게시글의 번호와 내용을 전달받음
    #     try:
    #         update_data = req_data.json
    #         Connector.mongodb_connector().recruit_post.update({"recruit_post_id": update_data["recruit_post_id"]}, update_data)
    #         return ResponseModel.set_response(req_data.path, 200, "Done", update_data["recruit_post_id"])
    #
    #     except:
    #         return ResponseModel.set_response(req_data.path, 200, "Fail", None)
    #
    #
    # def delete_post(req_data):
    #     # 기존 게시글 삭제
    #     # 삭제하고자 하는 게시글의 번호를 전달 받아 삭제
    #     try:
    #         delete_data = req_data.json
    #         delete_result = Connector.mongodb_connector().recruit_post.delete_one({"recruit_post_id": delete_data["recruit_post_id"]})
    #
    #         if delete_result.deleted_count == 0:
    #             return ResponseModel.set_response(req_data.path, 200, "Fail", f"No recruit_post_id: {delete_data['recruit_post_id']}")
    #         else:
    #             return ResponseModel.set_response(req_data.path, 200, "Done", delete_data["recruit_post_id"])
    #     except Exception as e:
    #         print(e)
    #         return ResponseModel.set_response(req_data.path, 200, "Fail", None)
