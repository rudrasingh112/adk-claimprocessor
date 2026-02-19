

def calculate_payout(claim_amount: float, deductible: float) -> float:
    """Calculates the final insurance payout after the deductible."""
    return max(0, claim_amount - deductible)

