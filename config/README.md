# Config

| Parameter | Description |
| ---- | ---- |
| depth | 回路のレイヤー数 |
| n_qubits | qubit数 |
| iter | VQE計算を実施する回数。各iterationごとに初期パラメータを変えて独立した計算を行う。 |
| optimizer.method | optimizer([scipy minimize](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)) |
| gate.type | "indirect_xy", "indirect_xyz", "indirect_ising" |
| gate.parametric_rotation_gate_set | 1レイヤー内に存在するパラメトリック量子ゲートの数 |
| gate.constraints |パラメータの制約条件([scipy minimize](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html))|
| gate.bounds |パラメータの上限、下限値([scipy minimize](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html))|
| gate.noise.singlequbit | ノイズを挿入する割合 [0.0, 1.0] |
| gate.noise.twoqubit | ノイズを挿入する割合 [0.0, 1.0] |
| gate.time.type | random: 時間発展ゲートの時刻パラメータ初期値をrandomにとる |
| gate.time.evol | "absolute": 時刻パラメータを絶対時刻とする |
| gate.time.min_val | 時刻の最小値(`gate.bounds`がTrueの時のみ有効) |
| gate.time.max_val | 時刻の最大値(`gate.bounds`がTrueの時のみ有効) |
| gate.time.init.min_val | 時刻パラメータの初期値の最小値 |
| gate.time.init.max_val | 時刻パラメータの初期値の最大値 |
| gate.bn.type | static: 磁場を固定値とする |
| gate.bn.value | 磁場の値(`gate.bn.type`が"static"の時のみ有効) |
| gate.cn.type | static: カップリング定数を固定値とする |
| gate.cn.value | カップリング定数値(`gate.cn.type`が"static"の時のみ有効) |
| gate.r.type | static: gammaを固定値とする |
| gate.r.value | gammaの値(`gate.r.type`が"static"の時のみ有効) |
| gcp.bigquery.import | bigqueryにimportする場合True. とりあえずはFalseにする |
