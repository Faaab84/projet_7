import csv


def read_file(csv_file):
    """Lire le CSV et retourner une liste d'actions avec coûts positifs."""
    actions = []
    with open(csv_file, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            name = row[0]
            cost = float(row[1])
            profit = float(row[2].strip('%')) / 100
            if cost > 0:
                actions.append((name, cost, profit))
    return actions


def display_results(best):
    """affiche les resultats."""
    print("les meilleurs combinaisons d'actions:")
    for action in best["actions"]:
        name, cost, profit = action
        print(f"{name} - Coût: {cost:.2f} €, Profit: {cost * profit:.2f} €")
    print(f"\nTotal des coût: {sum(cost for _, cost, _ in best['actions']):.2f} €")
    print(f"Total des profits apres 2 ans: {best['total_benefit']:.2f} €")


def knapsack_dp(max_budget, datas):
    """Utilise la programmation dynamique pour trouver la meilleure combinaison d'actions."""
    n = len(datas)
    max_budget = int(max_budget * 100)
    costs = [int(cost * 100) for _, cost, _ in datas]
    benefits = [int(cost * benefit * 100) for _, cost, benefit in datas]
    dp = [[0] * (max_budget + 1) for _ in range(n + 1)]
    keep = [[False] * (max_budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(max_budget + 1):
            if costs[i - 1] <= w and costs[i - 1] > 0:
                if dp[i - 1][w - costs[i - 1]] + benefits[i - 1] > dp[i - 1][w]:
                    dp[i][w] = dp[i - 1][w - costs[i - 1]] + benefits[i - 1]
                    keep[i][w] = True
                else:
                    dp[i][w] = dp[i - 1][w]
            else:
                dp[i][w] = dp[i - 1][w]

    w = max_budget
    selected_actions = []
    for i in range(n, 0, -1):
        if keep[i][w]:
            selected_actions.append(datas[i - 1])
            w -= costs[i - 1]

    total_benefit = dp[n][max_budget] / 100.0
    selected_actions.reverse()
    return {
        "total_benefit": total_benefit,
        "actions": selected_actions
    }


if __name__ == "__main__":
    CSV_FILE = "data/dataset2.csv"
    MAX_BUDGET = 500.0
    actions = read_file(CSV_FILE)
    result = knapsack_dp(MAX_BUDGET, actions)
    display_results(result)
