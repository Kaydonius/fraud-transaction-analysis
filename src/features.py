import logging

logger = logging.getLogger(__name__)


def engineer_features(df):
    # change if balance for origin account (how much money was taken out?)
    df["balance_change_origin"] = df["newbalanceorig"] - df["oldbalanceorg"]

    # change in balance for destination account (how much money was put in?)
    df["balance_change_dest"] = df["newbalancedest"] - df["oldbalancedest"]

    # ratio of amount to old balance (how large is the transaction relative to the account balance?)
    df["amount_to_oldbalance_ratio"] = df["amount"] / (df["oldbalanceorg"] + 1e-6)  # add small value to avoid division by zero

     # avg transaction amount for each origin account
    df["avg_amount_by_origin"] = df.groupby("nameorig")["amount"].transform("mean")

    # transaction frequency / velocity
    df["transaction_count_by_origin"] = df.groupby("nameorig")["amount"].transform("count")

    # amount vs user average
    df["amount_vs_avg"] = df["amount"] - df["avg_amount_by_origin"]

    # merchant fraud rate
    merchant_fraud_rate = df.groupby("namedest")["isfraud"].mean()
    df["merchant_fraud_rate"] = df["namedest"].map(merchant_fraud_rate)

    # flagged fraud accuracy (how often flagged frauds are actually fraud)
    flagged_fraud_accuracy = df[df["isflaggedfraud"] == 1].groupby("namedest")["isfraud"].mean()
    df["flagged_fraud_accuracy"] = df["namedest"].map(flagged_fraud_accuracy)


    # time-based features
    df["hour_of_day"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek


    logger.info(f"Engineered {len(df.columns) - 11} new features. Total columns: {len(df.columns)}")
    
    return df
