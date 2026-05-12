def quantiles(data, levels, weights=None):
    """Type 2 quantiles for sorted data, possibly weighted"""
    # https://robjhyndman.com/papers/sample_quantiles.pdf
    assert all(0 <= a < b <= 1 for a, b in zip(levels, levels[1:]))
    total = len(data) if weights is None else sum(weights)
    targets = [level * total for level in levels]
    level_index = 0
    value = float('-inf')
    cumulative = 0
    results = []
    for index in range(len(data)):
        assert data[index] >= value, 'data must be sorted'
        value = data[index]
        weight = 1 if weights is None else weights[index]
        assert weight > 0, 'weights must be positive'
        cumulative += weight
        while level_index < len(levels) and cumulative > targets[level_index]:
            results.append(value)
            level_index += 1
        if level_index < len(levels) and cumulative == targets[level_index]:
            next_value = data[index + 1] if index + 1 < len(data) else value
            results.append((value + next_value) / 2)
            level_index += 1
    return results


assert quantiles([1, 2, 3], [0.5]) == [2]
assert quantiles([1, 2], [0.5]) == [1.5]
assert quantiles([1, 2], [0.5, 0.8], [4, 1]) == [1, 1.5]
assert quantiles([1, 2, 3, 4, 5], [1]) == [5]
assert quantiles([1, 2, 3, 4, 5], [0.5, 1]) == [3, 5]
