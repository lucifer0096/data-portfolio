# app.R
# Telco Customer Churn Explorer – Shiny app

library(shiny)
library(dplyr)
library(ggplot2)
library(shinythemes)
library(readr)
library(stringr)
library(scales)
library(randomForest)

# Load data prep, EDA objects, and models (relative to this app's folder)
source("telco_customer_churn.R")

ui <- fluidPage(
  theme = shinytheme("flatly"),
  titlePanel("Telco Customer Churn Explorer – R & Shiny"),
  
  sidebarLayout(
    sidebarPanel(
      h4("Filters"),
      selectInput(
        "contract_filter",
        "Contract type",
        choices  = c("All", levels(telco_clean$Contract)),
        selected = "All"
      ),
      selectInput(
        "tenure_filter",
        "Tenure band",
        choices  = c("All", levels(telco_clean$TenureBand)),
        selected = "All"
      ),
      selectInput(
        "payment_filter",
        "Payment method",
        choices  = c("All", levels(telco_clean$PaymentMethod)),
        selected = "All"
      )
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel(
          "Overview",
          h4("Churn patterns by contract, tenure and payment"),
          fluidRow(
            column(6, plotOutput("plot_contract")),
            column(6, plotOutput("plot_tenure"))
          ),
          br(),
          plotOutput("plot_payment")
        ),
        tabPanel(
          "Model insights",
          h4("How to read these numbers"),
          p("This page summarises how well the models predict churn and which factors matter most."),
          p("Accuracy alone is misleading here: only about a quarter of test-set customers actually churn,",
            "so a model that always predicts \"No churn\" would already score roughly 75% accuracy without",
            "being useful. Precision, recall, and F1 (for the churn = \"Yes\" class) and AUC give a fuller picture."),
          h5("Test set performance"),
          tableOutput("metrics_table"),
          h5("Key logistic regression effects (odds ratios)"),
          tableOutput("logit_top_table"),
          h5("Random forest variable importance"),
          plotOutput("rf_importance_plot")
        )
      )
    )
  )
)

server <- function(input, output, session) {
  
  # ----------------------- Filtered data ---------------------------------
  
  filtered_data <- reactive({
    df <- telco_clean
    
    if (input$contract_filter != "All") {
      df <- df %>% filter(Contract == input$contract_filter)
    }
    if (input$tenure_filter != "All") {
      df <- df %>% filter(TenureBand == input$tenure_filter)
    }
    if (input$payment_filter != "All") {
      df <- df %>% filter(PaymentMethod == input$payment_filter)
    }
    
    df
  })
  
  # ----------------------- Overview plots --------------------------------
  
  output$plot_contract <- renderPlot({
    df <- filtered_data() %>%
      count(Contract, Churn) %>%
      group_by(Contract) %>%
      mutate(pct = n / sum(n)) %>%
      ungroup()
    
    ggplot(df, aes(x = Contract, y = pct, fill = Churn)) +
      geom_col(position = "fill") +
      scale_y_continuous(labels = scales::percent) +
      labs(
        title = "Churn rate by contract type",
        y = "Share within contract",
        x = "Contract"
      ) +
      theme_minimal()
  })
  
  output$plot_tenure <- renderPlot({
    df <- filtered_data() %>%
      count(TenureBand, Churn) %>%
      group_by(TenureBand) %>%
      mutate(pct = n / sum(n)) %>%
      ungroup()
    
    ggplot(df, aes(x = TenureBand, y = pct, fill = Churn)) +
      geom_col(position = "fill") +
      scale_y_continuous(labels = scales::percent) +
      labs(
        title = "Churn rate by tenure band",
        y = "Share within tenure band",
        x = "Tenure band"
      ) +
      theme_minimal()
  })
  
  output$plot_payment <- renderPlot({
    df <- filtered_data() %>%
      count(PaymentMethod, Churn) %>%
      group_by(PaymentMethod) %>%
      mutate(pct = n / sum(n)) %>%
      ungroup()
    
    ggplot(df, aes(x = PaymentMethod, y = pct, fill = Churn)) +
      geom_col(position = "fill") +
      scale_y_continuous(labels = scales::percent) +
      labs(
        title = "Churn rate by payment method",
        y = "Share within payment method",
        x = "Payment method"
      ) +
      coord_flip() +
      theme_minimal()
  })
  
  # ----------------------- Model insights --------------------------------

  # Precision/recall/F1/AUC for the churn = "Yes" class, plus accuracy for reference
  binary_classification_metrics <- function(actual, predicted, prob) {
    actual_pos    <- actual == "Yes"
    predicted_pos <- predicted == "Yes"

    tp <- sum(predicted_pos & actual_pos)
    fp <- sum(predicted_pos & !actual_pos)
    fn <- sum(!predicted_pos & actual_pos)

    precision <- if ((tp + fp) > 0) tp / (tp + fp) else NA
    recall    <- if ((tp + fn) > 0) tp / (tp + fn) else NA
    f1        <- if (!is.na(precision) && !is.na(recall) && (precision + recall) > 0) {
      2 * precision * recall / (precision + recall)
    } else {
      NA
    }
    accuracy <- mean(predicted == actual)

    # Rank-based AUC (Mann-Whitney U), avoids adding a pROC/ROCR dependency
    pos_scores <- prob[actual_pos]
    neg_scores <- prob[!actual_pos]
    auc <- mean(outer(pos_scores, neg_scores, ">")) +
      0.5 * mean(outer(pos_scores, neg_scores, "=="))

    data.frame(
      Accuracy  = round(accuracy, 3),
      Precision = round(precision, 3),
      Recall    = round(recall, 3),
      F1        = round(f1, 3),
      AUC       = round(auc, 3)
    )
  }

  output$metrics_table <- renderTable({
    logit_metrics <- binary_classification_metrics(
      telco_test$Churn, telco_test$pred_class, telco_test$pred_prob
    )
    rf_metrics <- binary_classification_metrics(
      telco_test$Churn, telco_test$pred_rf, telco_test$pred_prob_rf
    )

    cbind(
      Model = c("Logistic regression", "Random forest"),
      rbind(logit_metrics, rf_metrics)
    )
  }, rownames = FALSE)
  
  # Small odds-ratio table with only key terms
  output$logit_top_table <- renderTable({
    or <- as.data.frame(round(logit_odds, 2))
    or$Term <- rownames(or)
    
    or %>%
      filter(Term %in% c(
        "Tenure",
        "ContractOne year", "ContractTwo year",
        "PaymentMethodElectronic check",
        "InternetServiceFiber optic",
        "InternetServiceNo"
      )) %>%
      select(Term, OR, `2.5 %`, `97.5 %`)
  }, rownames = FALSE)
  
  # Random forest importance plot
  output$rf_importance_plot <- renderPlot({
    varImpPlot(model_rf, main = "Most important variables in random forest")
  })
}

shinyApp(ui = ui, server = server)
