import csv

def read_csv(path:str)->list:
   with open(path,newline='',encoding="utf-8") as file:
      reader = csv.DictReader(file)
      return list(reader)
   
def compare_with_policy(policy_value:float,expense_value:float)->str:
    return 'Conforme' if  expense_value - policy_value <= 0 else f'Non conforme de {expense_value - policy_value:.2f} $'

def compare_policy_to_expense(policy:list,expenses:list)->list:
   answers = []
   policy_by_category = {} 
   for rule in policy:
       policy_by_category[rule["category"]] = float(rule["max_amount"])

   for expense in expenses:
    amount = expense["amount"]
    category = expense["category"] 
   
    if category not in policy_by_category:
        print(f"Catégorie inconnue : {category}")
        continue
    try:
        amount = float(amount)
    except ValueError:
        print(f"Montant invalide ! : {amount}")
        continue
   
    answers.append(
        compare_with_policy(
               policy_by_category[category],
               amount
            )
         )

   return answers
if __name__ == '__main__':
   

   policy = read_csv('dataset/policy.csv')
   expenses = read_csv('dataset/expenses.csv')
        
   answers:list = compare_policy_to_expense(policy,expenses)

   for answer in answers:
      print(answer)


#gestion catégorie manquantes ou valeur pas convetisable en float 