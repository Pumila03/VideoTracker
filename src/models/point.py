class Point:
    """Represents an immutable point."""

    def __init__(self, x: float, y: float) -> None:
        self.__x = x
        self.__y = y

    @property
    def x(self) -> float:
        """The x coordinate of the point."""
        return self.__x

    @property
    def y(self) -> float:
        """The y coordinate of the point."""
        return self.__y

    def __repr__(self) -> str:
        """Returns a string representing the point with the format: (x, y)."""
        return f"({self.__x}, {self.__y})"
