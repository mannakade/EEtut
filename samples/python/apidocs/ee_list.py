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

# [START earthengine__apidocs__ee_list]
print(ee.List([]).getInfo())  # []
print(ee.List([None]).getInfo())  # [None]
print(ee.List([True]).getInfo())  # [True]
print(ee.List([1]).getInfo())  # [1]
print(ee.List([ee.Number(1)]).getInfo())  # [1]
print(ee.List(['a']).getInfo())  # ['a']
print(ee.List([[]]).getInfo())  # [[]]
print(ee.List([ee.List([])]).getInfo())  # [[]]
print(ee.List([[], [[]], [1, [], 'a']]).getInfo())  # [[], [[]], [1, [], 'a']]
# [END earthengine__apidocs__ee_list]
