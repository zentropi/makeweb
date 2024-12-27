def create_sparkline(
    data: list[float],
    width: int = 100,
    height: int = 20,
    line_color: str = "currentColor",
    line_width: float = 1.5,
    min_value: float = None,
    max_value: float = None,
) -> str:
    """Generate an SVG sparkline chart."""
    if not data:
        return ""

    # Use provided min/max or calculate from data
    min_y = min_value if min_value is not None else min(data)
    max_y = max_value if max_value is not None else max(data)

    # Prevent division by zero
    if min_y == max_y:
        max_y = min_y + 1

    # Calculate points
    points = []
    data_len = len(data)
    for i, value in enumerate(data):
        x = (i / (data_len - 1)) * width if data_len > 1 else width / 2
        y = height - ((value - min_y) / (max_y - min_y)) * height
        points.append(f"{x:.1f},{y:.1f}")

    return (
        f'<svg width="{width}" height="{height}" class="sparkline" '
        f'viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        f'<polyline fill="none" stroke="{line_color}" stroke-width="{line_width}" '
        f'points="{" ".join(points)}"/></svg>'
    )
