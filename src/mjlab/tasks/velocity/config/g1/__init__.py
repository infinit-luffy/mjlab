from mjlab.tasks.registry import register_mjlab_task
from mjlab.tasks.velocity.rl import VelocityOnPolicyRunner

from .env_cfgs import (
  unitree_g1_flat_env_cfg,
  unitree_g1_flat_terrain_env_cfg,
  unitree_g1_hf_pyramid_slope_env_cfg,
  unitree_g1_hf_pyramid_slope_inv_env_cfg,
  unitree_g1_pyramid_stairs_env_cfg,
  unitree_g1_pyramid_stairs_inv_env_cfg,
  unitree_g1_random_rough_env_cfg,
  unitree_g1_rough_env_cfg,
  unitree_g1_wave_terrain_env_cfg,
)
from .rl_cfg import unitree_g1_ppo_runner_cfg

register_mjlab_task(
  task_id="Mjlab-Velocity-Rough-Unitree-G1",
  env_cfg=unitree_g1_rough_env_cfg(),
  play_env_cfg=unitree_g1_rough_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Mjlab-Velocity-Flat-Unitree-G1",
  env_cfg=unitree_g1_flat_env_cfg(),
  play_env_cfg=unitree_g1_flat_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

# Per-sub-terrain variants of the ROUGH config. Each restricts the terrain
# generator to a single sub-terrain from ROUGH_TERRAINS_CFG (with its rough
# difficulty overrides preserved) while keeping curriculum enabled.
register_mjlab_task(
  task_id="Mjlab-Velocity-Flat-Terrain-Unitree-G1",
  env_cfg=unitree_g1_flat_terrain_env_cfg(),
  play_env_cfg=unitree_g1_flat_terrain_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Mjlab-Velocity-PyramidStairs-Unitree-G1",
  env_cfg=unitree_g1_pyramid_stairs_env_cfg(),
  play_env_cfg=unitree_g1_pyramid_stairs_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Mjlab-Velocity-PyramidStairsInv-Unitree-G1",
  env_cfg=unitree_g1_pyramid_stairs_inv_env_cfg(),
  play_env_cfg=unitree_g1_pyramid_stairs_inv_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Mjlab-Velocity-HfPyramidSlope-Unitree-G1",
  env_cfg=unitree_g1_hf_pyramid_slope_env_cfg(),
  play_env_cfg=unitree_g1_hf_pyramid_slope_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Mjlab-Velocity-HfPyramidSlopeInv-Unitree-G1",
  env_cfg=unitree_g1_hf_pyramid_slope_inv_env_cfg(),
  play_env_cfg=unitree_g1_hf_pyramid_slope_inv_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Mjlab-Velocity-RandomRough-Unitree-G1",
  env_cfg=unitree_g1_random_rough_env_cfg(),
  play_env_cfg=unitree_g1_random_rough_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)

register_mjlab_task(
  task_id="Mjlab-Velocity-WaveTerrain-Unitree-G1",
  env_cfg=unitree_g1_wave_terrain_env_cfg(),
  play_env_cfg=unitree_g1_wave_terrain_env_cfg(play=True),
  rl_cfg=unitree_g1_ppo_runner_cfg(),
  runner_cls=VelocityOnPolicyRunner,
)
