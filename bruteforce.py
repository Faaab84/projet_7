import csv
import sys
sys.setrecursionlimit(2000)


def read_file(filename):
    """Lire le csv puis retourner une liste actions."""

    actions = []
    with open(filename, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            name = row[0]
            cost = float(row[1])
            profit = float(row[2].strip('%')) / 100
            actions.append((name, cost, profit))
    return actions


def find_best_combination(max_budget, actions, index=0, current_combination=[],
                          best_combination={"total_profit": 0, "actions": []}):
    """Trouve la meilleure combinaison """

    total_cost = sum(cost for _, cost, _ in current_combination)
    total_profit = sum(cost * profit for _, cost, profit in current_combination)

    if total_cost <= max_budget and total_profit > best_combination["total_profit"]:
        best_combination["total_profit"] = total_profit
        best_combination["actions"] = current_combination[:]

    if index >= len(actions):
        return best_combination

    current_combination.append(actions[index])
    best_combination = find_best_combination(max_budget, actions, index + 1, current_combination, best_combination)

    current_combination.pop()
    best_combination = find_best_combination(max_budget, actions, index + 1, current_combination, best_combination)

    return best_combination


def display_results(best):
    """affiche les resultats."""

    print("les meilleurs combinaisons d'actions:")
    for action in best["actions"]:
        name, cost, profit = action
        print(f"{name} - Coût: {cost: .2f} €, Profit: {cost * profit: .2f} €")
    print(f"\nTotal des coût: {sum(cost for _, cost, _ in best['actions']): .2f} €")
    print(f"Total des profits apres 2 ans: {best['total_profit']: .2f} €")



def main():
    CSV_FILE = "actions.csv"
    MAX_BUDGET = 500.0

    actions = read_file(CSV_FILE)
    best_combination = find_best_combination(MAX_BUDGET, actions)
    display_results(best_combination)


if __name__ == "__main__":
    main()
