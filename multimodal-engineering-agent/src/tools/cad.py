from __future__ import annotations

from pathlib import Path
from typing import Any, Dict


def _import_trimesh():
    try:
        import trimesh
        return trimesh
    except ImportError as exc:
        raise ImportError(
            "trimesh is required for CAD/mesh processing. Install it with: pip install trimesh"
        ) from exc


def summarize_mesh(file_path: str) -> Dict[str, Any]:
    trimesh = _import_trimesh()
    mesh_or_scene = trimesh.load(file_path, force=None)

    if hasattr(mesh_or_scene, "geometry"):
        geometries = list(mesh_or_scene.geometry.values())
        if not geometries:
            raise ValueError(f"No geometry found in file: {file_path}")
        mesh = trimesh.util.concatenate(geometries)
        num_parts = len(geometries)
    else:
        mesh = mesh_or_scene
        num_parts = 1

    bbox = mesh.bounds
    extents = mesh.extents

    return {
        "file_name": Path(file_path).name,
        "num_parts": int(num_parts),
        "num_vertices": int(len(mesh.vertices)),
        "num_faces": int(len(mesh.faces)) if hasattr(mesh, "faces") else None,
        "min_bound": bbox[0].tolist(),
        "max_bound": bbox[1].tolist(),
        "extent": extents.tolist(),
        "volume": float(mesh.volume) if getattr(mesh, "is_watertight", False) else None,
        "is_watertight": bool(getattr(mesh, "is_watertight", False)),
    }


def compute_bounding_box(file_path: str) -> Dict[str, Any]:
    summary = summarize_mesh(file_path)
    return {
        "min_bound": summary["min_bound"],
        "max_bound": summary["max_bound"],
        "extent": summary["extent"],
    }


def run_cad_tool(file_path: str, task_type: str) -> Dict[str, Any]:
    suffix = Path(file_path).suffix.lower()

    if suffix in {".step", ".stp", ".iges", ".igs"}:
        return {
            "warning": "STEP/IGES support requires pythonOCC or cadquery. Current base implementation supports mesh-like formats through trimesh.",
            "file_path": file_path,
            "suggested_package": "pythonocc-core or cadquery",
        }

    if task_type == "bounding_box":
        return compute_bounding_box(file_path)
    return summarize_mesh(file_path)
