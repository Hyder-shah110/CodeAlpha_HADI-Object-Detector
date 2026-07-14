"""
summary.py
----------
Detection results ka summary banane wala helper.
Har object type kitni baar detect hua, ye count karta hai.

Example:
    Input:  [{"Object": "Car"}, {"Object": "Car"}, {"Object": "Person"}]
    Output: {"Car": 2, "Person": 1}
"""

from collections import Counter


def create_detection_summary(detections):
    """
    Detections ki list se object-wise count nikalta hai.

    Parameters
    ----------
    detections : list[dict]
        Har dict mein kam az kam "Object" key honi chahiye.

    Returns
    -------
    dict
        Object name -> count, sorted (sabse zyada detect hone wala pehle).
    """

    if not detections:
        return {}

    object_names = [item["Object"] for item in detections]

    counts = Counter(object_names)

    # Sabse zyada frequent object upar dikhane ke liye sort karo
    sorted_counts = dict(
        sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
    )

    return sorted_counts
