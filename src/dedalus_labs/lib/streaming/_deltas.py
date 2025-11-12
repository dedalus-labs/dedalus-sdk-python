from __future__ import annotations

from ..._utils import is_dict, is_list


def accumulate_delta(acc: dict[object, object], delta: dict[object, object]) -> dict[object, object]:
    """Merge a chunk delta into the running accumulator."""
    for key, delta_value in delta.items():
        if key not in acc:
            acc[key] = delta_value
            continue

        acc_value = acc[key]
        if acc_value is None:
            acc[key] = delta_value
            continue

        if key in {"index", "type"}:
            acc[key] = delta_value
            continue

        if isinstance(acc_value, str) and isinstance(delta_value, str):
            acc_value += delta_value
        elif isinstance(acc_value, (int, float)) and isinstance(delta_value, (int, float)):
            acc_value += delta_value
        elif is_dict(acc_value) and is_dict(delta_value):
            acc_value = accumulate_delta(acc_value, delta_value)
        elif is_list(acc_value) and is_list(delta_value):
            if all(isinstance(entry, (str, int, float)) for entry in acc_value):
                acc_value.extend(delta_value)
                acc[key] = acc_value
                continue

            for delta_entry in delta_value:
                if not is_dict(delta_entry):
                    raise TypeError(f"Expected chunk delta entry to be a dict, received {delta_entry!r}")

                index = delta_entry.get("index")
                if not isinstance(index, int):
                    raise TypeError(f"Chunk delta entry missing integer index: {delta_entry!r}")

                if index >= len(acc_value):
                    acc_value.insert(index, delta_entry)
                    continue

                acc_entry = acc_value[index]
                if not is_dict(acc_entry):
                    raise TypeError("Cannot merge non-dict list entries in streaming delta")

                acc_value[index] = accumulate_delta(acc_entry, delta_entry)

        acc[key] = acc_value

    return acc


__all__ = ["accumulate_delta"]
