from bot import dp
from middlewares.throttling import ThrottlingMiddleware

dp.middleware.setup(ThrottlingMiddleware(limit=0.5))