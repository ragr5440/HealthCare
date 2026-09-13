from src.governance.runtime_budget import (
    validate_budget,
)

query = "hello " * 5000

result = validate_budget(
    query
)

print(result)