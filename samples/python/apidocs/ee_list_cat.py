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

# [START earthengine__apidocs__ee_list_cat]
print(ee.List(['dog']).cat(['squirrel']).getInfo())  # ['dog', 'squirrel']

# ['moose', '&', 'squirrel']
print(ee.List(['moose']).cat(['&', 'squirrel']).getInfo())

# [['a', 'b'], ['1', 1]]
print(ee.List([['a', 'b']]).cat(ee.List([['1', 1]])).getInfo())

print(ee.List([]).cat(ee.List([])).getInfo())  # []
print(ee.List([1]).cat(ee.List([])).getInfo())  # [1]
print(ee.List([]).cat(ee.List([2])).getInfo())  # [2]
# [END earthengine__apidocs__ee_list_cat]
