from move import Move


def test_constructor():
    move1 = Move([2, 1], [4, 3], True, [3, 2])
    move2 = Move([2, 1], [4, 3], True, [3, 2])
    assert(move1 == move2)
