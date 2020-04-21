library(shinydashboard)
library(ggplot2)

df = read.csv(file = '../waqi-covid19-airqualitydata-2020.csv', encoding="UTF-8")
df = df %>% mutate(Date = as.Date(Date))
cities = sort(as.character(unique(df$City)))
df_city = df %>% filter(City == cities[1])
species = sort(as.character(unique(df_city$Specie)))
ui <- dashboardPage(
  dashboardHeader(title = "COVID & Air Quality"),
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
                              choices= cities, #list("Beijing", "NYC")
                  ),
                  selectInput("specie",
                              label = h3("specie"),
                              choices= species, #list("o3", "pm10")
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


server <- function(input, output, session) {
  observe({
    df_city = df %>% filter(City == input$city)
    species = sort(as.character(unique(df_city$Specie)))
  
    updateSelectInput(session, "specie",
                    choices = species,
      )
  })
  output$plot1 <- renderPlot({

    df_2 = df %>% 
      filter((City == input$city) & (Specie == input$specie)) %>%
      arrange(Date)
    ggplot(data=df_2, aes(x=Date, y=median, group=1)) +
      geom_line()+
      geom_point()+
      ggtitle(paste(input$city, input$specie))+
      scale_x_date(date_breaks = "2 week")
    
  })
}

shinyApp(ui, server)