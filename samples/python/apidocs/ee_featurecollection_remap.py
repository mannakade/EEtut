# Copyright 2023 The Google Earth Engine Community Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START earthengine__apidocs__ee_featurecollection_remap]
# Classify features based on a string property.
# The 'nonsense' category gets dropped.
fc = ee.FeatureCollection([
    ee.Feature(ee.Geometry.Point([1, 2]), {'isTree': 'Tree'}),
    ee.Feature(ee.Geometry.Point([3, 4]), {'isTree': 'NotTree'}),
    ee.Feature(ee.Geometry.Point([5, 6]), {'isTree': 'nonsense'}),
    ])

trees = fc.remap(['NotTree', 'Tree'], [0, 1], 'isTree')
print('Remapped trees:', trees.getInfo())
# [END earthengine__apidocs__ee_featurecollection_remap]
