#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os
import json
from earcut import earcut 
from math import inf

inputJSONPath = sys.argv[1]
outputJSONPath = sys.argv[2]

newJson = {}
newPolygonSets = []
newJson['polygon_sets'] = newPolygonSets
try:
    with open(inputJSONPath) as fR:
        jsonObj = json.load(fR)
        polygonSets = jsonObj['polygon_sets']
        for polygonSet in polygonSets:
            newPolygonSet = {}
            newPolygonSets.append(newPolygonSet)
            for k,v in polygonSet.items():
                if (k != 'vertices' and k != 'polygons'):
                    newPolygonSet[k] = v
            
            vertices = polygonSet["vertices"]
            newPolygonSet["vertices"] = vertices
            newTriangles = []
            newPolygonSet["triangles"] = newTriangles
            for polygon in polygonSet["polygons"]:
                indices = []
                holeStartIndices = []
                holeStart = 0
                flattenVertices = []
                outline = polygon["outline"]
                for i in range(len(outline)):
                    index = outline[i]
                    indices.append(index)
                    vertex = vertices[index]
                    flattenVertices.append(vertex[0])
                    flattenVertices.append(vertex[1])
                if ("holes" in polygon):
                    holeStart = len(outline)
                    holes = polygon["holes"]
                    for hole in holes:
                        holeStartIndices.append(holeStart)
                        holeStart += len(hole)
                        for j in range(len(hole)):
                            index = hole[j]
                            indices.append(index)
                            vertex = vertices[index]
                            flattenVertices.append(vertex[0])
                            flattenVertices.append(vertex[1])
                triangles = earcut.earcut(flattenVertices, holeStartIndices)
                triangles = list(map(lambda x: indices[x], triangles))
##                newTriangles.append({"flatten_vertices": flattenVertices, "indices": indices, "holes": holeStartIndices, "triangles": triangles, "triangles1": triangles1})
                newTriangles += triangles

except IOError:
    print('IOError')

try:
    with open(outputJSONPath, "w") as fW:
        json.dump(newJson, fW, indent=4)
except IOError:
    print('IOError')

## triangles = earcut.earcut([0,0, 100,0, 100,100, 0,100,  20,20, 80,20, 80,80, 20,80], [4])
## data = earcut.flatten([[(0,0), (100,0), (100,100), (0,100)], [(20,20), (80,20), (80,80), (20,80)]])
## data = earcut.flatten([[[0,0], [100,0], [100,100], [0,100]], [[20,20], [80,20], [80,80], [20,80]]])
## triangles = earcut.earcut(data['vertices'], data['holes'], data['dimensions'])
