from typing import Optional, Set
from fastapi import Query, HTTPException
from backend.app.helper.enums import PlayerIncludeParameter

def validate_include(include: Optional[str] = Query(None, description='Comma-separated, e.g. "inventory,item"')) -> Set[PlayerIncludeParameter]:
    if not include:
        return set()
    parts = {p.strip().lower() for p in include.split(",") if p.strip()}
    valid = {e.value for e in PlayerIncludeParameter}
    unknown = parts - valid
    if unknown:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported include(s): {', '.join(sorted(unknown))}. "
                   f"Supported: {', '.join(sorted(valid))}"
        )
    return {PlayerIncludeParameter(p) for p in parts}
