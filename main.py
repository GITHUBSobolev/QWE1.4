from imports import * 
tk = Bot(token=token_ch, disable_web_page_preview=True);
ch = Dispatcher(tk)
keep_alive()
if __name__ == "__main__":
  executor.start_polling(ch, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)