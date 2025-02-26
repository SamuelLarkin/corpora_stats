# corpora-stats

A CLI tool to calculate _count_, _min_, _max_, _mean_, _sdev_ for _bytes_, _chars_, _words_ & _lines_ for corpora files.

## Install

Create a virtual environment.

```sh
uv venv --relocatable --python=3.12 --prompt=corpora-stats venv
```

Activate the newly created environment.

```sh
source venv/bin/activate ""
```

Install the version from github.

```sh
uv pip install git+https://github.com/SamuelLarkin/corpora_stats
```

### Development

```sh
uv pip install -e .[dev]
```

### One file

[PyInstaller Manual](https://pyinstaller.org/en/stable/index.html)
Install `corpora-stats` as a one binary file.

First install the required tools to package python files in a single executable bundle.

```sh
uv pip install -e .[install]
```

Create the single file and install it.

```sh
pyinstaller --onefile venv/bin/corpora-stats
install dist/corpora-stats ~/.local/bin/
```

## Examples

### Table

```sh
corpora-stats \
  OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz \
  OPUS-qed-v2.0a-jpn-zho.jpn.gz
```

| line  | filename                               | byte_count | byte_min | byte_max | byte_mean | byte_sdev | char_count | char_min | char_max | char_mean | char_sdev | word_count | word_min | word_max | word_mean | word_sdev |
| ----- | -------------------------------------- | ---------- | -------- | -------- | --------- | --------- | ---------- | -------- | -------- | --------- | --------- | ---------- | -------- | -------- | --------- | --------- |
| 16439 | OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz | 2346756    | 3        | 1153     | 142.755   | 99.7559   | 2335033    | 3        | 1121     | 142.042   | 99.1905   | 377445     | 1        | 173      | 22.9603   | 16.4108   |
| 18098 | OPUS-qed-v2.0a-jpn-zho.jpn.gz          | 908633     | 3        | 262      | 50.2063   | 24.7079   | 326297     | 2        | 98       | 18.0295   | 8.74576   | 26421      | 1        | 14       | 1.45989   | 0.898058  |

| OVERALL | count   | min   | max   | mean     | sdev    |
| ------- | ------- | ----- | ----- | -------- | ------- |
| line    | 34537   | 16439 | 18098 | 17268.50 | 1173.09 |
| bytes   | 3255389 | 3     | 1153  | 94.26    | 84.81   |
| char    | 2661330 | 2     | 1121  | 77.06    | 92.52   |
| word    | 403866  | 1     | 173   | 11.69    | 15.62   |

### Latex

```sh
corpora-stats \
  --tablefmt=latex \
  OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz \
  OPUS-qed-v2.0a-jpn-zho.jpn.gz
```

```latex
\begin{tabular}{rlrrrrrrrrrrrrrrr}
\hline
   line & filename                                 &   byte\_count &   byte\_min &   byte\_max &   byte\_mean &   byte\_sdev &   char\_count &   char\_min &   char\_max &   char\_mean &   char\_sdev &   word\_count &   word\_min &   word\_max &   word\_mean &   word\_sdev \\
\hline
  16439 & OPUS-elrc\_euipo\_2017-v1-eng-spa.eng.gz &    2346756 &          3 &       1153 &    142.755  &     99.7559 &    2335033 &          3 &       1121 &    142.042  &    99.1905  &     377445 &          1 &        173 &    22.9603  &   16.4108   \\
  18098 & OPUS-qed-v2.0a-jpn-zho.jpn.gz          &     908633 &          3 &        262 &     50.2063 &     24.7079 &     326297 &          2 &         98 &     18.0295 &     8.74576 &      26421 &          1 &         14 &     1.45989 &    0.898058 \\
\hline
\end{tabular}

\begin{tabular}{lrrrrr}
\hline
 OVERALL   &     count &   min &   max &     mean &    sdev \\
\hline
 line      &   34537 & 16439 & 18098 & 17268.50 & 1173.09 \\
 bytes     & 3255389 &     3 &  1153 &    94.26 &   84.81 \\
 char      & 2661330 &     2 &  1121 &    77.06 &   92.52 \\
 word      &  403866 &     1 &   173 &    11.69 &   15.62 \\
\hline
\end{tabular}
```

### json

```sh
corpora-stats \
  --json \
  --indent=2 \
  OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz \
  OPUS-qed-v2.0a-jpn-zho.jpn.gz
```

```json
{
  "filename": "OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz",
  "line": 16439,
  "byte": {
    "count": 2346756,
    "min": 3,
    "max": 1153,
    "mean": 142.7553987468824,
    "sdev": 99.7559119415633
  },
  "char": {
    "count": 2335033,
    "min": 3,
    "max": 1121,
    "mean": 142.0422775107975,
    "sdev": 99.19047183551605
  },
  "word": {
    "count": 377445,
    "min": 1,
    "max": 173,
    "mean": 22.96033822008638,
    "sdev": 16.410819917770535
  }
}
{
  "filename": "OPUS-qed-v2.0a-jpn-zho.jpn.gz",
  "line": 18098,
  "byte": {
    "count": 908633,
    "min": 3,
    "max": 262,
    "mean": 50.20626588573323,
    "sdev": 24.707898451034612
  },
  "char": {
    "count": 326297,
    "min": 2,
    "max": 98,
    "mean": 18.029450768040668,
    "sdev": 8.74576067068077
  },
  "word": {
    "count": 26421,
    "min": 1,
    "max": 14,
    "mean": 1.4598850701734998,
    "sdev": 0.8980579441234613
  }
}
{
  "line": {
    "count": 34537,
    "min": 16439,
    "max": 18098,
    "mean": 17268.5,
    "sdev": 1173.0901499884824
  },
  "bytes": {
    "count": 3255389,
    "min": 3,
    "max": 1153,
    "mean": 94.25801314532241,
    "sdev": 84.81046123072933
  },
  "char": {
    "count": 2661330,
    "min": 2,
    "max": 1121,
    "mean": 77.05735877464748,
    "sdev": 92.51505981061287
  },
  "word": {
    "count": 403866,
    "min": 1,
    "max": 173,
    "mean": 11.693719778787967,
    "sdev": 15.617674254706742
  }
}
```

### Using `mlr`

```sh
corpora-stats --json  OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz  OPUS-qed-v2.0a-jpn-zho.jpn.gz \
| head -n -1 \
| mlr --ijson --opprint --barred cat
```

+------------------------------------------------------------------+-------+----------+----------+----------+-------------------+--------------------+----------+----------+----------+--------------------+-------------------+----------+----------+----------+--------------------+--------------------+
| filename | line | byte.count | byte.min | byte.max | byte.mean | byte.sdev | char.count | char.min | char.max | char.mean | char.sdev | word.count | word.min | word.max | word.mean | word.sdev |
+------------------------------------------------------------------+-------+----------+----------+----------+-------------------+--------------------+----------+----------+----------+--------------------+-------------------+----------+----------+----------+--------------------+--------------------+
| wmt24-eng-spa/train-parts/OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz | 16439 | 2346756 | 3 | 1153 | 142.7553987468824 | 99.7559119415633 | 2335033 | 3 | 1121 | 142.0422775107975 | 99.19047183551605 | 377445 | 1 | 173 | 22.96033822008638 | 16.410819917770535 |
| wmt24-jpn-zho/train-parts/OPUS-qed-v2.0a-jpn-zho.jpn.gz | 18098 | 908633 | 3 | 262 | 50.20626588573323 | 24.707898451034612 | 326297 | 2 | 98 | 18.029450768040668 | 8.74576067068077 | 26421 | 1 | 14 | 1.4598850701734998 | 0.8980579441234613 |
+------------------------------------------------------------------+-------+----------+----------+----------+-------------------+--------------------+----------+----------+----------+--------------------+-------------------+----------+----------+----------+--------------------+--------------------+
