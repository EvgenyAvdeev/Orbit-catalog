import { z } from 'zod';

//Map
export const PointTemplate = z.object({
  orbit_id: z.number().int().nonnegative(),
  x: z.number(),
  z: z.number(),
  vy: z.number(),
  cj: z.number(),
  ax: z.number(),
  ay: z.number(),
  az: z.number(),
  abs_v: z.number().nonnegative(),
  dist_primary: z.number().nonnegative(),
  dist_secondary: z.number().nonnegative()
});

export const PointArrayTemplate = z.array(PointTemplate);


//MinMax
export const MinMaxTemplate = z.object({
  min_ax: z.number().nonnegative(),
  max_ax: z.number().nonnegative(),
  min_ay: z.number().nonnegative(),
  max_ay: z.number().nonnegative(),
  min_az: z.number().nonnegative(),
  max_az: z.number().nonnegative(),
  min_cj: z.number(),
  max_cj: z.number(),
  min_t: z.number().nonnegative(),
  max_t: z.number().nonnegative(),
  min_dist_primary: z.number().nonnegative(),
  max_dist_primary: z.number().nonnegative(),
  min_dist_secondary: z.number().nonnegative(),
  max_dist_secondary: z.number().nonnegative(),
  min_stability_ind_1: z.number(),
  max_stability_ind_1: z.number(),
  min_stability_ind_2: z.number(),
  max_stability_ind_2: z.number(),
  min_stability_ind_3: z.number(),
  max_stability_ind_3: z.number()
});

export const MinMaxArrayTemplate = z.array(MinMaxTemplate);


//Poincare
export const floatArray = z.array(z.number());

export const PoincareTemplate = z.object({
  orbit_id: z.number().int().nonnegative(),
  x: z.number(),
  y: z.number(),
  z: z.number(),
  ax: z.number(),
  ay: z.number(),
  az: z.number(),
  vx: z.number(),
  vy: z.number(),
  vz: z.number(),
  dist_primary: z.number().nonnegative(),
  dist_secondary: z.number().nonnegative(),
  abs_v: z.number().nonnegative(),
  x_points: floatArray,
  y_points: floatArray,
  z_points: floatArray,
  vx_points: floatArray,
  vy_points: floatArray,
  vz_points: floatArray,
  points_count: z.number().int().nonnegative()
});


export const PoincareTemplateArray = z.array(PoincareTemplate);


//Family params
export const ParamsPoint = z.object({
  param_x: z.number(),
  param_y: z.number(),
  param_z: z.number(),
  x: z.number(),
  z: z.number(),
  cj: z.number()
});

export const ParamsArrayTemplate = z.array(ParamsPoint);

//Broucke 
export const BrouckePoint = z.object({
  orbit_id: z.number().int().nonnegative(),
  x: z.number(),
  z: z.number(),
  vy: z.number(),
  ax: z.number(),
  ay: z.number(),
  az: z.number(),
  t: z.number(),
  cj: z.number(),
  dist_primary: z.number(),
  dist_secondary: z.number(),
  family_tag: z.string(),
  lib_point: z.string(),
  stable: z.boolean(),
  alpha: z.number(),
  beta: z.number(),
  // floke: z.number()
});

export const BrouckeArrayTemplate = z.array(BrouckePoint);


//Orbit projections
export const OrbitTemplate = z.object({
  orbit_id: z.number().int().nonnegative(),
  x: z.number(),
  z: z.number(),
  ax: z.number(),
  ay: z.number(),
  az: z.number(),
  vy: z.number(),
  t: z.number(),
  cj: z.number(),
  dist_primary: z.number(),
  dist_secondary: z.number(),
  lib_point: z.string(),
  family_tag: z.string(),
  stable: z.boolean()
});

export const ChunkPointTemplate = z.object({
  orbit_id: z.number().int().nonnegative(),
  x: z.number(),
  y: z.number(),
  z: z.number(),
  vx: z.number(),
  vy: z.number(),
  vz: z.number(),
  t: z.number(),
  abs_v: z.number()
});

export const ChunkArrayTemplate = z.array(ChunkPointTemplate);

export const NeighbourOrbitTemplate = z.object({
  x: z.number(),
  z: z.number()
});