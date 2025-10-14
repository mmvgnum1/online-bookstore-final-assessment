import cProfile, pstats, io
from models import PaymentGateway

def run_many(n=500):
    for _ in range(n):
        PaymentGateway.process_payment({
            "payment_method": "credit_card",
            "card_number": "4242424242424242",
            "expiry_date": "12/30",
            "cvv": "123"
        })

if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    run_many()
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("tottime")
    ps.print_stats(10)
    print(s.getvalue())
