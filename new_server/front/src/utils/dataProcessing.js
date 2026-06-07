export function processPointsForMap(points, color_parameter, shift, plane) {
    var len = Object.values(points).length;
    var x = new Array(len);
    var y = new Array(len);
    var value = new Array(len);
    let param;
    
    if(plane === 'XZ') param = 'z';
    else param = 'abs_v'

    for(var i = 0; i < len; ++i){
        x[i] = points[i].x - shift;
        y[i] = points[i][param];
        value[i] = points[i][color_parameter];
    }
    
    return [x, y, value];
}

export function processMinMax(MinMaxValidated){
  var MinMaxValues = {};

  var fields = ['min_ax','max_ax','min_ay','max_ay','min_az','max_az','min_dist_primary', 'max_dist_primary', 'min_dist_secondary',
    'max_dist_secondary', 'min_cj','max_cj','min_t','max_t', 'min_stability_ind_1', 'max_stability_ind_1',
    'min_stability_ind_2', 'max_stability_ind_2', 'min_stability_ind_3', 'max_stability_ind_3'] //на четных индексах min, на нечетных - max

  for(var i = 0; i < fields.length; ++i){
    MinMaxValues[fields[i]] = MinMaxValidated[0][fields[i]];
  }

  for(var j = 0; j < MinMaxValidated.length; ++j){
    let val_j = MinMaxValidated[j];
    for(var i = 0; i < fields.length; ++i){
      if(i%2==0){
        MinMaxValues[fields[i]] = Math.min(MinMaxValues[fields[i]], val_j[fields[i]]);
      }
      else{
        MinMaxValues[fields[i]] = Math.max(MinMaxValues[fields[i]], val_j[fields[i]]);
      }
    }
  }
  return MinMaxValues;
}

export function processPointsForPoincare(obj, plane){
    const xyz = ['x = 0', 'y = 0', 'z = 0'], VxVyVz = ['vx = 0', 'vy = 0', 'vz = 0'];
    var data = new Array(2);
    var isXAssigned = 0;
    var array;

    if(xyz.includes(plane)){
        for(var i = 0; i < xyz.length; i++){
          if(xyz[i] == plane){continue;}
          
          if(xyz[i] == "x = 0"){
            array = obj.x_points;
          }
          else if(xyz[i] == "y = 0"){
            array = obj.y_points;
          }
          else {
            array = obj.z_points;
          }

          if(!isXAssigned){
            data[0] = array;
            isXAssigned = true;
          }
          else{
            data[1] = array;
          }
        }
      }
      else{
        for(var i = 0; i < xyz.length; i++){
          if(VxVyVz[i] == plane){continue;}
          
          if(VxVyVz[i] == "vx = 0"){
            array = obj.vx_points;
          }
          else if(VxVyVz[i] == "vy = 0"){
            array = obj.vy_points;
          }
          else {
            array = obj.vz_points;
          }

          if(!isXAssigned){
            data[0] = array;
            isXAssigned = true;
          }
          else{
            data[1] = array;
          }
        }
    }
    return data;
}

export function processPointsForCJPoincare(array, plane, parameter){
  var planeToAxis = {
    'x = 0': ['y_points', 'z_points'],
    'y = 0': ['x_points', 'z_points'],
    'z = 0': ['x_points', 'y_points'],
    'vx = 0': ['vy_points', 'vz_points'],
    'vy = 0': ['vx_points', 'vz_points'],
    'vz = 0': ['vx_points', 'vy_points'],
  };
  var params = planeToAxis[plane];

  var total_len = 0;
  for(var i = 0; i < array.length; ++i){
      total_len += array[i].points_count;
  }

  var x = new Array(total_len);
  var y = new Array(total_len);
  var value = new Array(total_len);

  var p = 0;
  for(var i = 0; i < array.length; ++i){
    for(var j = 0; j < array[i][params[0]].length; ++j){
      x[p] = array[i][params[0]][j];
      y[p] = array[i][params[1]][j];
      value[p] = array[i][parameter];
      ++p;
    }
  }
  return [x, y, value]
}

export function processFamilyParams(points){
  var len = Object.values(points).length; 
  var x = new Array(len);
  var y = new Array(len);
  var z = new Array(len);

  for(var i = 0; i < len; ++i){
      x[i] = points[i].param_x;
      y[i] = points[i].param_y;
      z[i] = points[i].param_z;
  }
  return [x, y, z];
}

export function processFamilyBroucke(points, param){
  var len = Object.values(points).length; 
  var x = new Array(len);
  var y = new Array(len);
  var z = new Array(len);

  for(var i = 0; i < len; ++i){
      x[i] = points[i].alpha;
      y[i] = points[i].beta;
      z[i] = points[i][param];
  }

  return [x, y, z];
}

export function processProjections(points, parameter){
  var len = Object.values(points).length;
  var x = new Array(len);
  var y = new Array(len);
  var z = new Array(len);

  for(var i = 0; i < len; ++i){
    x[i] = points[i].x;
    y[i] = points[i].y;
    z[i] = points[i].z;
  }

  if(parameter === '3rd_coord'){
    return [[x, y, z], [x, z, y], [y, z, x]];
  }

  var value = new Array(len);
  for(var i = 0; i < len; ++i){
    value[i] = points[i][parameter];
  }
  return [[x, y, value], [x, z, value], [y, z, value]];
}

export function processOrbit(points, parameter){
  var len = Object.values(points).length;
  var export_points = new Array(len);

  for(var i = 0; i < len; ++i){
    export_points[i] = [ points[i].x, points[i].y, points[i].z, points[i][parameter] ];
  }

  return export_points;
}