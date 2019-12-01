import collections
from lec_1.json.matplot_wine import create_map, create_bar


def dump_dict(obj):
    json = []
    for key, value in obj.items():
        if isinstance(value, list):
            json.append(''.join(['"', key, '":', dump_list(value), ',']))
        elif isinstance(value, dict):
            json.append(''.join(['"', key, '":', dump_dict(value), ',']))
        else:
            json.append(''.join(['"', key, '":', dump_simple_obj(value), ',']))
        result = ''.join(json)
    return f'{{{result[:-1]}}}'


def dump_list(obj):
    json = []
    for item in obj:
        if isinstance(item, dict):
            json.append(''.join([dump_dict(item), ',']))
        elif isinstance(item, list):
            json.append(''.join([dump_list(item), ',']))
        else:
            json.append(''.join([dump_simple_obj(item), ',']))
    result = ''.join(json)
    return f'[{result[:-1]}]'


def dump_simple_obj(obj):
    if isinstance(obj, str):
        return f'"{obj}"'
    if isinstance(obj, (int, float)):
        return str(obj)
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return ''.join(['"', str(obj).lower(), '"'])
    raise ValueError('This type is not supported in json')


def dump(obj):
    if isinstance(obj, dict):
        return dump_dict(obj)
    if isinstance(obj, list):
        return dump_list(obj)
    else:
        raise ValueError('This type is not supported in json')


def get_dict_list(start):
    if start in [' ', '\n', ',']:
        return [None, 1, 1]
    elif start == '{':
        return ['dict', 'open', 1]
    elif start == '}':
        return ['dict', 'close', 1]
    elif start == '[':
        return ['list', 'open', 1]
    elif start == ']':
        return ['list', 'close', 1]
    else:
        raise ValueError('json is incorrect')


def get_number(position, s, signal):
    pos = 1
    while s[pos + position].isnumeric() or s[pos + position] == '.':
        signal += s[pos + position]
        pos += 1
    token = ['value', float(signal), len(signal)]
    return token


def get_string(position, s):
    signal = ''
    pos = 1
    while s[pos + position] != '"' or s[pos + position - 1] == '\\':
        signal += s[pos + position]
        pos += 1
    if s[pos + position + 1] == ':':
        token = ['key', signal, pos + 2]
    else:
        token = ['value', signal, pos + 1]
    return token


def get_bool_none(signal):
    if signal == 'n':
        token = ['value', None, 4]
    elif signal == 't':
        token = ['value', True, 4]
    else:
        token = ['value', False, 5]
    return token


def parse(s):
    result = []
    position = 0
    while s:
        signal = s[position]
        if not (signal.isalnum() or signal == '"'):
            token = get_dict_list(signal)
        elif signal == '"':
            token = get_string(position, s)
        elif signal.isnumeric():
            token = get_number(position, s, signal)
        else:
            token = get_bool_none(signal)
        position += token[2]
        if token[0]:
            if token[0] == 'dict':
                if token[1] == 'open':
                    result.append({})
                else:
                    if len(result) == 1:
                        return result.pop()
                    closed_dict = result.pop()
                    if isinstance(result[-1], list):
                        result[-1].append(closed_dict)
                    else:
                        key = result.pop()
                        result[-1][key] = closed_dict
            elif token[0] == 'list':
                if token[1] == 'open':
                    result.append([])
                else:
                    if len(result) == 1:
                        return result.pop()
                    else:
                        closed_list = result.pop()
                        key = result.pop()
                        result[-1][key] = closed_list
            elif token[0] == 'key':
                result.append(token[1])
            elif token[0] == 'value':
                key = result.pop()
                result[-1][key] = token[1]


def create_full_sorted_json(wine_1, wine_2):
    with open(wine_1, 'r') as file:
        json_1 = file.read()
    data_1 = parse(json_1)
    with open(wine_2, 'r') as file:
        json_2 = file.read()
    data_2 = parse(json_2)
    data_1.extend(data_2)
    full_data = set()
    for wine in data_1:
        full_data.add(dump(wine))
    winedata_full = []
    for wine in full_data:
        winedata_full.append(parse(wine))
    winedata_full.sort(
        key=lambda i: (
            -i['price'] if i['price'] is not None else 1,
            i['variety'] if i['variety'] is not None else '~'
        )
    )
    json = dump(winedata_full)
    with open('winedata_full.json', 'w') as file:
        file.write(json)
    return winedata_full


def prepare_data(varieties, winedata):
    highest_score = 0
    lowest_score = float(winedata[0]['points'])
    country_price = {}
    country_rating = {}
    commentators = {}
    for wine in winedata:
        if wine['points']:
            wine_points = float(wine['points'])
            if wine_points > highest_score:
                highest_score = wine_points
            else:
                if wine_points < lowest_score:
                    lowest_score = wine_points
        if wine['country']:
            if wine['price']:
                country_price.setdefault(wine['country'], [])
                country_price[wine['country']].append(wine['price'])
            if wine['points']:
                country_rating.setdefault(wine['country'], [])
                country_rating[wine['country']].append(wine_points)
            if wine['taster_twitter_handle']:
                commentators.setdefault(wine['taster_twitter_handle'], 0)
                commentators[wine['taster_twitter_handle']] += 1
        if wine['variety'] in varieties:
            varieties[wine['variety']].append(wine)
    return commentators, country_price, country_rating, highest_score,\
        lowest_score


def create_statisics_for_varieties(varieties):
    result = {'wine': {}}
    for variety, wines in varieties.items():
        if wines:
            result_for_wine = {}
            prices = []
            regions = []
            countries = []
            scores = []
            for wine in wines:
                if wine['price'] is not None:
                    prices.append(wine['price'])
                if wine['points'] is not None:
                    scores.append(float(wine['points']))
                if wine['region_1'] is not None:
                    regions.append(wine['region_1'])
                if wine['region_2'] is not None:
                    regions.append(wine['region_1'])
                if wine['country'] is not None:
                    countries.append(wine['country'])
            result_for_wine['average_price'] = sum(prices) / len(prices)
            result_for_wine['min_price'] = min(prices)
            result_for_wine['max_price'] = max(prices)
            result_for_wine['most_common_region'] = collections.Counter(
                regions).most_common(1)[0][0]
            result_for_wine['most_common_country'] = collections.Counter(
                countries).most_common(1)[0][0]
            result_for_wine['average_score'] = sum(scores) / len(scores)
            result['wine'][variety] = result_for_wine
        else:
            result['wine'][variety] = 'There is no data for this variety'
    return result


def create_statistics(winedata):
    varieties = {'Gew\\u00fcrztraminer': [], 'Riesling': [], 'Merlot': [],
                 'Madera': [], 'Tempranillo': [], 'Red Blend': []}
    commentators, country_price, country_rating, highest_score,\
        lowest_score = prepare_data(varieties, winedata)
    result = create_statisics_for_varieties(varieties)
    expensive_wine = [winedata[0]['price'], set()]
    cheapest_wine = [winedata[0]['price'], set()]
    for wine in winedata:
        if wine['price'] == expensive_wine[0]:
            expensive_wine[1].add(wine['title'])
        else:
            break
    result['most_expensive_wine'] = list(expensive_wine[1])
    for wine in reversed(winedata):
        if wine['price']:
            if cheapest_wine[0] == wine['price']:
                cheapest_wine[1].add(wine['title'])
            elif cheapest_wine[0] > wine['price']:
                cheapest_wine[0] = wine['price']
                cheapest_wine[1].add(wine['title'])
            else:
                break
    result['cheapest_wine'] = list(cheapest_wine[1])
    result['highest_score'] = highest_score
    result['lowest_score'] = lowest_score
    for country, price in country_price.items():
        country_price[country] = sum(price)/len(price)
    ordered_country_price = collections.Counter(country_price).most_common()
    country = ordered_country_price.pop(0)
    result['most_expensive_country'] = [country[0]]
    while country[1] == ordered_country_price[0][1]:
        country = ordered_country_price.pop(0)
        result['most_expensive_country'].append(country[0])
    country = ordered_country_price.pop()
    result['cheapest_country'] = [country[0]]
    while country[1] == ordered_country_price[-1][1]:
        country = ordered_country_price.pop()
        result['cheapest_country'].append(country[0])
    for country, rate in country_rating.items():
        country_rating[country] = sum(rate)/len(rate)
    ordered_country_raiting = collections.Counter(country_rating).most_common()
    country = ordered_country_raiting.pop(0)
    result['most_rated_country'] = [country[0]]
    while country[1] == ordered_country_raiting[0][1]:
        country = ordered_country_raiting.pop(0)
        result['most_rated_country'].append(country[0])
    country = ordered_country_raiting.pop()
    result['underrated_country'] = [country[0]]
    while country[1] == ordered_country_raiting[-1][1]:
        country = ordered_country_raiting.pop()
        result['underrated_country'].append(country[0])
    ordered_commentators = collections.Counter(commentators).most_common()
    commentator = ordered_commentators.pop(0)
    result['most_active_commentator'] = [commentator[0]]
    while commentator[1] == ordered_commentators[0][1]:
        commentator = ordered_commentators.pop(0)
        result['most_active_commentator'].append(commentator[0])
    result_to_json = {'statistics': result}
    json = dump(result_to_json)
    with open('stats.json', 'w') as file:
        file.write(json)
    return result


if __name__ == '__main__':
    winedata_full = create_full_sorted_json(
        'winedata_1.json', 'winedata_2.json')
    statistics = create_statistics(winedata_full)
    # create_map()
    # create_bar(statistics)
