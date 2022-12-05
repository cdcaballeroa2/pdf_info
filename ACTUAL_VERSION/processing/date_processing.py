import glob
import os
import re
from datetime import datetime
import pandas as pd


def validate_date(dat):
    try:
        date_time = datetime.strptime(dat, '%d/%m/%Y')
    except:
        try:
            date_time = datetime.strptime(dat, '%Y/%m/%d')
        except:
            date_time = None
    if date_time and date_time > datetime.now():
        date_time = None
    return date_time


def get_date_formated(str_data: str, offset: int = 35, save_text: bool = False):
    res = [
        r'(\d{1,4}([\-/])\d{1,2}([\-/])\d{1,4})',
    ]

    month_list = [
        'enero',
        'febrero',
        'marzo',
        'abril',
        'mayo',
        'junio',
        'julio',
        'agosto',
        'septiembre',
        'octubre',
        'noviembre',
        'diciembre'
    ]

    stopws = [
        'DESDE',
        'HASTA',
        'ENTRE',
        'Y EL'
    ]

    date_ranges = {}
    range_counter = 0
    data = str_data.lower().replace('\n', '')

    # FECHA FORMATEADA
    for rr in res:
        for match in re.finditer(rr, data):
            s = match.start()
            e = match.end()
            # +offset if e<len(data)-offset else len(data)
            start_text = s - offset if s > offset else 0
            str_all = data[start_text: e]
            for wd in stopws:
                if str_all.__contains__(wd.lower()):
                    pending = True
                    date_text = data[s:e].replace('-', '/')
                    # guardado de fechas y rango
                    # verifica el ultimo registro. si tiene coincidencias, lo incluye
                    if range_counter > 0:
                        if date_ranges[range_counter - 1]['end'] > start_text:
                            date_ranges[range_counter - 1]['text'] = data[date_ranges[range_counter - 1]['start']: e]
                            date_ranges[range_counter - 1]['end'] = e
                            date_ranges[range_counter - 1]['dates'].append(validate_date(date_text))
                            pending = False

                    if pending:
                        date_ranges[range_counter] = {
                            'text': str_all,
                            'start': start_text,
                            'end': e,
                            'dates': [validate_date(date_text)]
                        }
                        range_counter += 1
                    break

    # verifica si existen pares de fechas
    for text_i in list(date_ranges.keys()):
        if len(date_ranges[text_i]['dates']) < 2:
            for rr in res:
                for match in re.finditer(rr, date_ranges[text_i]['text']):
                    s = match.start()
                    e = match.end()
                    date_text = date_ranges[text_i]['text'][s:e].replace('-', '/')
                    date_text = validate_date(date_text)
                    if date_text not in date_ranges[text_i]['dates']:
                        date_ranges[text_i]['dates'].append(date_text)

    # FECHA, VERIFICACION POR MESES
    for rr in month_list:
        for match in re.finditer("(" + rr + ")", data):
            s = match.start()
            e = match.end()
            start_text = s - offset if s > offset else 0
            end_text = e + offset if e < len(data) - offset else len(data)
            str_all = data[start_text: end_text]
            for wd in stopws:
                if str_all.__contains__(wd.lower()):
                    pending = True
                    month_text = data[s:e]

                    ##verificacion de ano
                    all_year_text = data[e:e + 30]
                    year_text = None
                    for year_match in re.finditer('\d{4}', all_year_text):
                        ys = year_match.start()
                        ye = year_match.end()
                        year_text = all_year_text[ys:ye]
                        break
                    # Si no lo encuentra, retira esta opcion como fecha
                    if not year_text:
                        break

                    ##verificacion de dia
                    all_day_text = data[s - 10:s]
                    day_text = None
                    for day_match in re.finditer('\d{1,2}', all_day_text):
                        ds = day_match.start()
                        de = day_match.end()
                        day_text = all_day_text[ds:de]
                    # Si no lo encuentra, asume como 1
                    if not day_text:
                        day_text = 1

                    date_text = f'{day_text}/{month_list.index(month_text) + 1}/{year_text}'
                    date_text = validate_date(date_text)
                    # guardado de fechas y rango
                    # verifica el ultimo registro. si tiene coincidencias, lo incluye
                    if range_counter > 0:
                        for text_i in list(date_ranges.keys()):
                            if date_ranges[text_i]['end'] > start_text > date_ranges[text_i]['start']:
                                date_ranges[text_i]['text'] = data[date_ranges[text_i]['start']: end_text]
                                date_ranges[text_i]['end'] = end_text
                                date_ranges[text_i]['dates'].append(date_text)
                                pending = False

                            if date_ranges[text_i]['end'] > end_text > date_ranges[text_i]['start']:
                                date_ranges[text_i]['text'] = data[start_text: date_ranges[text_i]['end']]
                                date_ranges[text_i]['end'] = end_text
                                date_ranges[text_i]['dates'].append(date_text)
                                pending = False

                    if pending:
                        date_ranges[range_counter] = {
                            'text': str_all,
                            'start': start_text,
                            'end': e,
                            'dates': [date_text]
                        }
                        range_counter += 1
                    break

    org_lst = date_ranges.copy()
    # verifica si existen pares de fechas
    for text_i in list(date_ranges.keys()):
        if len(date_ranges[text_i]['dates']) < 2 or len(date_ranges[text_i]['dates']) > 2:
            date_ranges.pop(text_i)
        else:
            for dd in date_ranges[text_i]['dates']:
                if not dd:
                    date_ranges.pop(text_i)

    if not save_text:
        for key_date in date_ranges.keys():
            date_ranges[key_date]['text'] = ""

    return date_ranges


def date_cols(date_vals):
    if date_vals[1] and date_vals[0]:
        if date_vals[0] < date_vals[1]:
            return {'start_date': date_vals[0],
                    'end_date': date_vals[1]}
        else:
            return {'start_date': date_vals[1],
                    'end_date': date_vals[0]}
    else:
        return {'start_date': None,
                'end_date': None}


def get_data_ranges(date_data):
    dates_df = pd.DataFrame(date_data).T.dates.apply(lambda s: pd.Series(date_cols(s))).sort_values(by='start_date')
    dates_df.reset_index(drop=True, inplace=True)

    date_list = {}
    counter = 0
    for idx in range(len(dates_df)):
        st = dates_df['start_date'].iloc[idx]
        en = dates_df['end_date'].iloc[idx]
        if idx > 0:
            if st < date_list[counter]['end']:
                date_list[counter] = {
                    'start': date_list[counter]['start'],
                    'end': en
                }
            else:
                counter += 1
                date_list[counter] = {
                    'start': st,
                    'end': en
                }
        else:
            date_list[counter] = {
                'start': st,
                'end': en
            }

    time_work = 0
    for idx in list(date_list.keys()):
        time_work += (date_list[idx]['end'] - date_list[idx]['start']).days + 1

    return date_list, time_work


def get_dates_from_txt(str_data: str, offset: int = 35, print_dates: bool = False):
    date_data = get_date_formated(str_data, offset)
    try:
        date_ranges, days_worked = get_data_ranges(date_data)
        output = {
            'dates': date_data,
            'date_ranges': date_ranges,
            'experience': days_worked
        }
    except Exception as ex:
        output = {
            'dates': date_data,
            'date_ranges': [],
            'experience': 0
        }
    if print_dates:
        print(date_ranges)
    return output


def get_dates_from_person(date_data: dict):
    date_ranges, days_worked = get_data_ranges(date_data)
    output = {
        'date_ranges': date_ranges,
        'experience': days_worked
    }
    return output
