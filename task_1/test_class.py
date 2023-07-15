from Cities_class import Cities

a = Cities('test_data.json')

test_rand = {}
for i in range(1000):
    test = a.choice_random_city()
    if test not in test_rand:
        test_rand[test] = 0
    test_rand[test] += 1

print(test_rand)