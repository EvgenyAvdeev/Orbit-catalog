export function getFor4thPage(data, plane){
  var planeToAxis = {
    'x = 0': ['y_points', 'z_points'],
    'y = 0': ['x_points', 'z_points'],
    'z = 0': ['x_points', 'y_points'],
    'vx = 0': ['vy_points', 'vz_points'],
    'vy = 0': ['vx_points', 'vz_points'],
    'vz = 0': ['vx_points', 'vy_points'],
  };
  var params = planeToAxis[plane];
  
  var paramsToXZ = {};

  for(var i = 0; i < data.length; ++i){
    for(var j = 0; j < data[i][params[0]].length; ++j){
      let val1 = data[i][params[0]][j];
      let val2 = data[i][params[1]][j];
      paramsToXZ[`${val1}:${val2}`] = { x: data[i].x, z: data[i].z };
    }
  }
  return paramsToXZ;
}

export function getForParamsPage(data){
  var paramsToCjXZ = {};

  for(var i = 0; i < data.length; ++i){
    let d = data[i];
    paramsToCjXZ[`${d['param_x']}:${d['param_y']}`] = { cj: d['cj'], x: d['x'], z: d['z'] }
  }

  return paramsToCjXZ;
}

export function getForBrouckePage(data){
  var alpbeToCjXZ = {};

  for(var i = 0; i < data.length; ++i){
    let d = data[i];
    alpbeToCjXZ[`${d['alpha']}:${d['beta']}`] = { cj: d['cj'], x: d['x'], z: d['z'] }
  }

  return alpbeToCjXZ;
}

export function getAbsVFor2ndPageProjections(points){
  let XYtoAbsV = {};
  let XZtoAbsV = {};
  let YZtoAbsV = {};

   for(var i = 0; i < points.length; ++i){
    var p = points[i];
    XYtoAbsV[`${p.x}:${p.y}`] = { 'abs_v': p['abs_v'], 'z': p.z };
    XZtoAbsV[`${p.x}:${p.z}`] = { 'abs_v': p['abs_v'], 'y': p.y };
    YZtoAbsV[`${p.y}:${p.z}`] = { 'abs_v': p['abs_v'], 'x': p.x };
  }

  return {
    'XY': XYtoAbsV,
    'XZ': XZtoAbsV,
    'YZ': YZtoAbsV
  }
}

export function getAbsVFor2ndPagePoincare(plane, points){
  let convert = { 
    'x = 0': ['y_points', 'z_points'],
    'y = 0': ['x_points', 'z_points'],
    'z = 0': ['x_points', 'y_points'],
    'vx = 0': ['vy_points', 'vz_points'],
    'vy = 0': ['vx_points', 'vz_points'],
    'vz = 0': ['vx_points', 'vy_points']
  }
  let [ param1, param2 ] = convert[plane]
  
  let toAbsV = {};
  
  for(var i = 0; i < points[param1].length; ++i){

    let abs_v = Math.sqrt(points['vx_points'][i]**2+points['vy_points'][i]**2+points['vz_points'][i]**2)

    toAbsV[`${points[param1][i]}:${points[param2][i]}`] = { 'abs_v': abs_v, 'x': points['x_points'][i], 
      'y': points['y_points'][i], 'z': points['z_points'][i], };
  }

  return toAbsV
}