import inspect
from types import FrameType
from typing import Any, NamedTuple, Optional

from ....operation_framework.operation import Operation


class LogCallerInfo(NamedTuple):
    package_name: Optional[str]
    file_name: str
    caller_type: str
    full_path: str
    line_number: int


class LogCallLocation(NamedTuple):
    callers: list[LogCallerInfo]


class GetLocationOfLogCall(Operation):
    def __init__(self, caller_frame: Optional[FrameType] = None, stack_level: int = 1) -> None:
        super().__init__()
        self.caller_frame = caller_frame
        self.stack_level = stack_level

    def execute(self, *args: Any, **kwargs: Any) -> str:
        location_data = self._gather_location_data()
        return self._generate_output_string(location_data)

    def _gather_location_data(self) -> Optional[LogCallLocation]:
        if not self.caller_frame:
            return None

        caller_info_list = []
        current_frame = self.caller_frame.f_back

        for _ in range(self.stack_level):
            if not current_frame:
                break
            if frame_details := self._gather_frame_details(current_frame):
                caller_info_list.append(frame_details)
            current_frame = current_frame.f_back

        return LogCallLocation(caller_info_list) if caller_info_list else None

    def _gather_frame_details(self, frame: Optional[FrameType]) -> Optional[LogCallerInfo]:
        if not frame or not (full_path := inspect.getfile(frame)):
            return None

        path_parts = full_path.split("/")
        return LogCallerInfo(
            package_name=self._extract_package_name(path_parts),
            file_name=path_parts[-1],
            caller_type=self._determine_caller_type(frame),
            full_path=full_path,
            line_number=frame.f_lineno,
        )

    def _extract_package_name(self, path_parts: list[str]) -> Optional[str]:
        try:
            idx = path_parts.index("My Packages")
            return path_parts[idx + 1] if len(path_parts) > idx + 1 else None
        except ValueError:
            return None

    def _determine_caller_type(self, frame: FrameType) -> str:
        func_name = frame.f_code.co_name
        if func_name == "<module>":
            return "Module Level"

        locals_dict = frame.f_locals
        if "self" in locals_dict:
            return self._get_method_type(locals_dict["self"], func_name)
        if "cls" in locals_dict:
            return f"Classmethod '{func_name}' of class '{locals_dict['cls'].__name__}'"
        if "decorator" in func_name.lower() or func_name.startswith("_wrapper"):
            return f"Decorator '{func_name}'"
        return f"Function '{func_name}'"

    def _get_method_type(self, instance: Any, func_name: str) -> str:
        class_name = instance.__class__.__name__
        if hasattr(instance.__class__, func_name):
            attr = getattr(instance.__class__, func_name)
            return (
                f"Property '{func_name}' of class '{class_name}'"
                if isinstance(attr, property)
                else f"Method '{func_name}' of class '{class_name}'"
            )
        return f"Method '{func_name}' of class '{class_name}'"

    def _generate_output_string(self, location_data: Optional[LogCallLocation]) -> str:
        if not location_data or not location_data.callers:
            return ""

        output = ["\n    📍 Location:"]
        for i, caller in enumerate(location_data.callers):
            indent = "    " * i
            base_indent = "\n        " if i == 0 else f"\n        {indent}↳ Called By:\n            {indent}"
            line_indent = "        " if i == 0 else f"            {indent}"

            if caller.package_name:
                output.append(f"{base_indent}🔹 Package: {caller.package_name}")
            output.extend(
                [
                    f"\n{line_indent}🔹 Called From: {caller.caller_type} at line {caller.line_number}",
                    f"\n{line_indent}🔹 Path: {caller.full_path}",
                ]
            )

        return "".join(output)
