# sfl-challenge
Code for the SFL take home challenge and assignment

**Author**: D. Bart Masters (d.bart.masters@gmail.com)
**Time requested**: Saturday, June 8th, 2024 12:00 pm CST
**Time due**: Tuesday, June 11th, 2024 12:00 pm CST
**Audience**: Deloitte-SFL Scientific

File link (private): [DS Manager Technical Assessment](https://docs.google.com/document/d/19pabLtQrG_KxkHHuwTKD1GqM3qnnoynt/edit) 

--- 
# Resources Used
## mido package used: 
https://mido.readthedocs.io/en/stable/ 
## music21 ideas: 
https://www.kaggle.com/code/wfaria/midi-music-data-extraction-using-music21/notebook
https://sean-hobin.medium.com/predicting-musical-genre-from-midi-files-e6c274cd9e6 
## cited paper: 
https://arxiv.org/pdf/1611.09827

--- 

# Assignment from Google Doc
## Scenario
A client has requested us to build a composer classifier based on live captured audio that can be set to stream chunks of data to our model at 15, 30, 60-second intervals, as desired. For this project, the client has collected and annotated several hundred audio files and have saved them as simple midi files. The provided PS1 Folder contains the known midi files pertaining to four (4) composers: Bach, Beethoven, Schubert, and Brahms.  
 
### Goal:  
The goal of this project is to develop a classifier/pipeline that is able to determine which midi files in the provided PS2 folder are not written by the four (4) composers above (it is a small number).  
 
### Details:  
In the interest of time, 30-seconds is the desired default setting. Analysis of how data quantity effects performance is not expected but will highlight important client requirements.  
  
The midi files contain additional information that may not be available at inference time; ensure that your algorithm can support this. 
 
The name of the file before the first underscore is the composition name. 
 
The attached dataset is provided in midi format and taken from Musicnet. 
(https://arxiv.org/pdf/1611.09827.pdf).   
 
Optimal model performance is not expected, and neither is the use of the entire dataset and information. Classical ML approach(es) are recommended as the main form of analysis as setting up a thorough pipeline will be evaluated by the client more favorably than a poorly implemented state-of-the-art model that is not well-validated or documented. A deep learning approach may be attempted based on results to showcase additional capabilities. 


The client exercise is geared towards a truncated, real-world scenario, demonstrating: 
- Efficacy: How fast you can build solutions and the quantity of analysis shown. 
- Quality: How well you showcase your understanding of the problem, data, and code.
- Robustness: The completeness of your analysis flow and the robustness of the validation process.  
 
In particular, the client will consider overall problem understanding and set up of the analysis; the completeness of your EDA and model building/tuning/validation; result interpretation and analysis approach and outcomes; code quality and completeness; and final conclusions and recommendations based on the brief sprint.  




### Using Open-source Libraries/Packages: 
Any open-source code/libraries and publicly available information is encouraged providing you cite the material. 
 
### Return & Due Date: 
Please email back the final notebook within 72 hours of receiving this exercise. Please return a brief abstract of the solution and findings.  
 
As discussed, the technical team will evaluate your code and if approved, you will be invited to a final round where you will present your background, methods, and results. I will provide additional information on the presentation when scheduling. In any case, I will email you after we review your submission and provide any additional feedback and next steps.  
 
Thank you for taking the time to complete this exercise; we appreciate your time, effort, and attention upfront. Eager to see your work and good luck in your analysis.
