## PythonTriangulator

利用earcut-python做二次封装，实现对输入JSON文件中描述的多边形作三角化，输出相应的三角网格描述JSON文件

目前仅支持2D多边形。可支持包含任意个（包括0个）孔洞的多边形


#### 命令格式：

python triangulate.py ${输入文件} ${输出文件}


#### 示例：
``` shell
python triangulate.py polygons.json triangles.json
```

#### 输入JSON格式说明：
示例：
``` javascript
{
    "polygon_sets": [
        {
            "type": "short_sleeved_shirt",
            "width": 540,
            "height": 342,
            "image_path": "short_sleeved_shirt.png",
            "vertices": [[0,0], [100,0], [100,100], [0,100], [20,20], [80,20], [80,80], [20,80]],
            "polygons": [
                {
                    "outline": [0, 1, 2, 3],
                    "holes": [[4, 5, 6, 7]]
                }
            ]
        },
        {
            "type": "long_sleeved_shirt",
            "width": 320,
            "height": 640,
            "image_path": "long_sleeved_shirt.png",
            "vertices": [[100,0], [200,0], [200,100], [100,100]],
            "polygons": [
                {
                    "outline": [0, 1, 2, 3]
                }
            ]
        }
    ]
}
```
输入JSON文件的根JSON对象必须包含一个名为polygon_sets的数组。

该数组中每个成员描述一组共享相同顶点的多边形，其包含的字段中只有vertices和polygons两个与多边形描述有关，其余键值对可任意添加，程序只会原样复制到输出JSON文件中。

vertices表示被该多边形组所共享的顶点数据，其每个元素为一个长度为2的数组，依次为x和y。

polygons数组表示该多边形组中的所有多边形，其每个元素包含一个必须的outline成员和一个可选的holes成员，

outline数组表示多边形的外轮廓，其中依序包含了多边形轮廓上各顶点对应在vertices中的序号，

holes为可选的数组，其中可包含一个或多个数组作为其元素，每个子数组表示一个孔洞的各顶点在vertices中的序号

#### 输出JSON格式说明：
输出的JSON中除每个多边形组中的polygons被替换成了三角形网格数组triangles以外，其余内容保持不变。triangles中以打平形式表示了所有三角形的顶点在vertices中的序号


本项目基于earcut-python实现：
https://github.com/joshuaskelly/earcut-python

以下是其原README内容


## earcut-python

A pure Python port of the earcut JavaScript triangulation library. The latest version is based off of the earcut 2.1.1 release, and is functionally identical.

The original project can be found here:
https://github.com/mapbox/earcut

#### Usage

```python
triangles = earcut([10,0, 0,50, 60,60, 70,10]) # Returns [1,0,3, 3,2,1]
```

Signature: `earcut(vertices[, holes, dimensions = 2])`.

* `vertices` is a flat array of vertex coordinates like `[x0,y0, x1,y1, x2,y2, ...]`.
* `holes` is an array of hole _indices_ if any
  (e.g. `[5, 8]` for a 12-vertex input would mean one hole with vertices 5&ndash;7 and another with 8&ndash;11).
* `dimensions` is the number of coordinates per vertex in the input array (`2` by default).

Each group of three vertex indices in the resulting array forms a triangle.

```python
# Triangulating a polygon with a hole
earcut([0,0, 100,0, 100,100, 0,100,  20,20, 80,20, 80,80, 20,80], [4])
# [3,0,4, 5,4,0, 3,4,7, 5,0,1, 2,3,7, 6,5,1, 2,7,6, 6,1,2]

# Triangulating a polygon with 3d coords
earcut([10,0,1, 0,50,2, 60,60,3, 70,10,4], null, 3)
# [1,0,3, 3,2,1]
```

If you pass a single vertex as a hole, Earcut treats it as a Steiner point.

If your input is a multi-dimensional array, you can convert it to the format expected by Earcut with `earcut.flatten`:

```python
# The first sequence of vertices is treated as the outer hull, the following sequneces are treated as holes.
data = earcut.flatten([[(0,0), (100,0), (100,100), (0,100)], [(20,20), (80,20), (80,80), (20,80)]])
triangles = earcut(data['vertices'], data['holes'], data['dimensions'])
```

After getting a triangulation, you can verify its correctness with `earcut.deviation`:

```python
deviation = earcut.deviation(vertices, holes, dimensions, triangles)
```

Returns the relative difference between the total area of triangles and the area of the input polygon.
`0` means the triangulation is fully correct.
