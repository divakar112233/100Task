# Currency Converter

usd_to_inr = 83.5
eur_to_inr = 90.2

print("1. USD to INR")
print("2. EUR to INR")

choice = input("Choose an option (1 or 2): ")

amount = float(input("Enter amount: "))

if choice == "1":
    converted = amount * usd_to_inr
    print(f"{amount} USD = {converted:.2f} INR")

elif choice == "2":
    converted = amount * eur_to_inr
    print(f"{amount} EUR = {converted:.2f} INR")

else:
    print("Invalid choice!")