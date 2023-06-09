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

# [START earthengine__apidocs__ee_string_encodejson]
print('JSON-encoded ee.String:',
      repr(ee.String.encodeJSON(ee.String('earth')).getInfo()))  # '\"earth\"'

print('JSON-encoded ee.Number:',
      repr(ee.String.encodeJSON(ee.Number(1)).getInfo()))  # '1'

print('JSON-encoded ee.List:',
      repr(ee.String.encodeJSON(ee.List([1, 2, 3])).getInfo()))  # '[1,2,3]'

print('JSON-encoded ee.Dictionary:',
      repr(ee.String.encodeJSON(
          ee.Dictionary({'lc_name': 'grassland', 'lc_class': 3})).getInfo()))
# '{\"lc_class\":3,\"lc_name\":\"grassland\"}'
# [END earthengine__apidocs__ee_string_encodejson]
