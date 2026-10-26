from abc import ABC, abstractmethod
from datetime import datetime
from Onlinerest import MenuItem


class Order:
  STATUSES = ["CREATED", "PREPARING", "READY", "DELIVERED"]

  def __init__(self):
    self.__items: list[MenuItem] = []
    self.__status_index: int = 0  

  @property
  def status(self) -> str:
    return self.STATUSES[self.__status_index]

  def next_step(self):
    """Переводит заказ на следующий этап."""
    if self.__status_index < len(self.STATUSES) - 1:
      self.__status_index += 1
      print(f"🔄 Статус заказа обновлен: **{self.status}**")
    else:
      print("⚠️ Заказ уже доставлен.")

  def add_item(self, item: MenuItem):
    """Добавляет блюдо, если заказ еще не начал готовиться."""
    if self.__status_index >= 1:
      raise ValueError(
          "❌ Ошибка: Нельзя добавить блюдо в заказ, который уже готовится или"
          " готов!"
      )
    self.__items.append(item)
    print(f"✅ Добавлено в заказ: {item.get_display_name()}")

  def get_total_cost(self) -> float:
    """Считает сумму всех calculate_price() элементов в заказе."""
    return sum(item.calculate_price() for item in self.__items)

  def pay(self, payment_method: "PaymentStrategy") -> bool:
    """Принимает любой способ оплаты и вызывает в нём нужный метод."""
    total = self.get_total_cost()
    print(f"\n💳 Сумма к оплате: {total:.2f} сом.")
    success = payment_method.collect_payment(total)

    if success and self.status == "CREATED":
      self.next_step()  # Переход в PREPARING при успешной оплате
    return success


class PaymentStrategy(ABC):

  @abstractmethod
  def collect_payment(self, amount: float) -> bool:
    pass


class CardPayment(PaymentStrategy):

  def __init__(self, card_number: str, expiry_date: str):
    self.__card_number = card_number
    self.expiry_date = expiry_date  # Формат "MM/YY"

  def collect_payment(self, amount: float) -> bool:
    print(
        f"|Банк| Проверка срока действия карты ****{self.__card_number[-4:]}..."
    )
    try:
      month_str, year_str = self.expiry_date.split("/")
      exp_month = int(month_str)
      exp_year = 2000 + int(year_str)

      now = datetime.now()
      if exp_year > now.year or (
          exp_year == now.year and exp_month >= now.month
      ):
        print(f"|Банк| Успешно списано {amount:.2f} сом с карты.")
        return True
      else:
        print("❌ Ошибка: Срок действия карты истек!")
        return False
    except Exception:
      print("❌ Ошибка: Неверный формат даты карты.")
      return False


class CashPayment(PaymentStrategy):

  def collect_payment(self, amount: float) -> bool:
    print(
        f"💵 Оплата наличными на сумму {amount:.2f} сом. Пожалуйста, передайте"
        " деньги курьеру."
    )
    return True
