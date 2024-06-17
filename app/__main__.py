from __init__ import prepare_bot_dispatcher

import asyncio

if __name__ == '__main__':
    bot, dp = prepare_bot_dispatcher()
    asyncio.run(dp.start_polling(bot))
