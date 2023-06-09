---
title: Rapid Classification of Croplands
description: This tutorial provides a quick template for rapid and replicable binary classification of maize-cultivated land in Nigeria, using Google Earth Engine (GEE).
author: PJNation
tags: maize, smallholder, cropland, classify, rapid, binary, s2, sentinel-2
date_published: 2020-08-03
---
<!--
Copyright 2020 The Google Earth Engine Community Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

## Background

Land-cover classification in complex landscapes has been constrained by
inherent short-distance transition in crop/vegetation types, especially in
smallholder farming systems. The increasing availability and accessibility of
earth observation imagery provides significant opportunities to assess status
and monitor changes in land cover, yet unlocking such capability is
contingent on availability of relevant ground truth data to calibrate and
validate classification algorithms. The critically needed spatially-explicit
ground-truth data are often unavailable in sub-Saharan African farming
systems and this constrains development of relevant analytical tools to
monitor cropland dynamics or generate [near]real-time insights on farming
systems. This tutorial was developed as a quick guide for users who are
interested in implementing land cover classification routine in Google Earth
Engine environment, using ground-truth data and available Sentinel-2 TOA
spectral bands. The goal is to provide an easy-to-implement workflow that can
be adapted by researchers and analysts to quickly classify croplands. As more
efforts are invested in collecting spatially rich, georeferenced data at
national and regional levels, this tutorial can be useful to generate
immediate/timely insights for maize and other crop types.

## Caveat

This land cover classification was implemented based on available data which
was collected under a multi-year project (https://tamasa.cimmyt.org/) which
was focused on advancing digital agronomic innovation for decision support in
maize-based farming systems. Therefore, the ground truth data in this
analytical workflow is rich in maize farm locations, and contains much fewer
data points for other crop types within the focal geography. Considering this
limitation, the scope of this classification tool and this tutorial is
limited to binary classification of maizelands (i.e. maize vs. non-maize
cultivated) within the period of data collection (i.e. 2017).

## Acknowledgement

This tutorial was composed using the data that have been generated by teams
who worked on TAMASA project, with funding from the Bill and Melinda Gates
Foundation (BMGF).

## 1. Importing and visualizing data

**a.** Import the Nigerian boundary as the focal geography and maize target
region boundary as the area of interest (AOI). Using the code below, you will
import a FeatureCollection object, and filter by "Country" to select
"Nigeria". FeatureCollections are groups of features (spatial data and
attributes). `Filter` is the method to extract a specific set of features from
a feature collection. Assign the output to a variable called `nigeriaBorder`.
The analyses will be limited to the maize target region in Nigeria,
i.e. the region that accounts for ~70% of Nigeria's maize production.
Therefore, you will import a predefined shapefile layer (already converted to
GEE asset) and assign it as the variable `aoi`. Display both layers to the map
using `Map.addLayer()` with customized display parameters.

```js
// Import country boundaries feature collection.
var dataset = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017');

// Apply filter where country name equals Nigeria.
var nigeria = dataset.filter(ee.Filter.eq('country_na', 'Nigeria'));

// Print the "nigeria" object and explore features and properties.
// There should only be one feature representing Nigeria.
print('Nigeria feature collection:', nigeria);

// Convert the Nigeria boundary feature collection to a line for map display.
var nigeriaBorder =
    ee.Image().byte().paint({featureCollection: nigeria, color: 1, width: 3});

// Set map options and add the Nigeria boundary as a layer to the map.
Map.setOptions('SATELLITE');
Map.centerObject(nigeria, 6);
Map.addLayer(nigeriaBorder, null, 'Nigeria border');

// Import the maize target region asset.
var aoi = ee.FeatureCollection(
    'projects/earthengine-community/tutorials/classify-maizeland-ng/aoi');

// Display the maize target area boundary to the map.
Map.addLayer(aoi, {color: 'white', strokeWidth: 5}, 'AOI', true, 0.6);
```

**b.** Import ground truth data for georeferenced locations where maize (and
other crops) were cultivated during the growing season of 2017 (June - Oct).
The data have been pre-processed and randomly split (70:30) into training and
validation datasets. Import the training and validation datasets, assigning
variable names as "trainingPts" and "validationPts", respectively. Add the
points as layers to the map.

```js
// Import ground truth data that are divided into training and validation sets.
var trainingPts = ee.FeatureCollection(
    'projects/earthengine-community/tutorials/classify-maizeland-ng/training-pts');
var validationPts = ee.FeatureCollection(
    'projects/earthengine-community/tutorials/classify-maizeland-ng/validation-pts');

// Display training and validation points to see distribution within the AOI.
Map.addLayer(trainingPts, {color: 'green'}, 'Training points');
Map.addLayer(validationPts, {color: 'yellow'}, 'Validation points');
```

**c.** Next, you will import Copernicus Sentinel-2 TOA imagery.
The imagery is organized as an ImageCollection object, which is a container
for a collection of individual images. With the code snippet below, you will
import the Sentinel-2 ImageCollection (the same method can be used to
import an ImageCollection for other types of multi-temporal or multi-spectral
data including Landsat, vegetation index, rainfall, temperature etc).
Considering the context, you will apply relevant filters to restrict selected
image tiles to the AOI and date range for the growing season in 2017 (to
coincide with the period of data collection). Clouds are masked from each image
using their corresponding [cloud probability](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_CLOUD_PROBABILITY)
layer. Two functions are provided to achieve cloud masking: a function to join
the cloud probability layer to the relevant image and one to apply the mask
where cloud probability is greater than 50 percent. Finally, a medoid composite
is generated from the set of overlapping pixels by selecting the pixel nearest
to the multi-dimensional median of overlapping pixels ([Flood, 2013](https://www.mdpi.com/2072-4292/5/12/6481/htm)).
The result minimizes contamination from residual clouds and cloud shadows.

```js
// Import S2 TOA reflectance and corresponding cloud probability collections.
var s2 = ee.ImageCollection('COPERNICUS/S2');
var s2c = ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY');

// Define dates over which to create a composite.
var start = ee.Date('2017-06-15');
var end = ee.Date('2017-10-15');

// Define a collection filtering function.
function filterBoundsDate(imgCol, aoi, start, end) {
  return imgCol.filterBounds(aoi).filterDate(start, end);
}

// Filter the collection by AOI and date.
s2 = filterBoundsDate(s2, aoi, start, end);
s2c = filterBoundsDate(s2c, aoi, start, end);

// Define a function to join the two collections on their 'system:index'
// property. The 'propName' parameter is the name of the property that
// references the joined image.
function indexJoin(colA, colB, propName) {
  var joined = ee.ImageCollection(ee.Join.saveFirst(propName).apply({
    primary: colA,
    secondary: colB,
    condition: ee.Filter.equals(
        {leftField: 'system:index', rightField: 'system:index'})
  }));
  // Merge the bands of the joined image.
  return joined.map(function(image) {
    return image.addBands(ee.Image(image.get(propName)));
  });
}

// Define a function to create a cloud masking function.
function buildMaskFunction(cloudProb) {
  return function(img) {
    // Define clouds as pixels having greater than the given cloud probability.
    var cloud = img.select('probability').gt(ee.Image(cloudProb));

    // Apply the cloud mask to the image and return it.
    return img.updateMask(cloud.not());
  };
}

// Join the cloud probability collection to the TOA reflectance collection.
var withCloudProbability = indexJoin(s2, s2c, 'cloud_probability');

// Map the cloud masking function over the joined collection, select only the
// reflectance bands.
var maskClouds = buildMaskFunction(50);
var s2Masked = ee.ImageCollection(withCloudProbability.map(maskClouds))
                   .select(ee.List.sequence(0, 12));

// Calculate the median of overlapping pixels per band.
var median = s2Masked.median();

// Calculate the difference between each image and the median.
var difFromMedian = s2Masked.map(function(img) {
  var dif = ee.Image(img).subtract(median).pow(ee.Image.constant(2));
  return dif.reduce(ee.Reducer.sum()).addBands(img).copyProperties(img, [
    'system:time_start'
  ]);
});

// Generate a composite image by selecting the pixel that is closest to the
// median.
var bandNames = difFromMedian.first().bandNames();
var bandPositions = ee.List.sequence(1, bandNames.length().subtract(1));
var mosaic = difFromMedian.reduce(ee.Reducer.min(bandNames.length()))
                 .select(bandPositions, bandNames.slice(1))
                 .clipToCollection(aoi);

// Display the mosaic.
Map.addLayer(
    mosaic, {bands: ['B11', 'B8', 'B3'], min: 225, max: 4000}, 'S2 mosaic');
```

## 2. Setting up and implementing analytics

**a.** Now that you have prepared the mosaic, proceed to select the spectral
bands that are relevant for the classification. By selecting more bands, the
analysis will become more computationally intensive. The bands have
differing spatial resolution (https://en.wikipedia.org/wiki/Sentinel-2), but
ultimately, the scale of analysis is determined by the argument provided to
the `scale` parameter in sampling and reduction steps. In the code below, all
reflectance bands of the S2 data are selected, but you can adjust this
by selecting fewer bands. Note that our goal is to utilize as much spectral
information as possible to train the classifier algorithm to differentiate
between maize and non-maize. The training points (`trainingPts`) will be used to
extract the reflectance values of the pixels from all spectral bands and this
will be passed to the classifier algorithms.

```js
// Specify and select bands that will be used in the classification.
var bands = [
  'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B9', 'B10', 'B11',
  'B12'
];
var imageCl = mosaic.select(bands);

// Overlay the training points on the imagery to get a training sample; include
// the crop classification property ('class') in the sample feature collection.
var training = imageCl
                   .sampleRegions({
                     collection: trainingPts,
                     properties: ['class'],
                     scale: 30,
                     tileScale: 8
                   })
                   .filter(ee.Filter.neq(
                       'B1', null)); // Remove null pixels.
```

**b.** For the binary classification you will be applying two classifiers:
classification and regression trees (CART) and Random Forest (RF), which are
both suitable for categorical classification and have been used in various
contexts for classification. By comparing outputs from both CART and RF,
users can make objective inference on the most accurate classifier. Default
parameters will be accepted (adjustments such as optimizing the number of
trees in RF, e.g., are outside the scope of this tutorial). The output images
will include values 0 (maize, shown as orange in the map) and 1
(non-maize, shown as grey in the map). Metrics regarding model accuracies are
printed to the console.

```js
// Train a CART classifier with default parameters.
var trainedCart = ee.Classifier.smileCart().train(
    {features: training, classProperty: 'class', inputProperties: bands});

// Train a random forest classifier with default parameters.
var trainedRf = ee.Classifier.smileRandomForest({numberOfTrees: 10}).train({
  features: training,
  classProperty: 'class',
  inputProperties: bands
});

// Classify the image with the same bands used for training.
var classifiedCart = imageCl.select(bands).classify(trainedCart);
var classifiedRf = imageCl.select(bands).classify(trainedRf);

// Define visualization parameters for classification display.
var classVis = {min: 0, max: 1, palette: ['f2c649', '484848']};

// Add the output of the training classification to the map.
Map.addLayer(classifiedCart.clipToCollection(aoi), classVis, 'Classes (CART)');
Map.addLayer(
    classifiedRf.clipToCollection(aoi), classVis, 'Classes (RF)');

// Calculate the training error matrix and accuracy for both classifiers by
// using the "confusionMatrix" function to generate metrics on the
// resubstitution accuracy.
var trainAccuracyCart = trainedCart.confusionMatrix();
var trainAccuracyRf = trainedRf.confusionMatrix();

// Print model accuracy results.
print('##### TRAINING ACCURACY #####');
print('CART: overall accuracy:', trainAccuracyCart.accuracy());
print('RF: overall accuracy:', trainAccuracyRf.accuracy());
print('CART: error matrix:', trainAccuracyCart);
print('RF: error matrix:', trainAccuracyRf);
```

**c.** To assess the reliability of the classification outputs, use the
`validationPts` dataset (imported previously) to extract spectral
information from the mosaic image bands. You will further apply
`ee.Filter.neq` on the "B1" band to remove pixels with null value, and predict
the classified values for the `validationPts` pixels based on the trained
models. Note that accuracy assessment is conducted for each classifier.

```js
// Extract band pixel values for validation points.
var validation = imageCl
                     .sampleRegions({
                       collection: validationPts,
                       properties: ['class'],
                       scale: 30,
                       tileScale: 8
                     })
                     .filter(ee.Filter.neq(
                         'B1', null)); // Remove null pixels.

// Classify the validation data.
var validatedCart = validation.classify(trainedCart);
var validatedRf = validation.classify(trainedRf);

// Calculate the validation error matrix and accuracy for both classifiers by
// using the "confusionMatrix" function to generate metrics on the
// resubstitution accuracy.

var validationAccuracyCart =
    validatedCart.errorMatrix('class', 'classification');
var validationAccuracyRf = validatedRf.errorMatrix('class', 'classification');

// Print validation accuracy results.
print('##### VALIDATION ACCURACY #####');
print('CART: overall accuracy:', validationAccuracyCart.accuracy());
print('RF: overall accuracy: ', validationAccuracyRf.accuracy());
print('CART: error matrix:', validationAccuracyCart);
print('RF: error matrix: ', validationAccuracyRf);
```

## 3. Calculate class area and export classified map

With the binary classification completed, you can now export the classified
imagery to Google Drive (or other [endpoint](https://developers.google.com/earth-engine/exporting#exporting-images))
for further analysis. Check the export resolution parameter (`scale`) and adjust
accordingly to control output file size, if necessary. The larger the scale,
the smaller the file size. The `maxPixels` parameter sets an upper boundary on
the number of pixels allowable for export to avoid export of large file or
prolonged file creation time. Calculate the area for each land cover class by
applying `ee.Image.pixelArea` on the RF-classified image and assign it as the
variable `areaImage`. By passing on the new variable to the sum reducing
function, constrained by the AOI boundary geometry and specifying other
parameters (per below), the area for both classes (maize and not) are generated
in square meters.

```js
// Export classified map (RF) to Google Drive; alter the command to export to
// other endpoints.
Export.image.toDrive({
  image: validatedRf,
  description: 'Maizeland_Classified_RF',
  scale: 20,
  region: aoi,
  maxPixels: 1e13,
});

// Calculate area of each class (based on RF) in square meters.
var areaImage = ee.Image.pixelArea().addBands(classifiedRf);
var areas = areaImage.reduceRegion({
  reducer: ee.Reducer.sum().group({
    groupField: 1,
    groupName: 'class',
  }),
  geometry: aoi.geometry(),
  scale: 500,
  maxPixels: 1e13,
  tileScale: 8
});

// Print the area calculations.
print('##### CLASS AREA SQ. METERS #####');
print(areas);
```

## 4.Final notes

Although this tutorial offers a template for users, further adjustments can
possibly improve the results. The results show that RF outperformed CART in the
validation mode (RF accuracy = 74.9%; CART accuracy = 67.4%). Also, the maize
area estimated was 165,338 square km (i.e. ~16.5 million ha). It is probable that
this is over/under estimated, so further area-based validation may be necessary
to validate the estimate. In any case, this analytical tool (and tutorial) can
support rapid generation of national cropland area estimate that is scalable
across regions, local governments/districts, wards, or villages.
