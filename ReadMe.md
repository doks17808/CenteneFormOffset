# **Form Mappping Project**

The following project attempted to address an issue with mapping values to their correct labels on health insurance claim HIC forms. The team on site dealt with scanned pdf documents of HIC red forms that contained only the filled in values and not the form background itself. They then used textract software to extract the bounding boxes of the filled forms. These bounding boxes were then compared to the locations of the fields in the form and boxes were assigned the field they overlapped the most with. 

The problem the team faced was caused by older scanners whose wheels would randomly slow/get stuck. This would cause the scanned document to be stretched out in certain areas by 2-12 pixels. These stretches could occur multiple times along the length of the document. 

To solve this problem a variety of methods were explored:

## Invesitgation Methods
1. Initial Investigation
2. Rotate, Crop, Resize and Overlay Filled Form and Blank Form
3. Duplicate Existing Method Using Intersection of Bounding Boxes
4. K-Nearest Neighbor Model Using the Top-Left Corner of Text
5. K-Nearest Neighbor Model Using the Center of the Text
6. Methods Comparison
---

## 1. Initial Invesigation
---
The initial stage attempted to use the pdfPlumber python library to extract structure from the underlying pdf. However, this method was quikcly abandoned as the documents were scanned pdfs and therefore basically image files. *see pdfPlumber.ipynb*

Since the pdfs are scanned documents the *pdf2image.ipynb* takes each pdf and seperates each page into a seperate image file that is then saved to the output directory. 

In an attempt to mimic the production data *MaskRed.ipynb* was used to try masking the form background however, due to slight changes in orientation and size this method did not produce the desired results and was quickly abandoned. 

## 2. Rotate, Crop, Resize and Overlay Filled Form and Blank Form
---
Since these were images the second stage consisted of a simple rotation, cropping, resizing, and overlaying of the forms to see if this would correct the issue enough to help increase the accuracy of the current system. 

To complete this step the dataset had to be enlarged so the *CreatingFakeForms.ipynb* reads in a scanned pdf and artifically offsets the image 1-3 times along its length by a factor of 2-12 pixels. Randomly selecting the number of offsets and randomly selecting the length of the offset was done in the hopes of creating an accurate representation of the problem that was faced. 

The data created from the aforementioned step was then passed to the *RotateCrop.ipynb* to fix any rotation of the document and then crop was done on the document to get rid of the surrounding whitespace. The results were then saved and read into the *ResizeOverlay.ipynb* to resize the document to match the dimensions of the blank form and then the two forms were overlayed with the output being saved for visual inspection.

Qualitatively, this method seemed to produce decent results. However, without access to production data or the current methods used by the client there was no way to obtain an accuracy from the system.

## 3. Duplicate Existing Method Using Intersection of Bounding Boxes
---
From the previous stage it was clear that the current system of classification needed to be duplicated in some manner to allow for metric comparison between any models being created. 

The things that needed to be address immediately were:
1. The cost associated with creating a working textraction software
2. Lack of bounding boxes
3. Cost of manually creating bounding boxes for the blank form

The solution for the first and second problems came from the two scanned white sheets of filled claim forms that already had their background removed. Since there was no plans to utilize text classification it was unnecesary to do more than locate the boudning boxes of the filled information. The problem with using the filled forms that had a background was that the openCV software was unable to distinguish between the form background and the filled information. The white sheets removed this problem and allowed for programatic isolation of the text bounding boxes *WhitePaper_IOU.ipynb*.

The third problem had no easy solution. Therefore, labelImg an open source graphical image annotation software was used to bound and label each field on the health insurance claim form.

The intersection over the union *IOU* of the bounding boxes was then computed. This was done by comparing the top left and bottom right corners of the field values and the form boxes to determine if the field value laid within the form field. The script iterates over the field values assigning the form label to the field value that has the largest IOU. 

This method resulted in 75% of the boxes being labeled. This does not equate to accuracy since the field values did not have an initial label to compare to the label that was predicted by the IOU. However, in the interests of time 75% was established as a baseline accuracy with the aforementioned understanding. 

## 4 K-Nearest Neighbor Model Using Top-Left Corner of Text
---
With a baseline accuracy established the fourth and fifth stages of the project were started.
---
#### What is a KNN model?
K-Nearest Neighbors *KNN* is a supervised machine learning classification method that follows the principle that closely grouped data points most likely belong to the same classification. For example if a persons close group of friends consist of college students then that person is most likely a college student themselves. The method is a form of supervised machine learning because it needs to be trained on labeled data to identify the neighbors of given points. 
---
The fourth and fifth stages of the project focused on creating K-Nearest Neighbor models to predict the labels associated with the location of the data. This stage of the project focused on utilizing the top left corner of the data bounding box. 

Since KNN is a **supervised** machine learning model the data had to be manually labelled to create a training and testing data set. The *LabelImg* application was used to draw and label the bounding boxes of a single blank HIC form outputting an XML file.The *XMLtoDataframe.ipynb* took the saved xml file and transformed it into a dataframe that could be easily read into python. The coordinates for these boxes were then run through the *KNN_TopLeftCorner.ipynb - Data Creation* section, where each box was offset by a random number of pixels between 0 and half the height of the box. This was done 3000 times to each of the labels to create a large enough dataset to train and test the model on. The data set was then changed to an array and split into training and testing datasets (Test Train Split Section). These two datasets were then used in the next two sections (KNN Uniform Weight and KNN Distance Weighted). The KNN Uniform Weight section created models with varying K-values (K-values indicate the number of neighbors the model will look at to classify the data point) and a uniform weighting applied to each neighbor. The KNN Distance Weighted section created models with the same K-values but this model weights the effect the neighbors have on the classification based on how far they are from the data point. In other words, neighbors that are closer to the data point have more influence than data points farther away in deciding the classification category. Both of these models returned 99% accuracry scores utilizing only one neighbor. The high level of accuracy and the optimal numbers of neighbors for the model was cause for concern. Therefore, the project moved to it fifth stage

## 5 K-Nearest Neighbor Model Using Center of the Text
---
Due to the results of the prior KNN Models, it was decided that exploration of a KNN model using the center point should be conducted. The *KNN_Center.ipynb* follows the same steps outlined in the stage above subsituting the center point for the left corner point. The results of the KNN Uniform Weight was an accuracy of 94.47% with 17 neighbors and the accuracy of the KNN Distance Weighted was . Th

## 6 Methods Comparison
---
The final stage of the project was to test the trained KNN_Center Model on the filled white sheet and obtain an accuracy score to comapre to the results from stage 3. The *CenterKNN_Comparison.ipynb* goes through the process of setting up the various datasets, models, and accuracy metric. From the comparison the KNN methods had an accuracy of only ~50% compared to the baseline of 97.63%. Upon further investigation of the model it is clear that the drop in accuracy is due to the training dataset and the horizontal offset causing the neighbors closest to the data point changing. 




# Future Iterations
---
Moving forward, the project should investigate creation of higher quality training data that better matches the forms that are being seen by the team. Better training data should increase the accuracy of the KNN Model. 

Another option would be text classification to identify the type of text being extracted to inform the labels that are being assigned. This method would require greater resources to train a model to recognize the different types of text being accepted and would not be as generalizable as the KNN Method. 

