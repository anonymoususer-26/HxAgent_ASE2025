from config import GLOBAL_CONFIG

class ConsoleLogger:
  def instruction(content: str, *args) -> None:
    print('[INSTRUCTION] {}'.format(content), *args, end = " ")

  def info(content: str, *args) -> None:
    if GLOBAL_CONFIG['logger']['level'] <= 1:
      print('[INFO] {}'.format(content), *args)

  def warning(content: str, *args) -> None:
    if GLOBAL_CONFIG['logger']['level'] <= 2:
      print('[WARNING] {}'.format(content), *args)
      
  def error(content: str, *args) -> None:
    if GLOBAL_CONFIG['logger']['level'] <= 3:
      print('[ERROR] {}'.format(content), *args)