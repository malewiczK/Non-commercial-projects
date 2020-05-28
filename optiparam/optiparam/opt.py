import sys
import os
from pathlib import Path

import pandas as pd
import click
from scipy.stats import ttest_ind
from .exceptions import EmptyTable, ColumnNameError
from .consts import *


def read_file(file_path):
    """ Expected csv format file """
    try:
        raw_data = pd.read_csv(file_path, index_col=0)
    except:
        filename = Path(file_path).name
        print(f"Unable to read file: {filename}")
        sys.exit(1)
    return raw_data


def check_formats(raw_data):
    if raw_data.empty:
        raise EmptyTable("No records to parse!")
    if [col for col in COLUMNS if col not in list(raw_data.columns)]:
        raise ColumnNameError("Divergence in columns names!")


def sort_pd_values(table):
    table = table.sort_values(PD_COL, ascending=True)
    table = table.reset_index(drop=True)
    return table


def divide_into_classes(table, num_class):
    df = table
    n_rows = df.shape[0]
    n_obs = round(n_rows / num_class)

    class_list = [i + 1 for i in range(num_class) for k in range(n_obs)]
    class_list_diff = n_rows - len(class_list)
    if class_list_diff < 0:
        class_list = class_list[:class_list_diff]
    elif class_list_diff > 0:
        add_list = [num_class for i in range(class_list_diff)]
        class_list.extend(add_list)

    df.insert(3, CLASS_COL, pd.Series(class_list))
    return df


def get_dummy_variables(table):
    df_dummy = pd.get_dummies(table[CLASS_COL])
    df_target = pd.concat([df_dummy, table[PD_COL]], axis=1)
    for col in df_dummy.columns:
        df_target[col] = df_target[col] * df_target[PD_COL]
    return df_target


def check_ttest(df, interval):
    df = df.iloc[:, :-1]
    t_score = list()
    class_name = None

    for col_1 in df.columns:
        for col_2 in df.columns:
            if col_1 < col_2:
                t_statistic = abs(ttest_ind(df[col_1], df[col_2])[0])
                p_value = ttest_ind(df[col_1], df[col_2])[1]
                if (1 - p_value) < interval:
                    if not t_score:
                        t_score.append(t_statistic)
                        class_name = (col_1, col_2)
                    if t_score:
                        if t_statistic < t_score[0]:
                            t_score[0] = t_statistic
                            class_name = (col_1, col_2)

    if t_score and class_name:
        return class_name
    return False


def merge_classes(df, class_names):
    lower_rank = min(class_names)
    higher_rank = max(class_names)
    df[CLASS_COL] = df[CLASS_COL].apply(lambda x: lower_rank if x == higher_rank else x)
    return df


def prepare_output(df):
    df_class = df.sort_values(CLASS_COL, ascending=True)
    df_class[CLASS_COL] = pd.factorize(df_class[CLASS_COL])[0] + 1
    df_class_grouped = df_class.groupby(CLASS_COL, as_index=False).agg(
        {PD_COL: "count"}
    )

    df_class_grouped.columns = [CLASS_COL, NUMBER]

    low_high_dict = dict()
    rating_classes = df_class[CLASS_COL].unique().tolist()
    for rank in sorted(rating_classes):
        low_high_dict[rank] = list()
        specified_df = df_class[df_class[CLASS_COL] == rank]
        low_high_dict[rank].append(specified_df[PD_COL].min())
        low_high_dict[rank].append(specified_df[PD_COL].max())
        low_high_dict[rank].append(specified_df[DEFAULT].sum() / specified_df.shape[0])

    low_high_df = pd.DataFrame.from_dict(low_high_dict, orient="index")
    low_high_df = low_high_df.reset_index()
    low_high_df.columns = COLUMNS_LOW_HIGH
    df_class_grouped = pd.merge(df_class_grouped, low_high_df, on=CLASS_COL, how="left")

    output_file_group = os.path.join(os.getcwd(), "optiparam.csv")
    output_file_df = os.path.join(os.getcwd(), "df.csv")
    df_class_grouped.to_csv(output_file_group, index=False)
    df_class.to_csv(output_file_df, index=False)


@click.command("optiparam")
@click.option(
    "--file_path", "-f", type=str, required=True, help="Specifies path to the file"
)
@click.option(
    "--n_classes",
    "-n",
    type=int,
    required=True,
    help="Specifies initial number of classes",
)
@click.option(
    "--interval", "-i", type=int, required=True, help="Specifies confidence interval"
)
def main(**click_args):

    file_path = click_args["file_path"]
    num_class = click_args["n_classes"]
    interval = click_args["interval"] / 100
    print(f"Processing: {file_path}")

    raw_data = read_file(file_path)
    try:
        check_formats(raw_data)
    except (EmptyTable, ColumnNameError):
        sys.exit(1)

    sorted_df = sort_pd_values(raw_data)
    df_class = divide_into_classes(sorted_df, num_class)
    df_dummy = get_dummy_variables(df_class)
    class_names = check_ttest(df_dummy, interval)
    print("Merging rating groups")
    while class_names:
        df_class = merge_classes(df_class, class_names)
        df_dummy = get_dummy_variables(df_class)
        class_names = check_ttest(df_dummy, interval)

    prepare_output(df_class)
    print("Output ready!")
