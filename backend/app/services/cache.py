import asyncio
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from app.models.cached_condition import CachedCondition
from ..db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import json

CACHE_FRESHNESS_MINUTES = 60

async def get_or_fetch( lat : float, long: float, source : str, fetch_fn ,db : AsyncSession = get_db,):
    """
    Checks cached_conditions table first. If fresh data exists, reuse it.
    Otherwise calls fetch_fn (your real API function), saves result, returns it.

    db: your async DB session
    source: "marine", "weather", or "tide" — identifies which API this is for
    fetch_fn: an async function like get_tide_forecast, called only if cache is stale/missing
    """

    cutoff = datetime.now(timezone.utc) - timedelta(minutes=CACHE_FRESHNESS_MINUTES)

    result = await db.execute(select(CachedCondition).where(
        CachedCondition.latitude == lat,
        CachedCondition.longitude == long,
        CachedCondition.source == source,
        CachedCondition.fetched_at >= cutoff
    ))

    cached_row = result.scalar_one_or_none()

    if cached_row:
        return json.loads(cached_row)

    fresh_data = await fetch_fn(lat, long)

    save_cache = CachedCondition(
        latitude=lat,
        longitude=long,
        source=source,
        data=json.dumps(fresh_data)
    )
    db.add(save_cache)
    await db.commit()

    return fresh_data

