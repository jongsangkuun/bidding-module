import bid.room

def main():
    user_id = "test"
    for i in range(5):
        bid.room.create_room(user_id=user_id)

    for i in bid.room._ROOMS:
        print("bid.room._ROOMS :::", i)

    test_room_uid = bid.room._ROOMS[list(bid.room._ROOMS.keys())[0]]["room_id"]
    print("test_room_id :::", test_room_uid)

    test_room_info = bid.room.get_room(room_id=test_room_uid)
    print("test_room_info :::", test_room_info)

    test_dealer_id = "test_dealer"
    bid.room.place_bid(room_id=test_room_uid, dealer_id=test_dealer_id, item_price=1000000)

    print("---------------------")
    for i in bid.room._ROOMS:
        print(bid.room.get_room(room_id=i))

    bid.room.close_room(room_id=test_room_uid)

    print("---------------------")
    for i in bid.room._ROOMS:
        print(bid.room.get_room(room_id=i))

if __name__ == "__main__":
    main()


