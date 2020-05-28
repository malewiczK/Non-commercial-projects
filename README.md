# Repository with sample non-commercial projects

Due to being obligated to keep my every day code away from open source, I prepared some example projects 
to grasp a bit my coding skills

----
## Projects available in this repo:

- **Optiparam** - [manual](#Optiparam)


<a name="Optiparam"/>

### [Optiparam](https://github.com/malewiczK/Non-commercial-projects/tree/master/optiparam)

Project prepared as solution for an recruitment task. Below I enclose the content:
<br><br>
Your role is to implement Optiparam Algorithm given the presented input format.
Based on the set of risk variables (model features) and a target variable (column: into_default_flag) probability of default (column: PD) is estimated. 
Those PDs were prepared for you. 

The Algorithm:<br>
Determine rating classes we use so called Optiparm Algorithm (OA). Below the general OA is described:

    1. The full dataset should be used when running Optiparm. 
    2. Order raw PD estimates from low values to high values.
    3. The ordered PDs are divided into 50 distinct classes (equal number of observations in each class).
    4. Each of the those classes will be used to make a dummy variable with a value that is either a ‘1’ if the PD 
    value belongs to that class or ‘0’ if not.
    5. The parameters of the sequential dummies are going to be tested (t-test) on their mutual significances 
    (assume confidence interval is equal to 95%).
    6. In case all tests are significant, step 9 will be next. Otherwise continue with step 7.
    7. The test – between every two sequential dummies - with the lowest t-value indicates the two dummies that 
    are least significantly different. The associated rating classes will be merged together. 
    The number of dummies reduces by one.
    8. The steps 4 to 7 will be run iteratively as long as the condition of significance from step 6 is not met.
    9. At this point all the remaining dummies are significant. Classes created this way are the final 
    rating classes.
    
After running, Optiparm provides the following output:
 1. The number of clients per class
 2. The lower and higher bounds per rating class of the original model values.
 3. The observed defaults percentages (flag into_default_flag equals 1 against all samples within the class).
    
Remarks:
 - The input parameters of the model can be tuned in order to get better results.

