from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_db
from app.services.citus_resharding_service import CitusReshardingService

router = APIRouter(prefix="/citus-resharding", tags=["Citus Resharding"])


@router.post("/enable-auto-rebalancing")
async def enable_auto_rebalancing(db: AsyncSession = Depends(get_db)):
    """Enable Citus automatic shard rebalancing"""
    service = CitusReshardingService(db)
    return await service.enable_auto_rebalancing()


@router.post("/rebalance")
async def trigger_rebalance(
    table_name: str = "messages", db: AsyncSession = Depends(get_db)
):
    """Manually trigger shard rebalancing for a table"""
    service = CitusReshardingService(db)
    return await service.rebalance_table(table_name)


@router.post("/add-worker")
async def add_worker_node(
    host: str, port: int = 5432, db: AsyncSession = Depends(get_db)
):
    """Add new worker node to Citus cluster"""
    service = CitusReshardingService(db)
    return await service.add_worker_node(host, port)


@router.get("/shard-distribution")
async def get_shard_distribution(
    table_name: str = "messages", db: AsyncSession = Depends(get_db)
):
    """Get current shard distribution across worker nodes"""
    service = CitusReshardingService(db)
    return await service.get_shard_distribution(table_name)


@router.get("/status")
async def get_rebalancer_status(db: AsyncSession = Depends(get_db)):
    """Get current rebalancer status"""
    service = CitusReshardingService(db)
    return await service.get_rebalancer_status()
