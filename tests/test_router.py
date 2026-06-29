from src.agent.router import classify_task_from_query
from src.parsers.file_type import detect_file_type


def test_detect_file_type():
    assert detect_file_type("sample.ply") == "point_cloud"
    assert detect_file_type("part.stl") == "cad"
    assert detect_file_type("manual.pdf") == "document"
    assert detect_file_type("building.ifc") == "bim"


def test_classify_task_from_query():
    assert classify_task_from_query("바닥면을 분리해줘") == "segmentation"
    assert classify_task_from_query("bounding box 계산") == "bounding_box"
    assert classify_task_from_query("문서에서 스펙 추출") == "text_extraction"
