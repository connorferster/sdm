from dataclasses import dataclass
from typing import Optional
from shapely import Point, Geometry, LineString, Polygon

@dataclass
class Element:
    """
    A dataclass to generically represent a structural element on a PDF page
    whether it is a beam, column, joist, or otherwise.

    Note: each Element has no "knowledge" of its intersections and correspondents.
    They are generated in a separate process and are not part of the capability
    of the class. These attributes are simply to keep track of pre-discovered
    intersections and correspondents.
    
    'tag': str, represent a unique name for this element, as per the designer's preference
    'type': str, describing what "type" of element it is. This is not an enumeration
        and can take any designer-defined value. It is for user-level categorization.
    'page': int, describing the page index of the PDF that this element is found on
    'geometry': the shapely geometry that represents this element in 2D space
    'intersections': list[tuple[str, Point]], where each 2-tuple represents the tag
        of the other Element that this element intersects with on plan and the point
        of intersection. Intersections exist only between elements that are on the same PDF page
        and thus are used to describe connections that occur on the horizontal plane.
    'correspondents': list[str], where each item in the list represents the tag of another
        Element that is approximately in the exact same position as this element but on the
        adjacent page. Correspondents exist only between elements that are on adjacent PDF
        pages and thus are used to describe connections that occur on the vertical plane
        such as the the top and bottom of a wall or column (the bottom may be on page 0 and 
        the top may be on page 1)
    'page_label': A designer-defined str label for the page (e.g. "Ground Floor" or "L03", etc.)
    """
    tag: str
    type: str
    page: int
    geometry: Geometry
    intersections: list[tuple[str, Point]]
    correspondents: list[tuple[str, Geometry]]
    page_label: Optional[str] = None


# Examples
## This example shows a beam that is connected to a joist and a column on the same page
## and with that column having a correspondent on the page below
E00 = Element(
    tag="FB1.1", 
    type="Flush Beam", 
    page=1, 
    geometry=LineString([[101.5, 52.0], [101.5, 85.3]]), 
    intersections=[("J1.1", Point([101.5, 65.2]))],
    correspondents=[],
)

E01 = Element(
    tag="C1.1", 
    type="Column", 
    page=1, 
    geometry=Polygon([[100.0, 100.0], [100.0, 103.0], [103.0, 103.0], [103.0, 100.0]]), 
    intersections=[("FB1.1", Point([101.5, 53.5]))],
    correspondents=["C0.1"],
    page_label="L02"
)

E02 = Element(
    tag="C0.1", 
    type="Column", 
    page=0, 
    geometry=Polygon([[100.0, 100.0], [100.0, 103.0], [103.0, 103.0], [103.0, 100.0]]), 
    intersections=[],
    correspondents=["C1.1"],
    page_label="L01"
)



