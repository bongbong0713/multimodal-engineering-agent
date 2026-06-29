from pathlib import Path


POINT_CLOUD_EXTENSIONS = {".pcd", ".ply", ".xyz", ".las", ".laz"}
CAD_EXTENSIONS = {".step", ".stp", ".iges", ".igs", ".stl", ".obj"}
DOCUMENT_EXTENSIONS = {".pdf", ".txt", ".md"}
DRAWING_EXTENSIONS = {".png", ".jpg", ".jpeg", ".dwg", ".dxf"}
BIM_EXTENSIONS = {".ifc"}
GIS_EXTENSIONS = {".geojson", ".shp", ".tif", ".tiff", ".geotiff"}


def detect_file_type(file_path: str) -> str:
    """Detect engineering domain from file extension."""
    ext = Path(file_path).suffix.lower()

    if ext in POINT_CLOUD_EXTENSIONS:
        return "point_cloud"
    if ext in CAD_EXTENSIONS:
        return "cad"
    if ext in DOCUMENT_EXTENSIONS:
        return "document"
    if ext in DRAWING_EXTENSIONS:
        return "drawing"
    if ext in BIM_EXTENSIONS:
        return "bim"
    if ext in GIS_EXTENSIONS:
        return "gis"
    return "unknown"
