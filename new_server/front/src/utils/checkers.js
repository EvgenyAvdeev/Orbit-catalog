export function checkFloat(str){
    if(str === '') return true;
    if(str === undefined) return false;

    var point_pos = -1;
    for(var i = 0; i < str.length; ++i){
        if(('0' > str[i] || str[i] > '9') && str[i] !== '.' && !(str[i] === '-' && i === 0)){
            return false;
        }
        if(str[i] === '.'){
            if(point_pos === -1){
                point_pos = i;
            }
            else return false; //значит точки хотя бы две
        }
    }
    if(point_pos === 0 || (point_pos === 1 && str[0] === '-')) return false;

    return true;
}

import { Gradients } from '../constants/gradients'
export function checkGradient(str){
    var gradientNames = Object.keys(Gradients);
    for(var i = 0; i < gradientNames.length; ++i){
        if(gradientNames[i] === str) return str;
    }
    return gradientNames[0];
}

export function checkParameter(parameterTag, nameToTag){
    var parametersNames = Object.keys(nameToTag);
    for(var i = 0; i < parametersNames.length; ++i){
        var name = parametersNames[i];
        if(nameToTag[name] === parameterTag) return name;
    }
    return parametersNames[0];
}

export function checkIncludes(value, array, defArgPos = 0){
    if(array.includes(value)){
        return value;
      }
      else{
        return array[defArgPos];
      }
}

export function checkIncludesReversed(value, dict, defArgPos = 0){
    let keys = Object.keys(dict);

    if(Object.values(dict).includes(value)){
        for(let i=0; i<keys.length; ++i){
            if(dict[keys[i]] === value){
                return keys[i];
            }
        }
      }
      else{
        return keys[defArgPos];
      }
}

export function checkFamilies(families, originalTags, tagToFamily, point){
    var resFamilies = [];

    for(var i = 0; i < families.length; ++i){
        if(originalTags.includes(families[i])){
            let familyTag = `${point}.${families[i]}`;
            resFamilies.push(tagToFamily[familyTag]);
        }
    }
    return resFamilies;
}

export function checkPoints(points){
    if(points === undefined || points.charAt(0) !== '[' || points.charAt(points.length-1) !== ']') return []
    
    points = points.replaceAll('];[', ']|[');
    points = points.slice(1, points.length-1).split('|')
    var res_points = [];

    for(let i = 0; i<points.length; ++i){
        if(points[i].charAt(0) !== '[' || points[i].charAt(points[i].length-1) !== ']') continue;
        
        var coords = points[i].slice(1, points[i].length-1).split(';');
        if(coords.length !== 2) continue

        var x = coords[0].replace(',', '.'), y = coords[1].replace(',', '.');
        if(x !== '' && y !== '' && checkFloat(x) && checkFloat(y)){
            res_points.push([x, y]);
        }
    }

    return res_points;
}