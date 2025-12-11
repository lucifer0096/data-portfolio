# ================== PACKAGES ==================
library(shiny)
library(leaflet)

# ================== DATA LOAD =================
# Read CSV and keep original column names (with spaces)
volcanoes <- read.csv(
  "C:/Users/Admin/Desktop/Projects/Volcano/volcanos.csv",
  check.names = FALSE
)


# ================== UI ========================
ui <- fluidPage(
  titlePanel("Global Holocene Volcanoes"),
  
  tabsetPanel(
    # ---- Map tab ----
    tabPanel(
      "Map",
      sidebarLayout(
        sidebarPanel(
          # Filter by country
          selectInput(
            "country", "Country:",
            choices = c("All", sort(unique(volcanoes$Country)))
          ),
          # Filter by activity evidence
          selectInput(
            "activity", "Activity evidence:",
            choices = c("All", sort(unique(volcanoes$`Activity Evidence`)))
          ),
          # Filter by risk band from Excel
          selectInput(
            "risk", "Risk level:",
            choices = c("All", sort(unique(volcanoes$Risk)))
          )
        ),
        mainPanel(
          textOutput("summary_text"),
          br(),
          leafletOutput("volcanoMap", height = 600)
        )
      )
    ),
    
    # ---- Info / Glossary tab ----
    tabPanel(
      "Info / Glossary",
      br(),
      h3("Volcano dataset – key terms"),
      tags$ul(
        tags$li(tags$b("Volcanic Region Group:"), " Broad geographic grouping of volcanic provinces (for example, European Volcanic Regions)."),
        tags$li(tags$b("Volcanic Region:"), " More detailed sub‑region containing one or more volcanic fields or centres."),
        tags$li(tags$b("Volcano Landform:"), " Physical shape of the volcano (for example, stratovolcano, shield, caldera, volcanic field)."),
        tags$li(tags$b("Primary Volcano Type:"), " Main eruptive structure or style, such as lava dome or cinder cone."),
        tags$li(tags$b("Activity Evidence:"), " Type of evidence for Holocene activity (observed, dated, credible, uncertain, or none)."),
        tags$li(tags$b("Risk:"), " Simple band derived from Activity Evidence (High, Medium, Low, Unknown) for visualisation in this app."),
        tags$li(tags$b("Last Known Eruption:"), " Most recent known eruptive episode (year or historical period; 'Unknown' if not constrained)."),
        tags$li(tags$b("Elevation (m):"), " Summit elevation above sea level in metres."),
        tags$li(tags$b("Tectonic Setting:"), " Plate‑tectonic environment (for example, subduction zone, rift zone, intraplate)."),
        tags$li(tags$b("Dominant Rock Type:"), " Main magma composition erupted (for example, basalt, andesite, rhyolite, trachyte)."),
        tags$li(tags$b("Latitude / Longitude:"), " Geographic coordinates of the volcano centre.")
      ),
      br(),
      p("This app visualises Holocene volcanoes and allows filtering by country, activity evidence, and a simple risk band derived from the activity information."),
      br(),
      h4("Glossary overview"),
      img(src = "Image1.png", width = "90%", style = "border:1px solid #ccc;"),
      br(), br(),
      h4("Volcano types and tectonic settings"),
      img(src = "Image2.png", width = "90%", style = "border:1px solid #ccc;"),
      br(), br(),
      hr(),
      h4("About this app"),
      p("This Shiny application was built as a personal data analytics project using the Global Volcanism Program Holocene volcano list. ",
        "It demonstrates data cleaning, simple risk banding based on activity evidence, and interactive geospatial visualisation with Leaflet."),
      p("Created by Rahul Bhaskaran, Data Analyst",
        a(href = "mailto:your.email@example.com", "rahulbhaskaran96@gmail.com"))
    )
  )
)

# ================== SERVER ====================
server <- function(input, output, session) {
  
  # Reactive filter based on user selections
  filtered_data <- reactive({
    data <- volcanoes
    
    if (input$country != "All") {
      data <- subset(data, Country == input$country)
    }
    if (input$activity != "All") {
      data <- subset(data, `Activity Evidence` == input$activity)
    }
    if (input$risk != "All") {
      data <- subset(data, Risk == input$risk)
    }
    
    data
  })
  
  # Summary text above the map
  output$summary_text <- renderText({
    data <- filtered_data()
    paste("Volcanoes shown:", nrow(data))
  })
  
  # Render the Leaflet map
  output$volcanoMap <- renderLeaflet({
    data <- filtered_data()
    
    # Colour palette by Risk
    pal <- colorFactor(
      palette = c("red", "yellow", "orange", "black"),
      domain  = volcanoes$Risk
    )
    
    leaflet(data) |>
      addTiles() |>
      addCircleMarkers(
        lng = ~`Longitude`,
        lat = ~`Latitude`,
        color = ~pal(Risk),
        radius = 5,
        stroke = FALSE,
        fillOpacity = 0.8,
        popup = ~paste0(
          "<b>", `Volcano Name`, "</b><br>",
          "Country: ", Country, "<br>",
          "Region: ", `Volcanic Region`, "<br>",
          "Landform: ", `Volcano Landform`, "<br>",
          "Primary type: ", `Primary Volcano Type`, "<br>",
          "Activity evidence: ", `Activity Evidence`, "<br>",
          "Risk level: ", Risk, "<br>",
          "Last known eruption: ", `Last Known Eruption`, "<br>",
          "Elevation: ", `Elevation (m)`, " m<br>",
          "Tectonic setting: ", `Tectonic Setting`, "<br>",
          "Rock type: ", `Dominant Rock Type`
        ),
        clusterOptions = markerClusterOptions()
      ) |>
      addLegend(
        "bottomright",
        pal = pal,
        values = ~Risk,
        title = "Risk level",
        opacity = 1
      )
  })
}

# ================== RUN APP ===================
shinyApp(ui = ui, server = server)
