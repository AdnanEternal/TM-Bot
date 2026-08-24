from core.database_manager import DatabaseManager

TABLE_NAME = "ai_gateway_models"


async def ensure_table(db: DatabaseManager) -> None:
    await db.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            plugin_id INTEGER NOT NULL,


            label TEXT NOT NULL,
            model_id TEXT NOT NULL,
            base_url TEXT NOT NULL,
            api_key TEXT NOT NULL,

            is_active INTEGER NOT NULL DEFAULT 0,
            
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (plugin_id)
                REFERENCES plugins(id)
                ON DELETE CASCADE,
            
            UNIQUE(plugin_id, label)
        )
        """
    )


async def add_model(
    db: DatabaseManager,
    *,
    plugin_id: int,
    label: str,
    base_url: str,
    api_key: str,
    model_id: str,
) -> None:
    
    await db.execute(
        f"""
        INSERT INTO {TABLE_NAME} 
        (
            plugin_id,
            label, 
            model_id, 
            base_url, 
            api_key
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            plugin_id,
            label, 
            model_id, 
            base_url, 
            api_key
        ),
    )

async def set_active_model(
    db: DatabaseManager,
    label: str,
) -> bool:
    model = await db.fetchone(
        f"""
        SELECT id
        FROM {TABLE_NAME}
        WHERE label = ?
        """,
        (label,),
    )

    if not model:
        return False

    await db.execute(
        f"""
        UPDATE {TABLE_NAME}
        SET is_active = 0
        """
    )

    await db.execute(
        f"""
        UPDATE {TABLE_NAME}
        SET is_active = 1
        WHERE label = ?
        """,
        (label,),
    )

    return True


async def list_models(db: DatabaseManager):
    return await db.fetchall(
        f"""
        SELECT label, model_id, base_url, is_active
        FROM {TABLE_NAME}
        ORDER BY id
        """
    )


async def get_active_model(db: DatabaseManager):
    return await db.fetchone(
        f"""
        SELECT label, model_id, base_url, api_key
        FROM {TABLE_NAME}
        WHERE is_active = 1
        """
    )