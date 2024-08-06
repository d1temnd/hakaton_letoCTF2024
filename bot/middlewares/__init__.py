from bot import router
from middlewares.throttling import ThrottlingMiddleware

router.message.middleware(ThrottlingMiddleware(sleep_sec=1))
