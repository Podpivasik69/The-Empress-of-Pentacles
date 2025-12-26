a, b = [], []
for _ in range(10):
    a.append(_ + 1)
    b.append(_ + 1)
for _1 in range(10):
    for _2 in range(10):
        if _2 % 10 == 0:
            print('------')
        print(f'{a[_1]} * {b[_2]} = {a[_1] * b[_2]}')
