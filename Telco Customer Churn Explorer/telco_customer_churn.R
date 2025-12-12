# Telco Customer Churn Explorer – R
# End-to-end script: load data, clean, EDA summaries/plots, baseline model.

# ======================= 0. Libraries ===================================

library(readr)     # reading CSV
library(dplyr)     # data wrangling
library(stringr)   # string helpers
library(ggplot2)   # visualisation


# ======================= 1. Load raw data ===============================

# Read the Telco churn CSV from your local path
telco_raw <- read_csv(
  "C:/Users/Admin/Desktop/Projects/Data Projects/Telco Customer Churn Explorer (R)/telco_customer_churn.csv"
)

# Inspect structure: column names, types, sample values
glimpse(telco_raw)


# ======================= 2. Basic cleaning ==============================

# - Convert key categorical variables to factors
# - Leave TotalCharges as-is (already numeric with 11 NA values)
telco_clean <- telco_raw %>%
  mutate(
    Churn         = factor(Churn, levels = c("No", "Yes")),
    Contract      = factor(Contract),
    PaymentMethod = factor(PaymentMethod)
  )

# Quick check: where is TotalCharges missing? (should be very low-tenure customers)
telco_clean %>%
  filter(is.na(TotalCharges)) %>%
  count(Tenure)


# ======================= 3. Create Tenure Band ===========================

# Replicate the Excel tenure bands used in your pivots:
# 0, 1–12, 13–24, 25–48, 49+ months
telco_clean <- telco_clean %>%
  mutate(
    TenureBand = case_when(
      Tenure == 0        ~ "0 months",
      Tenure <= 12       ~ "1–12 months",
      Tenure <= 24       ~ "13–24 months",
      Tenure <= 48       ~ "25–48 months",
      TRUE               ~ "49+ months"
    ),
    TenureBand = factor(
      TenureBand,
      levels = c("0 months", "1–12 months", "13–24 months", "25–48 months", "49+ months")
    )
  )


# ======================= 4. EDA: churn tables ===========================

# 4.1 Contract × Churn (row percentages)
contract_churn <- telco_clean %>%
  count(Contract, Churn) %>%          # counts per contract & churn outcome
  group_by(Contract) %>%
  mutate(
    pct = n / sum(n)                  # share within each contract type
  ) %>%
  ungroup()

contract_churn


# 4.2 TenureBand × Churn (row percentages)
tenure_churn <- telco_clean %>%
  count(TenureBand, Churn) %>%
  group_by(TenureBand) %>%
  mutate(
    pct = n / sum(n)                  # share within each tenure band
  ) %>%
  ungroup()

tenure_churn


# 4.3 PaymentMethod × Churn (row percentages)
payment_churn <- telco_clean %>%
  count(PaymentMethod, Churn) %>%
  group_by(PaymentMethod) %>%
  mutate(
    pct = n / sum(n)                  # share within each payment method
  ) %>%
  ungroup()

payment_churn


# ======================= 5. EDA: plots ==================================

# 5.1 Churn rate by contract type
ggplot(contract_churn, aes(x = Contract, y = pct, fill = Churn)) +
  geom_col(position = "fill") +
  scale_y_continuous(labels = scales::percent) +
  labs(
    title = "Churn rate by contract type",
    y = "Share within contract",
    x = "Contract"
  ) +
  theme_minimal()

# 5.2 Churn rate by tenure band
ggplot(tenure_churn, aes(x = TenureBand, y = pct, fill = Churn)) +
  geom_col(position = "fill") +
  scale_y_continuous(labels = scales::percent) +
  labs(
    title = "Churn rate by tenure band",
    y = "Share within tenure band",
    x = "Tenure band"
  ) +
  theme_minimal()

# 5.3 Churn rate by payment method
ggplot(payment_churn, aes(x = PaymentMethod, y = pct, fill = Churn)) +
  geom_col(position = "fill") +
  scale_y_continuous(labels = scales::percent) +
  labs(
    title = "Churn rate by payment method",
    y = "Share within payment method",
    x = "Payment method"
  ) +
  theme_minimal() +
  coord_flip()


# ======================= 6. Baseline logistic model =====================

# 6.1 Prepare modelling dataset
telco_model <- telco_clean %>%
  # Drop the 11 customers with missing TotalCharges (all Tenure = 0)
  filter(!is.na(TotalCharges)) %>%
  mutate(
    Churn = factor(Churn, levels = c("No", "Yes"))  # ensure reference level
  )

nrow(telco_model)  # number of rows used for modelling


# 6.2 Train / test split (70 / 30 random split)
set.seed(123)

n <- nrow(telco_model)
test_index <- sample(seq_len(n), size = floor(0.3 * n))

telco_test  <- telco_model[test_index, ]
telco_train <- telco_model[-test_index, ]


# 6.3 Fit baseline logistic regression
# Predict churn from tenure, price, contract, payment, internet type, and tenure band.
model_logit <- glm(
  Churn ~ Tenure + MonthlyCharges + Contract + PaymentMethod +
    InternetService + TenureBand,
  data   = telco_train,
  family = binomial
)

summary(model_logit)


# 6.4 Evaluate model on test set

# Predicted probability of churn (class "Yes")
telco_test$pred_prob <- predict(
  model_logit,
  newdata = telco_test,
  type    = "response"
)

# Convert probabilities to classes using 0.5 threshold
telco_test$pred_class <- ifelse(telco_test$pred_prob >= 0.5, "Yes", "No") %>%
  factor(levels = c("No", "Yes"))

# Confusion matrix: predicted vs actual churn
table(
  Actual    = telco_test$Churn,
  Predicted = telco_test$pred_class
)

# Overall accuracy on test data
mean(telco_test$Churn == telco_test$pred_class)

# 6.5 Odds ratios for logistic model -------------------------------

# Coefficients -> odds ratios with 95% CI
logit_odds <- exp(cbind(
  OR  = coef(model_logit),
  confint(model_logit)
))

logit_odds

# ======================= 7. Random forest model =========================

library(randomForest)

set.seed(123)

model_rf <- randomForest(
  Churn ~ Tenure + MonthlyCharges + Contract + PaymentMethod +
    InternetService + TenureBand,
  data      = telco_train,
  ntree     = 300,
  mtry      = 3,
  importance = TRUE
)

# Predict classes on test set
telco_test$pred_rf <- predict(model_rf, newdata = telco_test, type = "class")

# Confusion matrix for RF
table(
  Actual       = telco_test$Churn,
  Predicted_RF = telco_test$pred_rf
)

# Accuracy for RF
mean(telco_test$Churn == telco_test$pred_rf)

# Variable importance from RF
importance(model_rf)
varImpPlot(model_rf)


