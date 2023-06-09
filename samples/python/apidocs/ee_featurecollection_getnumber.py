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

# [START earthengine__apidocs__ee_featurecollection_getnumber]
# A FeatureCollection with a number property value.
fc = ee.FeatureCollection([]).set('number_property', 1.5)

# Fetch the number property value as an ee.Number object.
print('Number property value as ee.Number:',
      fc.getNumber('number_property').getInfo())
# [END earthengine__apidocs__ee_featurecollection_getnumber]
