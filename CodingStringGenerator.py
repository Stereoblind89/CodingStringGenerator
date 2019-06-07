import pandas as pd
import re


def load_option_codes(mfal_loc):
    df = pd.read_excel(mfal_loc, index_col=None, na_values=['NA'], usecols="A,H")
    df = df[5:]

    codes = df.iloc[:, 0]
    codes = codes.tolist()
    active = df.iloc[:, 1]
    active = active.tolist()

    dic = {}

    for index, optioncode in enumerate(codes):
        if active[index] == "X":
            active[index] = 1
        else:
            active[index] = 0

    codes_and_values = list(zip(codes, active))

    for i in range(len(codes_and_values)):
        if codes_and_values[i][0] in dic.keys():  # if key is present in the list, just append the value
            dic[codes_and_values[i][0]].append(codes_and_values[i][1])
        else:
            dic[codes_and_values[i][0]] = []  # else create a empty list as value for the key
            dic[codes_and_values[i][0]].append(codes_and_values[i][1])  # now append the value for that key

    return dic


def get_original_coding(original_coding_loc):
    df = pd.read_excel(original_coding_loc, sheet_name=1, index_col=None, na_values=['NA'], usecols="D,N,O")
    df = df[10:]

    df = df.values.tolist()

    for i, value in enumerate(df):
        no_spaces = str(value).replace(" ", "")
        no_spaces = str(no_spaces).replace("$", "")
        df[0][i] = no_spaces

    return df


def process_rule(coding_rule):
    current_value = ['(', coding_rule, ')']
    current_value = ''.join(current_value)
    current_value = str(current_value)
    current_value = str(current_value).replace("/", "|")
    current_value = str(current_value).replace("+", "&")
    current_value = str(current_value).replace(".", "_")
    current_value = str(current_value).replace("'", "")

    full_rule = current_value

    if current_value == '(;)':
        current_value = '1'
    elif current_value == '(-)':
        current_value = '0'

    non_alphanumeric = re.compile(r'\w+')
    current_value = non_alphanumeric.findall(current_value)

    return current_value, full_rule


def evaluate_option_rules(loc, codes, original_coding):
    df = pd.read_excel(loc, sheet_name=0, index_col=None, na_values=['NA'], usecols="I")
    df = df[10:]

    df = df.values.tolist()

    for i, value in enumerate(df):
        rule = str(df[i])[1:-1]
        rule = ''.join(rule)

        results, full_rule = process_rule(rule)

        for j, op_code in enumerate(results):
            if not results[0] == '1' and not results[0] == '0':
                if str(codes.get(op_code)) == 'None':
                    dictionary_val = str(0)
                else:
                    dictionary_val = str(codes.get(op_code))

                full_rule = full_rule.replace(op_code, dictionary_val)
                full_rule = str(full_rule).replace("[", "")
                full_rule = str(full_rule).replace("]", "")
            else:
                full_rule = str(results[0])

        print(i, ": ", full_rule)
        print(i, ": ", eval(str(full_rule)))


option_codes_loc = "1PT MFAL AM800.xlsx"
coding_table_loc = "HVAC222-HVAC222_HVAC_HSW11-00.08.00-C093-19.14.01.xlsx"

option_codes = load_option_codes(option_codes_loc)
original_coding = get_original_coding(coding_table_loc)

evaluate_option_rules(coding_table_loc, option_codes, original_coding)
