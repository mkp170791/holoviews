"""
Tests for the spatialpandas interface.
"""

from unittest import SkipTest

import numpy as np

try:
    import spatialpandas
    from spatialpandas.geometry import (
        LineDtype, PointDtype, PolygonDtype,
        MultiLineDtype, MultiPointDtype, MultiPolygonDtype
    )
except:
    spatialpandas = None

from holoviews.core.data import Dataset, SpatialPandasInterface
from holoviews.core.data.interface import DataError
from holoviews.element import Path, Points, Polygons

from .testmultiinterface import GeomTests


class SpatialPandasTest(GeomTests):
    """
    Test of the SpatialPandasInterface.
    """

    datatype = 'spatialpandas'

    interface = SpatialPandasInterface

    __test__ = True

    def setUp(self):
        if spatialpandas is None:
            raise SkipTest('SpatialPandasInterface requires spatialpandas, skipping tests')
        super(GeomTests, self).setUp()

    def test_multi_dict_groupby(self):
        arrays = [{'x': np.arange(i, i+2), 'y': i} for i in range(2)]
        mds = Dataset(arrays, kdims=['x', 'y'], datatype=[self.datatype])
        self.assertIs(mds.interface, self.interface)
        with self.assertRaises(DataError):
            mds.groupby('y')

    def test_multi_array_groupby(self):
        arrays = [np.array([(1+i, i), (2+i, i), (3+i, i)]) for i in range(2)]
        mds = Dataset(arrays, kdims=['x', 'y'], datatype=[self.datatype])
        self.assertIs(mds.interface, self.interface)
        with self.assertRaises(DataError):
            mds.groupby('y')

    def test_multi_array_points_iloc_index_rows_index_cols(self):
        arrays = [np.array([(1+i, i), (2+i, i), (3+i, i)]) for i in range(2)]
        mds = Dataset(arrays, kdims=['x', 'y'], datatype=[self.datatype])
        self.assertIs(mds.interface, self.interface)
        with self.assertRaises(DataError):
            mds.iloc[3, 0]

    def test_point_constructor(self):
        points = Points([{'x': 0, 'y': 1}, {'x': 1, 'y': 0}], ['x', 'y'],
                        datatype=[self.datatype])
        self.assertIsInstance(points.data.geometry.dtype, PointDtype)
        self.assertEqual(points.data.iloc[0, 0].flat_values, np.array([0, 1]))
        self.assertEqual(points.data.iloc[1, 0].flat_values, np.array([1, 0]))

    def test_multi_point_constructor(self):
        xs = [1, 2, 3, 2]
        ys = [2, 0, 7, 4]
        points = Points([{'x': xs, 'y': ys}, {'x': xs[::-1], 'y': ys[::-1]}], ['x', 'y'],
                        datatype=[self.datatype])
        self.assertIsInstance(points.data.geometry.dtype, MultiPointDtype)
        self.assertEqual(points.data.iloc[0, 0].buffer_values,
                         np.array([1, 2, 2, 0, 3, 7, 2, 4]))
        self.assertEqual(points.data.iloc[1, 0].buffer_values,
                         np.array([2, 4, 3, 7, 2, 0, 1, 2]))

    def test_line_constructor(self):
        xs = [1, 2, 3]
        ys = [2, 0, 7]
        path = Path([{'x': xs, 'y': ys}, {'x': xs[::-1], 'y': ys[::-1]}],
                    ['x', 'y'], datatype=[self.datatype])
        self.assertIsInstance(path.data.geometry.dtype, LineDtype)
        self.assertEqual(path.data.iloc[0, 0].buffer_values,
                         np.array([1, 2, 2, 0, 3, 7]))
        self.assertEqual(path.data.iloc[1, 0].buffer_values,
                         np.array([3, 7, 2, 0, 1, 2]))

    def test_multi_line_constructor(self):
        xs = [1, 2, 3, np.nan, 6, 7, 3]
        ys = [2, 0, 7, np.nan, 7, 5, 2]
        path = Path([{'x': xs, 'y': ys}, {'x': xs[::-1], 'y': ys[::-1]}],
                    ['x', 'y'], datatype=[self.datatype])
        self.assertIsInstance(path.data.geometry.dtype, MultiLineDtype)
        self.assertEqual(path.data.iloc[0, 0].buffer_values,
                         np.array([1, 2, 2, 0, 3, 7, 6, 7, 7, 5, 3, 2]))
        self.assertEqual(path.data.iloc[1, 0].buffer_values,
                         np.array([3, 2, 7, 5, 6, 7, 3, 7, 2, 0, 1, 2]))

    def test_polygon_constructor(self):
        xs = [1, 2, 3]
        ys = [2, 0, 7]
        holes = [
            [[(1.5, 2), (2, 3), (1.6, 1.6)], [(2.1, 4.5), (2.5, 5), (2.3, 3.5)]]
        ]
        path = Polygons([{'x': xs, 'y': ys, 'holes': holes}, {'x': xs[::-1], 'y': ys[::-1]}],
                        ['x', 'y'], datatype=[self.datatype])
        self.assertIsInstance(path.data.geometry.dtype, PolygonDtype)
        self.assertEqual(path.data.iloc[0, 0].buffer_values,
                         np.array([1., 2., 2., 0., 3., 7., 1.5, 2., 2., 3.,
                                   1.6, 1.6, 2.1, 4.5, 2.5, 5., 2.3, 3.5]))
        self.assertEqual(path.data.iloc[1, 0].buffer_values,
                         np.array([1, 2, 2, 0, 3, 7]))

    def test_multi_polygon_constructor(self):
        xs = [1, 2, 3, np.nan, 6, 7, 3]
        ys = [2, 0, 7, np.nan, 7, 5, 2]
        holes = [
            [[(1.5, 2), (2, 3), (1.6, 1.6)], [(2.1, 4.5), (2.5, 5), (2.3, 3.5)]],
            []
        ]
        path = Polygons([{'x': xs, 'y': ys, 'holes': holes},
                         {'x': xs[::-1], 'y': ys[::-1]}],
                        ['x', 'y'], datatype=[self.datatype])
        self.assertIsInstance(path.data.geometry.dtype, MultiPolygonDtype)
        self.assertEqual(path.data.iloc[0, 0].buffer_values,
                         np.array([1., 2., 2., 0., 3., 7., 1.5, 2., 2., 3., 1.6, 1.6,
                                   2.1, 4.5, 2.5, 5., 2.3, 3.5, 3., 2., 7., 5., 6., 7. ]))
        self.assertEqual(path.data.iloc[1, 0].buffer_values,
                         np.array([3, 2, 7, 5, 6, 7, 1, 2, 2, 0, 3, 7]))

    def test_point_roundtrip(self):
        points = Points([{'x': 0, 'y': 1, 'z': 0},
                         {'x': 1, 'y': 0, 'z': 1}], ['x', 'y'],
                        'z', datatype=[self.datatype])
        self.assertIsInstance(points.data.geometry.dtype, PointDtype)
        roundtrip = points.clone(datatype=['multitabular'])
        self.assertEqual(roundtrip.interface.datatype, 'multitabular')
        expected = Points([{'x': 0, 'y': 1, 'z': 0},
                           {'x': 1, 'y': 0, 'z': 1}], ['x', 'y'],
                          'z', datatype=['multitabular'])
        self.assertEqual(roundtrip, expected)

    def test_multi_point_roundtrip(self):
        xs = [1, 2, 3, 2]
        ys = [2, 0, 7, 4]
        points = Points([{'x': xs, 'y': ys, 'z': 0},
                         {'x': xs[::-1], 'y': ys[::-1], 'z': 1}],
                        ['x', 'y'], 'z', datatype=[self.datatype])
        self.assertIsInstance(points.data.geometry.dtype, MultiPointDtype)
        roundtrip = points.clone(datatype=['multitabular'])
        self.assertEqual(roundtrip.interface.datatype, 'multitabular')
        expected = Points([{'x': xs, 'y': ys, 'z': 0},
                           {'x': xs[::-1], 'y': ys[::-1], 'z': 1}],
                          ['x', 'y'], 'z', datatype=['multitabular'])
        self.assertEqual(roundtrip, expected)

    def test_line_roundtrip(self):
        xs = [1, 2, 3]
        ys = [2, 0, 7]
        path = Path([{'x': xs, 'y': ys, 'z': 1},
                     {'x': xs[::-1], 'y': ys[::-1], 'z': 2}],
                    ['x', 'y'], 'z', datatype=[self.datatype])
        self.assertIsInstance(path.data.geometry.dtype, LineDtype)
        roundtrip = path.clone(datatype=['multitabular'])
        self.assertEqual(roundtrip.interface.datatype, 'multitabular')
        expected = Path([{'x': xs, 'y': ys, 'z': 1},
                         {'x': xs[::-1], 'y': ys[::-1], 'z': 2}],
                        ['x', 'y'], 'z', datatype=['multitabular'])
        self.assertEqual(roundtrip, expected)
    
    def test_multi_line_roundtrip(self):
        xs = [1, 2, 3, np.nan, 6, 7, 3]
        ys = [2, 0, 7, np.nan, 7, 5, 2]
        path = Path([{'x': xs, 'y': ys, 'z': 0},
                     {'x': xs[::-1], 'y': ys[::-1], 'z': 1}],
                    ['x', 'y'], 'z', datatype=[self.datatype])
        self.assertIsInstance(path.data.geometry.dtype, MultiLineDtype)
        roundtrip = path.clone(datatype=['multitabular'])
        self.assertEqual(roundtrip.interface.datatype, 'multitabular')
        expected = Path([{'x': xs, 'y': ys, 'z': 0},
                         {'x': xs[::-1], 'y': ys[::-1], 'z': 1}],
                        ['x', 'y'], 'z', datatype=['multitabular'])
        self.assertEqual(roundtrip, expected)
    
    def test_polygon_roundtrip(self):
        xs = [1, 2, 3]
        ys = [2, 0, 7]
        poly = Polygons([{'x': xs, 'y': ys, 'z': 0},
                         {'x': xs[::-1], 'y': ys[::-1], 'z': 1}],
                        ['x', 'y'], 'z', datatype=[self.datatype])
        self.assertIsInstance(poly.data.geometry.dtype, PolygonDtype)
        roundtrip = poly.clone(datatype=['multitabular'])
        self.assertEqual(roundtrip.interface.datatype, 'multitabular')
        expected = Polygons([{'x': xs, 'y': ys, 'z': 0},
                             {'x': xs, 'y': ys, 'z': 1}],
                            ['x', 'y'], 'z', datatype=['multitabular'])
        self.assertEqual(roundtrip, expected)
    
    def test_multi_polygon_roundtrip(self):
        xs = [1, 2, 3, np.nan, 6, 7, 3]
        ys = [2, 0, 7, np.nan, 7, 5, 2]
        holes = [
            [[(1.5, 2), (2, 3), (1.6, 1.6)], [(2.1, 4.5), (2.5, 5), (2.3, 3.5)]],
            []
        ]
        poly = Polygons([{'x': xs, 'y': ys, 'holes': holes, 'z': 1},
                         {'x': xs[::-1], 'y': ys[::-1], 'z': 2}],
                        ['x', 'y'], 'z', datatype=[self.datatype])
        self.assertIsInstance(poly.data.geometry.dtype, MultiPolygonDtype)
        roundtrip = poly.clone(datatype=['multitabular'])
        self.assertEqual(roundtrip.interface.datatype, 'multitabular')
        expected = Polygons([{'x': [1, 2, 3, np.nan, 3, 7, 6],
                              'y': [2, 0, 7, np.nan, 2, 5, 7], 'holes': holes, 'z': 1},
                             {'x': [3, 7, 6, np.nan, 1, 2, 3],
                              'y': [2, 5, 7, np.nan, 2, 0, 7], 'z': 2}],
                            ['x', 'y'], 'z', datatype=['multitabular'])
        self.assertEqual(roundtrip, expected)
    