library(shinydashboard)
library(ggplot2)

ui <- dashboardPage(
  dashboardHeader(title = "Basic dashboard"),
  ## Sidebar content
  dashboardSidebar(
    sidebarMenu(
      menuItem("Dashboard", tabName = "dashboard", icon = icon("dashboard")),
      menuItem("Widgets", tabName = "widgets", icon = icon("th"))
    )
  ),
  ## Body content
  dashboardBody(
    tabItems(
      # First tab content
      tabItem(tabName = "dashboard",
              fluidRow(
                box(plotOutput("plot1")),
              ),
              fluidRow(
                box(
                  title = "Input",
                  selectInput("city",
                              label = h3("City"),
                              choices=list("Beijing", "NYC")
                  ),
                  selectInput("specie",
                              label = h3("specie"),
                              choices=list("o3", "pm10")
                  )
                )
              )
      ),
      
      # Second tab content
      tabItem(tabName = "widgets",
              h2("Widgets tab content")
      )
    )
  )
)

df = read.csv(file = '../waqi-covid19-airqualitydata-2020.csv')

server <- function(input, output) {
  
  output$plot1 <- renderPlot({
    df_2 = df %>% 
      filter((City == input$city) & (Specie == input$specie)) %>%
      arrange(Date)
    ggplot(data=df_2, aes(x=Date, y=median, group=1)) +
      geom_line()+
      geom_point()
  })
}

shinyApp(ui, server)