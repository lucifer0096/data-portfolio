# app.R
# Telco Customer Churn Explorer – Shiny app

library(shiny)
library(dplyr)
library(ggplot2)
library(shinythemes)

# Load data prep, EDA objects, and models
source("C:/Users/Admin/Desktop/Projects/Data Projects/Telco Customer Churn Explorer (R)/telco_customer_churn.R")

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
          h5("Test accuracy"),
          verbatimTextOutput("accuracy_text"),
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
  
  # Accuracy text in plain English
  output$accuracy_text <- renderPrint({
    acc_logit <- mean(telco_test$Churn == telco_test$pred_class)
    acc_rf    <- mean(telco_test$Churn == telco_test$pred_rf)
    
    cat(
      "Logistic regression correctly predicts about",
      round(acc_logit * 100, 1), "% of customers on the test set.\n",
      "Random forest correctly predicts about",
      round(acc_rf * 100, 1), "% of customers on the same test set."
    )
  })
  
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
