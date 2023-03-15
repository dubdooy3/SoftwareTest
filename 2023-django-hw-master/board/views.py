import json
from django.http import HttpRequest, HttpResponse

from board.models import Board, User
from utils.utils_request import BAD_METHOD, request_failed, request_success, return_field
from utils.utils_require import MAX_CHAR_LENGTH, CheckRequire, require
from utils.utils_time import get_timestamp

def judge_01(board): # judge the string board if it is consist of 0 and 1
    for ch in board:
        if (ch == '0' or ch == '1'):
            continue
        else:
            return 0
    return 1

def check_for_board_data(body):
    board = require(body, "board", "string", err_msg="Missing or error type of [board]")

    # TODO Start: [Student] add checks for type of boardName and userName
    board_name = require(body, "boardName", "string", err_msg="Missing or error type of [boardName]")
    user_name = require(body, "userName", "string", err_msg="Missing or error type of [userName]")
    # TODO End: [Student] add checks for type of boardName and userName
    assert 0 < len(board_name) <= 50, "Bad length of [boardName]"
    # TODO Start: [Student] add checks for length of userName and board
    assert 0 < len(user_name) <= 50, "bad length of [userName]"
    assert (len(board) == 2500),"bad length of [board]"
    assert judge_01(board),"Invalid char in [board]"
    # TODO End: [Student] add checks for length of userName and board

    # TODO Start: [Student] and more checks (you should read API docs carefully)

    # TODO End: [Student] and more checks (you should read API docs carefully)

    return board, board_name, user_name


@CheckRequire
def startup(req: HttpRequest):
    return HttpResponse("Congratulations! You have successfully installed the requirements. Go ahead!")


@CheckRequire
def boards(req: HttpRequest):

    if req.method == "GET": # get case
        params = req.GET
        boards = Board.objects.all().order_by('-created_time')# created time with negative order
        return_data = {
            "boards": [
                # Only provide required fields to lower the latency of
                # transmitting LARGE packets through unstable network
                return_field(board.serialize(), ["id", "boardName", "createdAt", "userName"])
            for board in boards],
        }
        return request_success(return_data) # react successfully

    elif req.method == "POST": # post case: need restrict
        body = json.loads(req.body.decode("utf-8")) # request version data

        board_state, board_name, user_name = check_for_board_data(body) # check the information is usageable

        # Find the corresponding user
        user = User.objects.filter(name=user_name).first()  # If not exists, return None

        if not user: # none case
            # User not exists, create user
            user = User(name=user_name)
            user.save()

        # First we lookup if the board with the same name and the same user exists
        board = Board.objects.filter(board_name=board_name, user=user).first()

        if not board: # none case
            # New an instance of Board type, then save it to the database
            board = Board(user=user, board_state=board_state, board_name=board_name)
            board.save()
            return request_success({"isCreate": True}) # is a new record

        else:
            # Board exists, change corresponding value of current `board`, then save it to the database
            board.board_state = board_state
            board.created_time = get_timestamp()
            board.save()
            return request_success({"isCreate": False}) # just renew a record

    else:
        return BAD_METHOD


@CheckRequire
def boards_index(req: HttpRequest, index: any):

    idx = require({"index": index}, "index", "int", err_msg="Bad param [id]", err_code=-1) # judge the id is a positive int

    if req.method == "GET":
        params = req.GET
        board = Board.objects.filter(id=idx).first()  # Return None if not exists

        if board:
            return request_success(
                return_field(board.serialize(), ["board", "boardName", "userName"])
            )
        else:
            return request_failed(1, "Board not found", status_code=404) # not find return "board not found"

    elif req.method == "DELETE":
        board = Board.objects.filter(id=idx).first()  # Return None if not exists, else corresponding instance
        if board:
            board.delete()
            return request_success()
        else:
            return request_failed(1, "Board not found", status_code=404)

    elif req.method == "PUT":
        body = json.loads(req.body.decode("utf-8"))
        # TODO Start: [Student] Finish PUT method for boards_index
        # 1. Check if body is valid and parse board_state, board_name and user_name from it
        #    Is there already a function for doing this?
        board_state, board_name, user_name = check_for_board_data(body) # check the information is usageable
        # 2. Using idx to filter board instance from Board.objects
        #    If it is None, return request_failed with code=1, message="Board not found" and status_code=404
        board = Board.objects.filter(id=idx).first()

        if not board:# none
            return request_failed(1, "Board not found", status_code=404)
        # 3. Find the corresponding user of the new board
        #    If the user does not exist, construct a new one and save it
        user = User.objects.filter(name=user_name).first()

        if not user:
        # User not exists, create user
            user = User(name=user_name)
            user.save()
        # 4. Find if the board with the same name and the same user exists and it is not the board to be updated
        #    If that board exists, return request_failed with code -2, message "Unique constraint failed" and http status code 400.
        board = Board.objects.filter(board_name=board_name, user=user).first()

        if board: # exist
            return request_failed(-2, "Unique constraint failed", status_code=400)
        # 5. Change corresponding properties of current `board`, and save it to the database
        #    Return request_success
            # not exist
        board = Board(user=user, board_state=board_state, board_name=board_name)
        board.save()
        return request_success()
        # TODO End: [Student] Finish PUT method for boards_index
    else:
        return BAD_METHOD



# TODO Start: [Student] Finish view function for user_board

@CheckRequire
def user_board(req: HttpRequest,userName:any):

    namex = require({"user": userName}, "user", "string", err_msg="Bad param [userName]", err_code=-1) # judge the id is a positive int

    try:
        0 < len(userName) <= 50
    except:
        return request_failed(-1,"Bad param [userName]") # length limitation

    if req.method == "GET": # get method
        params = req.GET

        user = User.objects.filter(name=namex).first()  # Return None if not exists
        if  not user: # empty
            return request_failed(1, "User not found", status_code=404)

        boards = Board.objects.filter(user=namex).order_by('-created_time')
        return_data = {
            "boards":[
                return_field(board.serialize(),["id","boardName","createdAt","username"])
            for board in boards],
        }
        return request_success(user,return_data) # success
    
    elif req.method == "DELETE":

        user = User.objects.filter(name=namex).first()  # Return None if not exists
        if not user: # empty
            return request_failed(1, "User not found", status_code=404)

        boards = Board.objects.filter(user=namex).order_by('-created_time')

        for board in boards:
            board.delete()

        if not boards.first(): # deleted clear
            return request_success()
    else:
        return BAD_METHOD


# TODO End: [Student] Finish view function for user_board
