pizza = {'ground pepper', 'salt', 'cheese', 'sweet basil', 'dough', 'oregano',
         'pepperoni', 'garlic', 'tomatoes', 'onion'}
shaverma = {'cabbage', 'fried chicken', 'cucumbers', 'sauce', 'lavash',
            'tomatoes', 'onion'}
size_pizza = len(pizza)
print('size_pizza', size_pizza)
size_shaverma = len(shaverma)
print('size_shaverma', size_shaverma)
salt_in_pizza = 'salt' in pizza
print('salt_in_pizza', salt_in_pizza)
salt_in_shaverma = 'salt' in shaverma
print('salt_in_shaverma', salt_in_shaverma)
pizza_and_shaverma_absolutly_differ = pizza.isdisjoint(shaverma)
print(
    'pizza_and_shaverma_absolutly_differ', pizza_and_shaverma_absolutly_differ)
pizza_is_shaverma = pizza == shaverma
print('pizza_is_shaverma', pizza_is_shaverma)
pizza_is_the_part_of_shaverma = pizza.issubset(shaverma)
print('pizza_is_the_part_of_shaverma', pizza_is_the_part_of_shaverma)
shaverma_is_the_part_of_pizza = pizza.issuperset(shaverma)
print('shaverma_is_the_part_of_pizza', shaverma_is_the_part_of_pizza)
pizza_and_shaverma = pizza.union(shaverma)
print('pizza_and_shaverma', pizza_and_shaverma)
common_ingredients = pizza.intersection(shaverma)
print('common_ingredients', common_ingredients)
only_in_pizza = pizza.difference(shaverma)
print('only_in_pizza', only_in_pizza)
in_pizza_or_in_shaverma = pizza.symmetric_difference(shaverma)
print('in_pizza_or_in_shaverma', in_pizza_or_in_shaverma)
one_more_pizza = pizza.copy()
print('one_more_pizza', one_more_pizza)
one_more_pizza.update(shaverma)
print('pizza+shaverma', one_more_pizza)
one_more_pizza = pizza.copy()
one_more_pizza.intersection_update(shaverma)
print('common ingredients', one_more_pizza)
one_more_pizza = pizza.copy()
one_more_pizza.difference_update(shaverma)
print('only in pizza', one_more_pizza)
one_more_pizza = pizza.copy()
one_more_pizza.symmetric_difference_update(shaverma)
print('special for pizza or shaverma', one_more_pizza)
one_more_pizza = pizza.copy()
one_more_pizza.add('pastry')
print('pizza with pastry', one_more_pizza)
one_more_pizza = pizza.copy()
one_more_pizza.remove('cheese')
one_more_pizza.discard('onion')
print('pizza wo cheese', one_more_pizza)
one_more_pizza = pizza.copy()
ingredient = one_more_pizza.pop()
print('pizza wo', ingredient, one_more_pizza)
one_more_pizza = pizza.copy()
one_more_pizza.clear()
print('no pizza', one_more_pizza)










