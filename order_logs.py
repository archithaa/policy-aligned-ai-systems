# order_logs.py
"""
Fake Swiggy order metadata for testing KARE on real 1★-style scenarios.

Each order_id is a 6-digit string so it is easy to reference in chat.
You can extend or tweak these as you refine your cases.
"""

from typing import Dict, Any, List

ORDER_DB: Dict[str, Dict[str, Any]] = {
    # 1) Mrityunjoy Bose — repeated delay + cold food + no comp + accidental order + fee (<1 min)
    "200001": {
        "customer_name": "Mrityunjoy Bose",
        "service_type": "food",
        "restaurant_or_store": "Spice Corner",
        "placed_at": "2025-07-25 20:00",
        "promised_eta_minutes": 30,
        "updated_eta_minutes": 30,
        "delivered_at": "2025-07-25 20:35",
        "cancelled_at": None,
        "delay_minutes": 35 - 30,
        "status": "delivered_delayed_cold",
        "issues": ["delay", "cold_food", "no_compensation"],
        "previous_compensation": False,
        "notes": "Order delivered ~5 minutes late, user reported food cold, support closed with generic apology and no credit.",
    },
    "200002": {
        "customer_name": "Mrityunjoy Bose",
        "service_type": "food",
        "restaurant_or_store": "Urban Biryani",
        "placed_at": "2025-08-02 19:01",
        "promised_eta_minutes": 30,
        "updated_eta_minutes": 30,
        "delivered_at": None,
        "cancelled_at": "2025-08-02 19:02",
        "delay_minutes": 0,
        "status": "cancelled_within_1_min_fee_charged",
        "issues": ["accidental_order", "cancellation_fee_charged"],
        "previous_compensation": False,
        "notes": "User triggered order while changing payment mode, cancellation attempt within ~1 minute, system still applied full cancellation fee.",
    },

    # 2) Likith Naik — two messed orders in a week + useless restaurant-only coupon, short validity, no stacking
    "200003": {
        "customer_name": "Likith Naik",
        "service_type": "food",
        "restaurant_or_store": "Tasty Bites",
        "placed_at": "2025-11-27 20:10",
        "promised_eta_minutes": 35,
        "updated_eta_minutes": 35,
        "delivered_at": "2025-11-27 20:40",
        "cancelled_at": None,
        "delay_minutes": 5,
        "status": "delivered_wrong_items",
        "issues": ["wrong_items", "partial_resolution_coupon"],
        "previous_compensation": True,
        "notes": "Wrong main item. Support issued restaurant-locked coupon valid 7 days, non-stackable with restaurant offers.",
    },
    "200004": {
        "customer_name": "Likith Naik",
        "service_type": "food",
        "restaurant_or_store": "Tasty Bites",
        "placed_at": "2025-12-02 21:00",
        "promised_eta_minutes": 40,
        "updated_eta_minutes": 40,
        "delivered_at": "2025-12-02 21:35",
        "cancelled_at": None,
        "delay_minutes": 0,
        "status": "delivered_wrong_items_repeat",
        "issues": ["wrong_items", "repeat_issue", "coupon_only_comp"],
        "previous_compensation": True,
        "notes": "Second wrong order in a week from same restaurant; again compensated only via same-restaurant coupon with 1-week validity and no stacking.",
    },

    # 3) Amarjeet Negi — chronic ETA lies + multi-order batching delays
    "200005": {
        "customer_name": "Amarjeet Negi",
        "service_type": "food",
        "restaurant_or_store": "North Feast",
        "placed_at": "2025-12-05 19:15",
        "promised_eta_minutes": 25,
        "updated_eta_minutes": 25,
        "delivered_at": "2025-12-05 19:45",
        "cancelled_at": None,
        "delay_minutes": 20,
        "status": "delivered_delayed_multibatch",
        "issues": ["delay", "multi_order_batching"],
        "previous_compensation": False,
        "notes": "Rider assigned 3 simultaneous orders; no automatic delay credit applied despite ETA overshoot by ~20 minutes.",
    },

    # 4) Abhinav Mahanta — order auto-placed when changing payment, coupon not applied, blocked cancellation
    "200006": {
        "customer_name": "Abhinav Mahanta",
        "service_type": "food",
        "restaurant_or_store": "Cafe Junction",
        "placed_at": "2025-12-06 18:59",
        "promised_eta_minutes": 35,
        "updated_eta_minutes": 35,
        "delivered_at": None,
        "cancelled_at": None,
        "delay_minutes": 0,
        "status": "preparation_started_within_1_min_blocked_cancel",
        "issues": ["accidental_order", "coupon_not_applied", "blocked_cancellation"],
        "previous_compensation": False,
        "notes": "Order triggered on payment-method change; coupon field never applied. Cancellation attempt at ~19:00 recorded after restaurant marked 'preparing', app shows 'cannot cancel'.",
    },

    # 5) Dinesh / repeated wrong items + no instant resolution, forced email, delay no cancel
    "200007": {
        "customer_name": "Dinesh Kumar",
        "service_type": "food",
        "restaurant_or_store": "Hungry Hub",
        "placed_at": "2025-11-18 21:00",
        "promised_eta_minutes": 30,
        "updated_eta_minutes": 35,
        "delivered_at": "2025-11-18 21:40",
        "cancelled_at": None,
        "delay_minutes": 10,
        "status": "delivered_wrong_items_and_delayed",
        "issues": ["wrong_items", "delay", "no_immediate_resolution", "forced_email"],
        "previous_compensation": False,
        "notes": "Multiple items incorrect; help centre only offers 'email support', no instant resolution or refund option during delay.",
    },

    # 6) Nida Firdose — Instamart batteries, policy allows return in 3 days, support denies
    "200008": {
        "customer_name": "Nida Firdose",
        "service_type": "instamart",
        "restaurant_or_store": "Instamart Warehouse - BLR",
        "placed_at": "2025-12-05 10:15",
        "promised_eta_minutes": 15,
        "updated_eta_minutes": 15,
        "delivered_at": "2025-12-05 10:27",
        "cancelled_at": None,
        "delay_minutes": 12 - 15 if 12 > 15 else 0,
        "status": "delivered_product_not_compatible",
        "issues": ["instamart_return_requested", "policy_mismatch", "return_denied"],
        "previous_compensation": False,
        "notes": "Toy batteries delivered intact; return policy on PDP shows '3-day return if intact'. Email support refused return citing 'non-returnable' despite policy text.",
    },

    # 7) Aaron de Sousa — missing item + app glitch preventing complaint submission
    "200009": {
        "customer_name": "Aaron de Sousa",
        "service_type": "food",
        "restaurant_or_store": "City Grill",
        "placed_at": "2025-10-27 19:20",
        "promised_eta_minutes": 35,
        "updated_eta_minutes": 40,
        "delivered_at": "2025-10-27 20:05",
        "cancelled_at": None,
        "delay_minutes": 10,
        "status": "delivered_missing_item_app_glitch",
        "issues": ["missing_item", "app_bug_reporting", "no_refund_yet"],
        "previous_compensation": False,
        "notes": "One side item missing. User repeatedly hit error on 'Report Issue' flow. Support suggested 'wait, it will fix itself'; no resolution even after 24+ hours.",
    },

    # 8) Arundhathi Sajeev — ETA jumps from 30–35 to 50–55 after payment + full cancellation fee
    "200010": {
        "customer_name": "Arundhathi Sajeev",
        "service_type": "food",
        "restaurant_or_store": "Green Leaf Restaurant",
        "placed_at": "2025-10-24 20:10",
        "promised_eta_minutes": 35,
        "updated_eta_minutes": 55,
        "delivered_at": None,
        "cancelled_at": "2025-10-24 20:12",
        "delay_minutes": 0,
        "status": "eta_jump_then_cancel_fee_shown",
        "issues": ["eta_misleading", "cancellation_fee_shown", "help_center_unhelpful"],
        "previous_compensation": False,
        "notes": "Pre-payment ETA 30–35 mins; post-payment ETA changes to 50–55 mins. User attempts immediate cancellation; system shows full cancellation fee equal to order value.",
    },

    # 9) Uma / abhiram — long wait then restaurant cancellation, no comp
    "200011": {
        "customer_name": "Uma Chatterjee",
        "service_type": "food",
        "restaurant_or_store": "Midnight Meals",
        "placed_at": "2025-11-29 21:00",
        "promised_eta_minutes": 40,
        "updated_eta_minutes": 45,
        "delivered_at": None,
        "cancelled_at": "2025-11-29 22:05",
        "delay_minutes": 25,
        "status": "restaurant_cancelled_after_1hr_no_comp",
        "issues": ["restaurant_cancelled_late", "no_compensation", "communication_delay"],
        "previous_compensation": False,
        "notes": "Order auto-cancelled after >1 hour citing 'restaurant too stressed'. No proactive comp or early heads-up to user.",
    },

    # 10) Repeated missing/quality issues + burnt/small item + useless coupon (Kavi / Rekha / Gayatri)
    "200012": {
        "customer_name": "Kavi Saini",
        "service_type": "food",
        "restaurant_or_store": "BBQ House",
        "placed_at": "2025-12-04 19:40",
        "promised_eta_minutes": 35,
        "updated_eta_minutes": 35,
        "delivered_at": "2025-12-04 20:10",
        "cancelled_at": None,
        "delay_minutes": 0,
        "status": "delivered_wrong_size_and_burnt",
        "issues": ["wrong_size", "burnt_food", "repeat_issue"],
        "previous_compensation": True,
        "notes": "User selected 'medium' portion; merchant packed 'small'. Food reported burnt. Similar complaints recorded on prior orders; earlier chats closed with small coupons only.",
    },
    "200013": {
        "customer_name": "Rekha Bhargava",
        "service_type": "instamart",
        "restaurant_or_store": "Instamart Warehouse - DEL",
        "placed_at": "2025-11-06 17:30",
        "promised_eta_minutes": 20,
        "updated_eta_minutes": 25,
        "delivered_at": "2025-11-06 17:55",
        "cancelled_at": None,
        "delay_minutes": 5,
        "status": "delivered_multiple_missing_items_poor_rider_behaviour",
        "issues": ["missing_items", "rider_behaviour", "support_unhelpful"],
        "previous_compensation": False,
        "notes": "Frequent missing items from Instamart orders; rider marked as 'rude' in prior feedback; support responses logged as 'template apology, no actionable resolution'.",
    },
}


def _list_issues(issues: List[str]) -> str:
    if not issues:
        return "None recorded"
    return ", ".join(issues)


def describe_order(order_id: str) -> str:
    """Return a human-readable summary of fake logs for a given order."""
    o = ORDER_DB[order_id]

    lines = [
        f"Order {order_id} logs:",
        f"- Customer: {o.get('customer_name', 'N/A')}",
        f"- Service type: {o.get('service_type', 'unknown')}",
        f"- Restaurant/store: {o.get('restaurant_or_store', 'N/A')}",
    ]

    placed_at = o.get("placed_at")
    if placed_at:
        lines.append(f"- Placed at: {placed_at}")

    promised = o.get("promised_eta_minutes")
    updated = o.get("updated_eta_minutes")
    if promised:
        if updated and updated != promised:
            lines.append(
                f"- Promised ETA: {promised} min, updated ETA after order: {updated} min"
            )
        else:
            lines.append(f"- Promised ETA: {promised} min")

    delivered_at = o.get("delivered_at")
    cancelled_at = o.get("cancelled_at")

    if delivered_at:
        lines.append(f"- Delivered at: {delivered_at}")
    if cancelled_at:
        lines.append(f"- Cancellation recorded at: {cancelled_at}")

    delay = o.get("delay_minutes")
    if delay and delay > 0:
        lines.append(f"- Delay vs promised time: {delay} minutes")

    lines.append(f"- Status: {o.get('status', 'N/A')}")
    lines.append(f"- Issues tagged: {_list_issues(o.get('issues', []))}")

    prev_comp = o.get("previous_compensation", False)
    lines.append(
        "- Previous compensation given: YES" if prev_comp else "- Previous compensation given: NO"
    )

    notes = o.get("notes")
    if notes:
        lines.append(f"- Notes: {notes}")

    return "\n".join(lines)


def describe_all_orders() -> str:
    """Return a human-readable list of all orders for this user."""
    lines = ["Recent orders for this user:"]
    for oid, o in ORDER_DB.items():
        lines.append(
            f"- {oid}: {o['restaurant_or_store']}, placed at {o['placed_at']}, "
            f"status: {o['status']}, issues: {', '.join(o['issues'])}"
        )
    return "\n".join(lines)
