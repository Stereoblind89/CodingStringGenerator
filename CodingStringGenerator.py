import pandas as pd
import re


def load_option_codes(mfal_loc):
    df = pd.read_excel(mfal_loc, index_col=None, na_values=['NA'], usecols="A,H")
    df = df[5:288]

    codes = df.iloc[:, 0]
    codes = codes.tolist()
    codes.extend(['TWB1', 'RK05', 'PRG1', 'LA01', 'HB00', 'GDO1', 'FPF1', 'HODL'])
    active = df.iloc[:, 1]
    active = active.tolist()
    active.extend(['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'])

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

    string_value = df.iloc[:, 0]
    string_value = string_value.tolist()

    did_value = df.iloc[:, 1]
    did_value = did_value.tolist()

    segment_value = df.iloc[:, 2]
    segment_value = segment_value.tolist()

    for i, value in enumerate(string_value):
        no_spaces = str(value).replace(' ', '')
        no_spaces = str(no_spaces).replace('$', '')
        string_value[i] = no_spaces

    return_set = list(zip(string_value, did_value, segment_value))

    return return_set


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


def evaluate_option_rules(loc, codes):
    df = pd.read_excel(loc, sheet_name=0, index_col=None, na_values=['NA'], usecols="B, C, D, E, I, O")
    df = df[10:]

    start_byte = df.iloc[:, 0]
    start_byte = start_byte.tolist()

    start_bit = df.iloc[:, 1]
    start_bit = start_bit.tolist()

    data_value = df.iloc[:, 2]
    data_value = data_value.tolist()

    data_length = df.iloc[:, 3]
    data_length = data_length.tolist()

    aston_rule = df.iloc[:, 4]
    aston_rule = aston_rule.tolist()

    segment = df.iloc[:, 5]
    segment = segment.tolist()

    rule_result = []

    for i, value in enumerate(aston_rule):
        rule = str(aston_rule[i])
        rule = ''.join(rule)
        codes_in_rule, full_rule = process_rule(rule)

        for j, op_code in enumerate(codes_in_rule):
            if not codes_in_rule[0] == '1' and not codes_in_rule[0] == '0':
                if op_code not in codes:
                    dictionary_val = str(0)
                else:
                    dictionary_val = str(codes.get(op_code))

                full_rule = full_rule.replace(op_code, dictionary_val)
                full_rule = str(full_rule).replace("[", "")
                full_rule = str(full_rule).replace("]", "")
            else:
                full_rule = str(codes_in_rule[0])

        rule_result.append(eval(str(full_rule)))

    coding_string_data = list(zip(start_byte, start_bit, data_value, data_length, rule_result, segment))

    return coding_string_data


def edit_original_coding(lines, original):

    final_string = []
    return final_string


option_codes_loc = "1PT MFAL AM800.xlsx"
coding_table_loc = "HVAC222-HVAC222_HVAC_HSW11-00.08.00-C093-19.14.01.xlsx"

option_codes = load_option_codes(option_codes_loc)
original_coding = get_original_coding(coding_table_loc)

coding_string_data = evaluate_option_rules(coding_table_loc, option_codes)
print(original_coding[0][0])
final_string = edit_original_coding(coding_string_data, original_coding)
