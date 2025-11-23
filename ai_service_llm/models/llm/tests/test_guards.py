from models.llm.core import guards


def test_is_safe_blocks_keywords():
    assert not guards.is_safe("I feel suicide")
    assert guards.is_safe("I feel tired")
