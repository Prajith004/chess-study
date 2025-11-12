library(dplyr)
library(readr)


data <- read_csv("D:/code/chess/data/Combined_FIDE_Rankings__Men___Women_.csv")


data <- data %>%
  rename(BirthYear = `Birth Year`)

#  Find the youngest player overall ---
youngest_player <- data %>%
  filter(BirthYear == max(BirthYear, na.rm = TRUE))

cat("???? Youngest Player:\n")
print(youngest_player)

# --- Step 2: Filter only Grandmasters (GM) ---
gm_data <- data %>%
  filter(grepl("^GM$", Title, ignore.case = TRUE))

#  Find the youngest GM ---
youngest_gm <- gm_data %>%
  filter(BirthYear == max(BirthYear, na.rm = TRUE))

cat("\n?????? Youngest Grandmaster:\n")
print(youngest_gm)


write_csv(gm_data, "D:/code/chess/data/fide_grandmasters_only.csv")

cat("\n??? Saved GM-only data to: D:/code/chess/data/fide_grandmasters_only.csv\n")
