# Multimodal Engineering Agent

A LangGraph-based AI agent for processing multimodal engineering data such as point clouds, CAD files, engineering drawings, and technical documents.

## Features

- **Point Cloud Processing**: load, downsample, plane segmentation, clustering, measurement
- **CAD Processing**: STEP/STL/OBJ loading, bounding box extraction, mesh summary
- **Document Processing**: PDF/text loading and lightweight QA-ready text extraction
- **Agentic Workflow**: query routing, tool execution, result summarization
- **Extensible Design**: add BIM, GIS, P&ID, or robotics simulation tools later

## Supported Data Types

| Domain | File Types | Example Tasks |
|---|---|---|
| Point Cloud | `.pcd`, `.ply`, `.xyz`, `.las`, `.laz` | segmentation, clustering, distance measurement |
| CAD / Mesh | `.step`, `.stp`, `.stl`, `.obj` | bounding box, geometry summary, conversion |
| Document | `.pdf`, `.txt`, `.md` | text extraction, spec lookup, summary |
| Drawing / P&ID | `.png`, `.jpg`, `.pdf`, `.dwg`, `.dxf` | planned extension |
| BIM / GIS | `.ifc`, `.geojson`, `.shp`, `.tif` | planned extension |

## Installation

```bash
git clone https://github.com/bongbong0713/multimodal-engineering-agent.git
cd multimodal-engineering-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Some CAD packages can be platform-dependent. The base project works with optional imports, so unavailable packages will not break the whole agent.

## Quick Start

```bash
python examples/run_agent.py --query "이 포인트 클라우드에서 바닥면을 분리해줘" --file data/sample.ply
```

```python
from src.agent.graph import build_agent

app = build_agent()
result = app.invoke({
    "query": "CAD 파일의 bounding box를 계산해줘",
    "file_path": "data/sample.stl",
    "file_type": None,
    "task_type": None,
    "result": None,
    "error": None,
})

print(result["result"])
```

## Project Structure

```text
src/
  agent/
    graph.py          # LangGraph workflow
    state.py          # Agent state schema
    router.py         # file/task routing
  tools/
    point_cloud.py    # Open3D point cloud tools
    cad.py            # CAD/mesh tools
    document.py       # PDF/text tools
  parsers/
    file_type.py      # extension-based file type parser
  utils/
    logger.py
examples/
  run_agent.py
tests/
  test_router.py
```

## Roadmap

- [ ] Add P&ID graph extraction
- [ ] Add BIM parser for IFC files
- [ ] Add GIS parser for GeoTIFF, Shapefile, GeoJSON
- [ ] Add VLM-based drawing understanding
- [ ] Add RAG over technical documents
- [ ] Add web UI with Streamlit or FastAPI

## Interview Pitch

This project implements a multimodal engineering data agent that routes user requests to specialized tools for point clouds, CAD files, and technical documents. Instead of asking an LLM to directly understand complex 3D data, the LLM acts as an orchestrator that selects reliable geometry-processing tools such as Open3D, trimesh, and CAD parsers. This design makes the system extensible to industrial domains such as construction, manufacturing, robotics, GIS, and digital twins.
