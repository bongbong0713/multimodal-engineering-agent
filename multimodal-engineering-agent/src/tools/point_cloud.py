from __future__ import annotations

from typing import Any, Dict

import numpy as np


def _import_open3d():
    try:
        import open3d as o3d
        return o3d
    except ImportError as exc:
        raise ImportError(
            "open3d is required for point cloud processing. Install it with: pip install open3d"
        ) from exc


def load_point_cloud(file_path: str):
    o3d = _import_open3d()
    pcd = o3d.io.read_point_cloud(file_path)
    if pcd.is_empty():
        raise ValueError(f"Empty or unreadable point cloud: {file_path}")
    return pcd


def summarize_point_cloud(file_path: str) -> Dict[str, Any]:
    pcd = load_point_cloud(file_path)
    points = np.asarray(pcd.points)
    bbox = pcd.get_axis_aligned_bounding_box()

    return {
        "num_points": int(len(points)),
        "has_colors": bool(pcd.has_colors()),
        "has_normals": bool(pcd.has_normals()),
        "min_bound": bbox.min_bound.tolist(),
        "max_bound": bbox.max_bound.tolist(),
        "extent": bbox.get_extent().tolist(),
    }


def downsample(file_path: str, voxel_size: float = 0.05) -> Dict[str, Any]:
    pcd = load_point_cloud(file_path)
    before = len(pcd.points)
    pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
    after = len(pcd_down.points)

    return {
        "voxel_size": voxel_size,
        "num_points_before": int(before),
        "num_points_after": int(after),
    }


def segment_plane(
    file_path: str,
    distance_threshold: float = 0.02,
    ransac_n: int = 3,
    num_iterations: int = 1000,
) -> Dict[str, Any]:
    pcd = load_point_cloud(file_path)
    plane_model, inliers = pcd.segment_plane(
        distance_threshold=distance_threshold,
        ransac_n=ransac_n,
        num_iterations=num_iterations,
    )

    return {
        "plane_model": [float(x) for x in plane_model],
        "num_plane_points": int(len(inliers)),
        "num_remaining_points": int(len(pcd.points) - len(inliers)),
        "description": "Plane equation: ax + by + cz + d = 0",
    }


def cluster_dbscan(file_path: str, eps: float = 0.05, min_points: int = 30) -> Dict[str, Any]:
    pcd = load_point_cloud(file_path)
    labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_points))
    valid_labels = labels[labels >= 0]
    num_clusters = int(valid_labels.max() + 1) if len(valid_labels) else 0
    num_noise = int(np.sum(labels == -1))

    return {
        "eps": eps,
        "min_points": min_points,
        "num_clusters": num_clusters,
        "num_noise_points": num_noise,
    }


def run_point_cloud_tool(file_path: str, task_type: str) -> Dict[str, Any]:
    if task_type == "segmentation":
        return segment_plane(file_path)
    if task_type == "clustering":
        return cluster_dbscan(file_path)
    if task_type == "measurement":
        return summarize_point_cloud(file_path)
    if task_type == "bounding_box":
        return summarize_point_cloud(file_path)
    return summarize_point_cloud(file_path)
