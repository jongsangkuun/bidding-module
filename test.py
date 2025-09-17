import bid.room

# 시나리오
# 1. 유저가 경매 요청을 진행함 -> create_room
# 2. 딜러가 입찰가 입력 -> place_bid
# 3. 진행 중인 입찰 정보 모두 조회 -> get_room
# 4. 입찰 종료 요청 -> close_room
def main():
    user_id = "test"

    # 1. 유저가 경매 요청을 진행함 -> create_room
    for i in range(5):
        bid.room.create_room(user_id=user_id)

    for i in bid.room._ROOMS:
        print("bid.room._ROOMS :::", i)

    test_room_uid = bid.room._ROOMS[list(bid.room._ROOMS.keys())[0]]["room_id"]
    print("test_room_id :::", test_room_uid)

    test_room_info = bid.room.get_room(room_id=test_room_uid)
    print("test_room_info :::", test_room_info)

    # 2. 딜러가 입찰가 입력 -> place_bid
    test_dealer_id = "test_dealer"
    bid.room.place_bid(room_id=test_room_uid, dealer_id=test_dealer_id, item_price=1000000)

    # 3. 진행 중인 입찰 정보 모두 조회 -> get_room
    print("---------------------")
    for i in bid.room._ROOMS:
        print(bid.room.get_room(room_id=i))

    bid.room.close_room(room_id=test_room_uid)

    # 4. 입찰 종료 요청 -> close_room
    print("---------------------")
    for i in bid.room._ROOMS:
        print(bid.room.get_room(room_id=i))

if __name__ == "__main__":
    main()


