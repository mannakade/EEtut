# Copyright 2022 The Google Earth Engine Community Authors
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

# [START earthengine__apidocs__ee_number_erfinv]
print('Inverse error function of -1:',
      ee.Number(-1).erfInv().getInfo())  # -Infinity

print('Inverse error function of -0.001:',
      ee.Number(-0.001).erfInv().getInfo())  # -0.000886227

print('Inverse error function of 0:',
      ee.Number(0).erfInv().getInfo())  # 0

print('Inverse error function of 0.001:',
      ee.Number(0.001).erfInv().getInfo())  # 0.000886227

print('Inverse error function of 1:',
      ee.Number(1).erfInv().getInfo())  # Infinity
# [END earthengine__apidocs__ee_number_erfinv]
