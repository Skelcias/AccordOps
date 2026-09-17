import csv

## Chargement des datasets

with open('dataset/policy.csv',newline='',encoding='utf-8') as file :
    reader = csv.DictReader(file)
    policy = list(reader)

with open('dataset/expenses.csv',newline='',encoding='utf-8') as file :
    reader = csv.DictReader(file)
    expenses = list(reader)

## fonction qui compare 2 item et print CONFORME  ou NON CONFORME + x e de non conformité

def compare_with_policy(policy_value:float,expense_value:float)->str:

    return 'Conforme' if policy_value - expense_value >= 0 else f'Non conforme de {policy_value - expense_value:.2f} $'
 
if __name__ == '__main__':
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

       

   for answer in answers:
      print(answer)


#gestion catégorie manquantes ou valeur pas convetisable en float 