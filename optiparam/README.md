# Optiparam Algorithm

## Installation

Use command below to install all scripts:

```bash
pip install -e .
```
----

### Optiparam transfroms continuous output into discrete buckets. 

You can find sample data in:
* [Link to data](https://github.com/malewiczK/Non-commercial-projects/tree/master/optiparam/optiparam/data)

Output consists of two files: 
- df.csv: DataFrame with final rating classes
- optiparam.csv: Desired output 

Main script takes 4 arguments:
- File path (-f) - Specifies path to the file
- Number of classes (-n) - Specifies initial number of classes
- Interval (-i) - Specifies confidence interval

**IMPORTANT** 
Output is generated in current directory

### Usage

```bash
optiparam -f /full/path/to/file/in/csv/format.csv -n 50 -i 95
```

### To check click options type:

```bash
optiparam --help
```

------------------------------------------------------------------------------

### Desired output should look like below

| Rating | Number | Lower       | Higher      | Observed |
|--------|--------|-------------|-------------|----------|
| 1      | 200    | 0.000048600 | 0.000049600 | 0        |
| 2      | 1400   | 0.000049600 | 0.000100474 | 0        |
| 3      | 600    | 0.000051100 | 0.000098900 | 0        |
| 4      | 3000   | 0.000052300 | 0.000168400 | 0        |
| 5      | 3200   | 0.000056000 | 0.000063100 | 0        |
| 6      | 200    | 0.000063100 | 0.000083300 | 0        |
| 7      | 400    | 0.000083300 | 0.000089700 | 0        |
| 8      | 800    | 0.000085400 | 0.000087600 | 0        |
| 9      | 200    | 0.000168545 | 0.996797697 | 0.205    |
