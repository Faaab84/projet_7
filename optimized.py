import csv


def read_file(csv_file):
    """Lire le CSV et retourner une liste d'actions avec coûts positifs."""
    actions = []
    with open(csv_file, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            name = row[0]
            cost = float(row[1])
            profit = float(row[2].strip('%')) / 100
            if cost > 0:
                actions.append((name, cost, profit))
    return actions


def start_optimized(csv, max_budget):
    """Point d'entrée principal pour le programme."""
    datas = read_file(csv)
    result = knapsack_dp(max_budget, datas)

    print("Meilleure combinaison d'actions:")
    for action in result["actions"]:
        action_name, cost, benefit = action
        print(f"{action_name} - Coût: {cost:.2f} €, Bénéfice: {cost * benefit:.2f} €")

    print(f"\nCoût total: {sum(cost for _, cost, _ in result['actions']):.2f} €")
    print(f"Bénéfice total après 2 ans: {result['total_benefit']:.2f} €")


def knapsack_dp(max_budget, datas):
    """Utilise la programmation dynamique pour trouver la meilleure combinaison d'actions."""
    n = len(datas)
    max_budget = int(max_budget * 100)  # Convertir en centimes
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
    CSV_FILE = "dataset1.csv"
    MAX_BUDGET = 500.0
    start_optimized(CSV_FILE, MAX_BUDGET)
