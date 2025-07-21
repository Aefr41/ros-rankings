import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import pytest
from ranking.rank_engine import compute_ros_points

@pytest.mark.parametrize("age,expected", [
    (25, 75.0),
    (30, 70.0),
    (0, 100.0),
    (None, 0.0),
    (120, 0.0),
])
def test_compute_ros_points(age, expected):
    player = {"age": age}
    assert compute_ros_points(player) == expected
