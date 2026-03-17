# Data Profile

## Dataset shape: (6362620, 11)
## Columns: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud
## Datatypes: int, str, float, str, float, float, str, float, float, int, int

## Missing values: None across all columns

## Class Balance Summary: Checking if the target column (isFraud) is balanced or not reveals ~8k cases of fraudulent transactions out of the 6 million rows present in the dataset. Conclusion: The column is extremely unbalanced.

#### Note: Due to the unbalanced nature of the dataset, I will be implementing the SMOTE technique. My goal is to balance the dataset somewhat, so trends are more obvious, and I can draw more relevant conclusions. 