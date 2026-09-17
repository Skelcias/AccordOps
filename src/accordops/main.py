import csv
def read_csv(path:str)->list:
   with open(path,newline='',encoding="utf-8") as file:
      reader = csv.DictReader(file)
      return list(reader)
   
def compare_with_policy(policy_value:float,expense_value:float)->tuple[str,str | None]:
    return ('Conforme',None) if expense_value - policy_value <= 0 else ('non_conforme', f"{expense_value - policy_value:.2f}")

def compare_policy_to_expense(policy:list,expenses:list)->list:
   answers = []
   policy_by_category = {} 
   
   for rule in policy:
       policy_by_category[rule["category"]] = float(rule["max_amount"])

   for expense in expenses:
    errors = []
    amount = expense["amount"]
    category = expense["category"] 
    id = expense["id"]

    if category not in policy_by_category:
        errors.append("Catégorie inconnue")
        answers.append({
        "id": id,
        "category": category,
        "status": "ERROR",
        "difference": None,
        "error": errors,
    })
        continue

    try:
        amount = float(amount)
    except ValueError:
        errors.append("Montant Invalide") 
        answers.append({
        "id": id,
        "category": category,
        "status": "ERROR",
        "difference": None,
        "error": errors,
    })
        continue

    s,d = compare_with_policy(policy_by_category[category],amount)
    answers.append(
       {
          "id":id,
          "category":category,
          "status" : s,
          "difference" : d,
          "error" : errors

       }
    )
   return answers
if __name__ == '__main__':
   

   policy = read_csv('dataset/policy.csv')
   expenses = read_csv('dataset/expenses.csv')

   answers:list = compare_policy_to_expense(policy,expenses)

   for answer in answers:
      print(answer)


#gestion catégorie manquantes ou valeur pas convetisable en float 