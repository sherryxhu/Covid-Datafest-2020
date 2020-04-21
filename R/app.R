library(shinydashboard)
library(ggplot2)

df = read.csv(file = '../waqi-covid19-airqualitydata-2020.csv', encoding="UTF-8")
df = df %>% mutate(Date = as.Date(Date))
cities = sort(as.character(unique(df$City)))
df_city = df %>% filter(City == cities[1])
previous_city = cities[1]
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
                              label = h3("Specie"),
                              choices= species, #list("o3", "pm10")
                              multiple = TRUE,
                              selected = "pm25"
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
    print(input$specie)
    print(typeof(input$Specie))
    if (input$city != previous_city){
      df_city = df %>% filter(City == input$city)
      species = sort(as.character(unique(df_city$Specie)))
      previous_city = input$city
      updateSelectInput(session, "specie",
                      choices = species,
        )
    }
  })
  output$plot1 <- renderPlot({


    p = ggplot()
    for (specie in input$specie){
      df_2 = df %>% 
        filter((City == input$city) & (Specie == input$specie)) %>%
        arrange(Date)
      p = p +
        geom_line(data = df_2, aes(x=Date, y=median)) +
        geom_point(data= df_2, aes(x=Date, y=median)) 
    }
    # ggplot(data=df_2, aes(x=Date, y=median, group=1)) +
    #   geom_line()+
    #   geom_point()+
    p = p +
      ggtitle(paste(input$city, input$specie))+
      scale_x_date(date_breaks = "2 week")
    p
  })
}

shinyApp(ui, server)