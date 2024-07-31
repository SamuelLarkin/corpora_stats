# corpora-stats

A CLI tool to calculate _count_, _min_, _max_, _mean_, _sdev_ for _bytes_, _chars_, _words_ & _lines_ for corpus files.

## Install

```sh
python -m venv venv
source venv/bin/activate ""
```

```sh
python -m pip install git+https://github.com/SamuelLarkin/corpora_stats
```

### Development

```sh
python -p pip install -e .[dev]
```

## Examples

### Table

```sh
copora-stats \
  OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz \
  OPUS-qed-v2.0a-jpn-zho.jpn.gz
```

| line  | filename                               | byte_sum | byte_min | byte_max | byte_mean | byte_sdev | char_sum | char_min | char_max | char_mean | char_sdev | word_sum | word_min | word_max | word_mean | word_sdev |
| ----- | -------------------------------------- | -------- | -------- | -------- | --------- | --------- | -------- | -------- | -------- | --------- | --------- | -------- | -------- | -------- | --------- | --------- |
| 16439 | OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz | 2346756  | 3        | 1153     | 142.755   | 99.7559   | 2335033  | 3        | 1121     | 142.042   | 99.1905   | 377445   | 1        | 173      | 22.9603   | 16.4108   |
| 18098 | OPUS-qed-v2.0a-jpn-zho.jpn.gz          | 908633   | 3        | 262      | 50.2063   | 24.7079   | 326297   | 2        | 98       | 18.0295   | 8.74576   | 26421    | 1        | 14       | 1.45989   | 0.898058  |

| OVERALL | sum     | min   | max   | mean     | sdev    |
| ------- | ------- | ----- | ----- | -------- | ------- |
| line    | 34537   | 16439 | 18098 | 17268.50 | 1173.09 |
| bytes   | 3255389 | 3     | 1153  | 94.26    | 84.81   |
| char    | 2661330 | 2     | 1121  | 77.06    | 92.52   |
| word    | 403866  | 1     | 173   | 11.69    | 15.62   |

### Latex

```sh
copora-stats \
  --tablefmt=latex \
  OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz \
  OPUS-qed-v2.0a-jpn-zho.jpn.gz
```

```latex
\begin{tabular}{rlrrrrrrrrrrrrrrr}
\hline
   line & filename                                 &   byte\_sum &   byte\_min &   byte\_max &   byte\_mean &   byte\_sdev &   char\_sum &   char\_min &   char\_max &   char\_mean &   char\_sdev &   word\_sum &   word\_min &   word\_max &   word\_mean &   word\_sdev \\
\hline
  16439 & OPUS-elrc\_euipo\_2017-v1-eng-spa.eng.gz &    2346756 &          3 &       1153 &    142.755  &     99.7559 &    2335033 &          3 &       1121 &    142.042  &    99.1905  &     377445 &          1 &        173 &    22.9603  &   16.4108   \\
  18098 & OPUS-qed-v2.0a-jpn-zho.jpn.gz          &     908633 &          3 &        262 &     50.2063 &     24.7079 &     326297 &          2 &         98 &     18.0295 &     8.74576 &      26421 &          1 &         14 &     1.45989 &    0.898058 \\
\hline
\end{tabular}

\begin{tabular}{lrrrrr}
\hline
 OVERALL   &     sum &   min &   max &     mean &    sdev \\
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
copora-stats \
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
    "sum": 2346756,
    "min": 3,
    "max": 1153,
    "mean": 142.7553987468824,
    "sdev": 99.7559119415633
  },
  "char": {
    "sum": 2335033,
    "min": 3,
    "max": 1121,
    "mean": 142.0422775107975,
    "sdev": 99.19047183551605
  },
  "word": {
    "sum": 377445,
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
    "sum": 908633,
    "min": 3,
    "max": 262,
    "mean": 50.20626588573323,
    "sdev": 24.707898451034612
  },
  "char": {
    "sum": 326297,
    "min": 2,
    "max": 98,
    "mean": 18.029450768040668,
    "sdev": 8.74576067068077
  },
  "word": {
    "sum": 26421,
    "min": 1,
    "max": 14,
    "mean": 1.4598850701734998,
    "sdev": 0.8980579441234613
  }
}
{
  "line": {
    "sum": 34537,
    "min": 16439,
    "max": 18098,
    "mean": 17268.5,
    "sdev": 1173.0901499884824
  },
  "bytes": {
    "sum": 3255389,
    "min": 3,
    "max": 1153,
    "mean": 94.25801314532241,
    "sdev": 84.81046123072933
  },
  "char": {
    "sum": 2661330,
    "min": 2,
    "max": 1121,
    "mean": 77.05735877464748,
    "sdev": 92.51505981061287
  },
  "word": {
    "sum": 403866,
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
| filename | line | byte.sum | byte.min | byte.max | byte.mean | byte.sdev | char.sum | char.min | char.max | char.mean | char.sdev | word.sum | word.min | word.max | word.mean | word.sdev |
+------------------------------------------------------------------+-------+----------+----------+----------+-------------------+--------------------+----------+----------+----------+--------------------+-------------------+----------+----------+----------+--------------------+--------------------+
| wmt24-eng-spa/train-parts/OPUS-elrc_euipo_2017-v1-eng-spa.eng.gz | 16439 | 2346756 | 3 | 1153 | 142.7553987468824 | 99.7559119415633 | 2335033 | 3 | 1121 | 142.0422775107975 | 99.19047183551605 | 377445 | 1 | 173 | 22.96033822008638 | 16.410819917770535 |
| wmt24-jpn-zho/train-parts/OPUS-qed-v2.0a-jpn-zho.jpn.gz | 18098 | 908633 | 3 | 262 | 50.20626588573323 | 24.707898451034612 | 326297 | 2 | 98 | 18.029450768040668 | 8.74576067068077 | 26421 | 1 | 14 | 1.4598850701734998 | 0.8980579441234613 |
+------------------------------------------------------------------+-------+----------+----------+----------+-------------------+--------------------+----------+----------+----------+--------------------+-------------------+----------+----------+----------+--------------------+--------------------+
