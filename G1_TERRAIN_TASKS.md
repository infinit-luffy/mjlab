# G1 Velocity 任务 —— 运行命令对照

这个分支(`claude/charming-swirles`)新增了 7 个针对单一 sub-terrain 的 G1
velocity task,下面列出**之前**和**现在**各自可用的 task id 以及对应的
`uv run train` / `uv run play` 命令模板。

所有命令都沿用项目标准入口:

```bash
uv run train <TASK_ID> [flags]   # 训练
uv run play  <TASK_ID> [flags]   # 回放 / 评估
```

项目要求本地先用 `make check` 跑格式、lint、类型检查;正式开 PR 之前再
`make test`。

---

## 之前(本分支改动之前)

G1 velocity 只有两个 task:

| Task ID | 地形 | 用途 |
|---|---|---|
| `Mjlab-Velocity-Rough-Unitree-G1` | ROUGH_TERRAINS_CFG 的 **7 种地形随机混合** | 通用 rough 训练 |
| `Mjlab-Velocity-Flat-Unitree-G1` | MuJoCo 原生 `plane`(纯平面) | 最轻量、无地形扫描 |

训练(示例):

```bash
# Rough 混合地形
uv run train Mjlab-Velocity-Rough-Unitree-G1 --env.scene.num-envs 4096

# 纯平面
uv run train Mjlab-Velocity-Flat-Unitree-G1 --env.scene.num-envs 4096
```

回放 / 评估(示例,`--wandb-run-path` 或 `--checkpoint-file` 二选一):

```bash
uv run play Mjlab-Velocity-Rough-Unitree-G1 \
    --wandb-run-path your-entity/mjlab/run-id

uv run play Mjlab-Velocity-Flat-Unitree-G1 \
    --checkpoint-file logs/rsl_rl/g1_velocity/<run-dir>/model_1000.pt
```

---

## 现在(本分支改动之后)

原来的两个 task **完全不变**,额外新增 7 个针对单一 sub-terrain 的 task:

| Task ID | 单一 sub-terrain | 含义 | 来源 preset |
|---|---|---|---|
| `Mjlab-Velocity-Flat-Terrain-Unitree-G1` | `flat` | 盒状平地(带围栏) | `BoxFlatTerrainCfg` |
| `Mjlab-Velocity-PyramidStairs-Unitree-G1` | `pyramid_stairs` | **上楼梯**(金字塔阶梯) | `BoxPyramidStairsTerrainCfg` |
| `Mjlab-Velocity-PyramidStairsInv-Unitree-G1` | `pyramid_stairs_inv` | **下楼梯**(反金字塔阶梯) | `BoxInvertedPyramidStairsTerrainCfg` |
| `Mjlab-Velocity-HfPyramidSlope-Unitree-G1` | `hf_pyramid_slope` | 上斜坡 | `HfPyramidSlopedTerrainCfg` |
| `Mjlab-Velocity-HfPyramidSlopeInv-Unitree-G1` | `hf_pyramid_slope_inv` | 下斜坡 | `HfPyramidSlopedTerrainCfg (inverted=True)` |
| `Mjlab-Velocity-RandomRough-Unitree-G1` | `random_rough` | Perlin 随机粗糙面 | `HfRandomUniformTerrainCfg` |
| `Mjlab-Velocity-WaveTerrain-Unitree-G1` | `wave_terrain` | 正弦波浪地形 | `HfWaveTerrainCfg` |

> **命名注意**:`Mjlab-Velocity-Flat-Terrain-Unitree-G1` 与旧的
> `Mjlab-Velocity-Flat-Unitree-G1` 是**不同地形**。前者是
> `BoxFlatTerrainCfg`(带围栏的盒状平地,含 terrain_scan 和 curriculum),
> 后者是 MuJoCo 原生 `plane`(彻底关闭地形扫描)。

### 训练模板

```bash
# 例:专练上楼梯
uv run train Mjlab-Velocity-PyramidStairs-Unitree-G1 --env.scene.num-envs 4096

# 例:专练下楼梯
uv run train Mjlab-Velocity-PyramidStairsInv-Unitree-G1 --env.scene.num-envs 4096

# 例:只在上斜坡上训练
uv run train Mjlab-Velocity-HfPyramidSlope-Unitree-G1 --env.scene.num-envs 4096
```

可以叠加所有已有的 CLI flag,例如:

```bash
uv run train Mjlab-Velocity-PyramidStairs-Unitree-G1 \
    --num-envs 4096 \
    --agent.max-iterations 10000 \
    --agent.algorithm.learning-rate 3e-4
```

多 GPU:

```bash
uv run train Mjlab-Velocity-PyramidStairs-Unitree-G1 \
    --gpu-ids "[0, 1]" \
    --env.scene.num-envs 4096
```

### 回放 / 评估模板

```bash
uv run play Mjlab-Velocity-PyramidStairs-Unitree-G1 \
    --wandb-run-path your-entity/mjlab/run-id

uv run play Mjlab-Velocity-PyramidStairsInv-Unitree-G1 \
    --checkpoint-file logs/rsl_rl/g1_velocity/<run-dir>/model_1000.pt
```

---

## 行为差异速览

| 维度 | `Rough`(旧) | 新的 7 个单地形 task | `Flat`(旧,plane) |
|---|---|---|---|
| `terrain_type` | `generator` | `generator` | `plane` |
| 子地形数 | 7 种混合 | **1 种** | — |
| Curriculum | ✅ 开 | ✅ 开(10 行 × 1 列难度阶梯) | ❌ 关 |
| Terrain scan / height scan | ✅ | ✅ | ❌ 已移除 |
| 模拟开销 | 高(CCD 500 iters, nconmax 70) | 高(沿用 rough) | 低(CCD 50 iters) |
| 难度参数 | ROUGH 自定义覆盖(如楼梯步高 `(0.0, 0.1)`) | **同 ROUGH 设置**,仅挑出单一子地形 | — |

---

## 逻辑自检(本地 Mac,不跑仿真)

```bash
make check         # ruff format + ruff check + ty/pyright
```

```bash
uv run python -c "
from mjlab.tasks.registry import load_env_cfg
ids = [
  'Mjlab-Velocity-Flat-Terrain-Unitree-G1',
  'Mjlab-Velocity-PyramidStairs-Unitree-G1',
  'Mjlab-Velocity-PyramidStairsInv-Unitree-G1',
  'Mjlab-Velocity-HfPyramidSlope-Unitree-G1',
  'Mjlab-Velocity-HfPyramidSlopeInv-Unitree-G1',
  'Mjlab-Velocity-RandomRough-Unitree-G1',
  'Mjlab-Velocity-WaveTerrain-Unitree-G1',
]
for tid in ids:
    cfg = load_env_cfg(tid)
    subs = cfg.scene.terrain.terrain_generator.sub_terrains
    assert len(subs) == 1, (tid, list(subs))
    print(tid, '->', list(subs.keys())[0])
"
```

上面这段只做 dataclass 构造,不会启动 MuJoCo / warp / CUDA,在 Mac 上也可直接跑。
