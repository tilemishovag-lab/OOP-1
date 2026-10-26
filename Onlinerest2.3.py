from Onlinerest import ComboSet, Drink, Pizza
from Onlinerest2Cus import CardPayment, CashPayment, Order

print("--- 1. Создание заказа и наполнение корзины ---")
my_order = Order()
print(f"Начальный статус заказа: {my_order.status}")

pizza_large = Pizza("Пепперони", 600.0, size="large")  # 600 * 1.3 = 780
cola = Drink("Кока-кола", 150.0, is_ice=True)

combo = ComboSet("Обед")
combo.add_item(Pizza("Маргарита", 500.0, size="small"))
combo.add_item(Drink("Сок", 200.0, is_ice=False))

my_order.add_item(pizza_large)
my_order.add_item(cola)
my_order.add_item(combo)

print(f"\nОбщая стоимость заказа: {my_order.get_total_cost():.2f} сом\n")

print("--- 2. Оплата заказа ---")
visa_card = CardPayment("4276123456789012", "12/28")
my_order.pay(visa_card)

print("\n--- 3. Проверка инкапсуляции (Защита данных) ---")
try:
  my_order.add_item(Drink("Чай", 100.0))
except ValueError as e:
  print(e)

print("\n--- 4. Дальнейшие шаги доставки ---")
my_order.next_step()  
my_order.next_step()  
