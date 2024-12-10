class AverageStrategy:
    def calculate(self, data):
        pass

class ArithmeticMeanStrategy(AverageStrategy):
    def calculate(self, data):
        if len(data) == 0:
            return 0
        return sum(data) / len(data)

class GeometricMeanStrategy(AverageStrategy):
    def calculate(self, data):
        if len(data) == 0:
            return 0
        product = 1
        for num in data:
            product *= num
        return product ** (1 / len(data))

class HarmonicMeanStrategy(AverageStrategy):
    def calculate(self, data):
        if len(data) == 0 or 0 in data:
            return 0
        return len(data) / sum(1 / num for num in data)

class Context:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, data):
        return self.strategy.calculate(data)

numbers = [1, 2, 3, 4, 5]

strategies = [
    ArithmeticMeanStrategy(),
    GeometricMeanStrategy(),
    HarmonicMeanStrategy()
]

results = []
context = Context(None)

for strat in strategies:
    context.set_strategy(strat)
    res = context.execute_strategy(numbers)
    results.append(res)
    print(f"Результат {strat.__class__.__name__}: {res}")

print("Максимальное значение:", max(results))
print("Минимальное значение:", min(results))
