from abc import ABC, abstractmethod


class MenuItem(ABC):

  def __init__(self, name: str, base_price: float):
    self.name = name
    self.base_price = base_price

  @abstractmethod
  def calculate_price(self) -> float:
    """Рассчитывает итоговую стоимость конкретного блюда."""
    pass

  @abstractmethod
  def get_display_name(self) -> str:
    """Возвращает название блюда (с учетом особенностей)."""
    pass


class Pizza(MenuItem):

  def __init__(self, name: str, base_price: float, size: str):
    super().__init__(name, base_price)
    self.size = size  # 'small', 'medium', 'large'

  def calculate_price(self) -> float:
    if self.size.lower() == "large":
      return self.base_price * 1.3  
    return self.base_price

  def get_display_name(self) -> str:
    return f"Пицца '{self.name}' (размер: {self.size})"


class Drink(MenuItem):

  def __init__(self, name: str, base_price: float, is_ice: bool = False):
    super().__init__(name, base_price)
    self.is_ice = is_ice

  def calculate_price(self) -> float:
    return self.base_price  

  def get_display_name(self) -> str:
    if self.is_ice:
      return f"{self.name} со льдом"
    return self.name


class ComboSet(MenuItem):

  def __init__(self, name: str, items: list[MenuItem] = None):
    super().__init__(name, 0.0)
    self.items = items if items else []

  def add_item(self, item: MenuItem):
    self.items.append(item)

  def calculate_price(self) -> float:
    total = sum(item.calculate_price() for item in self.items)
    return total * 0.85  # Скидка 15% на весь сет

  def get_display_name(self) -> str:
    sub_items = ", ".join([i.get_display_name() for i in self.items])
    return f"Комбо-сет '{self.name}' [Содержит: {sub_items}]"
