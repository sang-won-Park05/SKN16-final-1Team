from models.ocr.utils import postprocess


def test_normalize_units_trims():
    assert postprocess.normalize_units(" value \n") == "value"
