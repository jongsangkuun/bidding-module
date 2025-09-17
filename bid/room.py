import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, List, TypedDict, Any

# ... existing code ...
# 간단한 메모리 기반 저장소(샘플 구현)
_ROOMS: Dict[str, Dict[str, object]] = {}

class Room:
    room_id: str
    user_id: str
    created_at: str
    is_open: bool
    # 주의: mutable을 클래스 속성으로 두면 모든 인스턴스가 공유합니다.
    # 필요하면 dataclass로 구현하거나 인스턴스 레벨에서 초기화하세요.
    # bids: List[Bid]  # 인스턴스에서 사용 시 초기화 필요

class Bid(TypedDict):
    dealer_id: str
    item_info: str
    item_price: float
    item_option: str
    timestamp: datetime

def create_room(user_id: str) -> Dict[str, object]:
    """
    새 방(room) 정보를 생성하여 메모리 저장소에 추가하고 반환합니다.
    반환값 예시:
    {
        "room_id": "uuid-string",
        "owner_id": "user123",
        "created_at": datetime(..., tzinfo=timezone.utc),
        "is_open": True,
        "bids": []
    }
    """
    if not user_id:
        # Todo
        # DB에서 유저의 아이디 조회 로직 추가 필요
        raise ValueError("user_id must be provided")

    uid = uuid.uuid4()
    room_info: Dict[str, Any] = {
        "room_id": str(uid),
        "user_id": user_id,
        "created_at": datetime.now(tz=timezone.utc),
        "is_open": True,
        "bids": [],  # type: List[Bid]
    }

    # Todo
    # 룸 정보를 DB, MQ, Redis 등에 저장하는 로직 구현 필요
    _ROOMS[room_info["room_id"]] = room_info

    return room_info

# ... existing code ...
def get_room(room_id: str) -> Optional[Dict[str, object]]:
    """
    room_id에 해당하는 방 정보를 반환합니다. 없으면 None 반환.
    반환되는 dict에는 'bids' 키가 포함됩니다.
    """
    return _ROOMS.get(room_id)

def place_bid(room_id: str, dealer_id: str, item_price: float) -> Bid:
    """
    입찰을 추가합니다. 유효하지 않으면 ValueError를 발생시킵니다.
    규칙(예시):
    - 방이 존재하고 is_open이어야 함
    - item_price는 양수여야 함
    - 마지막 최고가보다 높은 금액이어야 함
    """
    if item_price <= 0:
        raise ValueError("item_price must be positive")
    room = _ROOMS.get(room_id)
    if not room:
        raise ValueError("room not found")
    if not room.get("is_open", False):
        raise ValueError("room is closed")

    bids: List[Bid] = room.setdefault("bids", [])

    # 현재 최고 입찰 검사
    if bids:
        current_lowest = min(b["item_price"] for b in bids)
        if item_price <= current_lowest:
            raise ValueError(f"item_price must be higher than current lowest ({current_lowest})")
    bid: Bid = {
        "dealer_id": dealer_id,
        "item_price": item_price,
        "item_info": "",
        "item_option": "",
        "timestamp": datetime.now(tz=timezone.utc),
    }

    bids.append(bid)
    return bid


def close_room(room_id: str) -> Optional[Dict[str, object]]:
    """
    방을 종료하고 낙찰자 정보를 반환합니다.
    반환값 예시:
    {
        "room_id": ...,
        "winner": {"bidder_id": ..., "amount": ..., "timestamp": ...}  # 또는 None
    }
    """
    room = _ROOMS.get(room_id)
    if not room:
        return None
    if not room.get("is_open", False):
        # 이미 닫혀 있으면 현재 상태를 반환
        return {"room_id": room_id, "winner": get_lowest_bid(room_id)}
    room["is_open"] = False
    winner = get_lowest_bid(room_id)
    return {"room_id": room_id, "winner": winner}


def get_lowest_bid(room_id: str) -> Optional[Dict[str, object]]:
    """
    주어진 room_id의 최고 입찰(bid)을 반환합니다.
    반환되는 객체 예시: {"dealer_id": ..., "item_price": ..., "timestamp": ...} 또는 None
    """
    room = _ROOMS.get(room_id)
    if not room:
        return None
    bids: List[Bid] = room.get("bids", [])
    if not bids:
        return None
    # 최저가 입찰(동일 금액이 여러개면 가장 먼저 올라온 것을 선택하려면 정렬/타임스탬프 비교 필요)
    lowest_bids = min(bids, key=lambda b: b["item_price"])
    # 반환 형식 통일
    return {
        "dealer_id": lowest_bids["dealer_id"],
        "amount": lowest_bids["item_price"],
        "timestamp": lowest_bids["timestamp"],
    }