from models import Book, Cart

def build_cart(n_items=1, quantity=100000):
    c = Cart()
    b = Book("Perf", "Test", 1.0, "")
    c.add_book(b, quantity)
    return c

if __name__ == "__main__":
    import timeit
    c = build_cart()
    t = timeit.timeit("c.get_total_price()", number=50, globals=globals())
    print(f"timeit: get_total_price() x50 -> {t:.4f}s")
