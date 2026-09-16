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
   for expense in expenses:
       for rule in policy:
           if expense["category"] == rule["category"]:
               answers.append(compare_with_policy(float(rule["max_amount"]),float(expense["amount"])))


for elem in answers:
    print(elem)


