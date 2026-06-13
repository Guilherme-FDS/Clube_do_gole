# services/scheduler.py
"""
Jobs periódicos do sistema.

Jobs ativos:
  - verificar_assinaturas_expiradas: diário às 03:00
    Marca como "expirada" toda assinatura ativa cujo proximo_ciclo já passou.
    Quando houver cobrança automática (Mercado Pago preapproval), substituir
    este job pela lógica de renovação.
"""
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("clube_do_gole.scheduler")

scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")


async def _verificar_expiradas() -> None:
    from database.engine import AsyncSessionLocal
    from repositories import assinatura_repo

    async with AsyncSessionLocal() as db:
        expiradas = await assinatura_repo.listar_ativas_expiradas(db)
        if not expiradas:
            return
        for a in expiradas:
            await assinatura_repo.atualizar_status(db, a.id, "expirada")
            logger.info(f"Assinatura #{a.id} (cliente #{a.id_cliente}) marcada como expirada.")
        await db.commit()
        logger.info(f"Job expiração: {len(expiradas)} assinatura(s) expirada(s).")


def iniciar_scheduler() -> None:
    scheduler.add_job(
        _verificar_expiradas,
        trigger=CronTrigger(hour=3, minute=0),
        id="verificar_expiradas",
        replace_existing=True,
        misfire_grace_time=3600,
    )
    scheduler.start()
    logger.info("Scheduler iniciado.")
