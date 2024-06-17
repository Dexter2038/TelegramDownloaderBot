from aiogram import Router


def get_router() -> Router:
    from . import instagram, youtube, tiktok

    router = Router()

    router.include_router(instagram.router)
    router.include_router(youtube.router)
    router.include_router(tiktok.router)

    return router
