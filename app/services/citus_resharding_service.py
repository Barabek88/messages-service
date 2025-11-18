from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class CitusReshardingService:
    """Simple service for Citus native auto-resharding"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def enable_auto_rebalancing(self):
        """Enable Citus auto-rebalancing"""
        await self.db.execute(
            text("ALTER SYSTEM SET citus.shard_rebalancer_mode = 'auto'")
        )
        await self.db.execute(text("SELECT pg_reload_conf()"))
        await self.db.commit()
        return {"status": "enabled", "message": "Auto-rebalancing enabled"}

    async def rebalance_table(self, table_name: str = "messages"):
        """Trigger manual rebalancing for a table"""
        await self.db.execute(
            text("SELECT rebalance_table_shards(:table)"), {"table": table_name}
        )
        await self.db.commit()
        return {
            "status": "triggered",
            "message": f"Rebalancing triggered for {table_name}",
        }

    async def add_worker_node(self, host: str, port: int = 5432):
        """Add new worker node to cluster"""
        await self.db.execute(
            text("SELECT citus_add_node(:host, :port)"), {"host": host, "port": port}
        )
        await self.db.commit()
        return {"status": "added", "message": f"Worker {host}:{port} added to cluster"}

    async def get_shard_distribution(self, table_name: str = "messages"):
        """Get current shard distribution across nodes"""
        result = await self.db.execute(
            text(
                """
            SELECT 
                nodename, 
                nodeport,
                count(*) as shard_count,
                pg_size_pretty(sum(shard_size)) as total_size
            FROM citus_shards 
            WHERE table_name = :table
            GROUP BY nodename, nodeport
            ORDER BY nodename
        """
            ),
            {"table": table_name},
        )

        rows = result.fetchall()
        return [
            {"node": f"{row[0]}:{row[1]}", "shard_count": row[2], "total_size": row[3]}
            for row in rows
        ]

    async def get_rebalancer_status(self):
        """Get current rebalancer status"""
        try:
            result = await self.db.execute(
                text("SELECT * FROM citus_rebalancer_status()")
            )
            row = result.fetchone()

            if row:
                return {
                    "active": row[0] if len(row) > 0 else False,
                    "message": "Rebalancer status retrieved",
                }
            else:
                return {"active": False, "message": "No rebalancer activity"}

        except Exception as e:
            return {"active": False, "message": f"Could not get status: {str(e)}"}
