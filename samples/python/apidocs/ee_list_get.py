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

# [START earthengine__apidocs__ee_list_get]
# An ee.List object.
ee_list = ee.List([5, 10, 15, 20, 25, 30])

# Fetch elements at specified 0-based positions in the list.
print('The second element:', ee_list.get(1).getInfo())
print('The fourth element:', ee_list.get(3).getInfo())
print('The last element:', ee_list.get(-1).getInfo())
print('The second to last element:', ee_list.get(-2).getInfo())

# ee.Number and integer computed objects are valid inputs.
print('Computed object index input:', ee_list.get(list.get(0)).getInfo())

# The result of ee.List.get is an ambiguous object type. You need to cast the
# result to the expected type to use it in subsequent instance methods. For
# example, if you are fetching a number and wish to add it to another number,
# you must cast the .get() result as an ee.Number.
print('Add fetched number to another number:',
      ee.Number(list.get(1)).add(2).getInfo())
# [END earthengine__apidocs__ee_list_get]
